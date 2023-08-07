from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Node(_message.Message):
    __slots__ = ['children']
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    children: _containers.RepeatedCompositeFieldContainer[Child]

    def __init__(self, children: _Optional[_Iterable[_Union[Child, _Mapping]]]=...) -> None:
        ...

class Child(_message.Message):
    __slots__ = ['index', 'accumulation']
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ACCUMULATION_FIELD_NUMBER: _ClassVar[int]
    index: bytes
    accumulation: str

    def __init__(self, index: _Optional[bytes]=..., accumulation: _Optional[str]=...) -> None:
        ...

class Leaf(_message.Message):
    __slots__ = ['leaf']
    LEAF_FIELD_NUMBER: _ClassVar[int]
    leaf: Child

    def __init__(self, leaf: _Optional[_Union[Child, _Mapping]]=...) -> None:
        ...