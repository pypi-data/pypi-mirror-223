"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'osmosis/protorev/v1beta1/protorev.proto\x12\x18osmosis.protorev.v1beta1\x1a\x19cosmos_proto/cosmos.proto\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\xba\x01\n\x12TokenPairArbRoutes\x12N\n\narb_routes\x18\x01 \x03(\x0b2\x1f.osmosis.protorev.v1beta1.RouteB\x19\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"arb_routes"\x12%\n\x08token_in\x18\x02 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:"token_in"\x12\'\n\ttoken_out\x18\x03 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"token_out":\x04\xe8\xa0\x1f\x01"\xac\x01\n\x05Route\x12F\n\x06trades\x18\x01 \x03(\x0b2\x1f.osmosis.protorev.v1beta1.TradeB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"trades"\x12U\n\tstep_size\x18\x02 \x01(\tBB\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x10yaml:"step_size":\x04\xe8\xa0\x1f\x01"|\n\x05Trade\x12\x1d\n\x04pool\x18\x01 \x01(\x04B\x0f\xf2\xde\x1f\x0byaml:"pool"\x12%\n\x08token_in\x18\x02 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:"token_in"\x12\'\n\ttoken_out\x18\x03 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"token_out":\x04\xe8\xa0\x1f\x01"\xdb\x01\n\x0fRouteStatistics\x12B\n\x07profits\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\x16\xc8\xde\x1f\x00\xf2\xde\x1f\x0eyaml:"profits"\x12c\n\x10number_of_trades\x18\x02 \x01(\tBI\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x17yaml:"number_of_trades"\x12\x1f\n\x05route\x18\x03 \x03(\x04B\x10\xf2\xde\x1f\x0cyaml:"route""\xb0\x01\n\x0bPoolWeights\x12/\n\rstable_weight\x18\x01 \x01(\x04B\x18\xf2\xde\x1f\x14yaml:"stable_weight"\x123\n\x0fbalancer_weight\x18\x02 \x01(\x04B\x1a\xf2\xde\x1f\x16yaml:"balancer_weight"\x12;\n\x13concentrated_weight\x18\x03 \x01(\x04B\x1e\xf2\xde\x1f\x1ayaml:"concentrated_weight""\x83\x01\n\tBaseDenom\x12\x1f\n\x05denom\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"denom"\x12U\n\tstep_size\x18\x02 \x01(\tBB\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x10yaml:"step_size"B6Z4github.com/osmosis-labs/osmosis/v16/x/protorev/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.protorev.v1beta1.protorev_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z4github.com/osmosis-labs/osmosis/v16/x/protorev/types'
    _TOKENPAIRARBROUTES.fields_by_name['arb_routes']._options = None
    _TOKENPAIRARBROUTES.fields_by_name['arb_routes']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"arb_routes"'
    _TOKENPAIRARBROUTES.fields_by_name['token_in']._options = None
    _TOKENPAIRARBROUTES.fields_by_name['token_in']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"token_in"'
    _TOKENPAIRARBROUTES.fields_by_name['token_out']._options = None
    _TOKENPAIRARBROUTES.fields_by_name['token_out']._serialized_options = b'\xf2\xde\x1f\x10yaml:"token_out"'
    _TOKENPAIRARBROUTES._options = None
    _TOKENPAIRARBROUTES._serialized_options = b'\xe8\xa0\x1f\x01'
    _ROUTE.fields_by_name['trades']._options = None
    _ROUTE.fields_by_name['trades']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"trades"'
    _ROUTE.fields_by_name['step_size']._options = None
    _ROUTE.fields_by_name['step_size']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x10yaml:"step_size"'
    _ROUTE._options = None
    _ROUTE._serialized_options = b'\xe8\xa0\x1f\x01'
    _TRADE.fields_by_name['pool']._options = None
    _TRADE.fields_by_name['pool']._serialized_options = b'\xf2\xde\x1f\x0byaml:"pool"'
    _TRADE.fields_by_name['token_in']._options = None
    _TRADE.fields_by_name['token_in']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"token_in"'
    _TRADE.fields_by_name['token_out']._options = None
    _TRADE.fields_by_name['token_out']._serialized_options = b'\xf2\xde\x1f\x10yaml:"token_out"'
    _TRADE._options = None
    _TRADE._serialized_options = b'\xe8\xa0\x1f\x01'
    _ROUTESTATISTICS.fields_by_name['profits']._options = None
    _ROUTESTATISTICS.fields_by_name['profits']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0eyaml:"profits"'
    _ROUTESTATISTICS.fields_by_name['number_of_trades']._options = None
    _ROUTESTATISTICS.fields_by_name['number_of_trades']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x17yaml:"number_of_trades"'
    _ROUTESTATISTICS.fields_by_name['route']._options = None
    _ROUTESTATISTICS.fields_by_name['route']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"route"'
    _POOLWEIGHTS.fields_by_name['stable_weight']._options = None
    _POOLWEIGHTS.fields_by_name['stable_weight']._serialized_options = b'\xf2\xde\x1f\x14yaml:"stable_weight"'
    _POOLWEIGHTS.fields_by_name['balancer_weight']._options = None
    _POOLWEIGHTS.fields_by_name['balancer_weight']._serialized_options = b'\xf2\xde\x1f\x16yaml:"balancer_weight"'
    _POOLWEIGHTS.fields_by_name['concentrated_weight']._options = None
    _POOLWEIGHTS.fields_by_name['concentrated_weight']._serialized_options = b'\xf2\xde\x1f\x1ayaml:"concentrated_weight"'
    _BASEDENOM.fields_by_name['denom']._options = None
    _BASEDENOM.fields_by_name['denom']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"denom"'
    _BASEDENOM.fields_by_name['step_size']._options = None
    _BASEDENOM.fields_by_name['step_size']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x10yaml:"step_size"'
    _globals['_TOKENPAIRARBROUTES']._serialized_start = 151
    _globals['_TOKENPAIRARBROUTES']._serialized_end = 337
    _globals['_ROUTE']._serialized_start = 340
    _globals['_ROUTE']._serialized_end = 512
    _globals['_TRADE']._serialized_start = 514
    _globals['_TRADE']._serialized_end = 638
    _globals['_ROUTESTATISTICS']._serialized_start = 641
    _globals['_ROUTESTATISTICS']._serialized_end = 860
    _globals['_POOLWEIGHTS']._serialized_start = 863
    _globals['_POOLWEIGHTS']._serialized_end = 1039
    _globals['_BASEDENOM']._serialized_start = 1042
    _globals['_BASEDENOM']._serialized_end = 1173