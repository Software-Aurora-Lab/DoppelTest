# Apollo enters a junction on red after a crosswalk hold

**Summary.** Apollo latches a traffic light as "done" as soon as the ADC comes
within 2.0 m of the stop line *while the light is green*, and never re-evaluates
it. If the ADC is then held behind the stop line by an unrelated constraint until
the light turns red, no stop fence is ever built for that signal and the ADC
drives into the junction on red.

The planner is not starved of input: it consumes a current `RED` traffic-light
message on every cycle throughout the crossing. The failure is in the decision
layer, not in perception or message delivery.

| | |
|---|---|
| Apollo | `YuqiHuai/BaiduApollo`, branch `v7_mozart` |
| Map | `borregas_ave` |
| Signal | `signal_3` (stop line at reference-line `s = 34.23`) |
| Source run | `data/records/2026-08-30_23-26-01`, `Generation_00032/Scenario_00007` |
| Instance | `apollo_dev_ROUTE_2` |
| Severity | Red-light running into a signalised junction |

## Files

| File | Description |
|---|---|
| `apollo_dev_ROUTE_2.Scenario_00007.00000` | cyber record of the violating instance (40 MB) |
| `c.json` | the scenario chromosome (all 5 ADCs, 6 pedestrians, signal program) |
| `analyze_deft.py` | reproduces the DeFT trace below |

The other four instances' records stay in the source run directory; they are not
needed to reproduce the finding.

Reproduce the trace from the repository root:

```bash
PYTHONPATH=. .venv/bin/python \
  case_studies/red_light_after_crosswalk_hold/analyze_deft.py
```

## Scenario

The violating instance is `ad_section.adcs[2]`:

- route `lane_10 → lane_47 → lane_30 → lane_18 → lane_26`, `start_s = 3.0`, `start_t = 4.0`
- approaches `signal_3` at roughly 7 m/s

Two other elements matter:

- **Pedestrian** `pd_section.pds[3]`: crosswalk `CW_2`, speed 2.3 m/s, `start_t = 6`.
  Apollo yields to it as a normal crosswalk obstacle (`STOP_REASON_CROSSWALK`,
  `"stop by CW_CW_2"`) — from the planner's point of view this is a lawful yield.
- **Signal program** (`tc_section`): `signal_3` runs `GREEN → RED` with
  `duration_g = 11 s`, `duration_y = 3 s`, `duration_b = 2 s`. Green therefore ends
  at t≈11 s and the first `RED` is published at t = +14.24 s.

## Timeline

All times are relative to the first message in the record.

| t (s) | Event |
|---|---|
| 9.0–10.0 | ADC approaches at ~7 m/s. Scenario `LANE_FOLLOW`. `signal_3` **GREEN**. |
| 10.13 | Scenario → `TRAFFIC_LIGHT_PROTECTED`, stage `..._APPROACH` (400). Still **GREEN**. ADC front `s = 29.38` (4.85 m to stop line). |
| ~10.2–12.1 | Approach stage finishes **while green**; stage → `..._INTERSECTION_CRUISE` (401). |
| 12.07 | Stage 401. ADC front `s = 33.43` (0.80 m to stop line). **Signal debug list is now empty.** |
| 12.25–14.75 | ADC stopped 0.72–0.75 m behind the stop line, holding `stop by CW_CW_2` for the pedestrian. |
| **14.24** | **`signal_3` turns RED** (traffic-light message seq 141). ADC stationary, still behind the line. |
| 14.98 | Pedestrian clears. Decision flips to `cruise { FORWARD }` **while consuming a RED message**. ADC begins accelerating from standstill. |
| 15.94 | ADC front crosses the stop line at 1.61 m/s, **on red**. |
| 17.59 | ADC clears the junction at 4.19 m/s. |

Across the whole record there are **zero** `STOP_REASON_SIGNAL` decisions. The only
stop decisions are 81 × `stop by CW_CW_2` (crosswalk) and 2 × `stop by 3_0`
(`STOP_REASON_HEAD_VEHICLE`, at t = 10.35 and 10.91, before the light changed).

## Evidence: the light was read, and it was red

`ADCTrajectory.deft` (`modules/planning/proto/planning.proto:52`, populated in
`modules/planning/on_lane_planning.cc:280`) records the `sequence_num` of the
traffic-light message each planning cycle consumed. `TrafficControlManager`
increments that sequence monotonically, so the mapping to a published colour is
exact.

