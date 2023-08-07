from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import any_pb2 as _any_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.poolmanager.v1beta1 import module_route_pb2 as _module_route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['pool_creation_fee']
    POOL_CREATION_FEE_FIELD_NUMBER: _ClassVar[int]
    pool_creation_fee: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, pool_creation_fee: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class GenesisState(_message.Message):
    __slots__ = ['next_pool_id', 'params', 'pool_routes']
    NEXT_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    POOL_ROUTES_FIELD_NUMBER: _ClassVar[int]
    next_pool_id: int
    params: Params
    pool_routes: _containers.RepeatedCompositeFieldContainer[_module_route_pb2.ModuleRoute]

    def __init__(self, next_pool_id: _Optional[int]=..., params: _Optional[_Union[Params, _Mapping]]=..., pool_routes: _Optional[_Iterable[_Union[_module_route_pb2.ModuleRoute, _Mapping]]]=...) -> None:
        ...