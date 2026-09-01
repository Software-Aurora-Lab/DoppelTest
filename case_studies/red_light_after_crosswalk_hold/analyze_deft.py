"""Trace the red-light entry: which traffic-light message did planning consume?

Run from the DoppelTest repository root so ``config`` and the generated protobuf
modules are importable:

    PYTHONPATH=. .venv/bin/python \\
      case_studies/red_light_after_crosswalk_hold/analyze_deft.py

Pass a record path as argv[1] to analyse a different record.
"""
import os
import sys
from shapely.geometry import Polygon
from cyber_record.record import Record
from apollo.utils import calculate_velocity, generate_adc_polygon
from framework.oracles.impl.TrafficSignalOracle import TrafficSignalOracle
from modules.perception.proto.traffic_light_detection_pb2 import TrafficLight

NAMES = {0: 'UNKNOWN', 1: 'RED', 2: 'YELLOW', 3: 'GREEN', 4: 'BLACK'}
SIG = 'signal_3'
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'apollo_dev_ROUTE_2.Scenario_00007.00000')
line = TrafficSignalOracle().traffic_signal_stop_line_string_dict[SIG]

# pass 1: index traffic light messages by sequence_num
tl_by_seq = {}      # seq -> (t_rel, color of SIG)
tl_stream = []      # (t_rel, seq, color)
t0 = None
for topic, msg, t in Record(path).read_messages():
    if t0 is None: t0 = t
    if topic != '/apollo/perception/traffic_light':
        continue
    seq = msg.header.sequence_num
    col = None
    for x in msg.traffic_light:
        if x.id == SIG: col = x.color
    tl_by_seq[seq] = ((t - t0) / 1e9, col)
    tl_stream.append(((t - t0) / 1e9, seq, col))

first_red = next((s for s in tl_stream if s[2] == TrafficLight.RED), None)
print(f'traffic light messages: {len(tl_stream)}  seq {tl_stream[0][1]}..{tl_stream[-1][1]}')
if first_red:
    print(f'{SIG} first published RED at t=+{first_red[0]:.2f}s (seq {first_red[1]})')

# pass 2: walk localization + planning together
touch = []
plans = []
t0 = None
for topic, msg, t in Record(path).read_messages():
    if t0 is None: t0 = t
    ts = (t - t0) / 1e9
    if topic == '/apollo/localization/pose':
        p = msg.pose
        poly = Polygon([[x.x, x.y] for x in generate_adc_polygon(p.position, p.heading)])
        if not line.intersection(poly).is_empty:
            touch.append((ts, calculate_velocity(p.linear_velocity)))
    elif topic == '/apollo/planning':
        if not msg.HasField('deft'):
            continue
        d = msg.deft
        tlh = d.traffic_light_header
        consumed = tl_by_seq.get(tlh)
        plans.append((ts, msg.header.sequence_num, tlh, consumed,
                      msg.trajectory_point[0].v if msg.trajectory_point else None,
                      str(msg.decision.main_decision).replace('\n', ' ')[:90]))

print(f'\nADC on {SIG} stop line: t=+{touch[0][0]:.2f}s .. +{touch[-1][0]:.2f}s '
      f'(speed {min(x[1] for x in touch):.2f}..{max(x[1] for x in touch):.2f} m/s)')

lo, hi = touch[0][0] - 3.0, touch[-1][0] + 0.5
print(f'\nplanning cycles from t=+{lo:.1f}s to +{hi:.1f}s:')
print(f"{'t_rel':>7} {'plan_seq':>8} {'deft.tl_hdr':>11} {'tl_pub_at':>9} {'colour':>7} {'lag':>6}  v     decision")
for ts, pseq, tlh, consumed, v, dec in plans:
    if not (lo <= ts <= hi):
        continue
    if consumed is None:
        print(f'{ts:7.2f} {pseq:8d} {tlh:11d}   <no such tl seq in record>')
        continue
    tpub, col = consumed
    live = [s for s in tl_stream if s[0] <= ts]
    lag = (live[-1][1] - tlh) if live else 0
    vs = f'{v:.2f}' if v is not None else '  - '
    print(f'{ts:7.2f} {pseq:8d} {tlh:11d} {tpub:9.2f} {NAMES.get(col,col):>7} {lag:5d}m {vs}  {dec}')
