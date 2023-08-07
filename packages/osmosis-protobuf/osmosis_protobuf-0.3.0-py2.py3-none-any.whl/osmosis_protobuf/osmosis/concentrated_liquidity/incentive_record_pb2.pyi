from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class IncentiveRecord(_message.Message):
    __slots__ = ['incentive_id', 'pool_id', 'incentive_record_body', 'min_uptime']
    INCENTIVE_ID_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    INCENTIVE_RECORD_BODY_FIELD_NUMBER: _ClassVar[int]
    MIN_UPTIME_FIELD_NUMBER: _ClassVar[int]
    incentive_id: int
    pool_id: int
    incentive_record_body: IncentiveRecordBody
    min_uptime: _duration_pb2.Duration

    def __init__(self, incentive_id: _Optional[int]=..., pool_id: _Optional[int]=..., incentive_record_body: _Optional[_Union[IncentiveRecordBody, _Mapping]]=..., min_uptime: _Optional[_Union[_duration_pb2.Duration, _Mapping]]=...) -> None:
        ...

class IncentiveRecordBody(_message.Message):
    __slots__ = ['remaining_coin', 'emission_rate', 'start_time']
    REMAINING_COIN_FIELD_NUMBER: _ClassVar[int]
    EMISSION_RATE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    remaining_coin: _coin_pb2.DecCoin
    emission_rate: str
    start_time: _timestamp_pb2.Timestamp

    def __init__(self, remaining_coin: _Optional[_Union[_coin_pb2.DecCoin, _Mapping]]=..., emission_rate: _Optional[str]=..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...