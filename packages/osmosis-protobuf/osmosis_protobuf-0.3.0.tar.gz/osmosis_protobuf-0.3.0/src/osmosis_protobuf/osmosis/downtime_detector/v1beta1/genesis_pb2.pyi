from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from osmosis.downtime_detector.v1beta1 import downtime_duration_pb2 as _downtime_duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisDowntimeEntry(_message.Message):
    __slots__ = ['duration', 'last_downtime']
    DURATION_FIELD_NUMBER: _ClassVar[int]
    LAST_DOWNTIME_FIELD_NUMBER: _ClassVar[int]
    duration: _downtime_duration_pb2.Downtime
    last_downtime: _timestamp_pb2.Timestamp

    def __init__(self, duration: _Optional[_Union[_downtime_duration_pb2.Downtime, str]]=..., last_downtime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...

class GenesisState(_message.Message):
    __slots__ = ['downtimes', 'last_block_time']
    DOWNTIMES_FIELD_NUMBER: _ClassVar[int]
    LAST_BLOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    downtimes: _containers.RepeatedCompositeFieldContainer[GenesisDowntimeEntry]
    last_block_time: _timestamp_pb2.Timestamp

    def __init__(self, downtimes: _Optional[_Iterable[_Union[GenesisDowntimeEntry, _Mapping]]]=..., last_block_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...