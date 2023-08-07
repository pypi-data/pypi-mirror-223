"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....osmosis.poolmanager.v1beta1 import genesis_pb2 as osmosis_dot_poolmanager_dot_v1beta1_dot_genesis__pb2
from ....osmosis.poolmanager.v1beta1 import tx_pb2 as osmosis_dot_poolmanager_dot_v1beta1_dot_tx__pb2
from ....osmosis.poolmanager.v1beta1 import swap_route_pb2 as osmosis_dot_poolmanager_dot_v1beta1_dot_swap__route__pb2
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'osmosis/poolmanager/v1beta1/query.proto\x12\x1bosmosis.poolmanager.v1beta1\x1a\x14gogoproto/gogo.proto\x1a)osmosis/poolmanager/v1beta1/genesis.proto\x1a$osmosis/poolmanager/v1beta1/tx.proto\x1a,osmosis/poolmanager/v1beta1/swap_route.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x19google/protobuf/any.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x0f\n\rParamsRequest"K\n\x0eParamsResponse\x129\n\x06params\x18\x01 \x01(\x0b2#.osmosis.poolmanager.v1beta1.ParamsB\x04\xc8\xde\x1f\x00"\xd3\x01\n EstimateSwapExactAmountInRequest\x12#\n\x07pool_id\x18\x02 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12%\n\x08token_in\x18\x03 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:"token_in"\x12U\n\x06routes\x18\x04 \x03(\x0b2..osmosis.poolmanager.v1beta1.SwapAmountInRouteB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"routes"J\x04\x08\x01\x10\x02R\x06sender"\xad\x01\n*EstimateSinglePoolSwapExactAmountInRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12%\n\x08token_in\x18\x02 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:"token_in"\x123\n\x0ftoken_out_denom\x18\x03 \x01(\tB\x1a\xf2\xde\x1f\x16yaml:"token_out_denom""\x88\x01\n!EstimateSwapExactAmountInResponse\x12c\n\x10token_out_amount\x18\x01 \x01(\tBI\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x17yaml:"token_out_amount""\xd7\x01\n!EstimateSwapExactAmountOutRequest\x12#\n\x07pool_id\x18\x02 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12V\n\x06routes\x18\x03 \x03(\x0b2/.osmosis.poolmanager.v1beta1.SwapAmountOutRouteB\x15\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"routes"\x12\'\n\ttoken_out\x18\x04 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"token_out"J\x04\x08\x01\x10\x02R\x06sender"\xae\x01\n+EstimateSinglePoolSwapExactAmountOutRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x121\n\x0etoken_in_denom\x18\x02 \x01(\tB\x19\xf2\xde\x1f\x15yaml:"token_in_denom"\x12\'\n\ttoken_out\x18\x03 \x01(\tB\x14\xf2\xde\x1f\x10yaml:"token_out""\x87\x01\n"EstimateSwapExactAmountOutResponse\x12a\n\x0ftoken_in_amount\x18\x01 \x01(\tBH\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x16yaml:"token_in_amount""\x11\n\x0fNumPoolsRequest";\n\x10NumPoolsResponse\x12\'\n\tnum_pools\x18\x01 \x01(\x04B\x14\xf2\xde\x1f\x10yaml:"num_pools""2\n\x0bPoolRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id""=\n\x0cPoolResponse\x12-\n\x04pool\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyB\t\xca\xb4-\x05PoolI"\x11\n\x0fAllPoolsRequest"B\n\x10AllPoolsResponse\x12.\n\x05pools\x18\x01 \x03(\x0b2\x14.google.protobuf.AnyB\t\xca\xb4-\x05PoolI"\xa7\x01\n\x10SpotPriceRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x125\n\x10base_asset_denom\x18\x02 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"base_asset_denom"\x127\n\x11quote_asset_denom\x18\x03 \x01(\tB\x1c\xf2\xde\x1f\x18yaml:"quote_asset_denom"">\n\x11SpotPriceResponse\x12)\n\nspot_price\x18\x01 \x01(\tB\x15\xf2\xde\x1f\x11yaml:"spot_price""@\n\x19TotalPoolLiquidityRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id""\x90\x01\n\x1aTotalPoolLiquidityResponse\x12r\n\tliquidity\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBD\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"liquidity"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins"\x17\n\x15TotalLiquidityRequest"\x8c\x01\n\x16TotalLiquidityResponse\x12r\n\tliquidity\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBD\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"liquidity"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins2\x85\x11\n\x05Query\x12\x8e\x01\n\x06Params\x12*.osmosis.poolmanager.v1beta1.ParamsRequest\x1a+.osmosis.poolmanager.v1beta1.ParamsResponse"+\x82\xd3\xe4\x93\x02%\x12#/osmosis/poolmanager/v1beta1/Params\x12\xe8\x01\n\x19EstimateSwapExactAmountIn\x12=.osmosis.poolmanager.v1beta1.EstimateSwapExactAmountInRequest\x1a>.osmosis.poolmanager.v1beta1.EstimateSwapExactAmountInResponse"L\x82\xd3\xe4\x93\x02F\x12D/osmosis/poolmanager/v1beta1/{pool_id}/estimate/swap_exact_amount_in\x12\x88\x02\n#EstimateSinglePoolSwapExactAmountIn\x12G.osmosis.poolmanager.v1beta1.EstimateSinglePoolSwapExactAmountInRequest\x1a>.osmosis.poolmanager.v1beta1.EstimateSwapExactAmountInResponse"X\x82\xd3\xe4\x93\x02R\x12P/osmosis/poolmanager/v1beta1/{pool_id}/estimate/single_pool_swap_exact_amount_in\x12\xec\x01\n\x1aEstimateSwapExactAmountOut\x12>.osmosis.poolmanager.v1beta1.EstimateSwapExactAmountOutRequest\x1a?.osmosis.poolmanager.v1beta1.EstimateSwapExactAmountOutResponse"M\x82\xd3\xe4\x93\x02G\x12E/osmosis/poolmanager/v1beta1/{pool_id}/estimate/swap_exact_amount_out\x12\x90\x02\n$EstimateSinglePoolSwapExactAmountOut\x12H.osmosis.poolmanager.v1beta1.EstimateSinglePoolSwapExactAmountOutRequest\x1a?.osmosis.poolmanager.v1beta1.EstimateSwapExactAmountOutResponse"]\x82\xd3\xe4\x93\x02W\x12U/osmosis/poolmanager/v1beta1/{pool_id}/estimate_out/single_pool_swap_exact_amount_out\x12\x97\x01\n\x08NumPools\x12,.osmosis.poolmanager.v1beta1.NumPoolsRequest\x1a-.osmosis.poolmanager.v1beta1.NumPoolsResponse".\x82\xd3\xe4\x93\x02(\x12&/osmosis/poolmanager/v1beta1/num_pools\x12\x91\x01\n\x04Pool\x12(.osmosis.poolmanager.v1beta1.PoolRequest\x1a).osmosis.poolmanager.v1beta1.PoolResponse"4\x82\xd3\xe4\x93\x02.\x12,/osmosis/poolmanager/v1beta1/pools/{pool_id}\x12\x97\x01\n\x08AllPools\x12,.osmosis.poolmanager.v1beta1.AllPoolsRequest\x1a-.osmosis.poolmanager.v1beta1.AllPoolsResponse".\x82\xd3\xe4\x93\x02(\x12&/osmosis/poolmanager/v1beta1/all-pools\x12\x9f\x01\n\tSpotPrice\x12-.osmosis.poolmanager.v1beta1.SpotPriceRequest\x1a..osmosis.poolmanager.v1beta1.SpotPriceResponse"3\x82\xd3\xe4\x93\x02-\x12+/osmosis/poolmanager/pools/{pool_id}/prices\x12\xd0\x01\n\x12TotalPoolLiquidity\x126.osmosis.poolmanager.v1beta1.TotalPoolLiquidityRequest\x1a7.osmosis.poolmanager.v1beta1.TotalPoolLiquidityResponse"I\x82\xd3\xe4\x93\x02C\x12A/osmosis/poolmanager/v1beta1/pools/{pool_id}/total_pool_liquidity\x12\xb5\x01\n\x0eTotalLiquidity\x122.osmosis.poolmanager.v1beta1.TotalLiquidityRequest\x1a3.osmosis.poolmanager.v1beta1.TotalLiquidityResponse":\x82\xd3\xe4\x93\x024\x122/osmosis/poolmanager/v1beta1/pools/total_liquidityBEZCgithub.com/osmosis-labs/osmosis/v16/x/poolmanager/client/queryprotob\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.poolmanager.v1beta1.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZCgithub.com/osmosis-labs/osmosis/v16/x/poolmanager/client/queryproto'
    _PARAMSRESPONSE.fields_by_name['params']._options = None
    _PARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _ESTIMATESWAPEXACTAMOUNTINREQUEST.fields_by_name['pool_id']._options = None
    _ESTIMATESWAPEXACTAMOUNTINREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _ESTIMATESWAPEXACTAMOUNTINREQUEST.fields_by_name['token_in']._options = None
    _ESTIMATESWAPEXACTAMOUNTINREQUEST.fields_by_name['token_in']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"token_in"'
    _ESTIMATESWAPEXACTAMOUNTINREQUEST.fields_by_name['routes']._options = None
    _ESTIMATESWAPEXACTAMOUNTINREQUEST.fields_by_name['routes']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"routes"'
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTINREQUEST.fields_by_name['pool_id']._options = None
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTINREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTINREQUEST.fields_by_name['token_in']._options = None
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTINREQUEST.fields_by_name['token_in']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"token_in"'
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTINREQUEST.fields_by_name['token_out_denom']._options = None
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTINREQUEST.fields_by_name['token_out_denom']._serialized_options = b'\xf2\xde\x1f\x16yaml:"token_out_denom"'
    _ESTIMATESWAPEXACTAMOUNTINRESPONSE.fields_by_name['token_out_amount']._options = None
    _ESTIMATESWAPEXACTAMOUNTINRESPONSE.fields_by_name['token_out_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x17yaml:"token_out_amount"'
    _ESTIMATESWAPEXACTAMOUNTOUTREQUEST.fields_by_name['pool_id']._options = None
    _ESTIMATESWAPEXACTAMOUNTOUTREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _ESTIMATESWAPEXACTAMOUNTOUTREQUEST.fields_by_name['routes']._options = None
    _ESTIMATESWAPEXACTAMOUNTOUTREQUEST.fields_by_name['routes']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\ryaml:"routes"'
    _ESTIMATESWAPEXACTAMOUNTOUTREQUEST.fields_by_name['token_out']._options = None
    _ESTIMATESWAPEXACTAMOUNTOUTREQUEST.fields_by_name['token_out']._serialized_options = b'\xf2\xde\x1f\x10yaml:"token_out"'
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTOUTREQUEST.fields_by_name['pool_id']._options = None
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTOUTREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTOUTREQUEST.fields_by_name['token_in_denom']._options = None
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTOUTREQUEST.fields_by_name['token_in_denom']._serialized_options = b'\xf2\xde\x1f\x15yaml:"token_in_denom"'
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTOUTREQUEST.fields_by_name['token_out']._options = None
    _ESTIMATESINGLEPOOLSWAPEXACTAMOUNTOUTREQUEST.fields_by_name['token_out']._serialized_options = b'\xf2\xde\x1f\x10yaml:"token_out"'
    _ESTIMATESWAPEXACTAMOUNTOUTRESPONSE.fields_by_name['token_in_amount']._options = None
    _ESTIMATESWAPEXACTAMOUNTOUTRESPONSE.fields_by_name['token_in_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x16yaml:"token_in_amount"'
    _NUMPOOLSRESPONSE.fields_by_name['num_pools']._options = None
    _NUMPOOLSRESPONSE.fields_by_name['num_pools']._serialized_options = b'\xf2\xde\x1f\x10yaml:"num_pools"'
    _POOLREQUEST.fields_by_name['pool_id']._options = None
    _POOLREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _POOLRESPONSE.fields_by_name['pool']._options = None
    _POOLRESPONSE.fields_by_name['pool']._serialized_options = b'\xca\xb4-\x05PoolI'
    _ALLPOOLSRESPONSE.fields_by_name['pools']._options = None
    _ALLPOOLSRESPONSE.fields_by_name['pools']._serialized_options = b'\xca\xb4-\x05PoolI'
    _SPOTPRICEREQUEST.fields_by_name['pool_id']._options = None
    _SPOTPRICEREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _SPOTPRICEREQUEST.fields_by_name['base_asset_denom']._options = None
    _SPOTPRICEREQUEST.fields_by_name['base_asset_denom']._serialized_options = b'\xf2\xde\x1f\x17yaml:"base_asset_denom"'
    _SPOTPRICEREQUEST.fields_by_name['quote_asset_denom']._options = None
    _SPOTPRICEREQUEST.fields_by_name['quote_asset_denom']._serialized_options = b'\xf2\xde\x1f\x18yaml:"quote_asset_denom"'
    _SPOTPRICERESPONSE.fields_by_name['spot_price']._options = None
    _SPOTPRICERESPONSE.fields_by_name['spot_price']._serialized_options = b'\xf2\xde\x1f\x11yaml:"spot_price"'
    _TOTALPOOLLIQUIDITYREQUEST.fields_by_name['pool_id']._options = None
    _TOTALPOOLLIQUIDITYREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _TOTALPOOLLIQUIDITYRESPONSE.fields_by_name['liquidity']._options = None
    _TOTALPOOLLIQUIDITYRESPONSE.fields_by_name['liquidity']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"liquidity"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _TOTALLIQUIDITYRESPONSE.fields_by_name['liquidity']._options = None
    _TOTALLIQUIDITYRESPONSE.fields_by_name['liquidity']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x10yaml:"liquidity"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02%\x12#/osmosis/poolmanager/v1beta1/Params'
    _QUERY.methods_by_name['EstimateSwapExactAmountIn']._options = None
    _QUERY.methods_by_name['EstimateSwapExactAmountIn']._serialized_options = b'\x82\xd3\xe4\x93\x02F\x12D/osmosis/poolmanager/v1beta1/{pool_id}/estimate/swap_exact_amount_in'
    _QUERY.methods_by_name['EstimateSinglePoolSwapExactAmountIn']._options = None
    _QUERY.methods_by_name['EstimateSinglePoolSwapExactAmountIn']._serialized_options = b'\x82\xd3\xe4\x93\x02R\x12P/osmosis/poolmanager/v1beta1/{pool_id}/estimate/single_pool_swap_exact_amount_in'
    _QUERY.methods_by_name['EstimateSwapExactAmountOut']._options = None
    _QUERY.methods_by_name['EstimateSwapExactAmountOut']._serialized_options = b'\x82\xd3\xe4\x93\x02G\x12E/osmosis/poolmanager/v1beta1/{pool_id}/estimate/swap_exact_amount_out'
    _QUERY.methods_by_name['EstimateSinglePoolSwapExactAmountOut']._options = None
    _QUERY.methods_by_name['EstimateSinglePoolSwapExactAmountOut']._serialized_options = b'\x82\xd3\xe4\x93\x02W\x12U/osmosis/poolmanager/v1beta1/{pool_id}/estimate_out/single_pool_swap_exact_amount_out'
    _QUERY.methods_by_name['NumPools']._options = None
    _QUERY.methods_by_name['NumPools']._serialized_options = b'\x82\xd3\xe4\x93\x02(\x12&/osmosis/poolmanager/v1beta1/num_pools'
    _QUERY.methods_by_name['Pool']._options = None
    _QUERY.methods_by_name['Pool']._serialized_options = b'\x82\xd3\xe4\x93\x02.\x12,/osmosis/poolmanager/v1beta1/pools/{pool_id}'
    _QUERY.methods_by_name['AllPools']._options = None
    _QUERY.methods_by_name['AllPools']._serialized_options = b'\x82\xd3\xe4\x93\x02(\x12&/osmosis/poolmanager/v1beta1/all-pools'
    _QUERY.methods_by_name['SpotPrice']._options = None
    _QUERY.methods_by_name['SpotPrice']._serialized_options = b'\x82\xd3\xe4\x93\x02-\x12+/osmosis/poolmanager/pools/{pool_id}/prices'
    _QUERY.methods_by_name['TotalPoolLiquidity']._options = None
    _QUERY.methods_by_name['TotalPoolLiquidity']._serialized_options = b'\x82\xd3\xe4\x93\x02C\x12A/osmosis/poolmanager/v1beta1/pools/{pool_id}/total_pool_liquidity'
    _QUERY.methods_by_name['TotalLiquidity']._options = None
    _QUERY.methods_by_name['TotalLiquidity']._serialized_options = b'\x82\xd3\xe4\x93\x024\x122/osmosis/poolmanager/v1beta1/pools/total_liquidity'
    _globals['_PARAMSREQUEST']._serialized_start = 414
    _globals['_PARAMSREQUEST']._serialized_end = 429
    _globals['_PARAMSRESPONSE']._serialized_start = 431
    _globals['_PARAMSRESPONSE']._serialized_end = 506
    _globals['_ESTIMATESWAPEXACTAMOUNTINREQUEST']._serialized_start = 509
    _globals['_ESTIMATESWAPEXACTAMOUNTINREQUEST']._serialized_end = 720
    _globals['_ESTIMATESINGLEPOOLSWAPEXACTAMOUNTINREQUEST']._serialized_start = 723
    _globals['_ESTIMATESINGLEPOOLSWAPEXACTAMOUNTINREQUEST']._serialized_end = 896
    _globals['_ESTIMATESWAPEXACTAMOUNTINRESPONSE']._serialized_start = 899
    _globals['_ESTIMATESWAPEXACTAMOUNTINRESPONSE']._serialized_end = 1035
    _globals['_ESTIMATESWAPEXACTAMOUNTOUTREQUEST']._serialized_start = 1038
    _globals['_ESTIMATESWAPEXACTAMOUNTOUTREQUEST']._serialized_end = 1253
    _globals['_ESTIMATESINGLEPOOLSWAPEXACTAMOUNTOUTREQUEST']._serialized_start = 1256
    _globals['_ESTIMATESINGLEPOOLSWAPEXACTAMOUNTOUTREQUEST']._serialized_end = 1430
    _globals['_ESTIMATESWAPEXACTAMOUNTOUTRESPONSE']._serialized_start = 1433
    _globals['_ESTIMATESWAPEXACTAMOUNTOUTRESPONSE']._serialized_end = 1568
    _globals['_NUMPOOLSREQUEST']._serialized_start = 1570
    _globals['_NUMPOOLSREQUEST']._serialized_end = 1587
    _globals['_NUMPOOLSRESPONSE']._serialized_start = 1589
    _globals['_NUMPOOLSRESPONSE']._serialized_end = 1648
    _globals['_POOLREQUEST']._serialized_start = 1650
    _globals['_POOLREQUEST']._serialized_end = 1700
    _globals['_POOLRESPONSE']._serialized_start = 1702
    _globals['_POOLRESPONSE']._serialized_end = 1763
    _globals['_ALLPOOLSREQUEST']._serialized_start = 1765
    _globals['_ALLPOOLSREQUEST']._serialized_end = 1782
    _globals['_ALLPOOLSRESPONSE']._serialized_start = 1784
    _globals['_ALLPOOLSRESPONSE']._serialized_end = 1850
    _globals['_SPOTPRICEREQUEST']._serialized_start = 1853
    _globals['_SPOTPRICEREQUEST']._serialized_end = 2020
    _globals['_SPOTPRICERESPONSE']._serialized_start = 2022
    _globals['_SPOTPRICERESPONSE']._serialized_end = 2084
    _globals['_TOTALPOOLLIQUIDITYREQUEST']._serialized_start = 2086
    _globals['_TOTALPOOLLIQUIDITYREQUEST']._serialized_end = 2150
    _globals['_TOTALPOOLLIQUIDITYRESPONSE']._serialized_start = 2153
    _globals['_TOTALPOOLLIQUIDITYRESPONSE']._serialized_end = 2297
    _globals['_TOTALLIQUIDITYREQUEST']._serialized_start = 2299
    _globals['_TOTALLIQUIDITYREQUEST']._serialized_end = 2322
    _globals['_TOTALLIQUIDITYRESPONSE']._serialized_start = 2325
    _globals['_TOTALLIQUIDITYRESPONSE']._serialized_end = 2465
    _globals['_QUERY']._serialized_start = 2468
    _globals['_QUERY']._serialized_end = 4649