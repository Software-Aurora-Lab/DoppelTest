import time
from typing import List, Tuple

from cyber_record.record import Record

from framework.oracles.impl.CollisionOracle import CollisionOracle
from framework.oracles.impl.ComfortOracle import ComfortOracle
from framework.oracles.impl.EStopOracle import EStopOracle
from framework.oracles.impl.JunctionLaneChangeOracle import \
    JunctionLaneChangeOracle
from framework.oracles.impl.ModuleOracle import ModuleOracle
from framework.oracles.impl.PlanningCrashOracle import PlanningCrashOracle
from framework.oracles.impl.SpeedingOracle import SpeedingOracle
from framework.oracles.impl.StopSignOracle import StopSignOracle
from framework.oracles.impl.TrafficSignalOracle import TrafficSignalOracle
from framework.oracles.impl.UnsafeLaneChangeOracle import \
    UnsafeLaneChangeOracle
from framework.oracles.impl.UUStopOracle import UUStopOracle
from framework.oracles.OracleManager import OracleManager


class RecordAnalyzer:
    """
    Record analyzer, used for analyzing cyber record files

    :param str record_path: filename of the record
    """
    record_path: str
    analyzed: bool
    MAX_RETRY = 3 # times
    RETRY_DELAY = 2 # seconds

    def __init__(self, record_path: str) -> None:
        self.oracle_manager = OracleManager()
        self.record_path = record_path
        self.register_oracles()
        self.analyzed = False

    def register_oracles(self):
        """
        Register oracles to be used
        """
        oracles = [
            CollisionOracle(),
            EStopOracle(),
            ModuleOracle(),
            ComfortOracle(),
            StopSignOracle(),
            TrafficSignalOracle(),
            UUStopOracle(),
            SpeedingOracle(),
            JunctionLaneChangeOracle(),
            UnsafeLaneChangeOracle(),
            # PlanningCrashOracle(),
        ]
        for o in oracles:
            self.oracle_manager.register_oracle(o)

    def analyze(self) -> List[Tuple]:
        """
        Analyze the record file and retrieve results from each of the oracles

        :returns: list of violations
        :rtype: List[Tuple]
        """
        trial = 1
        while trial <= RecordAnalyzer.MAX_RETRY:
            try :
                record = Record(self.record_path)
                for topic, message, t in record.read_messages():
                    self.oracle_manager.on_new_message(topic, message, t)
                self.analyzed = True
                return self.get_results()
            except AttributeError:
                time.sleep(2)
                trial += 1
            except FileNotFoundError:
                time.sleep(2)
                trial += 1
        return list()
        

    def get_results(self) -> List[Tuple]:
        """
        Retrieve results from each of the oracles

        :returns: list of violations
        :rtype: List[Tuple]
        """
        if not self.analyzed:
            return list()
        return self.oracle_manager.get_results()
