# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/planning/proto/traffic_rule_config.proto

import sys

_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='modules/planning/proto/traffic_rule_config.proto',
  package='apollo.planning',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n0modules/planning/proto/traffic_rule_config.proto\x12\x0f\x61pollo.planning\"7\n\x15\x42\x61\x63ksideVehicleConfig\x12\x1e\n\x13\x62\x61\x63kside_lane_width\x18\x01 \x01(\x01:\x01\x34\"\x8e\x02\n\x0f\x43rosswalkConfig\x12\x18\n\rstop_distance\x18\x01 \x01(\x01:\x01\x31\x12 \n\x15max_stop_deceleration\x18\x02 \x01(\x01:\x01\x34\x12\x1e\n\x13min_pass_s_distance\x18\x03 \x01(\x01:\x01\x31\x12\"\n\x17max_valid_stop_distance\x18\x04 \x01(\x01:\x01\x33\x12\x1c\n\x11\x65xpand_s_distance\x18\x05 \x01(\x01:\x01\x32\x12!\n\x16stop_strict_l_distance\x18\x06 \x01(\x01:\x01\x34\x12 \n\x15stop_loose_l_distance\x18\x07 \x01(\x01:\x01\x35\x12\x18\n\x0cstop_timeout\x18\x08 \x01(\x01:\x02\x31\x30\"/\n\x11\x44\x65stinationConfig\x12\x1a\n\rstop_distance\x18\x01 \x01(\x01:\x03\x30.5\"\xa6\x01\n\x0fKeepClearConfig\x12$\n\x16\x65nable_keep_clear_zone\x18\x01 \x01(\x08:\x04true\x12\x1d\n\x0f\x65nable_junction\x18\x02 \x01(\x08:\x04true\x12\x1e\n\x13min_pass_s_distance\x18\x03 \x01(\x01:\x01\x32\x12.\n!align_with_traffic_sign_tolerance\x18\x04 \x01(\x01:\x03\x34.5\"b\n\x16ReferenceLineEndConfig\x12\x1a\n\rstop_distance\x18\x01 \x01(\x01:\x03\x30.5\x12,\n min_reference_line_remain_length\x18\x02 \x01(\x01:\x02\x35\x30\"N\n\x0fReroutingConfig\x12\x18\n\rcooldown_time\x18\x01 \x01(\x01:\x01\x33\x12!\n\x16prepare_rerouting_time\x18\x02 \x01(\x01:\x01\x32\"A\n\x0eStopSignConfig\x12\x15\n\x07\x65nabled\x18\x01 \x01(\x08:\x04true\x12\x18\n\rstop_distance\x18\x02 \x01(\x01:\x01\x31\"g\n\x12TrafficLightConfig\x12\x15\n\x07\x65nabled\x18\x01 \x01(\x08:\x04true\x12\x18\n\rstop_distance\x18\x02 \x01(\x01:\x01\x31\x12 \n\x15max_stop_deceleration\x18\x03 \x01(\x01:\x01\x34\"c\n\x0fYieldSignConfig\x12\x15\n\x07\x65nabled\x18\x01 \x01(\x08:\x04true\x12\x18\n\rstop_distance\x18\x02 \x01(\x01:\x01\x31\x12\x1f\n\x14start_watch_distance\x18\x03 \x01(\x01:\x01\x32\"\xac\x06\n\x11TrafficRuleConfig\x12:\n\x07rule_id\x18\x01 \x01(\x0e\x32).apollo.planning.TrafficRuleConfig.RuleId\x12\x0f\n\x07\x65nabled\x18\x02 \x01(\x08\x12\x42\n\x10\x62\x61\x63kside_vehicle\x18\x03 \x01(\x0b\x32&.apollo.planning.BacksideVehicleConfigH\x00\x12\x35\n\tcrosswalk\x18\x04 \x01(\x0b\x32 .apollo.planning.CrosswalkConfigH\x00\x12\x39\n\x0b\x64\x65stination\x18\x05 \x01(\x0b\x32\".apollo.planning.DestinationConfigH\x00\x12\x36\n\nkeep_clear\x18\x06 \x01(\x0b\x32 .apollo.planning.KeepClearConfigH\x00\x12\x45\n\x12reference_line_end\x18\x07 \x01(\x0b\x32\'.apollo.planning.ReferenceLineEndConfigH\x00\x12\x35\n\trerouting\x18\x08 \x01(\x0b\x32 .apollo.planning.ReroutingConfigH\x00\x12\x34\n\tstop_sign\x18\t \x01(\x0b\x32\x1f.apollo.planning.StopSignConfigH\x00\x12<\n\rtraffic_light\x18\n \x01(\x0b\x32#.apollo.planning.TrafficLightConfigH\x00\x12\x36\n\nyield_sign\x18\x0b \x01(\x0b\x32 .apollo.planning.YieldSignConfigH\x00\"\xa7\x01\n\x06RuleId\x12\x14\n\x10\x42\x41\x43KSIDE_VEHICLE\x10\x01\x12\r\n\tCROSSWALK\x10\x02\x12\x0f\n\x0b\x44\x45STINATION\x10\x03\x12\x0e\n\nKEEP_CLEAR\x10\x04\x12\x16\n\x12REFERENCE_LINE_END\x10\x05\x12\r\n\tREROUTING\x10\x06\x12\r\n\tSTOP_SIGN\x10\x07\x12\x11\n\rTRAFFIC_LIGHT\x10\x08\x12\x0e\n\nYIELD_SIGN\x10\tB\x08\n\x06\x63onfig\"H\n\x12TrafficRuleConfigs\x12\x32\n\x06\x63onfig\x18\x01 \x03(\x0b\x32\".apollo.planning.TrafficRuleConfig')
)



