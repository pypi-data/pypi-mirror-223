from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import any_pb2 as _any_pb2
from osmosis.accum.v1beta1 import accum_pb2 as _accum_pb2
from osmosis.concentrated_liquidity import params_pb2 as _params_pb2
from osmosis.concentrated_liquidity import position_pb2 as _position_pb2
from osmosis.concentrated_liquidity import tickInfo_pb2 as _tickInfo_pb2
from osmosis.concentrated_liquidity import incentive_record_pb2 as _incentive_record_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class FullTick(_message.Message):
    __slots__ = ['pool_id', 'tick_index', 'info']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    TICK_INDEX_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    tick_index: int
    info: _tickInfo_pb2.TickInfo

    def __init__(self, pool_id: _Optional[int]=..., tick_index: _Optional[int]=..., info: _Optional[_Union[_tickInfo_pb2.TickInfo, _Mapping]]=...) -> None:
        ...

class PoolData(_message.Message):
    __slots__ = ['pool', 'ticks', 'spread_reward_accumulator', 'incentives_accumulators', 'incentive_records']
    POOL_FIELD_NUMBER: _ClassVar[int]
    TICKS_FIELD_NUMBER: _ClassVar[int]
    SPREAD_REWARD_ACCUMULATOR_FIELD_NUMBER: _ClassVar[int]
    INCENTIVES_ACCUMULATORS_FIELD_NUMBER: _ClassVar[int]
    INCENTIVE_RECORDS_FIELD_NUMBER: _ClassVar[int]
    pool: _any_pb2.Any
    ticks: _containers.RepeatedCompositeFieldContainer[FullTick]
    spread_reward_accumulator: AccumObject
    incentives_accumulators: _containers.RepeatedCompositeFieldContainer[AccumObject]
    incentive_records: _containers.RepeatedCompositeFieldContainer[_incentive_record_pb2.IncentiveRecord]

    def __init__(self, pool: _Optional[_Union[_any_pb2.Any, _Mapping]]=..., ticks: _Optional[_Iterable[_Union[FullTick, _Mapping]]]=..., spread_reward_accumulator: _Optional[_Union[AccumObject, _Mapping]]=..., incentives_accumulators: _Optional[_Iterable[_Union[AccumObject, _Mapping]]]=..., incentive_records: _Optional[_Iterable[_Union[_incentive_record_pb2.IncentiveRecord, _Mapping]]]=...) -> None:
        ...

class PositionData(_message.Message):
    __slots__ = ['position', 'lock_id', 'spread_reward_accum_record', 'uptime_accum_records']
    POSITION_FIELD_NUMBER: _ClassVar[int]
    LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    SPREAD_REWARD_ACCUM_RECORD_FIELD_NUMBER: _ClassVar[int]
    UPTIME_ACCUM_RECORDS_FIELD_NUMBER: _ClassVar[int]
    position: _position_pb2.Position
    lock_id: int
    spread_reward_accum_record: _accum_pb2.Record
    uptime_accum_records: _containers.RepeatedCompositeFieldContainer[_accum_pb2.Record]

    def __init__(self, position: _Optional[_Union[_position_pb2.Position, _Mapping]]=..., lock_id: _Optional[int]=..., spread_reward_accum_record: _Optional[_Union[_accum_pb2.Record, _Mapping]]=..., uptime_accum_records: _Optional[_Iterable[_Union[_accum_pb2.Record, _Mapping]]]=...) -> None:
        ...

class GenesisState(_message.Message):
    __slots__ = ['params', 'pool_data', 'position_data', 'next_position_id', 'next_incentive_record_id']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    POOL_DATA_FIELD_NUMBER: _ClassVar[int]
    POSITION_DATA_FIELD_NUMBER: _ClassVar[int]
    NEXT_POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    NEXT_INCENTIVE_RECORD_ID_FIELD_NUMBER: _ClassVar[int]
    params: _params_pb2.Params
    pool_data: _containers.RepeatedCompositeFieldContainer[PoolData]
    position_data: _containers.RepeatedCompositeFieldContainer[PositionData]
    next_position_id: int
    next_incentive_record_id: int

    def __init__(self, params: _Optional[_Union[_params_pb2.Params, _Mapping]]=..., pool_data: _Optional[_Iterable[_Union[PoolData, _Mapping]]]=..., position_data: _Optional[_Iterable[_Union[PositionData, _Mapping]]]=..., next_position_id: _Optional[int]=..., next_incentive_record_id: _Optional[int]=...) -> None:
        ...

class AccumObject(_message.Message):
    __slots__ = ['name', 'accum_content']
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACCUM_CONTENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    accum_content: _accum_pb2.AccumulatorContent

    def __init__(self, name: _Optional[str]=..., accum_content: _Optional[_Union[_accum_pb2.AccumulatorContent, _Mapping]]=...) -> None:
        ...