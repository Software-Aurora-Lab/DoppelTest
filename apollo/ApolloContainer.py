import subprocess
import time

import docker

from apollo.CyberBridge import CyberBridge
from apollo.Dreamview import Dreamview
from config import USE_SIM_CONTROL_STANDALONE
from utils import get_logger

SIM_CONTROL_BIN = '/apollo/bazel-bin/modules/sim_control_standalone/main'
"""Standalone SimControl binary shipped by the ``v7_mozart`` Apollo branch"""
SIM_CONTROL_PATTERN = 'sim_control'
"""Pattern matching any SimControl process, used to stop leftover instances"""


class ApolloContainer:
    """
    Class to represent Apollo container

    :param str apollo_root: root directory of Baidu Apollo
    :param str username: unique ID used to identify container
    """
    apollo_root: str
    username: str
    bridge: CyberBridge
    dreamview: Dreamview
    port = 8888
    bridge_port = 9090

    def __init__(self, apollo_root: str, username: str) -> None:
        """
        Constructor
        """
        self.apollo_root = apollo_root
        self.username = username
        self.logger = get_logger(f"ApolloContainer[{self.container_name}]")

    @property
    def container_name(self) -> str:
        """
        Gets the name of the container

        :type: str
        """
        return f"apollo_dev_{self.username}"

    def is_running(self) -> bool:
        """
        Checks if the container is running

        :returns: True if running, False otherwise
        :rtype: bool
        """
        try:
            return docker.from_env().containers.get(self.container_name).status == 'running'
        except:
            return False

    @property
    def ip(self) -> str:
        """
        Gets the ip address of the container

        :type: str
        """
        assert self.is_running(), f'Container {self.container_name} is not running.'
        ctn = docker.from_env().containers.get(self.container_name)
        
        ip_address = ""
        try:
            ip_address = ctn.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']
        except KeyError:
            try:
                ip_address = ctn.attrs['NetworkSettings']['IPAddress']
            except KeyError:
                raise Exception(f"Could not find IP address for container {self.container_name}")
        return ip_address

    def start_instance(self, restart=False):
        """
        Starts an Apollo instance

        :param bool restart: force container to restart
        """
        self.logger.debug(f'Starting container')
        if not restart and self.is_running():
            self.logger.debug(f'Already running at {self.ip}')
            return
        cmd = f'{self.apollo_root}/docker/scripts/dev_start.sh -l -y --fastest'
        subprocess.run(
            cmd.split(),
            env={
                'USER': self.username
            },
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.logger.debug(f'Started running at {self.ip}')

    def __dreamview_operation(self, op: str):
        """
        Helper function to start/stop/restart Dreamview

        :param str op: operation, can be any of stop/stop/restart
        """
        ops = {
            'start': ('Starting', 'start', f'Running Dreamview at http://{self.ip}:{self.port}'),
            'stop': ('Stopping', 'stop', f'Stopped Dreamview'),
            'restart': ('Restarting', 'restart', f'Restarted Dreamview at http://{self.ip}:{self.port}')
        }
        op_name, op_cmd, op_success_info = ops[op]
        self.logger.debug(f'{op_name} Dreamview')
        cmd = f"docker exec -u {self.username} {self.container_name} ./scripts/bootstrap.sh {op_cmd}"
        subprocess.run(cmd.split(), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        if op == 'stop':
            self.dreamview = None
        else:
            self.dreamview = self.__connect_dreamview()
            self.logger.debug(
                f'Dreamview running at http://{self.ip}:{self.port}')

        self.logger.debug(op_success_info)

    def __connect_dreamview(self, timeout: float = 300.0) -> Dreamview:
        """
        Connect to Dreamview's websocket, waiting for it to accept connections

        ``bootstrap.sh start`` returns before Dreamview is listening, so
        connecting right after it can be refused.

        :param float timeout: seconds to keep retrying before giving up

        :returns: a connected Dreamview client
        :rtype: Dreamview
        """
        deadline = time.time() + timeout
        while True:
            try:
                return Dreamview(self.ip, self.port)
            except (ConnectionRefusedError, OSError):
                if time.time() >= deadline:
                    raise
                self.logger.debug('Waiting for Dreamview to accept connections')
                time.sleep(1)

    def start_dreamview(self):
        """
        Start Dreamview
        """
        self.__dreamview_operation('start')

    def stop_dreamview(self):
        """
        Stop Dreamview
        """
        self.__dreamview_operation('stop')

    def restart_dreamview(self):
        """
        Restart Dreamview
        """
        self.__dreamview_operation('restart')

    def start_bridge(self):
        """
        Start cyber bridge
        """
        if not self.__is_bridge_started():
            self.logger.debug('Starting bridge')
            cmd = f"docker exec -u {self.username} -d {self.container_name} ./scripts/bridge.sh"
            subprocess.run(cmd.split())
        else:
            self.logger.debug('Bridge already running')
            pass

        while True:
            try:
                self.bridge = CyberBridge(self.ip, self.bridge_port)
                self.logger.debug('Bridge connected')
                break
            except ConnectionRefusedError:
                time.sleep(1)

    def reset_bridge_connection(self):
        """
        Close any existing connection to bridge and reconnect
        """
        self.logger.debug('Resetting bridge connection')
        if not self.__is_bridge_started():
            return
        if not self.bridge is None:
            self.bridge.conn.close()
        self.bridge = CyberBridge(self.ip, self.bridge_port)

    def __is_bridge_started(self) -> bool:
        """
        Checks if the bridge has been started already

        :returns: True if running, False otherwise
        :rtype: bool
        """
        try:
            b = CyberBridge(self.ip, self.bridge_port)
            b.conn.close()
            return True
        except:
            return False

    def __modules_operation(self, op: str):
        """
        Helper function to control planning/routing/...

        :param str op: operation, can be any of stop/stop/restart
        """
        ops = {
            'start': ('Starting', 'start', 'started'),
            'stop': ('Stopping', 'stop', 'stopped'),
            'restart': ('Restarting', 'restart', 'restarted')
        }
        op_name, op_cmd, op_success_info = ops[op]

        self.logger.debug(f"{op_name} required modules")
        cmd = f"docker exec -u {self.username} {self.container_name} ./scripts/bootstrap_doppeltest.sh {op_cmd}"
        subprocess.run(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.logger.debug(f'Modules {op_success_info}')

    def start_modules(self):
        """
        Start all the necessary modules
        """
        self.__modules_operation('start')

    def stop_modules(self):
        """
        Stop all the necessary modules
        """
        self.__modules_operation('stop')

    def restart_modules(self):
        """
        Restart all the necessary modules
        """
        self.__modules_operation('restart')

    def start_recorder(self, record_id: str):
        """
        Starts cyber_recorder

        :param str record_id: the name of the record file
        """
        self.logger.debug(f"Starting recorder")
        cyber_recorder = "/apollo/bazel-bin/cyber/tools/cyber_recorder/cyber_recorder"
        cmd = (f"docker exec -d -u {self.username} {self.container_name} "
               f"{cyber_recorder} record -a -i 600 -o /apollo/records/{self.container_name}.{record_id}")
        subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def stop_recorder(self):
        """
        Stops cyber_recorder
        """
        self.logger.debug(f"Stopping recorder")
        cmd = f"docker exec -d -u {self.username} {self.container_name} pkill --signal SIGINT -f 'cyber_recorder record'"
        subprocess.run(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def start_sim_control_standalone(self, x: float, y: float, heading: float):
        """
        Starts SimControlStandalone module at the given start pose

        ``sim_control_standalone`` latches the pose passed on its command line
        when it starts and ignores it afterwards, so it has to be restarted for
        every scenario with that scenario's initial position.

        :param float x: x coordinate the instance should spawn at
        :param float y: y coordinate the instance should spawn at
        :param float heading: heading the instance should spawn with
        """
        self.logger.debug(
            f"Starting sim_control_standalone at ({x}, {y}, {heading})")
        cmd = (f"docker exec -u {self.username} -d {self.container_name} "
               f"{SIM_CONTROL_BIN} {x} {y} {heading}")
        subprocess.run(
            cmd.split(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def __sim_control_pids(self) -> str:
        """
        Lists the pids of any SimControl process running in the container

        :returns: whitespace separated pids, empty if none are running
        :rtype: str
        """
        cmd = ["docker", "exec", "-u", self.username, self.container_name,
               "pgrep", "-f", SIM_CONTROL_PATTERN]
        result = subprocess.run(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL)
        return result.stdout.decode().split()

    def stop_sim_control_standalone(self):
        """
        Stops SimControlStandalone module

        Kills the process directly instead of going through
        ``modules/sim_control/script.sh``: that script is not executable in the
        Apollo checkout, so the ``docker exec`` invoking it failed silently and
        left SimControl running with a stale start pose across scenarios.
        """
        self.logger.debug(f"Stopping sim_control_standalone")
        cmd = ["docker", "exec", "-u", self.username, self.container_name,
               "pkill", "-9", "-f", SIM_CONTROL_PATTERN]
        subprocess.run(cmd, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        for _ in range(20):
            if not self.__sim_control_pids():
                return
            time.sleep(0.5)
        self.logger.error(
            'SimControl is still running after stop, '
            'the next scenario will start from a stale pose'
        )

    def stop_all(self):
        """
        Stops SimControl and all other AD related modules
        """
        self.bridge.stop()
        if USE_SIM_CONTROL_STANDALONE:
            self.stop_sim_control_standalone()
        else:
            self.dreamview.stop_sim_control()
        self.stop_modules()

    def reset(self):
        """
        Resets the container (e.g., stopps and restarts all related modules)
        """
        self.logger.debug(f'Resetting')
        if USE_SIM_CONTROL_STANDALONE:
            self.stop_sim_control_standalone()
        else:
            self.dreamview.stop_sim_control()
        self.stop_modules()
        self.start_bridge()
        self.reset_bridge_connection()
        self.start_modules()
        # SimControl is not started here: it needs the scenario's start pose,
        # so ApolloRunner.initialize starts it once that pose is known.
