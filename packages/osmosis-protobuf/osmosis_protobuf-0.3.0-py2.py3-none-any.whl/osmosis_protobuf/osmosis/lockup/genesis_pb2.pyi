from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.lockup import lock_pb2 as _lock_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['last_lock_id', 'locks', 'synthetic_locks']
    LAST_LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    LOCKS_FIELD_NUMBER: _ClassVar[int]
    SYNTHETIC_LOCKS_FIELD_NUMBER: _ClassVar[int]
    last_lock_id: int
    locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.PeriodLock]
    synthetic_locks: _containers.RepeatedCompositeFieldContainer[_lock_pb2.SyntheticLock]

    def __init__(self, last_lock_id: _Optional[int]=..., locks: _Optional[_Iterable[_Union[_lock_pb2.PeriodLock, _Mapping]]]=..., synthetic_locks: _Optional[_Iterable[_Union[_lock_pb2.SyntheticLock, _Mapping]]]=...) -> None:
        ...