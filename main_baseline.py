from datetime import datetime
import os
from apollo.ApolloContainer import ApolloContainer
from config import APOLLO_ROOT, HD_MAP_PATH, RECORDS_DIR, RUN_FOR_HOUR
from framework.baseline.BaseScenarioRunner import BaseScenarioRunner
from framework.oracles import RecordAnalyzer
from framework.oracles.ViolationTracker import ViolationTracker
from hdmap.MapParser import MapParser
from framework.scenario import Scenario
from utils import remove_record_files


def eval_scenario(ctn: ApolloContainer, s: Scenario):
    br = BaseScenarioRunner(ctn)
    br.set_scenario(s)
    br.init_scenario()
    g_name = f'Generation_{s.gid:05}'
    s_name = f'Scenario_{s.cid:05}'
    obs = br.run_scenario(g_name, s_name, True)
    obs_routing = dict()
    for x, y in obs:
        obs_routing[x] = y.routing_str
    r_name = f"{ctn.container_name}.{s_name}.00000"
    record_path = os.path.join(RECORDS_DIR, g_name, s_name, r_name)
    ra = RecordAnalyzer(record_path)
    ra.analyze()

    adc = s.ad_section.adcs[0]
    for v in ra.get_results():
        main_type = v[0]
        sub_type = v[1]
        if main_type == 'collision':
            if sub_type < 100:
                # pedestrian collisoin
                related_data = frozenset(
                    [adc.routing_str, s.pd_section.pds[sub_type].cw_id])
                sub_type = 'A&P'
            else:
                # adc to adc collision
                related_data = frozenset(
                    [adc.routing_str, obs_routing[sub_type]]
                )
                sub_type = 'A&A'
        else:
            related_data = adc.routing_str
        ViolationTracker.get_instance().add_violation(
            gname=g_name,
            sname=s_name,
            record_file=record_path,
            mt=main_type,
            st=sub_type,
            data=related_data
        )
    if len(ra.get_results()) == 0:
        remove_record_files(g_name, s_name)
    else:
        print(ra.get_results())


def main():
    ma = MapParser(HD_MAP_PATH)
    ctn = ApolloContainer(APOLLO_ROOT, 'ROUTE_0')
    ctn.start_instance()
    ctn.start_dreamview()
    vt = ViolationTracker()
    POP_SIZE = 10

    s = Scenario.get_one()
    s.gid = 0
    s.sid = 0

    start_time = datetime.now()

    curr_gen = 0
    while True:
        print(f'===== BASE Generation {curr_gen} =====')
        population = [Scenario.get_one() for _ in range(POP_SIZE)]
        for index, c in enumerate(population):
            c.gid = curr_gen
            c.cid = index

        for ind in population:
            for adc in ind.ad_section.adcs:
                adc.start_t = 0.0
            print(f'Running scenario {ind.cid} - {ind.gid}')
            eval_scenario(ctn, ind)

        curr_gen += 1
        vt.save_to_file()
        curr_time = datetime.now()
        tdelta = (curr_time - start_time).total_seconds()
        if tdelta / 3600 > RUN_FOR_HOUR:
            break


if __name__ == '__main__':
    main()
