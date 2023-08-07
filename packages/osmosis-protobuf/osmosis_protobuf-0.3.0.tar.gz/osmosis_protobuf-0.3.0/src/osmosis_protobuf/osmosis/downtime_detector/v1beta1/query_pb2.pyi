from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.downtime_detector.v1beta1 import genesis_pb2 as _genesis_pb2
from osmosis.downtime_detector.v1beta1 import downtime_duration_pb2 as _downtime_duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class RecoveredSinceDowntimeOfLengthRequest(_message.Message):
    __slots__ = ['downtime', 'recovery']
    DOWNTIME_FIELD_NUMBER: _ClassVar[int]
    RECOVERY_FIELD_NUMBER: _ClassVar[int]
    downtime: _downtime_duration_pb2.Downtime
    recovery: _duration_pb2.Duration

    def __init__(self, downtime: _Optional[_Union[_downtime_duration_pb2.Downtime, str]]=..., recovery: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class RecoveredSinceDowntimeOfLengthResponse(_message.Message):
    __slots__ = ['succesfully_recovered']
    SUCCESFULLY_RECOVERED_FIELD_NUMBER: _ClassVar[int]
    succesfully_recovered: bool

    def __init__(self, succesfully_recovered: bool=...) -> None:
        ...