_TRAFFICRULECONFIG_RULEID = _descriptor.EnumDescriptor(
  name='RuleId',
  full_name='apollo.planning.TrafficRuleConfig.RuleId',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='BACKSIDE_VEHICLE', index=0, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CROSSWALK', index=1, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DESTINATION', index=2, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KEEP_CLEAR', index=3, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REFERENCE_LINE_END', index=4, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REROUTING', index=5, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STOP_SIGN', index=6, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TRAFFIC_LIGHT', index=7, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='YIELD_SIGN', index=8, number=9,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1706,
  serialized_end=1873,
)
_sym_db.RegisterEnumDescriptor(_TRAFFICRULECONFIG_RULEID)


_BACKSIDEVEHICLECONFIG = _descriptor.Descriptor(
  name='BacksideVehicleConfig',
  full_name='apollo.planning.BacksideVehicleConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='backside_lane_width', full_name='apollo.planning.BacksideVehicleConfig.backside_lane_width', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(4),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=124,
)


_CROSSWALKCONFIG = _descriptor.Descriptor(
  name='CrosswalkConfig',
  full_name='apollo.planning.CrosswalkConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stop_distance', full_name='apollo.planning.CrosswalkConfig.stop_distance', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_stop_deceleration', full_name='apollo.planning.CrosswalkConfig.max_stop_deceleration', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(4),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_pass_s_distance', full_name='apollo.planning.CrosswalkConfig.min_pass_s_distance', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_valid_stop_distance', full_name='apollo.planning.CrosswalkConfig.max_valid_stop_distance', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(3),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expand_s_distance', full_name='apollo.planning.CrosswalkConfig.expand_s_distance', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(2),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop_strict_l_distance', full_name='apollo.planning.CrosswalkConfig.stop_strict_l_distance', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(4),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop_loose_l_distance', full_name='apollo.planning.CrosswalkConfig.stop_loose_l_distance', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop_timeout', full_name='apollo.planning.CrosswalkConfig.stop_timeout', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(10),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=127,
  serialized_end=397,
)


