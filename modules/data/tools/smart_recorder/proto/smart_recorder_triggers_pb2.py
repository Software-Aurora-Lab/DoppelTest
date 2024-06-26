# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/data/tools/smart_recorder/proto/smart_recorder_triggers.proto

import sys

_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='modules/data/tools/smart_recorder/proto/smart_recorder_triggers.proto',
  package='apollo.data',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\nEmodules/data/tools/smart_recorder/proto/smart_recorder_triggers.proto\x12\x0b\x61pollo.data\"L\n\x14RecordSegmentSetting\x12\x19\n\x0csize_segment\x18\x01 \x01(\x05:\x03\x35\x30\x30\x12\x19\n\x0ctime_segment\x18\x02 \x01(\x05:\x03\x31\x38\x30\"r\n\x07Trigger\x12\x14\n\x0ctrigger_name\x18\x01 \x01(\t\x12\x0f\n\x07\x65nabled\x18\x02 \x01(\x08\x12\x15\n\rbackward_time\x18\x03 \x01(\x01\x12\x14\n\x0c\x66orward_time\x18\x04 \x01(\x01\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\"\xd4\x01\n\x12SmartRecordTrigger\x12:\n\x0fsegment_setting\x18\x01 \x01(\x0b\x32!.apollo.data.RecordSegmentSetting\x12&\n\x08triggers\x18\x02 \x03(\x0b\x32\x14.apollo.data.Trigger\x12\x1d\n\x11max_backward_time\x18\x03 \x01(\x01:\x02\x33\x30\x12\x1c\n\x11min_restore_chunk\x18\x04 \x01(\x01:\x01\x35\x12\x1d\n\x15trigger_log_file_path\x18\x05 \x01(\t')
)




_RECORDSEGMENTSETTING = _descriptor.Descriptor(
  name='RecordSegmentSetting',
  full_name='apollo.data.RecordSegmentSetting',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='size_segment', full_name='apollo.data.RecordSegmentSetting.size_segment', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=500,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time_segment', full_name='apollo.data.RecordSegmentSetting.time_segment', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=180,
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
  serialized_start=86,
  serialized_end=162,
)


_TRIGGER = _descriptor.Descriptor(
  name='Trigger',
  full_name='apollo.data.Trigger',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='trigger_name', full_name='apollo.data.Trigger.trigger_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enabled', full_name='apollo.data.Trigger.enabled', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='backward_time', full_name='apollo.data.Trigger.backward_time', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='forward_time', full_name='apollo.data.Trigger.forward_time', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='apollo.data.Trigger.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=164,
  serialized_end=278,
)


_SMARTRECORDTRIGGER = _descriptor.Descriptor(
  name='SmartRecordTrigger',
  full_name='apollo.data.SmartRecordTrigger',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='segment_setting', full_name='apollo.data.SmartRecordTrigger.segment_setting', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='triggers', full_name='apollo.data.SmartRecordTrigger.triggers', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='max_backward_time', full_name='apollo.data.SmartRecordTrigger.max_backward_time', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(30),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='min_restore_chunk', full_name='apollo.data.SmartRecordTrigger.min_restore_chunk', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='trigger_log_file_path', full_name='apollo.data.SmartRecordTrigger.trigger_log_file_path', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=281,
  serialized_end=493,
)

_SMARTRECORDTRIGGER.fields_by_name['segment_setting'].message_type = _RECORDSEGMENTSETTING
_SMARTRECORDTRIGGER.fields_by_name['triggers'].message_type = _TRIGGER
DESCRIPTOR.message_types_by_name['RecordSegmentSetting'] = _RECORDSEGMENTSETTING
DESCRIPTOR.message_types_by_name['Trigger'] = _TRIGGER
DESCRIPTOR.message_types_by_name['SmartRecordTrigger'] = _SMARTRECORDTRIGGER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RecordSegmentSetting = _reflection.GeneratedProtocolMessageType('RecordSegmentSetting', (_message.Message,), dict(
  DESCRIPTOR = _RECORDSEGMENTSETTING,
  __module__ = 'modules.data.tools.smart_recorder.proto.smart_recorder_triggers_pb2'
  # @@protoc_insertion_point(class_scope:apollo.data.RecordSegmentSetting)
  ))
_sym_db.RegisterMessage(RecordSegmentSetting)

Trigger = _reflection.GeneratedProtocolMessageType('Trigger', (_message.Message,), dict(
  DESCRIPTOR = _TRIGGER,
  __module__ = 'modules.data.tools.smart_recorder.proto.smart_recorder_triggers_pb2'
  # @@protoc_insertion_point(class_scope:apollo.data.Trigger)
  ))
_sym_db.RegisterMessage(Trigger)

SmartRecordTrigger = _reflection.GeneratedProtocolMessageType('SmartRecordTrigger', (_message.Message,), dict(
  DESCRIPTOR = _SMARTRECORDTRIGGER,
  __module__ = 'modules.data.tools.smart_recorder.proto.smart_recorder_triggers_pb2'
  # @@protoc_insertion_point(class_scope:apollo.data.SmartRecordTrigger)
  ))
_sym_db.RegisterMessage(SmartRecordTrigger)


# @@protoc_insertion_point(module_scope)
