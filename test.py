import time
from unittest import runner
from apollo.ApolloContainer import ApolloContainer
from modules.map.proto.map_pb2 import Map
from scenario.ApolloRunner import ApolloRunner, PositionEstimate
map = Map()
f = open('./data/maps/borregas_ave_fix/base_map.bin', 'rb')
map.ParseFromString(f.read())

ctn = ApolloContainer('/home/yuqi/ResearchWorkspace/apollo', 'yuqi')
ctn.start_instance()
ctn.start_dreamview()
ctn.start_bridge()

ar = ApolloRunner(
    nid=0,
    ctn=ctn,
    map=map,
    start=PositionEstimate('lane_23', 13.04),  # 13.04
    destination=PositionEstimate('lane_27', 20),
    start_time=1
)


ar.initialize()
ar.send_routing()
while ar.get_exit_reason() is None:
    print('1')
    time.sleep(1)
    pass
ar.stop('asd')
