from hdmap.MapParser import MapParser

mp = MapParser('./data/maps/borregas_ave/base_map.bin')
# mp = MapParser('./data/maps/san_mateo/base_map.bin')
mp.get_signals_wrt('signal_0')

r = mp.get_coordinate_and_heading('lane_23', 0)
print(r)
