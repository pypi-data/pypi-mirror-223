"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1ccosmwasm/wasm/v1/authz.proto\x12\x10cosmwasm.wasm.v1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x19google/protobuf/any.proto"\x7f\n\x1eContractExecutionAuthorization\x125\n\x06grants\x18\x01 \x03(\x0b2\x1f.cosmwasm.wasm.v1.ContractGrantB\x04\xc8\xde\x1f\x00:&\xca\xb4-"cosmos.authz.v1beta1.Authorization"\x7f\n\x1eContractMigrationAuthorization\x125\n\x06grants\x18\x01 \x03(\x0b2\x1f.cosmwasm.wasm.v1.ContractGrantB\x04\xc8\xde\x1f\x00:&\xca\xb4-"cosmos.authz.v1beta1.Authorization"\xc1\x01\n\rContractGrant\x12\x10\n\x08contract\x18\x01 \x01(\t\x12M\n\x05limit\x18\x02 \x01(\x0b2\x14.google.protobuf.AnyB(\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX\x12O\n\x06filter\x18\x03 \x01(\x0b2\x14.google.protobuf.AnyB)\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX"L\n\rMaxCallsLimit\x12\x11\n\tremaining\x18\x01 \x01(\x04:(\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX"\x97\x01\n\rMaxFundsLimit\x12\\\n\x07amounts\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:(\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX"\xb0\x01\n\rCombinedLimit\x12\x17\n\x0fcalls_remaining\x18\x01 \x01(\x04\x12\\\n\x07amounts\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins:(\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX"C\n\x16AllowAllMessagesFilter:)\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX"T\n\x19AcceptedMessageKeysFilter\x12\x0c\n\x04keys\x18\x01 \x03(\t:)\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX"m\n\x16AcceptedMessagesFilter\x12(\n\x08messages\x18\x01 \x03(\x0cB\x16\xfa\xde\x1f\x12RawContractMessage:)\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterXB,Z&github.com/CosmWasm/wasmd/x/wasm/types\xc8\xe1\x1e\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmwasm.wasm.v1.authz_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z&github.com/CosmWasm/wasmd/x/wasm/types\xc8\xe1\x1e\x00'
    _CONTRACTEXECUTIONAUTHORIZATION.fields_by_name['grants']._options = None
    _CONTRACTEXECUTIONAUTHORIZATION.fields_by_name['grants']._serialized_options = b'\xc8\xde\x1f\x00'
    _CONTRACTEXECUTIONAUTHORIZATION._options = None
    _CONTRACTEXECUTIONAUTHORIZATION._serialized_options = b'\xca\xb4-"cosmos.authz.v1beta1.Authorization'
    _CONTRACTMIGRATIONAUTHORIZATION.fields_by_name['grants']._options = None
    _CONTRACTMIGRATIONAUTHORIZATION.fields_by_name['grants']._serialized_options = b'\xc8\xde\x1f\x00'
    _CONTRACTMIGRATIONAUTHORIZATION._options = None
    _CONTRACTMIGRATIONAUTHORIZATION._serialized_options = b'\xca\xb4-"cosmos.authz.v1beta1.Authorization'
    _CONTRACTGRANT.fields_by_name['limit']._options = None
    _CONTRACTGRANT.fields_by_name['limit']._serialized_options = b'\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX'
    _CONTRACTGRANT.fields_by_name['filter']._options = None
    _CONTRACTGRANT.fields_by_name['filter']._serialized_options = b'\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX'
    _MAXCALLSLIMIT._options = None
    _MAXCALLSLIMIT._serialized_options = b'\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX'
    _MAXFUNDSLIMIT.fields_by_name['amounts']._options = None
    _MAXFUNDSLIMIT.fields_by_name['amounts']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MAXFUNDSLIMIT._options = None
    _MAXFUNDSLIMIT._serialized_options = b'\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX'
    _COMBINEDLIMIT.fields_by_name['amounts']._options = None
    _COMBINEDLIMIT.fields_by_name['amounts']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _COMBINEDLIMIT._options = None
    _COMBINEDLIMIT._serialized_options = b'\xca\xb4-$cosmwasm.wasm.v1.ContractAuthzLimitX'
    _ALLOWALLMESSAGESFILTER._options = None
    _ALLOWALLMESSAGESFILTER._serialized_options = b'\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX'
    _ACCEPTEDMESSAGEKEYSFILTER._options = None
    _ACCEPTEDMESSAGEKEYSFILTER._serialized_options = b'\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX'
    _ACCEPTEDMESSAGESFILTER.fields_by_name['messages']._options = None
    _ACCEPTEDMESSAGESFILTER.fields_by_name['messages']._serialized_options = b'\xfa\xde\x1f\x12RawContractMessage'
    _ACCEPTEDMESSAGESFILTER._options = None
    _ACCEPTEDMESSAGESFILTER._serialized_options = b'\xca\xb4-%cosmwasm.wasm.v1.ContractAuthzFilterX'
    _globals['_CONTRACTEXECUTIONAUTHORIZATION']._serialized_start = 158
    _globals['_CONTRACTEXECUTIONAUTHORIZATION']._serialized_end = 285
    _globals['_CONTRACTMIGRATIONAUTHORIZATION']._serialized_start = 287
    _globals['_CONTRACTMIGRATIONAUTHORIZATION']._serialized_end = 414
    _globals['_CONTRACTGRANT']._serialized_start = 417
    _globals['_CONTRACTGRANT']._serialized_end = 610
    _globals['_MAXCALLSLIMIT']._serialized_start = 612
    _globals['_MAXCALLSLIMIT']._serialized_end = 688
    _globals['_MAXFUNDSLIMIT']._serialized_start = 691
    _globals['_MAXFUNDSLIMIT']._serialized_end = 842
    _globals['_COMBINEDLIMIT']._serialized_start = 845
    _globals['_COMBINEDLIMIT']._serialized_end = 1021
    _globals['_ALLOWALLMESSAGESFILTER']._serialized_start = 1023
    _globals['_ALLOWALLMESSAGESFILTER']._serialized_end = 1090
    _globals['_ACCEPTEDMESSAGEKEYSFILTER']._serialized_start = 1092
    _globals['_ACCEPTEDMESSAGEKEYSFILTER']._serialized_end = 1176
    _globals['_ACCEPTEDMESSAGESFILTER']._serialized_start = 1178
    _globals['_ACCEPTEDMESSAGESFILTER']._serialized_end = 1287