_DESTINATIONCONFIG = _descriptor.Descriptor(
  name='DestinationConfig',
  full_name='apollo.planning.DestinationConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stop_distance', full_name='apollo.planning.DestinationConfig.stop_distance', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=399,
  serialized_end=446,
)


_KEEPCLEARCONFIG = _descriptor.Descriptor(
  name='KeepClearConfig',
  full_name='apollo.planning.KeepClearConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='enable_keep_clear_zone', full_name='apollo.planning.KeepClearConfig.enable_keep_clear_zone', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enable_junction', full_name='apollo.planning.KeepClearConfig.enable_junction', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_pass_s_distance', full_name='apollo.planning.KeepClearConfig.min_pass_s_distance', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(2),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='align_with_traffic_sign_tolerance', full_name='apollo.planning.KeepClearConfig.align_with_traffic_sign_tolerance', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(4.5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=449,
  serialized_end=615,
)


_REFERENCELINEENDCONFIG = _descriptor.Descriptor(
  name='ReferenceLineEndConfig',
  full_name='apollo.planning.ReferenceLineEndConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stop_distance', full_name='apollo.planning.ReferenceLineEndConfig.stop_distance', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0.5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_reference_line_remain_length', full_name='apollo.planning.ReferenceLineEndConfig.min_reference_line_remain_length', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(50),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=617,
  serialized_end=715,
)


_REROUTINGCONFIG = _descriptor.Descriptor(
  name='ReroutingConfig',
  full_name='apollo.planning.ReroutingConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cooldown_time', full_name='apollo.planning.ReroutingConfig.cooldown_time', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(3),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='prepare_rerouting_time', full_name='apollo.planning.ReroutingConfig.prepare_rerouting_time', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(2),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=717,
  serialized_end=795,
)


_STOPSIGNCONFIG = _descriptor.Descriptor(
  name='StopSignConfig',
  full_name='apollo.planning.StopSignConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='enabled', full_name='apollo.planning.StopSignConfig.enabled', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop_distance', full_name='apollo.planning.StopSignConfig.stop_distance', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=797,
  serialized_end=862,
)


_TRAFFICLIGHTCONFIG = _descriptor.Descriptor(
  name='TrafficLightConfig',
  full_name='apollo.planning.TrafficLightConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='enabled', full_name='apollo.planning.TrafficLightConfig.enabled', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop_distance', full_name='apollo.planning.TrafficLightConfig.stop_distance', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_stop_deceleration', full_name='apollo.planning.TrafficLightConfig.max_stop_deceleration', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(4),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=864,
  serialized_end=967,
)


_YIELDSIGNCONFIG = _descriptor.Descriptor(
  name='YieldSignConfig',
  full_name='apollo.planning.YieldSignConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='enabled', full_name='apollo.planning.YieldSignConfig.enabled', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop_distance', full_name='apollo.planning.YieldSignConfig.stop_distance', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start_watch_distance', full_name='apollo.planning.YieldSignConfig.start_watch_distance', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(2),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=969,
  serialized_end=1068,
)


_TRAFFICRULECONFIG = _descriptor.Descriptor(
  name='TrafficRuleConfig',
  full_name='apollo.planning.TrafficRuleConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rule_id', full_name='apollo.planning.TrafficRuleConfig.rule_id', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enabled', full_name='apollo.planning.TrafficRuleConfig.enabled', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='backside_vehicle', full_name='apollo.planning.TrafficRuleConfig.backside_vehicle', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='crosswalk', full_name='apollo.planning.TrafficRuleConfig.crosswalk', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='destination', full_name='apollo.planning.TrafficRuleConfig.destination', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='keep_clear', full_name='apollo.planning.TrafficRuleConfig.keep_clear', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reference_line_end', full_name='apollo.planning.TrafficRuleConfig.reference_line_end', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rerouting', full_name='apollo.planning.TrafficRuleConfig.rerouting', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop_sign', full_name='apollo.planning.TrafficRuleConfig.stop_sign', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='traffic_light', full_name='apollo.planning.TrafficRuleConfig.traffic_light', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='yield_sign', full_name='apollo.planning.TrafficRuleConfig.yield_sign', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _TRAFFICRULECONFIG_RULEID,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='config', full_name='apollo.planning.TrafficRuleConfig.config',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=1071,
  serialized_end=1883,
)


