from framework.oracles import RecordAnalyzer
from hdmap.MapParser import MapParser

ma = MapParser('./data/maps/borregas_ave/base_map.bin')
record_path = ""
ra = RecordAnalyzer(record_path)
ra.analyze()
print(ra.get_results())
