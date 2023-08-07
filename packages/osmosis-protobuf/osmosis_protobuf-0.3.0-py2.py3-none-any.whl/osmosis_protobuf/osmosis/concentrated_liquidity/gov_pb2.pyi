from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class CreateConcentratedLiquidityPoolsProposal(_message.Message):
    __slots__ = ['title', 'description', 'pool_records']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    POOL_RECORDS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    pool_records: _containers.RepeatedCompositeFieldContainer[PoolRecord]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., pool_records: _Optional[_Iterable[_Union[PoolRecord, _Mapping]]]=...) -> None:
        ...

class TickSpacingDecreaseProposal(_message.Message):
    __slots__ = ['title', 'description', 'pool_id_to_tick_spacing_records']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_TO_TICK_SPACING_RECORDS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    pool_id_to_tick_spacing_records: _containers.RepeatedCompositeFieldContainer[PoolIdToTickSpacingRecord]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., pool_id_to_tick_spacing_records: _Optional[_Iterable[_Union[PoolIdToTickSpacingRecord, _Mapping]]]=...) -> None:
        ...

class PoolIdToTickSpacingRecord(_message.Message):
    __slots__ = ['pool_id', 'new_tick_spacing']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_TICK_SPACING_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    new_tick_spacing: int

    def __init__(self, pool_id: _Optional[int]=..., new_tick_spacing: _Optional[int]=...) -> None:
        ...

class PoolRecord(_message.Message):
    __slots__ = ['denom0', 'denom1', 'tick_spacing', 'exponent_at_price_one', 'spread_factor']
    DENOM0_FIELD_NUMBER: _ClassVar[int]
    DENOM1_FIELD_NUMBER: _ClassVar[int]
    TICK_SPACING_FIELD_NUMBER: _ClassVar[int]
    EXPONENT_AT_PRICE_ONE_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FACTOR_FIELD_NUMBER: _ClassVar[int]
    denom0: str
    denom1: str
    tick_spacing: int
    exponent_at_price_one: str
    spread_factor: str

    def __init__(self, denom0: _Optional[str]=..., denom1: _Optional[str]=..., tick_spacing: _Optional[int]=..., exponent_at_price_one: _Optional[str]=..., spread_factor: _Optional[str]=...) -> None:
        ...