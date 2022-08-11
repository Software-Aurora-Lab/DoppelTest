import os
from modules.map.proto.map_pb2 import Map
import pandas as pd


BASE_DIR = './data/maps'
maps = sorted(os.listdir(BASE_DIR))

data = list()
for x in maps:
    map_bin = os.path.join(BASE_DIR, x, "base_map.bin")
    f = open(map_bin, 'rb')
    map = Map()
    map.ParseFromString(f.read())
    f.close()

    data.append({
        'name': x,
        'lanes': len(map.lane),
        'junctions': len(map.junction),
        'signals': len(map.signal),
        'crosswalks': len(map.crosswalk)
    })

df = pd.DataFrame(data)
print(df)
