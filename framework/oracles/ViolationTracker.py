from collections import defaultdict
from typing import DefaultDict, Dict, List, Set, Tuple
import pandas as pd
import os
from config import RECORDS_DIR


class ViolationTracker:
    tracker: DefaultDict[str, DefaultDict[str, Set[object]]]
    scenario_tracker: List
    __instance = None

    def __init__(self) -> None:
        self.tracker = defaultdict(lambda: defaultdict(lambda: set()))
        self.scenario_tracker = list()
        ViolationTracker.__instance = self

    @staticmethod
    def get_instance():
        return ViolationTracker.__instance

    def add_violation(self, gname, sname, record_file, mt, st, data, force=True) -> bool:
        """
        Returns True if added (unique)
        """
        if force:
            self.scenario_tracker.append(
                (f"{gname}/{sname}", mt, st, data, record_file))
            return True

        if data not in self.tracker[mt][st]:
            self.tracker[mt][st].add(data)
            self.scenario_tracker.append(
                (f"{gname}/{sname}", mt, st, data, record_file)
            )
            return True
        return False

    def save_to_file(self):
        column_names = ['scenario_id', "main_type",
                        "sub_type", "data", "record_path"]
        df = pd.DataFrame(columns=column_names)
        for scenario in self.scenario_tracker:
            df.loc[len(df.index)] = [
                *scenario
            ]
        df.to_csv(os.path.join(RECORDS_DIR, "summary.csv"))
