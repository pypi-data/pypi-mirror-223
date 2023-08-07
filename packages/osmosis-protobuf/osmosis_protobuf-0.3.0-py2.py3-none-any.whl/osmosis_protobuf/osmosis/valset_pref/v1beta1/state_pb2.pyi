from gogoproto import gogo_pb2 as _gogo_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class ValidatorPreference(_message.Message):
    __slots__ = ['val_oper_address', 'weight']
    VAL_OPER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    val_oper_address: str
    weight: str

    def __init__(self, val_oper_address: _Optional[str]=..., weight: _Optional[str]=...) -> None:
        ...

class ValidatorSetPreferences(_message.Message):
    __slots__ = ['preferences']
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    preferences: _containers.RepeatedCompositeFieldContainer[ValidatorPreference]

    def __init__(self, preferences: _Optional[_Iterable[_Union[ValidatorPreference, _Mapping]]]=...) -> None:
        ...