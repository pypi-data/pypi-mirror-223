from gogoproto import gogo_pb2 as _gogo_pb2
from osmosis.txfees.v1beta1 import feetoken_pb2 as _feetoken_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class GenesisState(_message.Message):
    __slots__ = ['basedenom', 'feetokens']
    BASEDENOM_FIELD_NUMBER: _ClassVar[int]
    FEETOKENS_FIELD_NUMBER: _ClassVar[int]
    basedenom: str
    feetokens: _containers.RepeatedCompositeFieldContainer[_feetoken_pb2.FeeToken]

    def __init__(self, basedenom: _Optional[str]=..., feetokens: _Optional[_Iterable[_Union[_feetoken_pb2.FeeToken, _Mapping]]]=...) -> None:
        ...