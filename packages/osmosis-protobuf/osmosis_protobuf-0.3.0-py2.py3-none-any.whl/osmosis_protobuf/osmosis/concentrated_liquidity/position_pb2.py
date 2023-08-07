"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ...cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ...osmosis.lockup import lock_pb2 as osmosis_dot_lockup_dot_lock__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-osmosis/concentrated-liquidity/position.proto\x12%osmosis.concentratedliquidity.v1beta1\x1a\x19cosmos_proto/cosmos.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x19osmosis/lockup/lock.proto"\xcd\x02\n\x08Position\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id"\x12#\n\x07address\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12#\n\x07pool_id\x18\x03 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12\x12\n\nlower_tick\x18\x04 \x01(\x03\x12\x12\n\nupper_tick\x18\x05 \x01(\x03\x12K\n\tjoin_time\x18\x06 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1c\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"join_time"\x90\xdf\x1f\x01\x12U\n\tliquidity\x18\x07 \x01(\tBB\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x10yaml:"liquidity""\xba\x04\n\x15FullPositionBreakdown\x12G\n\x08position\x18\x01 \x01(\x0b2/.osmosis.concentratedliquidity.v1beta1.PositionB\x04\xc8\xde\x1f\x00\x12Z\n\x06asset0\x18\x02 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB/\xc8\xde\x1f\x00\xaa\xdf\x1f\'github.com/cosmos/cosmos-sdk/types.Coin\x12Z\n\x06asset1\x18\x03 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB/\xc8\xde\x1f\x00\xaa\xdf\x1f\'github.com/cosmos/cosmos-sdk/types.Coin\x12d\n\x18claimable_spread_rewards\x18\x04 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\'\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"claimable_spread_rewards"\x12\\\n\x14claimable_incentives\x18\x05 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB#\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"claimable_incentives"\x12\\\n\x14forfeited_incentives\x18\x06 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB#\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"forfeited_incentives""\x92\x01\n\x16PositionWithPeriodLock\x12G\n\x08position\x18\x01 \x01(\x0b2/.osmosis.concentratedliquidity.v1beta1.PositionB\x04\xc8\xde\x1f\x00\x12/\n\x05locks\x18\x02 \x01(\x0b2\x1a.osmosis.lockup.PeriodLockB\x04\xc8\xde\x1f\x00BDZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/modelb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.concentrated_liquidity.position_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/model'
    _POSITION.fields_by_name['position_id']._options = None
    _POSITION.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _POSITION.fields_by_name['address']._options = None
    _POSITION.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _POSITION.fields_by_name['pool_id']._options = None
    _POSITION.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _POSITION.fields_by_name['join_time']._options = None
    _POSITION.fields_by_name['join_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"join_time"\x90\xdf\x1f\x01'
    _POSITION.fields_by_name['liquidity']._options = None
    _POSITION.fields_by_name['liquidity']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x10yaml:"liquidity"'
    _FULLPOSITIONBREAKDOWN.fields_by_name['position']._options = None
    _FULLPOSITIONBREAKDOWN.fields_by_name['position']._serialized_options = b'\xc8\xde\x1f\x00'
    _FULLPOSITIONBREAKDOWN.fields_by_name['asset0']._options = None
    _FULLPOSITIONBREAKDOWN.fields_by_name['asset0']._serialized_options = b"\xc8\xde\x1f\x00\xaa\xdf\x1f'github.com/cosmos/cosmos-sdk/types.Coin"
    _FULLPOSITIONBREAKDOWN.fields_by_name['asset1']._options = None
    _FULLPOSITIONBREAKDOWN.fields_by_name['asset1']._serialized_options = b"\xc8\xde\x1f\x00\xaa\xdf\x1f'github.com/cosmos/cosmos-sdk/types.Coin"
    _FULLPOSITIONBREAKDOWN.fields_by_name['claimable_spread_rewards']._options = None
    _FULLPOSITIONBREAKDOWN.fields_by_name['claimable_spread_rewards']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"claimable_spread_rewards"'
    _FULLPOSITIONBREAKDOWN.fields_by_name['claimable_incentives']._options = None
    _FULLPOSITIONBREAKDOWN.fields_by_name['claimable_incentives']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"claimable_incentives"'
    _FULLPOSITIONBREAKDOWN.fields_by_name['forfeited_incentives']._options = None
    _FULLPOSITIONBREAKDOWN.fields_by_name['forfeited_incentives']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"forfeited_incentives"'
    _POSITIONWITHPERIODLOCK.fields_by_name['position']._options = None
    _POSITIONWITHPERIODLOCK.fields_by_name['position']._serialized_options = b'\xc8\xde\x1f\x00'
    _POSITIONWITHPERIODLOCK.fields_by_name['locks']._options = None
    _POSITIONWITHPERIODLOCK.fields_by_name['locks']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_POSITION']._serialized_start = 262
    _globals['_POSITION']._serialized_end = 595
    _globals['_FULLPOSITIONBREAKDOWN']._serialized_start = 598
    _globals['_FULLPOSITIONBREAKDOWN']._serialized_end = 1168
    _globals['_POSITIONWITHPERIODLOCK']._serialized_start = 1171
    _globals['_POSITIONWITHPERIODLOCK']._serialized_end = 1317