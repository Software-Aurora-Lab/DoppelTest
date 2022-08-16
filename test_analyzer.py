from framework.oracles import RecordAnalyzer
from hdmap.MapParser import MapParser

ma = MapParser('./data/maps/borregas_ave/base_map.bin')
record_path = "/home/yuqi/ResearchWorkspace/apollo/movies/movie_yuqi/Generation_00021/Scenario_00002/apollo_dev_ROUTE_1.Scenario_00002.00000"
ra = RecordAnalyzer(record_path)
ra.analyze()
print(ra.get_results())
