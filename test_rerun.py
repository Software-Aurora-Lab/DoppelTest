from config import HD_MAP_PATH
from framework.scenario import Scenario
from hdmap.MapParser import MapParser

ma = MapParser(HD_MAP_PATH)
chromosome = Scenario.from_json('/home/sora/Desktop/yhuai/DoppelTest/data/c.json')

print(chromosome)