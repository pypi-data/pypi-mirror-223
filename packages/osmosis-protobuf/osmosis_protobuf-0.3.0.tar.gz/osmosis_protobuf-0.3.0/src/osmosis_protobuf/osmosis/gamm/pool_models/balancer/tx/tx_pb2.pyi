from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from osmosis.gamm.pool_models.balancer import balancerPool_pb2 as _balancerPool_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateBalancerPool(_message.Message):
    __slots__ = ['sender', 'pool_params', 'pool_assets', 'future_pool_governor']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    POOL_ASSETS_FIELD_NUMBER: _ClassVar[int]
    FUTURE_POOL_GOVERNOR_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_params: _balancerPool_pb2.PoolParams
    pool_assets: _containers.RepeatedCompositeFieldContainer[_balancerPool_pb2.PoolAsset]
    future_pool_governor: str

    def __init__(self, sender: _Optional[str]=..., pool_params: _Optional[_Union[_balancerPool_pb2.PoolParams, _Mapping]]=..., pool_assets: _Optional[_Iterable[_Union[_balancerPool_pb2.PoolAsset, _Mapping]]]=..., future_pool_governor: _Optional[str]=...) -> None:
        ...

class MsgCreateBalancerPoolResponse(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...