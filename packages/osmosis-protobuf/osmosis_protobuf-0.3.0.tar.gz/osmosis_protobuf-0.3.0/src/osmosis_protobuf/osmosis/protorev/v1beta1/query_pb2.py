"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....osmosis.protorev.v1beta1 import params_pb2 as osmosis_dot_protorev_dot_v1beta1_dot_params__pb2
from ....osmosis.protorev.v1beta1 import protorev_pb2 as osmosis_dot_protorev_dot_v1beta1_dot_protorev__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$osmosis/protorev/v1beta1/query.proto\x12\x18osmosis.protorev.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a%osmosis/protorev/v1beta1/params.proto\x1a\'osmosis/protorev/v1beta1/protorev.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x14\n\x12QueryParamsRequest"^\n\x13QueryParamsResponse\x12G\n\x06params\x18\x01 \x01(\x0b2 .osmosis.protorev.v1beta1.ParamsB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"params""\'\n%QueryGetProtoRevNumberOfTradesRequest"\x8d\x01\n&QueryGetProtoRevNumberOfTradesResponse\x12c\n\x10number_of_trades\x18\x01 \x01(\tBI\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x17yaml:"number_of_trades""H\n%QueryGetProtoRevProfitsByDenomRequest\x12\x1f\n\x05denom\x18\x01 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"denom""f\n&QueryGetProtoRevProfitsByDenomResponse\x12<\n\x06profit\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x11\xf2\xde\x1f\ryaml:"profit""#\n!QueryGetProtoRevAllProfitsRequest"h\n"QueryGetProtoRevAllProfitsResponse\x12B\n\x07profits\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\x16\xc8\xde\x1f\x00\xf2\xde\x1f\x0eyaml:"profits""K\n(QueryGetProtoRevStatisticsByRouteRequest\x12\x1f\n\x05route\x18\x01 \x03(\x04B\x10\xf2\xde\x1f\x0cyaml:"route""\x85\x01\n)QueryGetProtoRevStatisticsByRouteResponse\x12X\n\nstatistics\x18\x01 \x01(\x0b2).osmosis.protorev.v1beta1.RouteStatisticsB\x19\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"statistics""+\n)QueryGetProtoRevAllRouteStatisticsRequest"\x86\x01\n*QueryGetProtoRevAllRouteStatisticsResponse\x12X\n\nstatistics\x18\x01 \x03(\x0b2).osmosis.protorev.v1beta1.RouteStatisticsB\x19\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"statistics""+\n)QueryGetProtoRevTokenPairArbRoutesRequest"\x81\x01\n*QueryGetProtoRevTokenPairArbRoutesResponse\x12S\n\x06routes\x18\x01 \x03(\x0b2,.osmosis.protorev.v1beta1.TokenPairArbRoutesB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"routes""%\n#QueryGetProtoRevAdminAccountRequest"W\n$QueryGetProtoRevAdminAccountResponse\x12/\n\radmin_account\x18\x01 \x01(\tB\x18\xf2\xde\x1f\x14yaml:"admin_account"")\n\'QueryGetProtoRevDeveloperAccountRequest"c\n(QueryGetProtoRevDeveloperAccountResponse\x127\n\x11developer_account\x18\x01 \x01(\tB\x1c\xf2\xde\x1f\x18yaml:"developer_account""$\n"QueryGetProtoRevPoolWeightsRequest"\x7f\n#QueryGetProtoRevPoolWeightsResponse\x12X\n\x0cpool_weights\x18\x01 \x01(\x0b2%.osmosis.protorev.v1beta1.PoolWeightsB\x1b\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"pool_weights"".\n,QueryGetProtoRevMaxPoolPointsPerBlockRequest"x\n-QueryGetProtoRevMaxPoolPointsPerBlockResponse\x12G\n\x19max_pool_points_per_block\x18\x01 \x01(\x04B$\xf2\xde\x1f yaml:"max_pool_points_per_block""+\n)QueryGetProtoRevMaxPoolPointsPerTxRequest"o\n*QueryGetProtoRevMaxPoolPointsPerTxResponse\x12A\n\x16max_pool_points_per_tx\x18\x01 \x01(\x04B!\xf2\xde\x1f\x1dyaml:"max_pool_points_per_tx""#\n!QueryGetProtoRevBaseDenomsRequest"z\n"QueryGetProtoRevBaseDenomsResponse\x12T\n\x0bbase_denoms\x18\x01 \x03(\x0b2#.osmosis.protorev.v1beta1.BaseDenomB\x1a\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"base_denoms"" \n\x1eQueryGetProtoRevEnabledRequest"F\n\x1fQueryGetProtoRevEnabledResponse\x12#\n\x07enabled\x18\x01 \x01(\x08B\x12\xf2\xde\x1f\x0eyaml:"enabled""u\n\x1bQueryGetProtoRevPoolRequest\x12)\n\nbase_denom\x18\x01 \x01(\tB\x15\xf2\xde\x1f\x11yaml:"base_denom"\x12+\n\x0bother_denom\x18\x02 \x01(\tB\x16\xf2\xde\x1f\x12yaml:"other_denom""C\n\x1cQueryGetProtoRevPoolResponse\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"2\xe7\x17\n\x05Query\x12\x8b\x01\n\x06Params\x12,.osmosis.protorev.v1beta1.QueryParamsRequest\x1a-.osmosis.protorev.v1beta1.QueryParamsResponse"$\x82\xd3\xe4\x93\x02\x1e\x12\x1c/osmosis/v14/protorev/params\x12\xce\x01\n\x19GetProtoRevNumberOfTrades\x12?.osmosis.protorev.v1beta1.QueryGetProtoRevNumberOfTradesRequest\x1a@.osmosis.protorev.v1beta1.QueryGetProtoRevNumberOfTradesResponse".\x82\xd3\xe4\x93\x02(\x12&/osmosis/v14/protorev/number_of_trades\x12\xce\x01\n\x19GetProtoRevProfitsByDenom\x12?.osmosis.protorev.v1beta1.QueryGetProtoRevProfitsByDenomRequest\x1a@.osmosis.protorev.v1beta1.QueryGetProtoRevProfitsByDenomResponse".\x82\xd3\xe4\x93\x02(\x12&/osmosis/v14/protorev/profits_by_denom\x12\xbd\x01\n\x15GetProtoRevAllProfits\x12;.osmosis.protorev.v1beta1.QueryGetProtoRevAllProfitsRequest\x1a<.osmosis.protorev.v1beta1.QueryGetProtoRevAllProfitsResponse")\x82\xd3\xe4\x93\x02#\x12!/osmosis/v14/protorev/all_profits\x12\xda\x01\n\x1cGetProtoRevStatisticsByRoute\x12B.osmosis.protorev.v1beta1.QueryGetProtoRevStatisticsByRouteRequest\x1aC.osmosis.protorev.v1beta1.QueryGetProtoRevStatisticsByRouteResponse"1\x82\xd3\xe4\x93\x02+\x12)/osmosis/v14/protorev/statistics_by_route\x12\xde\x01\n\x1dGetProtoRevAllRouteStatistics\x12C.osmosis.protorev.v1beta1.QueryGetProtoRevAllRouteStatisticsRequest\x1aD.osmosis.protorev.v1beta1.QueryGetProtoRevAllRouteStatisticsResponse"2\x82\xd3\xe4\x93\x02,\x12*/osmosis/v14/protorev/all_route_statistics\x12\xdf\x01\n\x1dGetProtoRevTokenPairArbRoutes\x12C.osmosis.protorev.v1beta1.QueryGetProtoRevTokenPairArbRoutesRequest\x1aD.osmosis.protorev.v1beta1.QueryGetProtoRevTokenPairArbRoutesResponse"3\x82\xd3\xe4\x93\x02-\x12+/osmosis/v14/protorev/token_pair_arb_routes\x12\xc5\x01\n\x17GetProtoRevAdminAccount\x12=.osmosis.protorev.v1beta1.QueryGetProtoRevAdminAccountRequest\x1a>.osmosis.protorev.v1beta1.QueryGetProtoRevAdminAccountResponse"+\x82\xd3\xe4\x93\x02%\x12#/osmosis/v14/protorev/admin_account\x12\xd5\x01\n\x1bGetProtoRevDeveloperAccount\x12A.osmosis.protorev.v1beta1.QueryGetProtoRevDeveloperAccountRequest\x1aB.osmosis.protorev.v1beta1.QueryGetProtoRevDeveloperAccountResponse"/\x82\xd3\xe4\x93\x02)\x12\'/osmosis/v14/protorev/developer_account\x12\xc1\x01\n\x16GetProtoRevPoolWeights\x12<.osmosis.protorev.v1beta1.QueryGetProtoRevPoolWeightsRequest\x1a=.osmosis.protorev.v1beta1.QueryGetProtoRevPoolWeightsResponse"*\x82\xd3\xe4\x93\x02$\x12"/osmosis/v14/protorev/pool_weights\x12\xe0\x01\n\x1dGetProtoRevMaxPoolPointsPerTx\x12C.osmosis.protorev.v1beta1.QueryGetProtoRevMaxPoolPointsPerTxRequest\x1aD.osmosis.protorev.v1beta1.QueryGetProtoRevMaxPoolPointsPerTxResponse"4\x82\xd3\xe4\x93\x02.\x12,/osmosis/v14/protorev/max_pool_points_per_tx\x12\xec\x01\n GetProtoRevMaxPoolPointsPerBlock\x12F.osmosis.protorev.v1beta1.QueryGetProtoRevMaxPoolPointsPerBlockRequest\x1aG.osmosis.protorev.v1beta1.QueryGetProtoRevMaxPoolPointsPerBlockResponse"7\x82\xd3\xe4\x93\x021\x12//osmosis/v14/protorev/max_pool_points_per_block\x12\xbd\x01\n\x15GetProtoRevBaseDenoms\x12;.osmosis.protorev.v1beta1.QueryGetProtoRevBaseDenomsRequest\x1a<.osmosis.protorev.v1beta1.QueryGetProtoRevBaseDenomsResponse")\x82\xd3\xe4\x93\x02#\x12!/osmosis/v14/protorev/base_denoms\x12\xb0\x01\n\x12GetProtoRevEnabled\x128.osmosis.protorev.v1beta1.QueryGetProtoRevEnabledRequest\x1a9.osmosis.protorev.v1beta1.QueryGetProtoRevEnabledResponse"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/osmosis/v14/protorev/enabled\x12\xa4\x01\n\x0fGetProtoRevPool\x125.osmosis.protorev.v1beta1.QueryGetProtoRevPoolRequest\x1a6.osmosis.protorev.v1beta1.QueryGetProtoRevPoolResponse""\x82\xd3\xe4\x93\x02\x1c\x12\x1a/osmosis/v14/protorev/poolB6Z4github.com/osmosis-labs/osmosis/v16/x/protorev/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.protorev.v1beta1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z4github.com/osmosis-labs/osmosis/v16/x/protorev/types'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"params"'
    _QUERYGETPROTOREVNUMBEROFTRADESRESPONSE.fields_by_name['number_of_trades']._options = None
    _QUERYGETPROTOREVNUMBEROFTRADESRESPONSE.fields_by_name['number_of_trades']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x17yaml:"number_of_trades"'
    _QUERYGETPROTOREVPROFITSBYDENOMREQUEST.fields_by_name['denom']._options = None
    _QUERYGETPROTOREVPROFITSBYDENOMREQUEST.fields_by_name['denom']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"denom"'
    _QUERYGETPROTOREVPROFITSBYDENOMRESPONSE.fields_by_name['profit']._options = None
    _QUERYGETPROTOREVPROFITSBYDENOMRESPONSE.fields_by_name['profit']._serialized_options = b'\xf2\xde\x1f\ryaml:"profit"'
    _QUERYGETPROTOREVALLPROFITSRESPONSE.fields_by_name['profits']._options = None
    _QUERYGETPROTOREVALLPROFITSRESPONSE.fields_by_name['profits']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x0eyaml:"profits"'
    _QUERYGETPROTOREVSTATISTICSBYROUTEREQUEST.fields_by_name['route']._options = None
    _QUERYGETPROTOREVSTATISTICSBYROUTEREQUEST.fields_by_name['route']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"route"'
    _QUERYGETPROTOREVSTATISTICSBYROUTERESPONSE.fields_by_name['statistics']._options = None
    _QUERYGETPROTOREVSTATISTICSBYROUTERESPONSE.fields_by_name['statistics']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"statistics"'
    _QUERYGETPROTOREVALLROUTESTATISTICSRESPONSE.fields_by_name['statistics']._options = None
    _QUERYGETPROTOREVALLROUTESTATISTICSRESPONSE.fields_by_name['statistics']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"statistics"'
    _QUERYGETPROTOREVTOKENPAIRARBROUTESRESPONSE.fields_by_name['routes']._options = None
    _QUERYGETPROTOREVTOKENPAIRARBROUTESRESPONSE.fields_by_name['routes']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"routes"'
    _QUERYGETPROTOREVADMINACCOUNTRESPONSE.fields_by_name['admin_account']._options = None
    _QUERYGETPROTOREVADMINACCOUNTRESPONSE.fields_by_name['admin_account']._serialized_options = b'\xf2\xde\x1f\x14yaml:"admin_account"'
    _QUERYGETPROTOREVDEVELOPERACCOUNTRESPONSE.fields_by_name['developer_account']._options = None
    _QUERYGETPROTOREVDEVELOPERACCOUNTRESPONSE.fields_by_name['developer_account']._serialized_options = b'\xf2\xde\x1f\x18yaml:"developer_account"'
    _QUERYGETPROTOREVPOOLWEIGHTSRESPONSE.fields_by_name['pool_weights']._options = None
    _QUERYGETPROTOREVPOOLWEIGHTSRESPONSE.fields_by_name['pool_weights']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"pool_weights"'
    _QUERYGETPROTOREVMAXPOOLPOINTSPERBLOCKRESPONSE.fields_by_name['max_pool_points_per_block']._options = None
    _QUERYGETPROTOREVMAXPOOLPOINTSPERBLOCKRESPONSE.fields_by_name['max_pool_points_per_block']._serialized_options = b'\xf2\xde\x1f yaml:"max_pool_points_per_block"'
    _QUERYGETPROTOREVMAXPOOLPOINTSPERTXRESPONSE.fields_by_name['max_pool_points_per_tx']._options = None
    _QUERYGETPROTOREVMAXPOOLPOINTSPERTXRESPONSE.fields_by_name['max_pool_points_per_tx']._serialized_options = b'\xf2\xde\x1f\x1dyaml:"max_pool_points_per_tx"'
    _QUERYGETPROTOREVBASEDENOMSRESPONSE.fields_by_name['base_denoms']._options = None
    _QUERYGETPROTOREVBASEDENOMSRESPONSE.fields_by_name['base_denoms']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x12yaml:"base_denoms"'
    _QUERYGETPROTOREVENABLEDRESPONSE.fields_by_name['enabled']._options = None
    _QUERYGETPROTOREVENABLEDRESPONSE.fields_by_name['enabled']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"enabled"'
    _QUERYGETPROTOREVPOOLREQUEST.fields_by_name['base_denom']._options = None
    _QUERYGETPROTOREVPOOLREQUEST.fields_by_name['base_denom']._serialized_options = b'\xf2\xde\x1f\x11yaml:"base_denom"'
    _QUERYGETPROTOREVPOOLREQUEST.fields_by_name['other_denom']._options = None
    _QUERYGETPROTOREVPOOLREQUEST.fields_by_name['other_denom']._serialized_options = b'\xf2\xde\x1f\x12yaml:"other_denom"'
    _QUERYGETPROTOREVPOOLRESPONSE.fields_by_name['pool_id']._options = None
    _QUERYGETPROTOREVPOOLRESPONSE.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1e\x12\x1c/osmosis/v14/protorev/params'
    _QUERY.methods_by_name['GetProtoRevNumberOfTrades']._options = None
    _QUERY.methods_by_name['GetProtoRevNumberOfTrades']._serialized_options = b'\x82\xd3\xe4\x93\x02(\x12&/osmosis/v14/protorev/number_of_trades'
    _QUERY.methods_by_name['GetProtoRevProfitsByDenom']._options = None
    _QUERY.methods_by_name['GetProtoRevProfitsByDenom']._serialized_options = b'\x82\xd3\xe4\x93\x02(\x12&/osmosis/v14/protorev/profits_by_denom'
    _QUERY.methods_by_name['GetProtoRevAllProfits']._options = None
    _QUERY.methods_by_name['GetProtoRevAllProfits']._serialized_options = b'\x82\xd3\xe4\x93\x02#\x12!/osmosis/v14/protorev/all_profits'
    _QUERY.methods_by_name['GetProtoRevStatisticsByRoute']._options = None
    _QUERY.methods_by_name['GetProtoRevStatisticsByRoute']._serialized_options = b'\x82\xd3\xe4\x93\x02+\x12)/osmosis/v14/protorev/statistics_by_route'
    _QUERY.methods_by_name['GetProtoRevAllRouteStatistics']._options = None
    _QUERY.methods_by_name['GetProtoRevAllRouteStatistics']._serialized_options = b'\x82\xd3\xe4\x93\x02,\x12*/osmosis/v14/protorev/all_route_statistics'
    _QUERY.methods_by_name['GetProtoRevTokenPairArbRoutes']._options = None
    _QUERY.methods_by_name['GetProtoRevTokenPairArbRoutes']._serialized_options = b'\x82\xd3\xe4\x93\x02-\x12+/osmosis/v14/protorev/token_pair_arb_routes'
    _QUERY.methods_by_name['GetProtoRevAdminAccount']._options = None
    _QUERY.methods_by_name['GetProtoRevAdminAccount']._serialized_options = b'\x82\xd3\xe4\x93\x02%\x12#/osmosis/v14/protorev/admin_account'
    _QUERY.methods_by_name['GetProtoRevDeveloperAccount']._options = None
    _QUERY.methods_by_name['GetProtoRevDeveloperAccount']._serialized_options = b"\x82\xd3\xe4\x93\x02)\x12'/osmosis/v14/protorev/developer_account"
    _QUERY.methods_by_name['GetProtoRevPoolWeights']._options = None
    _QUERY.methods_by_name['GetProtoRevPoolWeights']._serialized_options = b'\x82\xd3\xe4\x93\x02$\x12"/osmosis/v14/protorev/pool_weights'
    _QUERY.methods_by_name['GetProtoRevMaxPoolPointsPerTx']._options = None
    _QUERY.methods_by_name['GetProtoRevMaxPoolPointsPerTx']._serialized_options = b'\x82\xd3\xe4\x93\x02.\x12,/osmosis/v14/protorev/max_pool_points_per_tx'
    _QUERY.methods_by_name['GetProtoRevMaxPoolPointsPerBlock']._options = None
    _QUERY.methods_by_name['GetProtoRevMaxPoolPointsPerBlock']._serialized_options = b'\x82\xd3\xe4\x93\x021\x12//osmosis/v14/protorev/max_pool_points_per_block'
    _QUERY.methods_by_name['GetProtoRevBaseDenoms']._options = None
    _QUERY.methods_by_name['GetProtoRevBaseDenoms']._serialized_options = b'\x82\xd3\xe4\x93\x02#\x12!/osmosis/v14/protorev/base_denoms'
    _QUERY.methods_by_name['GetProtoRevEnabled']._options = None
    _QUERY.methods_by_name['GetProtoRevEnabled']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1f\x12\x1d/osmosis/v14/protorev/enabled'
    _QUERY.methods_by_name['GetProtoRevPool']._options = None
    _QUERY.methods_by_name['GetProtoRevPool']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1c\x12\x1a/osmosis/v14/protorev/pool'
    _globals['_QUERYPARAMSREQUEST']._serialized_start = 274
    _globals['_QUERYPARAMSREQUEST']._serialized_end = 294
    _globals['_QUERYPARAMSRESPONSE']._serialized_start = 296
    _globals['_QUERYPARAMSRESPONSE']._serialized_end = 390
    _globals['_QUERYGETPROTOREVNUMBEROFTRADESREQUEST']._serialized_start = 392
    _globals['_QUERYGETPROTOREVNUMBEROFTRADESREQUEST']._serialized_end = 431
    _globals['_QUERYGETPROTOREVNUMBEROFTRADESRESPONSE']._serialized_start = 434
    _globals['_QUERYGETPROTOREVNUMBEROFTRADESRESPONSE']._serialized_end = 575
    _globals['_QUERYGETPROTOREVPROFITSBYDENOMREQUEST']._serialized_start = 577
    _globals['_QUERYGETPROTOREVPROFITSBYDENOMREQUEST']._serialized_end = 649
    _globals['_QUERYGETPROTOREVPROFITSBYDENOMRESPONSE']._serialized_start = 651
    _globals['_QUERYGETPROTOREVPROFITSBYDENOMRESPONSE']._serialized_end = 753
    _globals['_QUERYGETPROTOREVALLPROFITSREQUEST']._serialized_start = 755
    _globals['_QUERYGETPROTOREVALLPROFITSREQUEST']._serialized_end = 790
    _globals['_QUERYGETPROTOREVALLPROFITSRESPONSE']._serialized_start = 792
    _globals['_QUERYGETPROTOREVALLPROFITSRESPONSE']._serialized_end = 896
    _globals['_QUERYGETPROTOREVSTATISTICSBYROUTEREQUEST']._serialized_start = 898
    _globals['_QUERYGETPROTOREVSTATISTICSBYROUTEREQUEST']._serialized_end = 973
    _globals['_QUERYGETPROTOREVSTATISTICSBYROUTERESPONSE']._serialized_start = 976
    _globals['_QUERYGETPROTOREVSTATISTICSBYROUTERESPONSE']._serialized_end = 1109
    _globals['_QUERYGETPROTOREVALLROUTESTATISTICSREQUEST']._serialized_start = 1111
    _globals['_QUERYGETPROTOREVALLROUTESTATISTICSREQUEST']._serialized_end = 1154
    _globals['_QUERYGETPROTOREVALLROUTESTATISTICSRESPONSE']._serialized_start = 1157
    _globals['_QUERYGETPROTOREVALLROUTESTATISTICSRESPONSE']._serialized_end = 1291
    _globals['_QUERYGETPROTOREVTOKENPAIRARBROUTESREQUEST']._serialized_start = 1293
    _globals['_QUERYGETPROTOREVTOKENPAIRARBROUTESREQUEST']._serialized_end = 1336
    _globals['_QUERYGETPROTOREVTOKENPAIRARBROUTESRESPONSE']._serialized_start = 1339
    _globals['_QUERYGETPROTOREVTOKENPAIRARBROUTESRESPONSE']._serialized_end = 1468
    _globals['_QUERYGETPROTOREVADMINACCOUNTREQUEST']._serialized_start = 1470
    _globals['_QUERYGETPROTOREVADMINACCOUNTREQUEST']._serialized_end = 1507
    _globals['_QUERYGETPROTOREVADMINACCOUNTRESPONSE']._serialized_start = 1509
    _globals['_QUERYGETPROTOREVADMINACCOUNTRESPONSE']._serialized_end = 1596
    _globals['_QUERYGETPROTOREVDEVELOPERACCOUNTREQUEST']._serialized_start = 1598
    _globals['_QUERYGETPROTOREVDEVELOPERACCOUNTREQUEST']._serialized_end = 1639
    _globals['_QUERYGETPROTOREVDEVELOPERACCOUNTRESPONSE']._serialized_start = 1641
    _globals['_QUERYGETPROTOREVDEVELOPERACCOUNTRESPONSE']._serialized_end = 1740
    _globals['_QUERYGETPROTOREVPOOLWEIGHTSREQUEST']._serialized_start = 1742
    _globals['_QUERYGETPROTOREVPOOLWEIGHTSREQUEST']._serialized_end = 1778
    _globals['_QUERYGETPROTOREVPOOLWEIGHTSRESPONSE']._serialized_start = 1780
    _globals['_QUERYGETPROTOREVPOOLWEIGHTSRESPONSE']._serialized_end = 1907
    _globals['_QUERYGETPROTOREVMAXPOOLPOINTSPERBLOCKREQUEST']._serialized_start = 1909
    _globals['_QUERYGETPROTOREVMAXPOOLPOINTSPERBLOCKREQUEST']._serialized_end = 1955
    _globals['_QUERYGETPROTOREVMAXPOOLPOINTSPERBLOCKRESPONSE']._serialized_start = 1957
    _globals['_QUERYGETPROTOREVMAXPOOLPOINTSPERBLOCKRESPONSE']._serialized_end = 2077
    _globals['_QUERYGETPROTOREVMAXPOOLPOINTSPERTXREQUEST']._serialized_start = 2079
    _globals['_QUERYGETPROTOREVMAXPOOLPOINTSPERTXREQUEST']._serialized_end = 2122
    _globals['_QUERYGETPROTOREVMAXPOOLPOINTSPERTXRESPONSE']._serialized_start = 2124
    _globals['_QUERYGETPROTOREVMAXPOOLPOINTSPERTXRESPONSE']._serialized_end = 2235
    _globals['_QUERYGETPROTOREVBASEDENOMSREQUEST']._serialized_start = 2237
    _globals['_QUERYGETPROTOREVBASEDENOMSREQUEST']._serialized_end = 2272
    _globals['_QUERYGETPROTOREVBASEDENOMSRESPONSE']._serialized_start = 2274
    _globals['_QUERYGETPROTOREVBASEDENOMSRESPONSE']._serialized_end = 2396
    _globals['_QUERYGETPROTOREVENABLEDREQUEST']._serialized_start = 2398
    _globals['_QUERYGETPROTOREVENABLEDREQUEST']._serialized_end = 2430
    _globals['_QUERYGETPROTOREVENABLEDRESPONSE']._serialized_start = 2432
    _globals['_QUERYGETPROTOREVENABLEDRESPONSE']._serialized_end = 2502
    _globals['_QUERYGETPROTOREVPOOLREQUEST']._serialized_start = 2504
    _globals['_QUERYGETPROTOREVPOOLREQUEST']._serialized_end = 2621
    _globals['_QUERYGETPROTOREVPOOLRESPONSE']._serialized_start = 2623
    _globals['_QUERYGETPROTOREVPOOLRESPONSE']._serialized_end = 2690
    _globals['_QUERY']._serialized_start = 2693
    _globals['_QUERY']._serialized_end = 5740