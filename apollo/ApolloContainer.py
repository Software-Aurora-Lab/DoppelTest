import subprocess
import docker
import time
from apollo.CyberBridge import CyberBridge
from apollo.Dreamview import Dreamview

from utils import get_logger


class ApolloContainer:
    apollo_root: str
    username: str
    bridge: CyberBridge
    dreamview: Dreamview
    port = 8888
    bridge_port = 9090

    cyber_recorder = '/apollo/bazel-bin/cyber/tools/cyber_recorder/cyber_recorder'

    def __init__(self, apollo_root: str, username: str) -> None:
        self.apollo_root = apollo_root
        self.username = username
        self.logger = get_logger(f"ApolloContainer[{self.container_name}]")

    @property
    def container_name(self):
        return f"apollo_dev_{self.username}"

    def is_running(self) -> bool:
        ''' Checks if the Apollo container is running
        '''
        try:
            return docker.from_env().containers.get(self.container_name).status == 'running'
        except:
            return False

    @property
    def ip(self) -> str:
        assert self.is_running(
        ), f'Instance {self.container_name} is not running.'
        ctn = docker.from_env().containers.get(self.container_name)
        return ctn.attrs['NetworkSettings']['IPAddress']

    def start_instance(self, restart=False):
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
            self.logger.info(
                f'Dreamview running at http://{self.ip}:{self.port}')

        self.logger.debug(s2)

    def start_dreamview(self):
        self.__dreamview_operation('start')

    def stop_dreamview(self):
        self.__dreamview_operation('stop')

    def restart_dreamview(self):
        self.__dreamview_operation('restart')

    def start_bridge(self):
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
        self.logger.debug('Resetting bridge connection')
        if not self.__is_bridge_started():
            return
        if not self.bridge is None:
            self.bridge.conn.close()
        self.bridge = CyberBridge(self.ip, self.bridge_port)

    def __is_bridge_started(self):
        try:
            b = CyberBridge(self.ip, self.bridge_port)
            b.conn.close()
            return True
        except:
            return False

    def __modules_operation(self, op: str):
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
        self.__modules_operation('start')

    def stop_modules(self):
        self.__modules_operation('stop')

    def restart_modules(self):
        self.__modules_operation('restart')

    def start_recorder(self, record_id: str):
        self.logger.debug(f"Starting recorder")
        cmd = f"docker exec {self.container_name} /apollo/bazel-bin/modules/custom_nodes/record_node start {self.container_name}.{record_id}"
        subprocess.run(
            cmd.split(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def stop_recorder(self):
        self.logger.debug(f"Stopping recorder")
        cmd = f"docker exec {self.container_name} /apollo/bazel-bin/modules/custom_nodes/record_node stop"
        subprocess.run(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def start_sim_control_standalone(self):
        self.logger.debug(f"Starting sim_control_standalone")
        cmd = f"docker exec {self.container_name} /apollo/modules/sim_control/script.sh start"
        subprocess.run(
            cmd.split(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def stop_sim_control_standalone(self):
        self.logger.debug(f"Stopping sim_control_standalone")
        cmd = f"docker exec {self.container_name} /apollo/modules/sim_control/script.sh stop"
        subprocess.run(
            cmd.split(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def reset(self):
        self.logger.debug(f'Resetting')
        self.stop_modules()
        self.stop_sim_control_standalone()
        self.start_bridge()
        self.reset_bridge_connection()
        self.start_sim_control_standalone()
        self.start_modules()
