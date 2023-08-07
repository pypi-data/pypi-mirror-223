"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)osmosis/concentrated-liquidity/pool.proto\x12%osmosis.concentratedliquidity.v1beta1\x1a\x19cosmos_proto/cosmos.proto\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xa6\x06\n\x04Pool\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x129\n\x12incentives_address\x18\x02 \x01(\tB\x1d\xf2\xde\x1f\x19yaml:"incentives_address"\x12A\n\x16spread_rewards_address\x18\x03 \x01(\tB!\xf2\xde\x1f\x1dyaml:"spread_rewards_address"\x12\n\n\x02id\x18\x04 \x01(\x04\x12o\n\x16current_tick_liquidity\x18\x05 \x01(\tBO\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x1dyaml:"current_tick_liquidity"\x12\x0e\n\x06token0\x18\x06 \x01(\t\x12\x0e\n\x06token1\x18\x07 \x01(\t\x12h\n\x12current_sqrt_price\x18\x08 \x01(\tBL\xc8\xde\x1f\x00\xda\xde\x1f/github.com/osmosis-labs/osmosis/osmomath.BigDec\xf2\xde\x1f\x11yaml:"spot_price"\x12-\n\x0ccurrent_tick\x18\t \x01(\x03B\x17\xf2\xde\x1f\x13yaml:"current_tick"\x12-\n\x0ctick_spacing\x18\n \x01(\x04B\x17\xf2\xde\x1f\x13yaml:"tick_spacing"\x12?\n\x15exponent_at_price_one\x18\x0b \x01(\x03B \xf2\xde\x1f\x1cyaml:"exponent_at_price_one"\x12]\n\rspread_factor\x18\x0c \x01(\tBF\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"spread_factor"\x12c\n\x15last_liquidity_update\x18\r \x01(\x0b2\x1a.google.protobuf.TimestampB(\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"last_liquidity_update"\x90\xdf\x1f\x01:\x11\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xca\xb4-\x05PoolIBDZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/modelb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.concentrated_liquidity.pool_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/model'
    _POOL.fields_by_name['address']._options = None
    _POOL.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _POOL.fields_by_name['incentives_address']._options = None
    _POOL.fields_by_name['incentives_address']._serialized_options = b'\xf2\xde\x1f\x19yaml:"incentives_address"'
    _POOL.fields_by_name['spread_rewards_address']._options = None
    _POOL.fields_by_name['spread_rewards_address']._serialized_options = b'\xf2\xde\x1f\x1dyaml:"spread_rewards_address"'
    _POOL.fields_by_name['current_tick_liquidity']._options = None
    _POOL.fields_by_name['current_tick_liquidity']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x1dyaml:"current_tick_liquidity"'
    _POOL.fields_by_name['current_sqrt_price']._options = None
    _POOL.fields_by_name['current_sqrt_price']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f/github.com/osmosis-labs/osmosis/osmomath.BigDec\xf2\xde\x1f\x11yaml:"spot_price"'
    _POOL.fields_by_name['current_tick']._options = None
    _POOL.fields_by_name['current_tick']._serialized_options = b'\xf2\xde\x1f\x13yaml:"current_tick"'
    _POOL.fields_by_name['tick_spacing']._options = None
    _POOL.fields_by_name['tick_spacing']._serialized_options = b'\xf2\xde\x1f\x13yaml:"tick_spacing"'
    _POOL.fields_by_name['exponent_at_price_one']._options = None
    _POOL.fields_by_name['exponent_at_price_one']._serialized_options = b'\xf2\xde\x1f\x1cyaml:"exponent_at_price_one"'
    _POOL.fields_by_name['spread_factor']._options = None
    _POOL.fields_by_name['spread_factor']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"spread_factor"'
    _POOL.fields_by_name['last_liquidity_update']._options = None
    _POOL.fields_by_name['last_liquidity_update']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"last_liquidity_update"\x90\xdf\x1f\x01'
    _POOL._options = None
    _POOL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xca\xb4-\x05PoolI'
    _globals['_POOL']._serialized_start = 167
    _globals['_POOL']._serialized_end = 973