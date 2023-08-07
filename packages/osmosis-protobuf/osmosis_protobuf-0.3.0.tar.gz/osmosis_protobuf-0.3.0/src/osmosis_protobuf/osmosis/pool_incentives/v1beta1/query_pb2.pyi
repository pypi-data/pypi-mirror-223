from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from osmosis.incentives import gauge_pb2 as _gauge_pb2
from osmosis.pool_incentives.v1beta1 import incentives_pb2 as _incentives_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryGaugeIdsRequest(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class QueryGaugeIdsResponse(_message.Message):
    __slots__ = ['gauge_ids_with_duration']

    class GaugeIdWithDuration(_message.Message):
        __slots__ = ['gauge_id', 'duration', 'gauge_incentive_percentage']
        GAUGE_ID_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        GAUGE_INCENTIVE_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
        gauge_id: int
        duration: _duration_pb2.Duration
        gauge_incentive_percentage: str

        def __init__(self, gauge_id: _Optional[int]=..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., gauge_incentive_percentage: _Optional[str]=...) -> None:
            ...
    GAUGE_IDS_WITH_DURATION_FIELD_NUMBER: _ClassVar[int]
    gauge_ids_with_duration: _containers.RepeatedCompositeFieldContainer[QueryGaugeIdsResponse.GaugeIdWithDuration]

    def __init__(self, gauge_ids_with_duration: _Optional[_Iterable[_Union[QueryGaugeIdsResponse.GaugeIdWithDuration, _Mapping]]]=...) -> None:
        ...

class QueryDistrInfoRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryDistrInfoResponse(_message.Message):
    __slots__ = ['distr_info']
    DISTR_INFO_FIELD_NUMBER: _ClassVar[int]
    distr_info: _incentives_pb2.DistrInfo

    def __init__(self, distr_info: _Optional[_Union[_incentives_pb2.DistrInfo, _Mapping]]=...) -> None:
        ...

class QueryParamsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryParamsResponse(_message.Message):
    __slots__ = ['params']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _incentives_pb2.Params

    def __init__(self, params: _Optional[_Union[_incentives_pb2.Params, _Mapping]]=...) -> None:
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

class QueryIncentivizedPoolsRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class IncentivizedPool(_message.Message):
    __slots__ = ['pool_id', 'lockable_duration', 'gauge_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    LOCKABLE_DURATION_FIELD_NUMBER: _ClassVar[int]
    GAUGE_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    lockable_duration: _duration_pb2.Duration
    gauge_id: int

    def __init__(self, pool_id: _Optional[int]=..., lockable_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=..., gauge_id: _Optional[int]=...) -> None:
        ...

class QueryIncentivizedPoolsResponse(_message.Message):
    __slots__ = ['incentivized_pools']
    INCENTIVIZED_POOLS_FIELD_NUMBER: _ClassVar[int]
    incentivized_pools: _containers.RepeatedCompositeFieldContainer[IncentivizedPool]

    def __init__(self, incentivized_pools: _Optional[_Iterable[_Union[IncentivizedPool, _Mapping]]]=...) -> None:
        ...

class QueryExternalIncentiveGaugesRequest(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class QueryExternalIncentiveGaugesResponse(_message.Message):
    __slots__ = ['data']
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_gauge_pb2.Gauge]

    def __init__(self, data: _Optional[_Iterable[_Union[_gauge_pb2.Gauge, _Mapping]]]=...) -> None:
        ...