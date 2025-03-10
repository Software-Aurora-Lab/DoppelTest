# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/perception/proto/sensor_meta_schema.proto

import sys

_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='modules/perception/proto/sensor_meta_schema.proto',
  package='apollo.perception',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n1modules/perception/proto/sensor_meta_schema.proto\x12\x11\x61pollo.perception\"\xad\x04\n\nSensorMeta\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x36\n\x04type\x18\x02 \x01(\x0e\x32(.apollo.perception.SensorMeta.SensorType\x12\x44\n\x0borientation\x18\x03 \x01(\x0e\x32/.apollo.perception.SensorMeta.SensorOrientation\"\xf7\x01\n\nSensorType\x12 \n\x13UNKNOWN_SENSOR_TYPE\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x0f\n\x0bVELODYNE_64\x10\x00\x12\x0f\n\x0bVELODYNE_32\x10\x01\x12\x0f\n\x0bVELODYNE_16\x10\x02\x12\r\n\tLDLIDAR_4\x10\x03\x12\r\n\tLDLIDAR_1\x10\x04\x12\x15\n\x11SHORT_RANGE_RADAR\x10\x05\x12\x14\n\x10LONG_RANGE_RADAR\x10\x06\x12\x14\n\x10MONOCULAR_CAMERA\x10\x07\x12\x11\n\rSTEREO_CAMERA\x10\x08\x12\x0e\n\nULTRASONIC\x10\t\x12\x10\n\x0cVELODYNE_128\x10\n\"\x98\x01\n\x11SensorOrientation\x12\t\n\x05\x46RONT\x10\x00\x12\x10\n\x0cLEFT_FORWARD\x10\x01\x12\x08\n\x04LEFT\x10\x02\x12\x11\n\rLEFT_BACKWARD\x10\x03\x12\x08\n\x04REAR\x10\x04\x12\x12\n\x0eRIGHT_BACKWARD\x10\x05\x12\t\n\x05RIGHT\x10\x06\x12\x11\n\rRIGHT_FORWARD\x10\x07\x12\r\n\tPANORAMIC\x10\x08\"E\n\x0fMultiSensorMeta\x12\x32\n\x0bsensor_meta\x18\x01 \x03(\x0b\x32\x1d.apollo.perception.SensorMeta')
)



_SENSORMETA_SENSORTYPE = _descriptor.EnumDescriptor(
  name='SensorType',
  full_name='apollo.perception.SensorMeta.SensorType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_SENSOR_TYPE', index=0, number=-1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VELODYNE_64', index=1, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VELODYNE_32', index=2, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VELODYNE_16', index=3, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LDLIDAR_4', index=4, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LDLIDAR_1', index=5, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHORT_RANGE_RADAR', index=6, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LONG_RANGE_RADAR', index=7, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MONOCULAR_CAMERA', index=8, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STEREO_CAMERA', index=9, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ULTRASONIC', index=10, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='VELODYNE_128', index=11, number=10,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=228,
  serialized_end=475,
)
_sym_db.RegisterEnumDescriptor(_SENSORMETA_SENSORTYPE)

_SENSORMETA_SENSORORIENTATION = _descriptor.EnumDescriptor(
  name='SensorOrientation',
  full_name='apollo.perception.SensorMeta.SensorOrientation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FRONT', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEFT_FORWARD', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEFT', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEFT_BACKWARD', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REAR', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RIGHT_BACKWARD', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RIGHT', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RIGHT_FORWARD', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PANORAMIC', index=8, number=8,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=478,
  serialized_end=630,
)
_sym_db.RegisterEnumDescriptor(_SENSORMETA_SENSORORIENTATION)


_SENSORMETA = _descriptor.Descriptor(
  name='SensorMeta',
  full_name='apollo.perception.SensorMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='apollo.perception.SensorMeta.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='apollo.perception.SensorMeta.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=-1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='orientation', full_name='apollo.perception.SensorMeta.orientation', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SENSORMETA_SENSORTYPE,
    _SENSORMETA_SENSORORIENTATION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=630,
)


_MULTISENSORMETA = _descriptor.Descriptor(
  name='MultiSensorMeta',
  full_name='apollo.perception.MultiSensorMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sensor_meta', full_name='apollo.perception.MultiSensorMeta.sensor_meta', index=0,
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
  serialized_start=632,
  serialized_end=701,
)

_SENSORMETA.fields_by_name['type'].enum_type = _SENSORMETA_SENSORTYPE
_SENSORMETA.fields_by_name['orientation'].enum_type = _SENSORMETA_SENSORORIENTATION
_SENSORMETA_SENSORTYPE.containing_type = _SENSORMETA
_SENSORMETA_SENSORORIENTATION.containing_type = _SENSORMETA
_MULTISENSORMETA.fields_by_name['sensor_meta'].message_type = _SENSORMETA
DESCRIPTOR.message_types_by_name['SensorMeta'] = _SENSORMETA
DESCRIPTOR.message_types_by_name['MultiSensorMeta'] = _MULTISENSORMETA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SensorMeta = _reflection.GeneratedProtocolMessageType('SensorMeta', (_message.Message,), dict(
  DESCRIPTOR = _SENSORMETA,
  __module__ = 'modules.perception.proto.sensor_meta_schema_pb2'
  # @@protoc_insertion_point(class_scope:apollo.perception.SensorMeta)
  ))
_sym_db.RegisterMessage(SensorMeta)

MultiSensorMeta = _reflection.GeneratedProtocolMessageType('MultiSensorMeta', (_message.Message,), dict(
  DESCRIPTOR = _MULTISENSORMETA,
  __module__ = 'modules.perception.proto.sensor_meta_schema_pb2'
  # @@protoc_insertion_point(class_scope:apollo.perception.MultiSensorMeta)
  ))
_sym_db.RegisterMessage(MultiSensorMeta)


# @@protoc_insertion_point(module_scope)
