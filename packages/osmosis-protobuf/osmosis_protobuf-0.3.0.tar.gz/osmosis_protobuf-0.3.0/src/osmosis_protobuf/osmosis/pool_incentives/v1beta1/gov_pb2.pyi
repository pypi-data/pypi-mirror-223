from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.pool_incentives.v1beta1 import incentives_pb2 as _incentives_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ReplacePoolIncentivesProposal(_message.Message):
    __slots__ = ['title', 'description', 'records']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    records: _containers.RepeatedCompositeFieldContainer[_incentives_pb2.DistrRecord]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., records: _Optional[_Iterable[_Union[_incentives_pb2.DistrRecord, _Mapping]]]=...) -> None:
        ...

class UpdatePoolIncentivesProposal(_message.Message):
    __slots__ = ['title', 'description', 'records']
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    records: _containers.RepeatedCompositeFieldContainer[_incentives_pb2.DistrRecord]

    def __init__(self, title: _Optional[str]=..., description: _Optional[str]=..., records: _Optional[_Iterable[_Union[_incentives_pb2.DistrRecord, _Mapping]]]=...) -> None:
        ...