"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ...cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ...cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ...osmosis.accum.v1beta1 import accum_pb2 as osmosis_dot_accum_dot_v1beta1_dot_accum__pb2
from ...osmosis.concentrated_liquidity import params_pb2 as osmosis_dot_concentrated__liquidity_dot_params__pb2
from ...osmosis.concentrated_liquidity import position_pb2 as osmosis_dot_concentrated__liquidity_dot_position__pb2
from ...osmosis.concentrated_liquidity import tickInfo_pb2 as osmosis_dot_concentrated__liquidity_dot_tickInfo__pb2
from ...osmosis.concentrated_liquidity import incentive_record_pb2 as osmosis_dot_concentrated__liquidity_dot_incentive__record__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,osmosis/concentrated-liquidity/genesis.proto\x12%osmosis.concentratedliquidity.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x19google/protobuf/any.proto\x1a!osmosis/accum/v1beta1/accum.proto\x1a+osmosis/concentrated-liquidity/params.proto\x1a-osmosis/concentrated-liquidity/position.proto\x1a-osmosis/concentrated-liquidity/tickInfo.proto\x1a5osmosis/concentrated-liquidity/incentive_record.proto"\xb3\x01\n\x08FullTick\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12)\n\ntick_index\x18\x02 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"tick_index"\x12W\n\x04info\x18\x03 \x01(\x0b2/.osmosis.concentratedliquidity.v1beta1.TickInfoB\x18\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"tick_info""\xe5\x03\n\x08PoolData\x12-\n\x04pool\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyB\t\xca\xb4-\x05PoolI\x12T\n\x05ticks\x18\x02 \x03(\x0b2/.osmosis.concentratedliquidity.v1beta1.FullTickB\x14\xc8\xde\x1f\x00\xf2\xde\x1f\x0cyaml:"ticks"\x12\x7f\n\x19spread_reward_accumulator\x18\x03 \x01(\x0b22.osmosis.concentratedliquidity.v1beta1.AccumObjectB(\xc8\xde\x1f\x00\xf2\xde\x1f yaml:"spread_reward_accumulator"\x12z\n\x17incentives_accumulators\x18\x04 \x03(\x0b22.osmosis.concentratedliquidity.v1beta1.AccumObjectB%\xc8\xde\x1f\x00\xf2\xde\x1f\x1dyaml:"incentives_accumulator"\x12W\n\x11incentive_records\x18\x05 \x03(\x0b26.osmosis.concentratedliquidity.v1beta1.IncentiveRecordB\x04\xc8\xde\x1f\x00"\x82\x02\n\x0cPositionData\x12A\n\x08position\x18\x01 \x01(\x0b2/.osmosis.concentratedliquidity.v1beta1.Position\x12#\n\x07lock_id\x18\x02 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"lock_id"\x12G\n\x1aspread_reward_accum_record\x18\x03 \x01(\x0b2\x1d.osmosis.accum.v1beta1.RecordB\x04\xc8\xde\x1f\x00\x12A\n\x14uptime_accum_records\x18\x04 \x03(\x0b2\x1d.osmosis.accum.v1beta1.RecordB\x04\xc8\xde\x1f\x00"\xe5\x02\n\x0cGenesisState\x12;\n\x06params\x18\x01 \x01(\x0b2%.osmosis.concentratedliquidity.ParamsB\x04\xc8\xde\x1f\x00\x12H\n\tpool_data\x18\x02 \x03(\x0b2/.osmosis.concentratedliquidity.v1beta1.PoolDataB\x04\xc8\xde\x1f\x00\x12P\n\rposition_data\x18\x03 \x03(\x0b23.osmosis.concentratedliquidity.v1beta1.PositionDataB\x04\xc8\xde\x1f\x00\x125\n\x10next_position_id\x18\x04 \x01(\x04B\x1b\xf2\xde\x1f\x17yaml:"next_position_id"\x12E\n\x18next_incentive_record_id\x18\x05 \x01(\x04B#\xf2\xde\x1f\x1fyaml:"next_incentive_record_id""n\n\x0bAccumObject\x12\x1d\n\x04name\x18\x01 \x01(\tB\x0f\xf2\xde\x1f\x0byaml:"name"\x12@\n\raccum_content\x18\x02 \x01(\x0b2).osmosis.accum.v1beta1.AccumulatorContentBLZJgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/types/genesisb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.concentrated_liquidity.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZJgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/types/genesis'
    _FULLTICK.fields_by_name['pool_id']._options = None
    _FULLTICK.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _FULLTICK.fields_by_name['tick_index']._options = None
    _FULLTICK.fields_by_name['tick_index']._serialized_options = b'\xf2\xde\x1f\x11yaml:"tick_index"'
    _FULLTICK.fields_by_name['info']._options = None
    _FULLTICK.fields_by_name['info']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"tick_info"'
    _POOLDATA.fields_by_name['pool']._options = None
    _POOLDATA.fields_by_name['pool']._serialized_options = b'\xca\xb4-\x05PoolI'
    _POOLDATA.fields_by_name['ticks']._options = None
    _POOLDATA.fields_by_name['ticks']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0cyaml:"ticks"'
    _POOLDATA.fields_by_name['spread_reward_accumulator']._options = None
    _POOLDATA.fields_by_name['spread_reward_accumulator']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f yaml:"spread_reward_accumulator"'
    _POOLDATA.fields_by_name['incentives_accumulators']._options = None
    _POOLDATA.fields_by_name['incentives_accumulators']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1dyaml:"incentives_accumulator"'
    _POOLDATA.fields_by_name['incentive_records']._options = None
    _POOLDATA.fields_by_name['incentive_records']._serialized_options = b'\xc8\xde\x1f\x00'
    _POSITIONDATA.fields_by_name['lock_id']._options = None
    _POSITIONDATA.fields_by_name['lock_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"lock_id"'
    _POSITIONDATA.fields_by_name['spread_reward_accum_record']._options = None
    _POSITIONDATA.fields_by_name['spread_reward_accum_record']._serialized_options = b'\xc8\xde\x1f\x00'
    _POSITIONDATA.fields_by_name['uptime_accum_records']._options = None
    _POSITIONDATA.fields_by_name['uptime_accum_records']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['params']._options = None
    _GENESISSTATE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['pool_data']._options = None
    _GENESISSTATE.fields_by_name['pool_data']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['position_data']._options = None
    _GENESISSTATE.fields_by_name['position_data']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['next_position_id']._options = None
    _GENESISSTATE.fields_by_name['next_position_id']._serialized_options = b'\xf2\xde\x1f\x17yaml:"next_position_id"'
    _GENESISSTATE.fields_by_name['next_incentive_record_id']._options = None
    _GENESISSTATE.fields_by_name['next_incentive_record_id']._serialized_options = b'\xf2\xde\x1f\x1fyaml:"next_incentive_record_id"'
    _ACCUMOBJECT.fields_by_name['name']._options = None
    _ACCUMOBJECT.fields_by_name['name']._serialized_options = b'\xf2\xde\x1f\x0byaml:"name"'
    _globals['_FULLTICK']._serialized_start = 425
    _globals['_FULLTICK']._serialized_end = 604
    _globals['_POOLDATA']._serialized_start = 607
    _globals['_POOLDATA']._serialized_end = 1092
    _globals['_POSITIONDATA']._serialized_start = 1095
    _globals['_POSITIONDATA']._serialized_end = 1353
    _globals['_GENESISSTATE']._serialized_start = 1356
    _globals['_GENESISSTATE']._serialized_end = 1713
    _globals['_ACCUMOBJECT']._serialized_start = 1715
    _globals['_ACCUMOBJECT']._serialized_end = 1825