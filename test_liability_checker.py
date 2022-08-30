from framework.baseline.liability_checker import CollisionLiabilityChecker
from hdmap.MapParser import MapParser

ma = MapParser('./data/maps/borregas_ave_fix/base_map.bin')
# record_path = "/home/nkt/Desktop/AV_Project/apollo_issues_13638/08261958_BASE/Generation_00003/Scenario_00006/apollo_dev_ROUTE_0.Scenario_00006.00000"
record_path = "/home/nkt/Desktop/AV_Project/apollo_issues_13638/08261958_BASE/Generation_00024/Scenario_00008/apollo_dev_ROUTE_0.Scenario_00008.00000"
lc = CollisionLiabilityChecker(record_path)
lc.start()
print(lc.get_results())
