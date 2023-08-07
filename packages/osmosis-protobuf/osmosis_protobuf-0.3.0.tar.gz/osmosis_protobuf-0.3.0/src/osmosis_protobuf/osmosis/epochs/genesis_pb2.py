"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cosmosis/epochs/genesis.proto\x12\x16osmosis.epochs.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x9a\x03\n\tEpochInfo\x12\x12\n\nidentifier\x18\x01 \x01(\t\x12M\n\nstart_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01\x12^\n\x08duration\x18\x03 \x01(\x0b2\x19.google.protobuf.DurationB1\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01\x12\x15\n\rcurrent_epoch\x18\x04 \x01(\x03\x12i\n\x18current_epoch_start_time\x18\x05 \x01(\x0b2\x1a.google.protobuf.TimestampB+\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"current_epoch_start_time"\x90\xdf\x1f\x01\x12\x1e\n\x16epoch_counting_started\x18\x06 \x01(\x08\x12"\n\x1acurrent_epoch_start_height\x18\x08 \x01(\x03J\x04\x08\x07\x10\x08"G\n\x0cGenesisState\x127\n\x06epochs\x18\x01 \x03(\x0b2!.osmosis.epochs.v1beta1.EpochInfoB\x04\xc8\xde\x1f\x00B0Z.github.com/osmosis-labs/osmosis/x/epochs/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.epochs.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z.github.com/osmosis-labs/osmosis/x/epochs/types'
    _EPOCHINFO.fields_by_name['start_time']._options = None
    _EPOCHINFO.fields_by_name['start_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01'
    _EPOCHINFO.fields_by_name['duration']._options = None
    _EPOCHINFO.fields_by_name['duration']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01'
    _EPOCHINFO.fields_by_name['current_epoch_start_time']._options = None
    _EPOCHINFO.fields_by_name['current_epoch_start_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"current_epoch_start_time"\x90\xdf\x1f\x01'
    _GENESISSTATE.fields_by_name['epochs']._options = None
    _GENESISSTATE.fields_by_name['epochs']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_EPOCHINFO']._serialized_start = 144
    _globals['_EPOCHINFO']._serialized_end = 554
    _globals['_GENESISSTATE']._serialized_start = 556
    _globals['_GENESISSTATE']._serialized_end = 627