from gogoproto import gogo_pb2 as _gogo_pb2
from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['authorized_tick_spacing', 'authorized_spread_factors', 'balancer_shares_reward_discount', 'authorized_quote_denoms', 'authorized_uptimes', 'is_permissionless_pool_creation_enabled']
    AUTHORIZED_TICK_SPACING_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_SPREAD_FACTORS_FIELD_NUMBER: _ClassVar[int]
    BALANCER_SHARES_REWARD_DISCOUNT_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_QUOTE_DENOMS_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_UPTIMES_FIELD_NUMBER: _ClassVar[int]
    IS_PERMISSIONLESS_POOL_CREATION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    authorized_tick_spacing: _containers.RepeatedScalarFieldContainer[int]
    authorized_spread_factors: _containers.RepeatedScalarFieldContainer[str]
    balancer_shares_reward_discount: str
    authorized_quote_denoms: _containers.RepeatedScalarFieldContainer[str]
    authorized_uptimes: _containers.RepeatedCompositeFieldContainer[_duration_pb2.Duration]
    is_permissionless_pool_creation_enabled: bool

    def __init__(self, authorized_tick_spacing: _Optional[_Iterable[int]]=..., authorized_spread_factors: _Optional[_Iterable[str]]=..., balancer_shares_reward_discount: _Optional[str]=..., authorized_quote_denoms: _Optional[_Iterable[str]]=..., authorized_uptimes: _Optional[_Iterable[_Union[_duration_pb2.Duration, _Mapping]]]=..., is_permissionless_pool_creation_enabled: bool=...) -> None:
        ...