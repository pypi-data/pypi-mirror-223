"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....amino import amino_pb2 as amino_dot_amino__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from .....cosmos.auth.v1beta1 import auth_pb2 as cosmos_dot_auth_dot_v1beta1_dot_auth__pb2
from .....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4osmosis/gamm/pool-models/balancer/balancerPool.proto\x12\x14osmosis.gamm.v1beta1\x1a\x19cosmos_proto/cosmos.proto\x1a\x14gogoproto/gogo.proto\x1a\x11amino/amino.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1ecosmos/auth/v1beta1/auth.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x8f\x03\n\x18SmoothWeightChangeParams\x12M\n\nstart_time\x18\x01 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01\x12^\n\x08duration\x18\x02 \x01(\x0b2\x19.google.protobuf.DurationB1\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01\x12b\n\x14initial_pool_weights\x18\x03 \x03(\x0b2\x1f.osmosis.gamm.v1beta1.PoolAssetB#\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"initial_pool_weights"\x12`\n\x13target_pool_weights\x18\x04 \x03(\x0b2\x1f.osmosis.gamm.v1beta1.PoolAssetB"\xc8\xde\x1f\x00\xf2\xde\x1f\x1ayaml:"target_pool_weights""\xdd\x02\n\nPoolParams\x12S\n\x08swap_fee\x18\x01 \x01(\tBA\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x0fyaml:"swap_fee"\x12S\n\x08exit_fee\x18\x02 \x01(\tBA\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x0fyaml:"exit_fee"\x12\x7f\n\x1bsmooth_weight_change_params\x18\x03 \x01(\x0b2..osmosis.gamm.v1beta1.SmoothWeightChangeParamsB*\xc8\xde\x1f\x01\xf2\xde\x1f"yaml:"smooth_weight_change_params":$\x8a\xe7\xb0*\x1fosmosis/gamm/BalancerPoolParams"\x9c\x01\n\tPoolAsset\x12>\n\x05token\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x14\xc8\xde\x1f\x00\xf2\xde\x1f\x0cyaml:"token"\x12O\n\x06weight\x18\x02 \x01(\tB?\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\ryaml:"weight""\x80\x04\n\x04Pool\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12\n\n\x02id\x18\x02 \x01(\x04\x12Z\n\x0bpool_params\x18\x03 \x01(\x0b2 .osmosis.gamm.v1beta1.PoolParamsB#\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"balancer_pool_params"\x12=\n\x14future_pool_governor\x18\x04 \x01(\tB\x1f\xf2\xde\x1f\x1byaml:"future_pool_governor"\x12L\n\x0ctotal_shares\x18\x05 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x1b\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"total_shares"\x12P\n\x0bpool_assets\x18\x06 \x03(\x0b2\x1f.osmosis.gamm.v1beta1.PoolAssetB\x1a\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"pool_assets"\x12[\n\x0ctotal_weight\x18\x07 \x01(\tBE\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x13yaml:"total_weight":/\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xca\xb4-\x05PoolI\x8a\xe7\xb0*\x19osmosis/gamm/BalancerPoolBAZ?github.com/osmosis-labs/osmosis/v16/x/gamm/pool-models/balancerb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.gamm.pool_models.balancer.balancerPool_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z?github.com/osmosis-labs/osmosis/v16/x/gamm/pool-models/balancer'
    _SMOOTHWEIGHTCHANGEPARAMS.fields_by_name['start_time']._options = None
    _SMOOTHWEIGHTCHANGEPARAMS.fields_by_name['start_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01'
    _SMOOTHWEIGHTCHANGEPARAMS.fields_by_name['duration']._options = None
    _SMOOTHWEIGHTCHANGEPARAMS.fields_by_name['duration']._serialized_options = b'\xc8\xde\x1f\x00\xea\xde\x1f\x12duration,omitempty\xf2\xde\x1f\x0fyaml:"duration"\x98\xdf\x1f\x01'
    _SMOOTHWEIGHTCHANGEPARAMS.fields_by_name['initial_pool_weights']._options = None
    _SMOOTHWEIGHTCHANGEPARAMS.fields_by_name['initial_pool_weights']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"initial_pool_weights"'
    _SMOOTHWEIGHTCHANGEPARAMS.fields_by_name['target_pool_weights']._options = None
    _SMOOTHWEIGHTCHANGEPARAMS.fields_by_name['target_pool_weights']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1ayaml:"target_pool_weights"'
    _POOLPARAMS.fields_by_name['swap_fee']._options = None
    _POOLPARAMS.fields_by_name['swap_fee']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x0fyaml:"swap_fee"'
    _POOLPARAMS.fields_by_name['exit_fee']._options = None
    _POOLPARAMS.fields_by_name['exit_fee']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x0fyaml:"exit_fee"'
    _POOLPARAMS.fields_by_name['smooth_weight_change_params']._options = None
    _POOLPARAMS.fields_by_name['smooth_weight_change_params']._serialized_options = b'\xc8\xde\x1f\x01\xf2\xde\x1f"yaml:"smooth_weight_change_params"'
    _POOLPARAMS._options = None
    _POOLPARAMS._serialized_options = b'\x8a\xe7\xb0*\x1fosmosis/gamm/BalancerPoolParams'
    _POOLASSET.fields_by_name['token']._options = None
    _POOLASSET.fields_by_name['token']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0cyaml:"token"'
    _POOLASSET.fields_by_name['weight']._options = None
    _POOLASSET.fields_by_name['weight']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\ryaml:"weight"'
    _POOL.fields_by_name['address']._options = None
    _POOL.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _POOL.fields_by_name['pool_params']._options = None
    _POOL.fields_by_name['pool_params']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"balancer_pool_params"'
    _POOL.fields_by_name['future_pool_governor']._options = None
    _POOL.fields_by_name['future_pool_governor']._serialized_options = b'\xf2\xde\x1f\x1byaml:"future_pool_governor"'
    _POOL.fields_by_name['total_shares']._options = None
    _POOL.fields_by_name['total_shares']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"total_shares"'
    _POOL.fields_by_name['pool_assets']._options = None
    _POOL.fields_by_name['pool_assets']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"pool_assets"'
    _POOL.fields_by_name['total_weight']._options = None
    _POOL.fields_by_name['total_weight']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x13yaml:"total_weight"'
    _POOL._options = None
    _POOL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xca\xb4-\x05PoolI\x8a\xe7\xb0*\x19osmosis/gamm/BalancerPool'
    _globals['_SMOOTHWEIGHTCHANGEPARAMS']._serialized_start = 276
    _globals['_SMOOTHWEIGHTCHANGEPARAMS']._serialized_end = 675
    _globals['_POOLPARAMS']._serialized_start = 678
    _globals['_POOLPARAMS']._serialized_end = 1027
    _globals['_POOLASSET']._serialized_start = 1030
    _globals['_POOLASSET']._serialized_end = 1186
    _globals['_POOL']._serialized_start = 1189
    _globals['_POOL']._serialized_end = 1701