from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Pool(_message.Message):
    __slots__ = ['address', 'incentives_address', 'spread_rewards_address', 'id', 'current_tick_liquidity', 'token0', 'token1', 'current_sqrt_price', 'current_tick', 'tick_spacing', 'exponent_at_price_one', 'spread_factor', 'last_liquidity_update']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    INCENTIVES_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SPREAD_REWARDS_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TICK_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    TOKEN0_FIELD_NUMBER: _ClassVar[int]
    TOKEN1_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SQRT_PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TICK_FIELD_NUMBER: _ClassVar[int]
    TICK_SPACING_FIELD_NUMBER: _ClassVar[int]
    EXPONENT_AT_PRICE_ONE_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FACTOR_FIELD_NUMBER: _ClassVar[int]
    LAST_LIQUIDITY_UPDATE_FIELD_NUMBER: _ClassVar[int]
    address: str
    incentives_address: str
    spread_rewards_address: str
    id: int
    current_tick_liquidity: str
    token0: str
    token1: str
    current_sqrt_price: str
    current_tick: int
    tick_spacing: int
    exponent_at_price_one: int
    spread_factor: str
    last_liquidity_update: _timestamp_pb2.Timestamp

    def __init__(self, address: _Optional[str]=..., incentives_address: _Optional[str]=..., spread_rewards_address: _Optional[str]=..., id: _Optional[int]=..., current_tick_liquidity: _Optional[str]=..., token0: _Optional[str]=..., token1: _Optional[str]=..., current_sqrt_price: _Optional[str]=..., current_tick: _Optional[int]=..., tick_spacing: _Optional[int]=..., exponent_at_price_one: _Optional[int]=..., spread_factor: _Optional[str]=..., last_liquidity_update: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]]=...) -> None:
        ...