"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ...osmosis.concentrated_liquidity import params_pb2 as osmosis_dot_concentrated__liquidity_dot_params__pb2
from ...osmosis.concentrated_liquidity import tickInfo_pb2 as osmosis_dot_concentrated__liquidity_dot_tickInfo__pb2
from ...cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ...cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ...google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ...cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ...osmosis.concentrated_liquidity import position_pb2 as osmosis_dot_concentrated__liquidity_dot_position__pb2
from ...osmosis.concentrated_liquidity import incentive_record_pb2 as osmosis_dot_concentrated__liquidity_dot_incentive__record__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*osmosis/concentrated-liquidity/query.proto\x12%osmosis.concentratedliquidity.v1beta1\x1a\x14gogoproto/gogo.proto\x1a+osmosis/concentrated-liquidity/params.proto\x1a-osmosis/concentrated-liquidity/tickInfo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x19google/protobuf/any.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a-osmosis/concentrated-liquidity/position.proto\x1a5osmosis/concentrated-liquidity/incentive_record.proto"\x9c\x01\n\x14UserPositionsRequest\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12#\n\x07pool_id\x18\x02 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12:\n\npagination\x18\x03 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\xab\x01\n\x15UserPositionsResponse\x12U\n\tpositions\x18\x01 \x03(\x0b2<.osmosis.concentratedliquidity.v1beta1.FullPositionBreakdownB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"B\n\x13PositionByIdRequest\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id""l\n\x14PositionByIdResponse\x12T\n\x08position\x18\x01 \x01(\x0b2<.osmosis.concentratedliquidity.v1beta1.FullPositionBreakdownB\x04\xc8\xde\x1f\x00"J\n\x0cPoolsRequest\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"|\n\rPoolsResponse\x12.\n\x05pools\x18\x01 \x03(\x0b2\x14.google.protobuf.AnyB\t\xca\xb4-\x05PoolI\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"\x0f\n\rParamsRequest"M\n\x0eParamsResponse\x12;\n\x06params\x18\x01 \x01(\x0b2%.osmosis.concentratedliquidity.ParamsB\x04\xc8\xde\x1f\x00"\x9c\x01\n\x10TickLiquidityNet\x12]\n\rliquidity_net\x18\x01 \x01(\tBF\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"liquidity_net"\x12)\n\ntick_index\x18\x02 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"tick_index""\xd1\x01\n\x17LiquidityDepthWithRange\x12`\n\x10liquidity_amount\x18\x01 \x01(\tBF\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"liquidity_net"\x12)\n\nlower_tick\x18\x02 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"lower_tick"\x12)\n\nupper_tick\x18\x03 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"upper_tick""\xa0\x02\n\x1eLiquidityNetInDirectionRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12%\n\x08token_in\x18\x02 \x01(\tB\x13\xf2\xde\x1f\x0fyaml:"token_in"\x12)\n\nstart_tick\x18\x03 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"start_tick"\x12-\n\x0cuse_cur_tick\x18\x04 \x01(\x08B\x17\xf2\xde\x1f\x13yaml:"use_cur_tick"\x12)\n\nbound_tick\x18\x05 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"bound_tick"\x12-\n\x0cuse_no_bound\x18\x06 \x01(\x08B\x17\xf2\xde\x1f\x13yaml:"use_no_bound""\xf7\x01\n\x1fLiquidityNetInDirectionResponse\x12W\n\x10liquidity_depths\x18\x01 \x03(\x0b27.osmosis.concentratedliquidity.v1beta1.TickLiquidityNetB\x04\xc8\xde\x1f\x00\x12\x14\n\x0ccurrent_tick\x18\x02 \x01(\x03\x12e\n\x11current_liquidity\x18\x03 \x01(\tBJ\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x18yaml:"current_liquidity""C\n\x1cLiquidityPerTickRangeRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id""x\n\x1dLiquidityPerTickRangeResponse\x12W\n\tliquidity\x18\x01 \x03(\x0b2>.osmosis.concentratedliquidity.v1beta1.LiquidityDepthWithRangeB\x04\xc8\xde\x1f\x00"L\n\x1dClaimableSpreadRewardsRequest\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id""\x86\x01\n\x1eClaimableSpreadRewardsResponse\x12d\n\x18claimable_spread_rewards\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\'\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"claimable_spread_rewards""I\n\x1aClaimableIncentivesRequest\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id""\xd9\x01\n\x1bClaimableIncentivesResponse\x12\\\n\x14claimable_incentives\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB#\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"claimable_incentives"\x12\\\n\x14forfeited_incentives\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB#\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"forfeited_incentives""D\n\x1dPoolAccumulatorRewardsRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id""\x91\x02\n\x1ePoolAccumulatorRewardsResponse\x12v\n\x1bspread_reward_growth_global\x18\x01 \x03(\x0b2\x1c.cosmos.base.v1beta1.DecCoinB3\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins\x12w\n\x14uptime_growth_global\x18\x02 \x03(\x0b24.osmosis.concentratedliquidity.v1beta1.UptimeTrackerB#\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"uptime_growth_global""p\n\x1eTickAccumulatorTrackersRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12)\n\ntick_index\x18\x02 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"tick_index""\xa7\x02\n\x1fTickAccumulatorTrackersResponse\x12\x94\x01\n9spread_reward_growth_opposite_direction_of_last_traversal\x18\x01 \x03(\x0b2\x1c.cosmos.base.v1beta1.DecCoinB3\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins\x12m\n\x0fuptime_trackers\x18\x02 \x03(\x0b24.osmosis.concentratedliquidity.v1beta1.UptimeTrackerB\x1e\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"uptime_trackers""z\n\x17IncentiveRecordsRequest\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12:\n\npagination\x18\x02 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"\xb0\x01\n\x18IncentiveRecordsResponse\x12W\n\x11incentive_records\x18\x01 \x03(\x0b26.osmosis.concentratedliquidity.v1beta1.IncentiveRecordB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"l\n+CFMMPoolIdLinkFromConcentratedPoolIdRequest\x12=\n\x14concentrated_pool_id\x18\x01 \x01(\x04B\x1f\xf2\xde\x1f\x1byaml:"concentrated_pool_id""]\n,CFMMPoolIdLinkFromConcentratedPoolIdResponse\x12-\n\x0ccfmm_pool_id\x18\x01 \x01(\x04B\x17\xf2\xde\x1f\x13yaml:"cfmm_pool_id""D\n\x1dUserUnbondingPositionsRequest\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address""\x89\x01\n\x1eUserUnbondingPositionsResponse\x12g\n\x1apositions_with_period_lock\x18\x01 \x03(\x0b2=.osmosis.concentratedliquidity.v1beta1.PositionWithPeriodLockB\x04\xc8\xde\x1f\x00"\x1a\n\x18GetTotalLiquidityRequest"\x81\x01\n\x19GetTotalLiquidityResponse\x12d\n\x0ftotal_liquidity\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins2\xfb\x18\n\x05Query\x12\xa8\x01\n\x05Pools\x123.osmosis.concentratedliquidity.v1beta1.PoolsRequest\x1a4.osmosis.concentratedliquidity.v1beta1.PoolsResponse"4\x82\xd3\xe4\x93\x02.\x12,/osmosis/concentratedliquidity/v1beta1/pools\x12\xac\x01\n\x06Params\x124.osmosis.concentratedliquidity.v1beta1.ParamsRequest\x1a5.osmosis.concentratedliquidity.v1beta1.ParamsResponse"5\x82\xd3\xe4\x93\x02/\x12-/osmosis/concentratedliquidity/v1beta1/params\x12\xce\x01\n\rUserPositions\x12;.osmosis.concentratedliquidity.v1beta1.UserPositionsRequest\x1a<.osmosis.concentratedliquidity.v1beta1.UserPositionsResponse"B\x82\xd3\xe4\x93\x02<\x12:/osmosis/concentratedliquidity/v1beta1/positions/{address}\x12\xeb\x01\n\x15LiquidityPerTickRange\x12C.osmosis.concentratedliquidity.v1beta1.LiquidityPerTickRangeRequest\x1aD.osmosis.concentratedliquidity.v1beta1.LiquidityPerTickRangeResponse"G\x82\xd3\xe4\x93\x02A\x12?/osmosis/concentratedliquidity/v1beta1/liquidity_per_tick_range\x12\xf3\x01\n\x17LiquidityNetInDirection\x12E.osmosis.concentratedliquidity.v1beta1.LiquidityNetInDirectionRequest\x1aF.osmosis.concentratedliquidity.v1beta1.LiquidityNetInDirectionResponse"I\x82\xd3\xe4\x93\x02C\x12A/osmosis/concentratedliquidity/v1beta1/liquidity_net_in_direction\x12\xee\x01\n\x16ClaimableSpreadRewards\x12D.osmosis.concentratedliquidity.v1beta1.ClaimableSpreadRewardsRequest\x1aE.osmosis.concentratedliquidity.v1beta1.ClaimableSpreadRewardsResponse"G\x82\xd3\xe4\x93\x02A\x12?/osmosis/concentratedliquidity/v1beta1/claimable_spread_rewards\x12\xe1\x01\n\x13ClaimableIncentives\x12A.osmosis.concentratedliquidity.v1beta1.ClaimableIncentivesRequest\x1aB.osmosis.concentratedliquidity.v1beta1.ClaimableIncentivesResponse"C\x82\xd3\xe4\x93\x02=\x12;/osmosis/concentratedliquidity/v1beta1/claimable_incentives\x12\xc6\x01\n\x0cPositionById\x12:.osmosis.concentratedliquidity.v1beta1.PositionByIdRequest\x1a;.osmosis.concentratedliquidity.v1beta1.PositionByIdResponse"=\x82\xd3\xe4\x93\x027\x125/osmosis/concentratedliquidity/v1beta1/position_by_id\x12\xe8\x01\n\x16PoolAccumulatorRewards\x12D.osmosis.concentratedliquidity.v1beta1.PoolAccumulatorRewardsRequest\x1aE.osmosis.concentratedliquidity.v1beta1.PoolAccumulatorRewardsResponse"A\x82\xd3\xe4\x93\x02;\x129/osmosis/concentratedliquidity/v1beta1/pool_accum_rewards\x12\xd5\x01\n\x10IncentiveRecords\x12>.osmosis.concentratedliquidity.v1beta1.IncentiveRecordsRequest\x1a?.osmosis.concentratedliquidity.v1beta1.IncentiveRecordsResponse"@\x82\xd3\xe4\x93\x02:\x128/osmosis/concentratedliquidity/v1beta1/incentive_records\x12\xec\x01\n\x17TickAccumulatorTrackers\x12E.osmosis.concentratedliquidity.v1beta1.TickAccumulatorTrackersRequest\x1aF.osmosis.concentratedliquidity.v1beta1.TickAccumulatorTrackersResponse"B\x82\xd3\xe4\x93\x02<\x12:/osmosis/concentratedliquidity/v1beta1/tick_accum_trackers\x12\xba\x02\n$CFMMPoolIdLinkFromConcentratedPoolId\x12R.osmosis.concentratedliquidity.v1beta1.CFMMPoolIdLinkFromConcentratedPoolIdRequest\x1aS.osmosis.concentratedliquidity.v1beta1.CFMMPoolIdLinkFromConcentratedPoolIdResponse"i\x82\xd3\xe4\x93\x02c\x12a/osmosis/concentratedliquidity/v1beta1/cfmm_pool_id_link_from_concentrated/{concentrated_pool_id}\x12\xf8\x01\n\x16UserUnbondingPositions\x12D.osmosis.concentratedliquidity.v1beta1.UserUnbondingPositionsRequest\x1aE.osmosis.concentratedliquidity.v1beta1.UserUnbondingPositionsResponse"Q\x82\xd3\xe4\x93\x02K\x12I/osmosis/concentratedliquidity/v1beta1/user_unbonding_positions/{address}\x12\xda\x01\n\x11GetTotalLiquidity\x12?.osmosis.concentratedliquidity.v1beta1.GetTotalLiquidityRequest\x1a@.osmosis.concentratedliquidity.v1beta1.GetTotalLiquidityResponse"B\x82\xd3\xe4\x93\x02<\x12:/osmosis/concentratedliquidity/v1beta1/get_total_liquidityBPZNgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/client/queryprotob\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.concentrated_liquidity.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZNgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/client/queryproto'
    _USERPOSITIONSREQUEST.fields_by_name['address']._options = None
    _USERPOSITIONSREQUEST.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _USERPOSITIONSREQUEST.fields_by_name['pool_id']._options = None
    _USERPOSITIONSREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _USERPOSITIONSRESPONSE.fields_by_name['positions']._options = None
    _USERPOSITIONSRESPONSE.fields_by_name['positions']._serialized_options = b'\xc8\xde\x1f\x00'
    _POSITIONBYIDREQUEST.fields_by_name['position_id']._options = None
    _POSITIONBYIDREQUEST.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _POSITIONBYIDRESPONSE.fields_by_name['position']._options = None
    _POSITIONBYIDRESPONSE.fields_by_name['position']._serialized_options = b'\xc8\xde\x1f\x00'
    _POOLSRESPONSE.fields_by_name['pools']._options = None
    _POOLSRESPONSE.fields_by_name['pools']._serialized_options = b'\xca\xb4-\x05PoolI'
    _PARAMSRESPONSE.fields_by_name['params']._options = None
    _PARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _TICKLIQUIDITYNET.fields_by_name['liquidity_net']._options = None
    _TICKLIQUIDITYNET.fields_by_name['liquidity_net']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"liquidity_net"'
    _TICKLIQUIDITYNET.fields_by_name['tick_index']._options = None
    _TICKLIQUIDITYNET.fields_by_name['tick_index']._serialized_options = b'\xf2\xde\x1f\x11yaml:"tick_index"'
    _LIQUIDITYDEPTHWITHRANGE.fields_by_name['liquidity_amount']._options = None
    _LIQUIDITYDEPTHWITHRANGE.fields_by_name['liquidity_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"liquidity_net"'
    _LIQUIDITYDEPTHWITHRANGE.fields_by_name['lower_tick']._options = None
    _LIQUIDITYDEPTHWITHRANGE.fields_by_name['lower_tick']._serialized_options = b'\xf2\xde\x1f\x11yaml:"lower_tick"'
    _LIQUIDITYDEPTHWITHRANGE.fields_by_name['upper_tick']._options = None
    _LIQUIDITYDEPTHWITHRANGE.fields_by_name['upper_tick']._serialized_options = b'\xf2\xde\x1f\x11yaml:"upper_tick"'
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['pool_id']._options = None
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['token_in']._options = None
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['token_in']._serialized_options = b'\xf2\xde\x1f\x0fyaml:"token_in"'
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['start_tick']._options = None
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['start_tick']._serialized_options = b'\xf2\xde\x1f\x11yaml:"start_tick"'
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['use_cur_tick']._options = None
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['use_cur_tick']._serialized_options = b'\xf2\xde\x1f\x13yaml:"use_cur_tick"'
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['bound_tick']._options = None
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['bound_tick']._serialized_options = b'\xf2\xde\x1f\x11yaml:"bound_tick"'
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['use_no_bound']._options = None
    _LIQUIDITYNETINDIRECTIONREQUEST.fields_by_name['use_no_bound']._serialized_options = b'\xf2\xde\x1f\x13yaml:"use_no_bound"'
    _LIQUIDITYNETINDIRECTIONRESPONSE.fields_by_name['liquidity_depths']._options = None
    _LIQUIDITYNETINDIRECTIONRESPONSE.fields_by_name['liquidity_depths']._serialized_options = b'\xc8\xde\x1f\x00'
    _LIQUIDITYNETINDIRECTIONRESPONSE.fields_by_name['current_liquidity']._options = None
    _LIQUIDITYNETINDIRECTIONRESPONSE.fields_by_name['current_liquidity']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x18yaml:"current_liquidity"'
    _LIQUIDITYPERTICKRANGEREQUEST.fields_by_name['pool_id']._options = None
    _LIQUIDITYPERTICKRANGEREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _LIQUIDITYPERTICKRANGERESPONSE.fields_by_name['liquidity']._options = None
    _LIQUIDITYPERTICKRANGERESPONSE.fields_by_name['liquidity']._serialized_options = b'\xc8\xde\x1f\x00'
    _CLAIMABLESPREADREWARDSREQUEST.fields_by_name['position_id']._options = None
    _CLAIMABLESPREADREWARDSREQUEST.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _CLAIMABLESPREADREWARDSRESPONSE.fields_by_name['claimable_spread_rewards']._options = None
    _CLAIMABLESPREADREWARDSRESPONSE.fields_by_name['claimable_spread_rewards']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"claimable_spread_rewards"'
    _CLAIMABLEINCENTIVESREQUEST.fields_by_name['position_id']._options = None
    _CLAIMABLEINCENTIVESREQUEST.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _CLAIMABLEINCENTIVESRESPONSE.fields_by_name['claimable_incentives']._options = None
    _CLAIMABLEINCENTIVESRESPONSE.fields_by_name['claimable_incentives']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"claimable_incentives"'
    _CLAIMABLEINCENTIVESRESPONSE.fields_by_name['forfeited_incentives']._options = None
    _CLAIMABLEINCENTIVESRESPONSE.fields_by_name['forfeited_incentives']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"forfeited_incentives"'
    _POOLACCUMULATORREWARDSREQUEST.fields_by_name['pool_id']._options = None
    _POOLACCUMULATORREWARDSREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _POOLACCUMULATORREWARDSRESPONSE.fields_by_name['spread_reward_growth_global']._options = None
    _POOLACCUMULATORREWARDSRESPONSE.fields_by_name['spread_reward_growth_global']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins'
    _POOLACCUMULATORREWARDSRESPONSE.fields_by_name['uptime_growth_global']._options = None
    _POOLACCUMULATORREWARDSRESPONSE.fields_by_name['uptime_growth_global']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"uptime_growth_global"'
    _TICKACCUMULATORTRACKERSREQUEST.fields_by_name['pool_id']._options = None
    _TICKACCUMULATORTRACKERSREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _TICKACCUMULATORTRACKERSREQUEST.fields_by_name['tick_index']._options = None
    _TICKACCUMULATORTRACKERSREQUEST.fields_by_name['tick_index']._serialized_options = b'\xf2\xde\x1f\x11yaml:"tick_index"'
    _TICKACCUMULATORTRACKERSRESPONSE.fields_by_name['spread_reward_growth_opposite_direction_of_last_traversal']._options = None
    _TICKACCUMULATORTRACKERSRESPONSE.fields_by_name['spread_reward_growth_opposite_direction_of_last_traversal']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f+github.com/cosmos/cosmos-sdk/types.DecCoins'
    _TICKACCUMULATORTRACKERSRESPONSE.fields_by_name['uptime_trackers']._options = None
    _TICKACCUMULATORTRACKERSRESPONSE.fields_by_name['uptime_trackers']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"uptime_trackers"'
    _INCENTIVERECORDSREQUEST.fields_by_name['pool_id']._options = None
    _INCENTIVERECORDSREQUEST.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _INCENTIVERECORDSRESPONSE.fields_by_name['incentive_records']._options = None
    _INCENTIVERECORDSRESPONSE.fields_by_name['incentive_records']._serialized_options = b'\xc8\xde\x1f\x00'
    _CFMMPOOLIDLINKFROMCONCENTRATEDPOOLIDREQUEST.fields_by_name['concentrated_pool_id']._options = None
    _CFMMPOOLIDLINKFROMCONCENTRATEDPOOLIDREQUEST.fields_by_name['concentrated_pool_id']._serialized_options = b'\xf2\xde\x1f\x1byaml:"concentrated_pool_id"'
    _CFMMPOOLIDLINKFROMCONCENTRATEDPOOLIDRESPONSE.fields_by_name['cfmm_pool_id']._options = None
    _CFMMPOOLIDLINKFROMCONCENTRATEDPOOLIDRESPONSE.fields_by_name['cfmm_pool_id']._serialized_options = b'\xf2\xde\x1f\x13yaml:"cfmm_pool_id"'
    _USERUNBONDINGPOSITIONSREQUEST.fields_by_name['address']._options = None
    _USERUNBONDINGPOSITIONSREQUEST.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _USERUNBONDINGPOSITIONSRESPONSE.fields_by_name['positions_with_period_lock']._options = None
    _USERUNBONDINGPOSITIONSRESPONSE.fields_by_name['positions_with_period_lock']._serialized_options = b'\xc8\xde\x1f\x00'
    _GETTOTALLIQUIDITYRESPONSE.fields_by_name['total_liquidity']._options = None
    _GETTOTALLIQUIDITYRESPONSE.fields_by_name['total_liquidity']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _QUERY.methods_by_name['Pools']._options = None
    _QUERY.methods_by_name['Pools']._serialized_options = b'\x82\xd3\xe4\x93\x02.\x12,/osmosis/concentratedliquidity/v1beta1/pools'
    _QUERY.methods_by_name['Params']._options = None
    _QUERY.methods_by_name['Params']._serialized_options = b'\x82\xd3\xe4\x93\x02/\x12-/osmosis/concentratedliquidity/v1beta1/params'
    _QUERY.methods_by_name['UserPositions']._options = None
    _QUERY.methods_by_name['UserPositions']._serialized_options = b'\x82\xd3\xe4\x93\x02<\x12:/osmosis/concentratedliquidity/v1beta1/positions/{address}'
    _QUERY.methods_by_name['LiquidityPerTickRange']._options = None
    _QUERY.methods_by_name['LiquidityPerTickRange']._serialized_options = b'\x82\xd3\xe4\x93\x02A\x12?/osmosis/concentratedliquidity/v1beta1/liquidity_per_tick_range'
    _QUERY.methods_by_name['LiquidityNetInDirection']._options = None
    _QUERY.methods_by_name['LiquidityNetInDirection']._serialized_options = b'\x82\xd3\xe4\x93\x02C\x12A/osmosis/concentratedliquidity/v1beta1/liquidity_net_in_direction'
    _QUERY.methods_by_name['ClaimableSpreadRewards']._options = None
    _QUERY.methods_by_name['ClaimableSpreadRewards']._serialized_options = b'\x82\xd3\xe4\x93\x02A\x12?/osmosis/concentratedliquidity/v1beta1/claimable_spread_rewards'
    _QUERY.methods_by_name['ClaimableIncentives']._options = None
    _QUERY.methods_by_name['ClaimableIncentives']._serialized_options = b'\x82\xd3\xe4\x93\x02=\x12;/osmosis/concentratedliquidity/v1beta1/claimable_incentives'
    _QUERY.methods_by_name['PositionById']._options = None
    _QUERY.methods_by_name['PositionById']._serialized_options = b'\x82\xd3\xe4\x93\x027\x125/osmosis/concentratedliquidity/v1beta1/position_by_id'
    _QUERY.methods_by_name['PoolAccumulatorRewards']._options = None
    _QUERY.methods_by_name['PoolAccumulatorRewards']._serialized_options = b'\x82\xd3\xe4\x93\x02;\x129/osmosis/concentratedliquidity/v1beta1/pool_accum_rewards'
    _QUERY.methods_by_name['IncentiveRecords']._options = None
    _QUERY.methods_by_name['IncentiveRecords']._serialized_options = b'\x82\xd3\xe4\x93\x02:\x128/osmosis/concentratedliquidity/v1beta1/incentive_records'
    _QUERY.methods_by_name['TickAccumulatorTrackers']._options = None
    _QUERY.methods_by_name['TickAccumulatorTrackers']._serialized_options = b'\x82\xd3\xe4\x93\x02<\x12:/osmosis/concentratedliquidity/v1beta1/tick_accum_trackers'
    _QUERY.methods_by_name['CFMMPoolIdLinkFromConcentratedPoolId']._options = None
    _QUERY.methods_by_name['CFMMPoolIdLinkFromConcentratedPoolId']._serialized_options = b'\x82\xd3\xe4\x93\x02c\x12a/osmosis/concentratedliquidity/v1beta1/cfmm_pool_id_link_from_concentrated/{concentrated_pool_id}'
    _QUERY.methods_by_name['UserUnbondingPositions']._options = None
    _QUERY.methods_by_name['UserUnbondingPositions']._serialized_options = b'\x82\xd3\xe4\x93\x02K\x12I/osmosis/concentratedliquidity/v1beta1/user_unbonding_positions/{address}'
    _QUERY.methods_by_name['GetTotalLiquidity']._options = None
    _QUERY.methods_by_name['GetTotalLiquidity']._serialized_options = b'\x82\xd3\xe4\x93\x02<\x12:/osmosis/concentratedliquidity/v1beta1/get_total_liquidity'
    _globals['_USERPOSITIONSREQUEST']._serialized_start = 527
    _globals['_USERPOSITIONSREQUEST']._serialized_end = 683
    _globals['_USERPOSITIONSRESPONSE']._serialized_start = 686
    _globals['_USERPOSITIONSRESPONSE']._serialized_end = 857
    _globals['_POSITIONBYIDREQUEST']._serialized_start = 859
    _globals['_POSITIONBYIDREQUEST']._serialized_end = 925
    _globals['_POSITIONBYIDRESPONSE']._serialized_start = 927
    _globals['_POSITIONBYIDRESPONSE']._serialized_end = 1035
    _globals['_POOLSREQUEST']._serialized_start = 1037
    _globals['_POOLSREQUEST']._serialized_end = 1111
    _globals['_POOLSRESPONSE']._serialized_start = 1113
    _globals['_POOLSRESPONSE']._serialized_end = 1237
    _globals['_PARAMSREQUEST']._serialized_start = 1239
    _globals['_PARAMSREQUEST']._serialized_end = 1254
    _globals['_PARAMSRESPONSE']._serialized_start = 1256
    _globals['_PARAMSRESPONSE']._serialized_end = 1333
    _globals['_TICKLIQUIDITYNET']._serialized_start = 1336
    _globals['_TICKLIQUIDITYNET']._serialized_end = 1492
    _globals['_LIQUIDITYDEPTHWITHRANGE']._serialized_start = 1495
    _globals['_LIQUIDITYDEPTHWITHRANGE']._serialized_end = 1704
    _globals['_LIQUIDITYNETINDIRECTIONREQUEST']._serialized_start = 1707
    _globals['_LIQUIDITYNETINDIRECTIONREQUEST']._serialized_end = 1995
    _globals['_LIQUIDITYNETINDIRECTIONRESPONSE']._serialized_start = 1998
    _globals['_LIQUIDITYNETINDIRECTIONRESPONSE']._serialized_end = 2245
    _globals['_LIQUIDITYPERTICKRANGEREQUEST']._serialized_start = 2247
    _globals['_LIQUIDITYPERTICKRANGEREQUEST']._serialized_end = 2314
    _globals['_LIQUIDITYPERTICKRANGERESPONSE']._serialized_start = 2316
    _globals['_LIQUIDITYPERTICKRANGERESPONSE']._serialized_end = 2436
    _globals['_CLAIMABLESPREADREWARDSREQUEST']._serialized_start = 2438
    _globals['_CLAIMABLESPREADREWARDSREQUEST']._serialized_end = 2514
    _globals['_CLAIMABLESPREADREWARDSRESPONSE']._serialized_start = 2517
    _globals['_CLAIMABLESPREADREWARDSRESPONSE']._serialized_end = 2651
    _globals['_CLAIMABLEINCENTIVESREQUEST']._serialized_start = 2653
    _globals['_CLAIMABLEINCENTIVESREQUEST']._serialized_end = 2726
    _globals['_CLAIMABLEINCENTIVESRESPONSE']._serialized_start = 2729
    _globals['_CLAIMABLEINCENTIVESRESPONSE']._serialized_end = 2946
    _globals['_POOLACCUMULATORREWARDSREQUEST']._serialized_start = 2948
    _globals['_POOLACCUMULATORREWARDSREQUEST']._serialized_end = 3016
    _globals['_POOLACCUMULATORREWARDSRESPONSE']._serialized_start = 3019
    _globals['_POOLACCUMULATORREWARDSRESPONSE']._serialized_end = 3292
    _globals['_TICKACCUMULATORTRACKERSREQUEST']._serialized_start = 3294
    _globals['_TICKACCUMULATORTRACKERSREQUEST']._serialized_end = 3406
    _globals['_TICKACCUMULATORTRACKERSRESPONSE']._serialized_start = 3409
    _globals['_TICKACCUMULATORTRACKERSRESPONSE']._serialized_end = 3704
    _globals['_INCENTIVERECORDSREQUEST']._serialized_start = 3706
    _globals['_INCENTIVERECORDSREQUEST']._serialized_end = 3828
    _globals['_INCENTIVERECORDSRESPONSE']._serialized_start = 3831
    _globals['_INCENTIVERECORDSRESPONSE']._serialized_end = 4007
    _globals['_CFMMPOOLIDLINKFROMCONCENTRATEDPOOLIDREQUEST']._serialized_start = 4009
    _globals['_CFMMPOOLIDLINKFROMCONCENTRATEDPOOLIDREQUEST']._serialized_end = 4117
    _globals['_CFMMPOOLIDLINKFROMCONCENTRATEDPOOLIDRESPONSE']._serialized_start = 4119
    _globals['_CFMMPOOLIDLINKFROMCONCENTRATEDPOOLIDRESPONSE']._serialized_end = 4212
    _globals['_USERUNBONDINGPOSITIONSREQUEST']._serialized_start = 4214
    _globals['_USERUNBONDINGPOSITIONSREQUEST']._serialized_end = 4282
    _globals['_USERUNBONDINGPOSITIONSRESPONSE']._serialized_start = 4285
    _globals['_USERUNBONDINGPOSITIONSRESPONSE']._serialized_end = 4422
    _globals['_GETTOTALLIQUIDITYREQUEST']._serialized_start = 4424
    _globals['_GETTOTALLIQUIDITYREQUEST']._serialized_end = 4450
    _globals['_GETTOTALLIQUIDITYRESPONSE']._serialized_start = 4453
    _globals['_GETTOTALLIQUIDITYRESPONSE']._serialized_end = 4582
    _globals['_QUERY']._serialized_start = 4585
    _globals['_QUERY']._serialized_end = 7780