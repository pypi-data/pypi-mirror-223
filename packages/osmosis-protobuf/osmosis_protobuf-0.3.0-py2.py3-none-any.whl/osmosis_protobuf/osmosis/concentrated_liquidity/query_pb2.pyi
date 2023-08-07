from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.concentrated_liquidity import params_pb2 as _params_pb2
from osmosis.concentrated_liquidity import tickInfo_pb2 as _tickInfo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from osmosis.concentrated_liquidity import position_pb2 as _position_pb2
from osmosis.concentrated_liquidity import incentive_record_pb2 as _incentive_record_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class UserPositionsRequest(_message.Message):
    __slots__ = ['address', 'pool_id', 'pagination']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    address: str
    pool_id: int
    pagination: _pagination_pb2.PageRequest

    def __init__(self, address: _Optional[str]=..., pool_id: _Optional[int]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class UserPositionsResponse(_message.Message):
    __slots__ = ['positions', 'pagination']
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    positions: _containers.RepeatedCompositeFieldContainer[_position_pb2.FullPositionBreakdown]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, positions: _Optional[_Iterable[_Union[_position_pb2.FullPositionBreakdown, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class PositionByIdRequest(_message.Message):
    __slots__ = ['position_id']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    position_id: int

    def __init__(self, position_id: _Optional[int]=...) -> None:
        ...

class PositionByIdResponse(_message.Message):
    __slots__ = ['position']
    POSITION_FIELD_NUMBER: _ClassVar[int]
    position: _position_pb2.FullPositionBreakdown

    def __init__(self, position: _Optional[_Union[_position_pb2.FullPositionBreakdown, _Mapping]]=...) -> None:
        ...

class PoolsRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class PoolsResponse(_message.Message):
    __slots__ = ['pools', 'pagination']
    POOLS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pools: _containers.RepeatedCompositeFieldContainer[_any_pb2.Any]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, pools: _Optional[_Iterable[_Union[_any_pb2.Any, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class ParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class ParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=...) -> None:
        ...

class TickLiquidityNet(_message.Message):
    __slots__ = ['liquidity_net', 'tick_index']
    LIQUIDITY_NET_FIELD_NUMBER: _ClassVar[int]
    TICK_INDEX_FIELD_NUMBER: _ClassVar[int]
    liquidity_net: str
    tick_index: int

    def __init__(self, liquidity_net: _Optional[str]=..., tick_index: _Optional[int]=...) -> None:
        ...

class LiquidityDepthWithRange(_message.Message):
    __slots__ = ['liquidity_amount', 'lower_tick', 'upper_tick']
    LIQUIDITY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    LOWER_TICK_FIELD_NUMBER: _ClassVar[int]
    UPPER_TICK_FIELD_NUMBER: _ClassVar[int]
    liquidity_amount: str
    lower_tick: int
    upper_tick: int

    def __init__(self, liquidity_amount: _Optional[str]=..., lower_tick: _Optional[int]=..., upper_tick: _Optional[int]=...) -> None:
        ...

class LiquidityNetInDirectionRequest(_message.Message):
    __slots__ = ['pool_id', 'token_in', 'start_tick', 'use_cur_tick', 'bound_tick', 'use_no_bound']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    START_TICK_FIELD_NUMBER: _ClassVar[int]
    USE_CUR_TICK_FIELD_NUMBER: _ClassVar[int]
    BOUND_TICK_FIELD_NUMBER: _ClassVar[int]
    USE_NO_BOUND_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    token_in: str
    start_tick: int
    use_cur_tick: bool
    bound_tick: int
    use_no_bound: bool

    def __init__(self, pool_id: _Optional[int]=..., token_in: _Optional[str]=..., start_tick: _Optional[int]=..., use_cur_tick: bool=..., bound_tick: _Optional[int]=..., use_no_bound: bool=...) -> None:
        ...

class LiquidityNetInDirectionResponse(_message.Message):
    __slots__ = ['liquidity_depths', 'current_tick', 'current_liquidity']
    LIQUIDITY_DEPTHS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TICK_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    liquidity_depths: _containers.RepeatedCompositeFieldContainer[TickLiquidityNet]
    current_tick: int
    current_liquidity: str

    def __init__(self, liquidity_depths: _Optional[_Iterable[_Union[TickLiquidityNet, _Mapping]]]=..., current_tick: _Optional[int]=..., current_liquidity: _Optional[str]=...) -> None:
        ...

class LiquidityPerTickRangeRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class LiquidityPerTickRangeResponse(_message.Message):
    __slots__ = ['liquidity']
    LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    liquidity: _containers.RepeatedCompositeFieldContainer[LiquidityDepthWithRange]

    def __init__(self, liquidity: _Optional[_Iterable[_Union[LiquidityDepthWithRange, _Mapping]]]=...) -> None:
        ...

class ClaimableSpreadRewardsRequest(_message.Message):
    __slots__ = ['position_id']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    position_id: int

    def __init__(self, position_id: _Optional[int]=...) -> None:
        ...

class ClaimableSpreadRewardsResponse(_message.Message):
    __slots__ = ['claimable_spread_rewards']
    CLAIMABLE_SPREAD_REWARDS_FIELD_NUMBER: _ClassVar[int]
    claimable_spread_rewards: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, claimable_spread_rewards: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class ClaimableIncentivesRequest(_message.Message):
    __slots__ = ['position_id']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    position_id: int

    def __init__(self, position_id: _Optional[int]=...) -> None:
        ...

class ClaimableIncentivesResponse(_message.Message):
    __slots__ = ['claimable_incentives', 'forfeited_incentives']
    CLAIMABLE_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    FORFEITED_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    claimable_incentives: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    forfeited_incentives: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, claimable_incentives: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., forfeited_incentives: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class PoolAccumulatorRewardsRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class PoolAccumulatorRewardsResponse(_message.Message):
    __slots__ = ['spread_reward_growth_global', 'uptime_growth_global']
    SPREAD_REWARD_GROWTH_GLOBAL_FIELD_NUMBER: _ClassVar[int]
    UPTIME_GROWTH_GLOBAL_FIELD_NUMBER: _ClassVar[int]
    spread_reward_growth_global: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]
    uptime_growth_global: _containers.RepeatedCompositeFieldContainer[_tickInfo_pb2.UptimeTracker]

    def __init__(self, spread_reward_growth_global: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]]=..., uptime_growth_global: _Optional[_Iterable[_Union[_tickInfo_pb2.UptimeTracker, _Mapping]]]=...) -> None:
        ...

class TickAccumulatorTrackersRequest(_message.Message):
    __slots__ = ['pool_id', 'tick_index']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TICK_INDEX_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    tick_index: int

    def __init__(self, pool_id: _Optional[int]=..., tick_index: _Optional[int]=...) -> None:
        ...

class TickAccumulatorTrackersResponse(_message.Message):
    __slots__ = ['spread_reward_growth_opposite_direction_of_last_traversal', 'uptime_trackers']
    SPREAD_REWARD_GROWTH_OPPOSITE_DIRECTION_OF_LAST_TRAVERSAL_FIELD_NUMBER: _ClassVar[int]
    UPTIME_TRACKERS_FIELD_NUMBER: _ClassVar[int]
    spread_reward_growth_opposite_direction_of_last_traversal: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]
    uptime_trackers: _containers.RepeatedCompositeFieldContainer[_tickInfo_pb2.UptimeTracker]

    def __init__(self, spread_reward_growth_opposite_direction_of_last_traversal: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]]=..., uptime_trackers: _Optional[_Iterable[_Union[_tickInfo_pb2.UptimeTracker, _Mapping]]]=...) -> None:
        ...

