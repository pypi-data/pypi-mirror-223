from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from osmosis.incentives import gauge_pb2 as _gauge_pb2
from osmosis.lockup import lock_pb2 as _lock_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ModuleToDistributeCoinsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class ModuleToDistributeCoinsResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class GaugeByIDRequest(_message.Message):
    __slots__ = ['id']
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int

    def __init__(self, id: _Optional[int]=...) -> None:
        ...

class GaugeByIDResponse(_message.Message):
    __slots__ = ['gauge']
    GAUGE_FIELD_NUMBER: _ClassVar[int]
    gauge: _gauge_pb2.Gauge

    def __init__(self, gauge: _Optional[_Union[_gauge_pb2.Gauge, _Mapping]]=...) -> None:
        ...

class GaugesRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class GaugesResponse(_message.Message):
    __slots__ = ['data', 'pagination']
    DATA_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_gauge_pb2.Gauge]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, data: _Optional[_Iterable[_Union[_gauge_pb2.Gauge, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class ActiveGaugesRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class ActiveGaugesResponse(_message.Message):
    __slots__ = ['data', 'pagination']
    DATA_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_gauge_pb2.Gauge]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, data: _Optional[_Iterable[_Union[_gauge_pb2.Gauge, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class ActiveGaugesPerDenomRequest(_message.Message):
    __slots__ = ['denom', 'pagination']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    denom: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, denom: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class ActiveGaugesPerDenomResponse(_message.Message):
    __slots__ = ['data', 'pagination']
    DATA_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_gauge_pb2.Gauge]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, data: _Optional[_Iterable[_Union[_gauge_pb2.Gauge, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class UpcomingGaugesRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class UpcomingGaugesResponse(_message.Message):
    __slots__ = ['data', 'pagination']
    DATA_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_gauge_pb2.Gauge]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, data: _Optional[_Iterable[_Union[_gauge_pb2.Gauge, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class UpcomingGaugesPerDenomRequest(_message.Message):
    __slots__ = ['denom', 'pagination']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    denom: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, denom: _Optional[str]=..., pagination: _Optional[_Union[_pagination_pb2.PageRequest, _Mapping]]=...) -> None:
        ...

class UpcomingGaugesPerDenomResponse(_message.Message):
    __slots__ = ['upcoming_gauges', 'pagination']
    UPCOMING_GAUGES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    upcoming_gauges: _containers.RepeatedCompositeFieldContainer[_gauge_pb2.Gauge]
    pagination: _pagination_pb2.PageResponse

    def __init__(self, upcoming_gauges: _Optional[_Iterable[_Union[_gauge_pb2.Gauge, _Mapping]]]=..., pagination: _Optional[_Union[_pagination_pb2.PageResponse, _Mapping]]=...) -> None:
        ...

class RewardsEstRequest(_message.Message):
    __slots__ = ['owner', 'lock_ids', 'end_epoch']
    OWNER_FIELD_NUMBER: _ClassVar[int]
    LOCK_IDS_FIELD_NUMBER: _ClassVar[int]
    END_EPOCH_FIELD_NUMBER: _ClassVar[int]
    owner: str
    lock_ids: _containers.RepeatedScalarFieldContainer[int]
    end_epoch: int

    def __init__(self, owner: _Optional[str]=..., lock_ids: _Optional[_Iterable[int]]=..., end_epoch: _Optional[int]=...) -> None:
        ...

class RewardsEstResponse(_message.Message):
    __slots__ = ['coins']
    COINS_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, coins: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class QueryLockableDurationsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryLockableDurationsResponse(_message.Message):
    __slots__ = ['lockable_durations']
    LOCKABLE_DURATIONS_FIELD_NUMBER: _ClassVar[int]
    lockable_durations: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]

    def __init__(self, lockable_durations: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]]=...) -> None:
        ...