_TRAFFICRULECONFIGS = _descriptor.Descriptor(
  name='TrafficRuleConfigs',
  full_name='apollo.planning.TrafficRuleConfigs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='apollo.planning.TrafficRuleConfigs.config', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1885,
  serialized_end=1957,
)

_TRAFFICRULECONFIG.fields_by_name['rule_id'].enum_type = _TRAFFICRULECONFIG_RULEID
_TRAFFICRULECONFIG.fields_by_name['backside_vehicle'].message_type = _BACKSIDEVEHICLECONFIG
_TRAFFICRULECONFIG.fields_by_name['crosswalk'].message_type = _CROSSWALKCONFIG
_TRAFFICRULECONFIG.fields_by_name['destination'].message_type = _DESTINATIONCONFIG
_TRAFFICRULECONFIG.fields_by_name['keep_clear'].message_type = _KEEPCLEARCONFIG
_TRAFFICRULECONFIG.fields_by_name['reference_line_end'].message_type = _REFERENCELINEENDCONFIG
_TRAFFICRULECONFIG.fields_by_name['rerouting'].message_type = _REROUTINGCONFIG
_TRAFFICRULECONFIG.fields_by_name['stop_sign'].message_type = _STOPSIGNCONFIG
_TRAFFICRULECONFIG.fields_by_name['traffic_light'].message_type = _TRAFFICLIGHTCONFIG
_TRAFFICRULECONFIG.fields_by_name['yield_sign'].message_type = _YIELDSIGNCONFIG
_TRAFFICRULECONFIG_RULEID.containing_type = _TRAFFICRULECONFIG
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['backside_vehicle'])
_TRAFFICRULECONFIG.fields_by_name['backside_vehicle'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['crosswalk'])
_TRAFFICRULECONFIG.fields_by_name['crosswalk'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['destination'])
_TRAFFICRULECONFIG.fields_by_name['destination'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['keep_clear'])
_TRAFFICRULECONFIG.fields_by_name['keep_clear'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['reference_line_end'])
_TRAFFICRULECONFIG.fields_by_name['reference_line_end'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['rerouting'])
_TRAFFICRULECONFIG.fields_by_name['rerouting'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['stop_sign'])
_TRAFFICRULECONFIG.fields_by_name['stop_sign'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['traffic_light'])
_TRAFFICRULECONFIG.fields_by_name['traffic_light'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIG.oneofs_by_name['config'].fields.append(
  _TRAFFICRULECONFIG.fields_by_name['yield_sign'])
_TRAFFICRULECONFIG.fields_by_name['yield_sign'].containing_oneof = _TRAFFICRULECONFIG.oneofs_by_name['config']
_TRAFFICRULECONFIGS.fields_by_name['config'].message_type = _TRAFFICRULECONFIG
DESCRIPTOR.message_types_by_name['BacksideVehicleConfig'] = _BACKSIDEVEHICLECONFIG
DESCRIPTOR.message_types_by_name['CrosswalkConfig'] = _CROSSWALKCONFIG
DESCRIPTOR.message_types_by_name['DestinationConfig'] = _DESTINATIONCONFIG
DESCRIPTOR.message_types_by_name['KeepClearConfig'] = _KEEPCLEARCONFIG
DESCRIPTOR.message_types_by_name['ReferenceLineEndConfig'] = _REFERENCELINEENDCONFIG
DESCRIPTOR.message_types_by_name['ReroutingConfig'] = _REROUTINGCONFIG
DESCRIPTOR.message_types_by_name['StopSignConfig'] = _STOPSIGNCONFIG
DESCRIPTOR.message_types_by_name['TrafficLightConfig'] = _TRAFFICLIGHTCONFIG
DESCRIPTOR.message_types_by_name['YieldSignConfig'] = _YIELDSIGNCONFIG
DESCRIPTOR.message_types_by_name['TrafficRuleConfig'] = _TRAFFICRULECONFIG
DESCRIPTOR.message_types_by_name['TrafficRuleConfigs'] = _TRAFFICRULECONFIGS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BacksideVehicleConfig = _reflection.GeneratedProtocolMessageType('BacksideVehicleConfig', (_message.Message,), dict(
  DESCRIPTOR = _BACKSIDEVEHICLECONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.BacksideVehicleConfig)
  ))
