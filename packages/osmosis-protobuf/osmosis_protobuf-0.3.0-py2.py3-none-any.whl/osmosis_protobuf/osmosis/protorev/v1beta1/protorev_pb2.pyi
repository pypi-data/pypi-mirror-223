from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class TokenPairArbRoutes(_message.Message):
    __slots__ = ['arb_routes', 'token_in', 'token_out']
    ARB_ROUTES_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    arb_routes: _containers.RepeatedCompositeFieldContainer[Route]
    token_in: str
    token_out: str

    def __init__(self, arb_routes: _Optional[_Iterable[_Union[Route, _Mapping]]]=..., token_in: _Optional[str]=..., token_out: _Optional[str]=...) -> None:
        ...

class Route(_message.Message):
    __slots__ = ['trades', 'step_size']
    TRADES_FIELD_NUMBER: _ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: _ClassVar[int]
    trades: _containers.RepeatedCompositeFieldContainer[Trade]
    step_size: str

    def __init__(self, trades: _Optional[_Iterable[_Union[Trade, _Mapping]]]=..., step_size: _Optional[str]=...) -> None:
        ...

class Trade(_message.Message):
    __slots__ = ['pool', 'token_in', 'token_out']
    POOL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_IN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUT_FIELD_NUMBER: _ClassVar[int]
    pool: int
    token_in: str
    token_out: str

    def __init__(self, pool: _Optional[int]=..., token_in: _Optional[str]=..., token_out: _Optional[str]=...) -> None:
        ...

class RouteStatistics(_message.Message):
    __slots__ = ['profits', 'number_of_trades', 'route']
    PROFITS_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_TRADES_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    profits: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    number_of_trades: str
    route: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, profits: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., number_of_trades: _Optional[str]=..., route: _Optional[_Iterable[int]]=...) -> None:
        ...

class PoolWeights(_message.Message):
    __slots__ = ['stable_weight', 'balancer_weight', 'concentrated_weight']
    STABLE_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    BALANCER_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    CONCENTRATED_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    stable_weight: int
    balancer_weight: int
    concentrated_weight: int

    def __init__(self, stable_weight: _Optional[int]=..., balancer_weight: _Optional[int]=..., concentrated_weight: _Optional[int]=...) -> None:
        ...

class BaseDenom(_message.Message):
    __slots__ = ['denom', 'step_size']
    DENOM_FIELD_NUMBER: _ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: _ClassVar[int]
    denom: str
    step_size: str

    def __init__(self, denom: _Optional[str]=..., step_size: _Optional[str]=...) -> None:
        ...