import time
from apollo.ApolloContainer import ApolloContainer
from apollo.MessageBroker import MessageBroker
from modules.map.proto.map_pb2 import Map
from scenario.ApolloRunner import ApolloRunner, PositionEstimate
map = Map()
f = open('./data/maps/borregas_ave_fix/base_map.bin', 'rb')
map.ParseFromString(f.read())

genes = [
    ('yuqi', 1, ('lane_25', 190), ('lane_27', 20), 77777),
    ('josh', 1, ('lane_23', 13.04), ('lane_27', 20), 66666),
]

runners = list()
for a, b, c, d, e in genes:
    ctn = ApolloContainer('/home/yuqi/ResearchWorkspace/apollo', a)
    ctn.start_instance()
    ctn.start_dreamview()
    ctn.start_bridge()

    ar = ApolloRunner(
        nid=e,
        ctn=ctn,
        map=map,
        start=PositionEstimate(*c),
        destination=PositionEstimate(*d),
        start_time=1
    )
    ar.initialize()
    runners.append(ar)


mbk = MessageBroker(runners)
mbk.spin()


runner_time = 0
while True:
    exit_reasons = list()
    for ar in runners:
        if ar.should_send_routing(runner_time):
            ar.send_routing()
        exit_reasons.append(ar.get_exit_reason())
    if all(exit_reasons):
        print(exit_reasons)
        break
    print(exit_reasons)
    time.sleep(0.1)
    runner_time += 100

mbk.stop()
for r in runners:
    r.stop('MAIN')
