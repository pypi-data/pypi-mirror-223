from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from osmosis.pool_incentives.v1beta1 import incentives_pb2 as _incentives_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MigrationRecords(_message.Message):
    __slots__ = ['balancer_to_concentrated_pool_links']
    BALANCER_TO_CONCENTRATED_POOL_LINKS_FIELD_NUMBER: _ClassVar[int]
    balancer_to_concentrated_pool_links: _containers.RepeatedCompositeFieldContainer[BalancerToConcentratedPoolLink]

    def __init__(self, balancer_to_concentrated_pool_links: _Optional[_Iterable[_Union[BalancerToConcentratedPoolLink, _Mapping]]]=...) -> None:
        ...

class BalancerToConcentratedPoolLink(_message.Message):
    __slots__ = ['balancer_pool_id', 'cl_pool_id']
    BALANCER_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    CL_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    balancer_pool_id: int
    cl_pool_id: int

    def __init__(self, balancer_pool_id: _Optional[int]=..., cl_pool_id: _Optional[int]=...) -> None:
        ...