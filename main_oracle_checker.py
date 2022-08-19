from framework.oracles import RecordAnalyzer
from hdmap.MapParser import MapParser


def main():
    ma = MapParser('./data/maps/shalun/base_map.bin')
    record_path = "/home/nkt/Desktop/AV_Project/apollo_issues_13638/apollo_7.0_simcontrol__shalun__planning_deadlock_at_stop_sign__1.record.00000"
    ra = RecordAnalyzer(record_path)
    ra.analyze()
    # print(ra.get_results())


if __name__ == '__main__':
    main()
