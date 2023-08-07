from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from osmosis.pool_incentives.v1beta1 import incentives_pb2 as _incentives_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['params', 'lockable_durations', 'distr_info', 'pool_to_gauges']
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    LOCKABLE_DURATIONS_FIELD_NUMBER: _ClassVar[int]
    DISTR_INFO_FIELD_NUMBER: _ClassVar[int]
    POOL_TO_GAUGES_FIELD_NUMBER: _ClassVar[int]
    params: _incentives_pb2.Params
    lockable_durations: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]
    distr_info: _incentives_pb2.DistrInfo
    pool_to_gauges: _incentives_pb2.PoolToGauges

    def __init__(self, params: _Optional[_Union[_incentives_pb2.Params, _Mapping]]=..., lockable_durations: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]]=..., distr_info: _Optional[_Union[_incentives_pb2.DistrInfo, _Mapping]]=..., pool_to_gauges: _Optional[_Union[_incentives_pb2.PoolToGauges, _Mapping]]=...) -> None:
        ...