class IncentiveRecordsRequest(_message.Message):
    __slots__ = ['pool_id', 'pagination']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pool_id: _Optional[int]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class IncentiveRecordsResponse(_message.Message):
    __slots__ = ['incentive_records', 'pagination']
    INCENTIVE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    incentive_records: _containers.RepeatedCompositeFieldContainer[_incentive_record_pb2.IncentiveRecord]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, incentive_records: _Optional[_Iterable[_Union[_incentive_record_pb2.IncentiveRecord, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class CFMMPoolIdLinkFromConcentratedPoolIdRequest(_message.Message):
    __slots__ = ['concentrated_pool_id']
    CONCENTRATED_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    concentrated_pool_id: int

    def __init__(self, concentrated_pool_id: _Optional[int]=...) -> None:
        ...

class CFMMPoolIdLinkFromConcentratedPoolIdResponse(_message.Message):
    __slots__ = ['cfmm_pool_id']
    CFMM_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    cfmm_pool_id: int

    def __init__(self, cfmm_pool_id: _Optional[int]=...) -> None:
        ...

class UserUnbondingPositionsRequest(_message.Message):
    __slots__ = ['address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str

    def __init__(self, address: _Optional[str]=...) -> None:
        ...

class UserUnbondingPositionsResponse(_message.Message):
    __slots__ = ['positions_with_period_lock']
    POSITIONS_WITH_PERIOD_LOCK_FIELD_NUMBER: _ClassVar[int]
    positions_with_period_lock: _containers.RepeatedCompositeFieldContainer[_position_pb2.PositionWithPeriodLock]

    def __init__(self, positions_with_period_lock: _Optional[_Iterable[_Union[_position_pb2.PositionWithPeriodLock, _Mapping]]]=...) -> None:
        ...

class GetTotalLiquidityRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class GetTotalLiquidityResponse(_message.Message):
    __slots__ = ['total_liquidity']
    TOTAL_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    total_liquidity: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, total_liquidity: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...