```
signal_3 first published RED at t=+14.24s (tl seq 141)

t_rel  plan_seq  deft.tl_hdr  tl_pub_at  colour  lag   v     decision
14.29     148        140       14.14    YELLOW   1m   0.00  stop  STOP_REASON_CROSSWALK "stop by CW_CW_2"
14.45     149        141       14.24    RED      2m   0.00  stop  STOP_REASON_CROSSWALK "stop by CW_CW_2"
14.83     152        145       14.65    RED      1m   0.00  stop  STOP_REASON_CROSSWALK "stop by CW_CW_2"
14.98     153        146       14.75    RED      2m   0.00  cruise { change_lane_type: FORWARD }   <-- flips here
15.50     155        150       15.16    RED      3m   0.02  cruise
16.23     158        158       15.98    RED      2m   1.09  cruise
17.85     168        174       17.61    RED      2m   4.04  cruise
```

Every cycle from 14.45 onward consumed a genuinely `RED` message with a lag of
0–3 messages (≤ 0.3 s). This rules out stale input, dropped messages, and CPU
starvation as explanations.

## Root cause

`modules/planning/scenarios/traffic_light/protected/stage_approach.cc:83-93`
finishes the approach stage as soon as the ADC is close enough **and** the light
is green:

```cpp
// check distance to stop line
if (distance_adc_to_stop_line >
    scenario_config_.max_valid_stop_distance()) {   // 2.0 m
  traffic_light_all_done = false;
  break;
}

// check on traffic light color
if (signal_color != TrafficLight::GREEN) {
  traffic_light_all_done = false;
  break;
}
```

`FinishStage()` then records the overlap as done (`stage_approach.cc:110`), and
`TrafficLight::MakeDecisions` skips that signal from then on:

```cpp
// modules/planning/traffic_rules/traffic_light.cc:93
if (traffic_light_done) {
  continue;
}
```

That `continue` sits **before** `signal_light_debug->add_signal()` at
`traffic_light.cc:131`, which is why the signal debug list is empty from t = 12.07
onward — the observable that identifies which branch was taken. The two other
early `continue`s cannot apply here:

- `traffic_light.cc:80` (`end_s <= adc_back_edge_s`) requires the ADC to be past
  the signal; its front edge was at `s = 33.43` against a stop line at 34.23.
- `traffic_light.cc:113` (s-projection discrepancy) requires a mismatch greater
  than 10 m; the along-reference-line and Euclidean distances agreed to ~0.8 m.

So `BuildStopDecision(... STOP_REASON_SIGNAL ...)` at `traffic_light.cc:155` was
never reached.

### The latch is one-way

`done_traffic_light_overlap_id` (`planning_status.proto:132`) is written for this
scenario in exactly one place and cleared in exactly one place — line 107 of the
*next* approach stage's `FinishStage()`, immediately before it is repopulated.
There is no clear on stage exit, no timeout, and no invalidation when the signal
colour changes. Once set for `signal_3`, it holds for the whole junction
traversal, and nothing in the path re-checks the light before the ADC enters the
junction.

## Triggering conditions

The pedestrian is incidental. The defect needs only:

1. the ADC crosses into the 2.0 m window while the light is green, latching the
   signal as done;
2. any independent constraint holds it behind the stop line;
3. the light turns red during that hold.

A lead vehicle or a stop-and-go queue satisfies (2) equally well, so the defect
should be reproducible without DoppelTest's pedestrian model. Both correct
behaviours — entering the window on green, and yielding at the crosswalk —
compose into a red-light violation.

## Scope: related code paths

The same latch is populated by two other traffic-light scenarios, and the skip in
`traffic_light.cc:93` is shared by all of them:

- `scenarios/traffic_light/unprotected_left_turn/stage_approach.cc:142`
- `scenarios/traffic_light/unprotected_right_turn/stage_stop.cc:187`

Whether those paths carry a re-check that the protected path lacks has not been
verified. If they do not, this is a class of three rather than a single bug.

## Note on the source run's violation counts

`summary.csv` for the source run lists 255 `traffic_signal` rows, which are **not**
255 instances of this bug:

- The rows are an occurrence log, not a violation list —
  `ViolationTracker.add_violation` defaults to `force=True`, so every re-detection
  is appended. The 255 rows collapse to 2 distinct `(type, sub_type, data)` keys.
- Classifying 18 of the flagged rows by the light colour at the moment the ADC
  first touched the stop line gives 8 entered on green, 9 entered on yellow, and
  **1 entered on red** — this case. `TrafficSignalOracle` has no notion of when
  the ADC entered, so it flags any sample where the ADC polygon touches the stop
  line while the light is red.

This case study is the single confirmed red-light entry from that run.
