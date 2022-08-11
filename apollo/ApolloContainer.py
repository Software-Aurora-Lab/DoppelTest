import time
import docker
import subprocess

from apollo.CyberBridge import CyberBridge
from apollo.Dreamview import Dreamview
from utils import get_logger
from config import USE_SIM_CONTROL_STANDALONE


class ApolloContainer:
    """
    Class to represent Apollo container

    Attributes:
    apollo_root: str
        Root directory of Baidu Apollo
    username: str
        Unique id used to identify container
    bridge: CyberBridge
        Used to connect to cyber bridge
    dreamview: Dreamview
        Websocket connection to control Dreamview
    port: int
        Network port for Dreamview
    bridge_port: int
        Network port for cyber bridge
    """
    apollo_root: str
    username: str
    bridge: CyberBridge
    dreamview: Dreamview
    port = 8888
    bridge_port = 9090

    def __init__(self, apollo_root: str, username: str) -> None:
        """
        Constructs all the attributes for ApolloContainer object

        Parameters:
            apollo_root: str
                Root directory of Baidu Apollo
            username: str
                Unique id used to identify container
        """
        self.apollo_root = apollo_root
        self.username = username
        self.logger = get_logger(f"ApolloContainer[{self.container_name}]")

    @property
    def container_name(self) -> str:
        """
        Gets the name of the container

        Returns:
            name: str
                name of the container
        """
        return f"apollo_dev_{self.username}"

    def is_running(self) -> bool:
        """
        Checks if the container is running

        Returns:
            status: bool
                True if running, False otherwise
        """
        try:
            return docker.from_env().containers.get(self.container_name).status == 'running'
        except:
            return False

    @property
    def ip(self) -> str:
        """
        Gets the ip address of the container

        Returns:
            ip: str
                ip address of the container
        """
        assert self.is_running(
        ), f'Instance {self.container_name} is not running.'
        ctn = docker.from_env().containers.get(self.container_name)
        return ctn.attrs['NetworkSettings']['IPAddress']

    def start_instance(self, restart=False):
        """
        Starts an Apollo instance

        Parameters:
            restart : bool
                forcing container to restart
        """
        self.logger.debug(f'Starting container')
        if not restart and self.is_running():
            self.logger.debug(f'Already running at {self.ip}')
            return
        cmd = f'{self.apollo_root}/docker/scripts/dev_start.sh -l -y'
        result = subprocess.run(
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

        Parameters:
            op: str
                Operation can be one of [start, stop, restart]
        """
        ops = {
            'start': ('Starting', 'start', f'Running Dreamview at http://{self.ip}:{self.port}'),
            'stop': ('Stopping', 'stop', f'Stopped Dreamview'),
            'restart': ('Restarting', 'restart', f'Restarted Dreamview at http://{self.ip}:{self.port}')
        }
        s0, s1, s2 = ops[op]
        self.logger.debug(f'{s0} Dreamview')
        cmd = f"docker exec {self.container_name} ./scripts/bootstrap.sh {s1}"
        subprocess.run(cmd.split(), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        if op == 'stop':
            self.dreamview = None
        else:
            self.dreamview = Dreamview(self.ip, self.port)
            self.logger.debug(
                f'Dreamview running at http://{self.ip}:{self.port}')

        self.logger.debug(s2)

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
            cmd = f"docker exec -d {self.container_name} ./scripts/bridge.sh"
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

        Returns:
            status: bool
                True if running, False otherwise
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

        Parameters
            op: str
                Operation can be one of [start, stop, restart]
        """
        ops = {
            'start': ('Starting', 'start', 'started'),
            'stop': ('Stopping', 'stop', 'stopped'),
            'restart': ('Restarting', 'restart', 'restarted')
        }
        s0, s1, s2 = ops[op]

        self.logger.debug(f"{s0} required modules")
        cmd = f"docker exec {self.container_name} ./scripts/bootstrap_maggie.sh {s1}"
        subprocess.run(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.logger.debug(f'Modules {s2}')

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

        Parameters:
            record_id: str
                The name of the record file
        """
        self.logger.debug(f"Starting recorder")
        cmd = f"docker exec {self.container_name} /apollo/bazel-bin/modules/custom_nodes/record_node start {self.container_name}.{record_id}"
        subprocess.run(
            cmd.split(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def stop_recorder(self):
        """
        Stops cyber_recorder
        """
        self.logger.debug(f"Stopping recorder")
        cmd = f"docker exec {self.container_name} /apollo/bazel-bin/modules/custom_nodes/record_node stop"
        subprocess.run(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def start_sim_control_standalone(self):
        """
        Starts SimControlStandalone module
        """
        self.logger.debug(f"Starting sim_control_standalone")
        cmd = f"docker exec -d {self.container_name} /apollo/bazel-bin/modules/sim_control/sim_control_main"
        result = subprocess.run(
            cmd.split(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def stop_sim_control_standalone(self):
        """
        Stops SimControlStandalone module
        """
        self.logger.debug(f"Stopping sim_control_standalone")
        cmd = f"docker exec {self.container_name} /apollo/modules/sim_control/script.sh stop"
        subprocess.run(
            cmd.split(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def stop_all(self):
        self.bridge.stop()
        if USE_SIM_CONTROL_STANDALONE:
            self.stop_sim_control_standalone()
        else:
            self.dreamview.stop_sim_control()
        self.stop_modules()

    def reset(self):
        """
        Resets the container
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
        if USE_SIM_CONTROL_STANDALONE:
            self.start_sim_control_standalone()
