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

while True:
    ar.initialize()
    runner_time = 0
    ar.container.start_recorder()
    while True:
        if runner_time % 1000 == 0:
            print(runner_time)
        if ar.should_send_routing(runner_time):
            ar.send_routing()
        time.sleep(0.01)
        runner_time += 10

        exit_reason = ar.get_exit_reason()
        if exit_reason:
            ar.stop(exit_reason)
            ar.container.stop_recorder()
            break

    x = input('Continue? y/n')
    if x == 'n':
        break
