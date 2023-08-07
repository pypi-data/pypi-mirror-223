"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ...cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+osmosis/concentrated-liquidity/params.proto\x12\x1dosmosis.concentratedliquidity\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1egoogle/protobuf/duration.proto"\xe6\x04\n\x06Params\x12C\n\x17authorized_tick_spacing\x18\x01 \x03(\x04B"\xf2\xde\x1f\x1eyaml:"authorized_tick_spacing"\x12u\n\x19authorized_spread_factors\x18\x02 \x03(\tBR\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f yaml:"authorized_spread_factors"\x12\x81\x01\n\x1fbalancer_shares_reward_discount\x18\x03 \x01(\tBX\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f&yaml:"balancer_shares_reward_discount"\x12C\n\x17authorized_quote_denoms\x18\x04 \x03(\tB"\xf2\xde\x1f\x1eyaml:"authorized_quote_denoms"\x12r\n\x12authorized_uptimes\x18\x05 \x03(\x0b2\x19.google.protobuf.DurationB;\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x19yaml:"authorized_uptimes"\x98\xdf\x1f\x01\x12c\n\'is_permissionless_pool_creation_enabled\x18\x06 \x01(\x08B2\xf2\xde\x1f.yaml:"is_permissionless_pool_creation_enabled"BDZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.concentrated_liquidity.params_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/types'
    _PARAMS.fields_by_name['authorized_tick_spacing']._options = None
    _PARAMS.fields_by_name['authorized_tick_spacing']._serialized_options = b'\xf2\xde\x1f\x1eyaml:"authorized_tick_spacing"'
    _PARAMS.fields_by_name['authorized_spread_factors']._options = None
    _PARAMS.fields_by_name['authorized_spread_factors']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f yaml:"authorized_spread_factors"'
    _PARAMS.fields_by_name['balancer_shares_reward_discount']._options = None
    _PARAMS.fields_by_name['balancer_shares_reward_discount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f&yaml:"balancer_shares_reward_discount"'
    _PARAMS.fields_by_name['authorized_quote_denoms']._options = None
    _PARAMS.fields_by_name['authorized_quote_denoms']._serialized_options = b'\xf2\xde\x1f\x1eyaml:"authorized_quote_denoms"'
    _PARAMS.fields_by_name['authorized_uptimes']._options = None
    _PARAMS.fields_by_name['authorized_uptimes']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x19yaml:"authorized_uptimes"\x98\xdf\x1f\x01'
    _PARAMS.fields_by_name['is_permissionless_pool_creation_enabled']._options = None
    _PARAMS.fields_by_name['is_permissionless_pool_creation_enabled']._serialized_options = b'\xf2\xde\x1f.yaml:"is_permissionless_pool_creation_enabled"'
    _globals['_PARAMS']._serialized_start = 160
    _globals['_PARAMS']._serialized_end = 774