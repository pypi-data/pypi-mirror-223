from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from cosmos.auth.v1beta1 import auth_pb2 as _auth_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class PoolParams(_message.Message):
    __slots__ = ['swap_fee', 'exit_fee']
    SWAP_FEE_FIELD_NUMBER: _ClassVar[int]
    EXIT_FEE_FIELD_NUMBER: _ClassVar[int]
    swap_fee: str
    exit_fee: str

    def __init__(self, swap_fee: _Optional[str]=..., exit_fee: _Optional[str]=...) -> None:
        ...

class Pool(_message.Message):
    __slots__ = ['address', 'id', 'pool_params', 'future_pool_governor', 'total_shares', 'pool_liquidity', 'scaling_factors', 'scaling_factor_controller']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POOL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    FUTURE_POOL_GOVERNOR_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SHARES_FIELD_NUMBER: _ClassVar[int]
    POOL_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    SCALING_FACTORS_FIELD_NUMBER: _ClassVar[int]
    SCALING_FACTOR_CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    pool_params: PoolParams
    future_pool_governor: str
    total_shares: _coin_pb2.Coin
    pool_liquidity: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    scaling_factors: _containers.RepeatedScalarFieldContainer[int]
    scaling_factor_controller: str

    def __init__(self, address: _Optional[str]=..., id: _Optional[int]=..., pool_params: _Optional[_Union[PoolParams, _Mapping]]=..., future_pool_governor: _Optional[str]=..., total_shares: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=..., pool_liquidity: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., scaling_factors: _Optional[_Iterable[int]]=..., scaling_factor_controller: _Optional[str]=...) -> None:
        ...