_sym_db.RegisterMessage(BacksideVehicleConfig)

CrosswalkConfig = _reflection.GeneratedProtocolMessageType('CrosswalkConfig', (_message.Message,), dict(
  DESCRIPTOR = _CROSSWALKCONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.CrosswalkConfig)
  ))
_sym_db.RegisterMessage(CrosswalkConfig)

DestinationConfig = _reflection.GeneratedProtocolMessageType('DestinationConfig', (_message.Message,), dict(
  DESCRIPTOR = _DESTINATIONCONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.DestinationConfig)
  ))
_sym_db.RegisterMessage(DestinationConfig)

KeepClearConfig = _reflection.GeneratedProtocolMessageType('KeepClearConfig', (_message.Message,), dict(
  DESCRIPTOR = _KEEPCLEARCONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.KeepClearConfig)
  ))
_sym_db.RegisterMessage(KeepClearConfig)

ReferenceLineEndConfig = _reflection.GeneratedProtocolMessageType('ReferenceLineEndConfig', (_message.Message,), dict(
  DESCRIPTOR = _REFERENCELINEENDCONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.ReferenceLineEndConfig)
  ))
_sym_db.RegisterMessage(ReferenceLineEndConfig)

ReroutingConfig = _reflection.GeneratedProtocolMessageType('ReroutingConfig', (_message.Message,), dict(
  DESCRIPTOR = _REROUTINGCONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.ReroutingConfig)
  ))
_sym_db.RegisterMessage(ReroutingConfig)

StopSignConfig = _reflection.GeneratedProtocolMessageType('StopSignConfig', (_message.Message,), dict(
  DESCRIPTOR = _STOPSIGNCONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.StopSignConfig)
  ))
_sym_db.RegisterMessage(StopSignConfig)

TrafficLightConfig = _reflection.GeneratedProtocolMessageType('TrafficLightConfig', (_message.Message,), dict(
  DESCRIPTOR = _TRAFFICLIGHTCONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.TrafficLightConfig)
  ))
_sym_db.RegisterMessage(TrafficLightConfig)

YieldSignConfig = _reflection.GeneratedProtocolMessageType('YieldSignConfig', (_message.Message,), dict(
  DESCRIPTOR = _YIELDSIGNCONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.YieldSignConfig)
  ))
_sym_db.RegisterMessage(YieldSignConfig)

TrafficRuleConfig = _reflection.GeneratedProtocolMessageType('TrafficRuleConfig', (_message.Message,), dict(
  DESCRIPTOR = _TRAFFICRULECONFIG,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.TrafficRuleConfig)
  ))
_sym_db.RegisterMessage(TrafficRuleConfig)

TrafficRuleConfigs = _reflection.GeneratedProtocolMessageType('TrafficRuleConfigs', (_message.Message,), dict(
  DESCRIPTOR = _TRAFFICRULECONFIGS,
  __module__ = 'modules.planning.proto.traffic_rule_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.planning.TrafficRuleConfigs)
  ))
_sym_db.RegisterMessage(TrafficRuleConfigs)


# @@protoc_insertion_point(module_scope)
