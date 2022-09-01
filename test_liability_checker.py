from collections import defaultdict

from apollo.utils import find_all_files_by_wildcard, get_current_timestamp
from framework.baseline.liability_checker import CollisionLiabilityChecker
from framework.baseline.liability_checker.CollisionLiabilityChecker import CollisionType
from framework.oracles import RecordAnalyzer
from hdmap.MapParser import MapParser
from utils import get_logger

logger = get_logger(__name__)


def analyze_record_files():
    base_record_dir = "./data/records"
    all_record_file_paths = find_all_files_by_wildcard(base_record_dir, "Generation_*/Scenario_*/apollo_dev_*")
    record_file_count = len(all_record_file_paths)
    violation_type_counter = defaultdict(int)
    not_rear_end_files = set()

    for i, r_path in enumerate(all_record_file_paths):
        found_violations = check_violation(r_path)
        violation_type_counter["stop_sign"] += found_violations.count("stop_sign")
        violation_type_counter["traffic_signal"] += found_violations.count("traffic_signal")
        if "collision" in found_violations:
            collision_type_count = count_collision_types(r_path)
            for c_type, count in collision_type_count.items():
                violation_type_counter[c_type] += count
            if collision_type_count.get("collision_a_and_a__default", 0) > 0:
                not_rear_end_files.add(r_path)
        logger.info(f"[{i}/{record_file_count}] Counted violations from {r_path} - {str(dict(violation_type_counter))}")

    report_output = f"{dict(violation_type_counter)}\n{not_rear_end_files}"
    print(report_output)

    with open(f"liability_checker_report_{get_current_timestamp()}.txt", "w+") as out_file:
        out_file.write(report_output)


def check_violation(record_file_path):
    ra = RecordAnalyzer(record_file_path)
    ra.analyze()
    oracle_checking_results = ra.get_results()
    return [r[0] for r in oracle_checking_results]


def count_collision_types(record_file_path):
    lc = CollisionLiabilityChecker(record_file_path)
    lc.start()
    liability_checking_results = lc.get_results()

    collision_type_counter = defaultdict(int)
    collision_type_counter["collision_a_and_p"] = 0
    collision_type_counter["collision_a_and_a__rear_end"] = 0
    collision_type_counter["collision_a_and_a__default"] = 0

    for r in liability_checking_results.get("collision", []):
        collision_type = r["type"]
        obstacle_id = r["obstacle_id"]
        if obstacle_id < 100:
            collision_type_counter["collision_a_and_p"] += 1
        else:
            if collision_type == CollisionType.REAR_END:
                collision_type_counter["collision_a_and_a__rear_end"] += 1
            else:
                collision_type_counter["collision_a_and_a__default"] += 1
    return dict(collision_type_counter)


if __name__ == '__main__':
    map_dir = "./data/maps/borregas_ave_fix/base_map.bin"
    MapParser(map_dir)

    analyze_record_files()
