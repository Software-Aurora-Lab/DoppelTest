# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/prediction/proto/scenario.proto

import sys

_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='modules/prediction/proto/scenario.proto',
  package='apollo.prediction',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\'modules/prediction/proto/scenario.proto\x12\x11\x61pollo.prediction\"\xe8\x01\n\x08Scenario\x12\x37\n\x04type\x18\x01 \x01(\x0e\x32 .apollo.prediction.Scenario.Type:\x07UNKNOWN\x12\x13\n\x0bjunction_id\x18\x02 \x01(\t\"\x8d\x01\n\x04Type\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x06\x43RUISE\x10\xe8\x07\x12\x11\n\x0c\x43RUISE_URBAN\x10\xe9\x07\x12\x13\n\x0e\x43RUISE_HIGHWAY\x10\xea\x07\x12\r\n\x08JUNCTION\x10\xd0\x0f\x12\x1b\n\x16JUNCTION_TRAFFIC_LIGHT\x10\xd1\x0f\x12\x17\n\x12JUNCTION_STOP_SIGN\x10\xd2\x0f')
)



_SCENARIO_TYPE = _descriptor.EnumDescriptor(
  name='Type',
  full_name='apollo.prediction.Scenario.Type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRUISE', index=1, number=1000,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRUISE_URBAN', index=2, number=1001,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRUISE_HIGHWAY', index=3, number=1002,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JUNCTION', index=4, number=2000,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JUNCTION_TRAFFIC_LIGHT', index=5, number=2001,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JUNCTION_STOP_SIGN', index=6, number=2002,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=154,
  serialized_end=295,
)
_sym_db.RegisterEnumDescriptor(_SCENARIO_TYPE)


_SCENARIO = _descriptor.Descriptor(
  name='Scenario',
  full_name='apollo.prediction.Scenario',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='apollo.prediction.Scenario.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='junction_id', full_name='apollo.prediction.Scenario.junction_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SCENARIO_TYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=63,
  serialized_end=295,
)

_SCENARIO.fields_by_name['type'].enum_type = _SCENARIO_TYPE
_SCENARIO_TYPE.containing_type = _SCENARIO
DESCRIPTOR.message_types_by_name['Scenario'] = _SCENARIO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Scenario = _reflection.GeneratedProtocolMessageType('Scenario', (_message.Message,), dict(
  DESCRIPTOR = _SCENARIO,
  __module__ = 'modules.prediction.proto.scenario_pb2'
  # @@protoc_insertion_point(class_scope:apollo.prediction.Scenario)
  ))
_sym_db.RegisterMessage(Scenario)


# @@protoc_insertion_point(module_scope)
