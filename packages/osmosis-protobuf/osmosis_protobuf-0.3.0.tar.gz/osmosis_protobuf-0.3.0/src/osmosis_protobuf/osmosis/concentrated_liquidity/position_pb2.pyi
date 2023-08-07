from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.lockup import lock_pb2 as _lock_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Position(_message.Message):
    __slots__ = ['position_id', 'address', 'pool_id', 'lower_tick', 'upper_tick', 'join_time', 'liquidity']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    LOWER_TICK_FIELD_NUMBER: _ClassVar[int]
    UPPER_TICK_FIELD_NUMBER: _ClassVar[int]
    JOIN_TIME_FIELD_NUMBER: _ClassVar[int]
    LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    position_id: int
    address: str
    pool_id: int
    lower_tick: int
    upper_tick: int
    join_time: _timestamp_pb2.Timestamp
    liquidity: str

    def __init__(self, position_id: _Optional[int]=..., address: _Optional[str]=..., pool_id: _Optional[int]=..., lower_tick: _Optional[int]=..., upper_tick: _Optional[int]=..., join_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=..., liquidity: _Optional[str]=...) -> None:
        ...

class FullPositionBreakdown(_message.Message):
    __slots__ = ['position', 'asset0', 'asset1', 'claimable_spread_rewards', 'claimable_incentives', 'forfeited_incentives']
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ASSET0_FIELD_NUMBER: _ClassVar[int]
    ASSET1_FIELD_NUMBER: _ClassVar[int]
    CLAIMABLE_SPREAD_REWARDS_FIELD_NUMBER: _ClassVar[int]
    CLAIMABLE_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    FORFEITED_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    position: Position
    asset0: _coin_pb2.Coin
    asset1: _coin_pb2.Coin
    claimable_spread_rewards: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    claimable_incentives: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    forfeited_incentives: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, position: _Optional[_Union[Position, _Mapping]]=..., asset0: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., asset1: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., claimable_spread_rewards: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., claimable_incentives: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., forfeited_incentives: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class PositionWithPeriodLock(_message.Message):
    __slots__ = ['position', 'locks']
    POSITION_FIELD_NUMBER: _ClassVar[int]
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    position: Position
    locks: _lock_pb2.PeriodLock

    def __init__(self, position: _Optional[_Union[Position, _Mapping]]=..., locks: _Optional[_Union[_lock_pb2.PeriodLock, _Mapping]]=...) -> None:
        ...