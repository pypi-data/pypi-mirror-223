from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from osmosis.gamm.pool_models.stableswap import stableswap_pool_pb2 as _stableswap_pool_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreateStableswapPool(_message.Message):
    __slots__ = ['sender', 'pool_params', 'initial_pool_liquidity', 'scaling_factors', 'future_pool_governor', 'scaling_factor_controller']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_PARAMS_FIELD_NUMBER: _ClassVar[int]
    INITIAL_POOL_LIQUIDITY_FIELD_NUMBER: _ClassVar[int]
    SCALING_FACTORS_FIELD_NUMBER: _ClassVar[int]
    FUTURE_POOL_GOVERNOR_FIELD_NUMBER: _ClassVar[int]
    SCALING_FACTOR_CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_params: _stableswap_pool_pb2.PoolParams
    initial_pool_liquidity: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    scaling_factors: _containers.RepeatedScalarFieldContainer[int]
    future_pool_governor: str
    scaling_factor_controller: str

    def __init__(self, sender: _Optional[str]=..., pool_params: _Optional[_Union[_stableswap_pool_pb2.PoolParams, _Mapping]]=..., initial_pool_liquidity: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., scaling_factors: _Optional[_Iterable[int]]=..., future_pool_governor: _Optional[str]=..., scaling_factor_controller: _Optional[str]=...) -> None:
        ...

class MsgCreateStableswapPoolResponse(_message.Message):
    __slots__ = ['pool_id']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    pool_id: int

    def __init__(self, pool_id: _Optional[int]=...) -> None:
        ...

class MsgStableSwapAdjustScalingFactors(_message.Message):
    __slots__ = ['sender', 'pool_id', 'scaling_factors']
    SENDER_FIELD_NUMBER: _ClassVar[int]
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    SCALING_FACTORS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    pool_id: int
    scaling_factors: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, sender: _Optional[str]=..., pool_id: _Optional[int]=..., scaling_factors: _Optional[_Iterable[int]]=...) -> None:
        ...

class MsgStableSwapAdjustScalingFactorsResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...