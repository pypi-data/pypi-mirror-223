from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['minted_denom']
    MINTED_DENOM_FIELD_NUMBER: _ClassVar[int]
    minted_denom: str

    def __init__(self, minted_denom: _Optional[str]=...) -> None:
        ...

class LockableDurationsInfo(_message.Message):
    __slots__ = ['lockable_durations']
    LOCKABLE_DURATIONS_FIELD_NUMBER: _ClassVar[int]
    lockable_durations: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]

    def __init__(self, lockable_durations: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]]=...) -> None:
        ...

class DistrInfo(_message.Message):
    __slots__ = ['total_weight', 'records']
    TOTAL_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    total_weight: str
    records: _containers.RepeatedCompositeFieldContainer[DistrRecord]

    def __init__(self, total_weight: _Optional[str]=..., records: _Optional[_Iterable[_Union[DistrRecord, _Mapping]]]=...) -> None:
        ...

class DistrRecord(_message.Message):
    __slots__ = ['gauge_id', 'weight']
    GAUGE_ID_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    gauge_id: int
    weight: str

    def __init__(self, gauge_id: _Optional[int]=..., weight: _Optional[str]=...) -> None:
        ...

class PoolToGauge(_message.Message):
    __slots__ = ['pool_id', 'gauge_id', 'duration']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    GAUGE_ID_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    gauge_id: int
    duration: _duration_pb2.Duration

    def __init__(self, pool_id: _Optional[int]=..., gauge_id: _Optional[int]=..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class PoolToGauges(_message.Message):
    __slots__ = ['pool_to_gauge']
    POOL_TO_GAUGE_FIELD_NUMBER: _ClassVar[int]
    pool_to_gauge: _containers.RepeatedCompositeFieldContainer[PoolToGauge]

    def __init__(self, pool_to_gauge: _Optional[_Iterable[_Union[PoolToGauge, _Mapping]]]=...) -> None:
        ...