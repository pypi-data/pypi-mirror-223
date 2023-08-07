"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'osmosis/valset-pref/v1beta1/state.proto\x12\x1aosmosis.valsetpref.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto"\x8c\x01\n\x13ValidatorPreference\x125\n\x10val_oper_address\x18\x01 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"val_oper_address"\x12>\n\x06weight\x18\x02 \x01(\tB.\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec"{\n\x17ValidatorSetPreferences\x12`\n\x0bpreferences\x18\x02 \x03(\x0b2/.osmosis.valsetpref.v1beta1.ValidatorPreferenceB\x1a\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"preferences"B=Z7github.com/osmosis-labs/osmosis/v16/x/valset-pref/types\xc8\xe1\x1e\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.valset_pref.v1beta1.state_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z7github.com/osmosis-labs/osmosis/v16/x/valset-pref/types\xc8\xe1\x1e\x00'
    _VALIDATORPREFERENCE.fields_by_name['val_oper_address']._options = None
    _VALIDATORPREFERENCE.fields_by_name['val_oper_address']._serialized_options = b'\xf2\xde\x1f\x17yaml:"val_oper_address"'
    _VALIDATORPREFERENCE.fields_by_name['weight']._options = None
    _VALIDATORPREFERENCE.fields_by_name['weight']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec'
    _VALIDATORSETPREFERENCES.fields_by_name['preferences']._options = None
    _VALIDATORSETPREFERENCES.fields_by_name['preferences']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"preferences"'
    _globals['_VALIDATORPREFERENCE']._serialized_start = 124
    _globals['_VALIDATORPREFERENCE']._serialized_end = 264
    _globals['_VALIDATORSETPREFERENCES']._serialized_start = 266
    _globals['_VALIDATORSETPREFERENCES']._serialized_end = 389