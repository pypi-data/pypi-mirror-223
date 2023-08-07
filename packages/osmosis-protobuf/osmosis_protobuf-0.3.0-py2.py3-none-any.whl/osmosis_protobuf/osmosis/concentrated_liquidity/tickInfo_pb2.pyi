from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class TickInfo(_message.Message):
    __slots__ = ['liquidity_gross', 'liquidity_net', 'spread_reward_growth_opposite_direction_of_last_traversal', 'uptime_trackers']
    LIQUIDITY_GROSS_FIELD_NUMBER: _ClassVar[int]
    LIQUIDITY_NET_FIELD_NUMBER: _ClassVar[int]
    SPREAD_REWARD_GROWTH_OPPOSITE_DIRECTION_OF_LAST_TRAVERSAL_FIELD_NUMBER: _ClassVar[int]
    UPTIME_TRACKERS_FIELD_NUMBER: _ClassVar[int]
    liquidity_gross: str
    liquidity_net: str
    spread_reward_growth_opposite_direction_of_last_traversal: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]
    uptime_trackers: UptimeTrackers

    def __init__(self, liquidity_gross: _Optional[str]=..., liquidity_net: _Optional[str]=..., spread_reward_growth_opposite_direction_of_last_traversal: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]]=..., uptime_trackers: _Optional[_Union[UptimeTrackers, _Mapping]]=...) -> None:
        ...

class UptimeTrackers(_message.Message):
    __slots__ = ['list']
    LIST_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedCompositeFieldContainer[UptimeTracker]

    def __init__(self, list: _Optional[_Iterable[_Union[UptimeTracker, _Mapping]]]=...) -> None:
        ...

class UptimeTracker(_message.Message):
    __slots__ = ['uptime_growth_outside']
    UPTIME_GROWTH_OUTSIDE_FIELD_NUMBER: _ClassVar[int]
    uptime_growth_outside: _containers.RepeatedCompositeFieldContainer[_coin_pb2.DecCoin]

    def __init__(self, uptime_growth_outside: _Optional[_Iterable[_Union[_coin_pb2.DecCoin, _Mapping]]]=...) -> None:
        ...