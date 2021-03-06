# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='susu',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n\rmessage.proto\x12\x04susu\"\xeb\x01\n\x07Message\x12\x11\n\tstr_field\x18\x01 \x01(\t\x12-\n\nlist_field\x18\x02 \x03(\x0b\x32\x19.susu.Message.list_record\x12-\n\ndict_field\x18\x03 \x03(\x0b\x32\x19.susu.Message.dict_record\x12\x11\n\tint_field\x18\x04 \x01(\x05\x12\x13\n\x0b\x66loat_field\x18\x05 \x01(\x02\x1a\x1c\n\x0blist_record\x12\r\n\x05value\x18\x01 \x02(\x05\x1a)\n\x0b\x64ict_record\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\t'
)




_MESSAGE_LIST_RECORD = _descriptor.Descriptor(
  name='list_record',
  full_name='susu.Message.list_record',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='susu.Message.list_record.value', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=188,
  serialized_end=216,
)

_MESSAGE_DICT_RECORD = _descriptor.Descriptor(
  name='dict_record',
  full_name='susu.Message.dict_record',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='susu.Message.dict_record.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='susu.Message.dict_record.value', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=218,
  serialized_end=259,
)

_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='susu.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='str_field', full_name='susu.Message.str_field', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='list_field', full_name='susu.Message.list_field', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dict_field', full_name='susu.Message.dict_field', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='int_field', full_name='susu.Message.int_field', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='float_field', full_name='susu.Message.float_field', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_MESSAGE_LIST_RECORD, _MESSAGE_DICT_RECORD, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=259,
)

_MESSAGE_LIST_RECORD.containing_type = _MESSAGE
_MESSAGE_DICT_RECORD.containing_type = _MESSAGE
_MESSAGE.fields_by_name['list_field'].message_type = _MESSAGE_LIST_RECORD
_MESSAGE.fields_by_name['dict_field'].message_type = _MESSAGE_DICT_RECORD
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {

  'list_record' : _reflection.GeneratedProtocolMessageType('list_record', (_message.Message,), {
    'DESCRIPTOR' : _MESSAGE_LIST_RECORD,
    '__module__' : 'message_pb2'
    # @@protoc_insertion_point(class_scope:susu.Message.list_record)
    })
  ,

  'dict_record' : _reflection.GeneratedProtocolMessageType('dict_record', (_message.Message,), {
    'DESCRIPTOR' : _MESSAGE_DICT_RECORD,
    '__module__' : 'message_pb2'
    # @@protoc_insertion_point(class_scope:susu.Message.dict_record)
    })
  ,
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:susu.Message)
  })
_sym_db.RegisterMessage(Message)
_sym_db.RegisterMessage(Message.list_record)
_sym_db.RegisterMessage(Message.dict_record)


# @@protoc_insertion_point(module_scope)
