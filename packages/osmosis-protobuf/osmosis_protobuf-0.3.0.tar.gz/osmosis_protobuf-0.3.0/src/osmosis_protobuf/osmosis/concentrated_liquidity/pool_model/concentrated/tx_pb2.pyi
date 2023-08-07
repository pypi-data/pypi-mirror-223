from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateConcentratedPool(_message.Message):
    __slots__ = ['sender', 'denom0', 'denom1', 'tick_spacing', 'spread_factor']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    DENOM0_FIELD_NUMBER: _ClassVar[int]
    DENOM1_FIELD_NUMBER: _ClassVar[int]
    TICK_SPACING_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FACTOR_FIELD_NUMBER: _ClassVar[int]
    sender: str
    denom0: str
    denom1: str
    tick_spacing: int
    spread_factor: str

    def __init__(self, sender: _Optional[str]=..., denom0: _Optional[str]=..., denom1: _Optional[str]=..., tick_spacing: _Optional[int]=..., spread_factor: _Optional[str]=...) -> None:
        ...

class MsgCreateConcentratedPoolResponse(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...