# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/guardian/proto/guardian_conf.proto

import sys

_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='modules/guardian/proto/guardian_conf.proto',
  package='apollo.guardian',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n*modules/guardian/proto/guardian_conf.proto\x12\x0f\x61pollo.guardian\"\x91\x01\n\x0cGuardianConf\x12\x1e\n\x0fguardian_enable\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x32\n&guardian_cmd_emergency_stop_percentage\x18\x02 \x01(\x01:\x02\x35\x30\x12-\n!guardian_cmd_soft_stop_percentage\x18\x03 \x01(\x01:\x02\x32\x35')
)




_GUARDIANCONF = _descriptor.Descriptor(
  name='GuardianConf',
  full_name='apollo.guardian.GuardianConf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='guardian_enable', full_name='apollo.guardian.GuardianConf.guardian_enable', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='guardian_cmd_emergency_stop_percentage', full_name='apollo.guardian.GuardianConf.guardian_cmd_emergency_stop_percentage', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(50),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='guardian_cmd_soft_stop_percentage', full_name='apollo.guardian.GuardianConf.guardian_cmd_soft_stop_percentage', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(25),
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
  serialized_start=64,
  serialized_end=209,
)

DESCRIPTOR.message_types_by_name['GuardianConf'] = _GUARDIANCONF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GuardianConf = _reflection.GeneratedProtocolMessageType('GuardianConf', (_message.Message,), dict(
  DESCRIPTOR = _GUARDIANCONF,
  __module__ = 'modules.guardian.proto.guardian_conf_pb2'
  # @@protoc_insertion_point(class_scope:apollo.guardian.GuardianConf)
  ))
_sym_db.RegisterMessage(GuardianConf)


# @@protoc_insertion_point(module_scope)
