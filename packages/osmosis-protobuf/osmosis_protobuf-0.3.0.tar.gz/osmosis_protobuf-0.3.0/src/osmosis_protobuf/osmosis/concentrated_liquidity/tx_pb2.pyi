from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgCreatePosition(_message.Message):
    __slots__ = ['pool_id', 'sender', 'lower_tick', 'upper_tick', 'tokens_provided', 'token_min_amount0', 'token_min_amount1']
    POOL_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    LOWER_TICK_FIELD_NUMBER: _ClassVar[int]
    UPPER_TICK_FIELD_NUMBER: _ClassVar[int]
    TOKENS_PROVIDED_FIELD_NUMBER: _ClassVar[int]
    TOKEN_MIN_AMOUNT0_FIELD_NUMBER: _ClassVar[int]
    TOKEN_MIN_AMOUNT1_FIELD_NUMBER: _ClassVar[int]
    pool_id: int
    sender: str
    lower_tick: int
    upper_tick: int
    tokens_provided: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    token_min_amount0: str
    token_min_amount1: str

    def __init__(self, pool_id: _Optional[int]=..., sender: _Optional[str]=..., lower_tick: _Optional[int]=..., upper_tick: _Optional[int]=..., tokens_provided: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., token_min_amount0: _Optional[str]=..., token_min_amount1: _Optional[str]=...) -> None:
        ...

class MsgCreatePositionResponse(_message.Message):
    __slots__ = ['position_id', 'amount0', 'amount1', 'liquidity_created', 'lower_tick', 'upper_tick']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT0_FIELD_NUMBER: _ClassVar[int]
    AMOUNT1_FIELD_NUMBER: _ClassVar[int]
    LIQUIDITY_CREATED_FIELD_NUMBER: _ClassVar[int]
    LOWER_TICK_FIELD_NUMBER: _ClassVar[int]
    UPPER_TICK_FIELD_NUMBER: _ClassVar[int]
    position_id: int
    amount0: str
    amount1: str
    liquidity_created: str
    lower_tick: int
    upper_tick: int

    def __init__(self, position_id: _Optional[int]=..., amount0: _Optional[str]=..., amount1: _Optional[str]=..., liquidity_created: _Optional[str]=..., lower_tick: _Optional[int]=..., upper_tick: _Optional[int]=...) -> None:
        ...

class MsgAddToPosition(_message.Message):
    __slots__ = ['position_id', 'sender', 'amount0', 'amount1', 'token_min_amount0', 'token_min_amount1']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    AMOUNT0_FIELD_NUMBER: _ClassVar[int]
    AMOUNT1_FIELD_NUMBER: _ClassVar[int]
    TOKEN_MIN_AMOUNT0_FIELD_NUMBER: _ClassVar[int]
    TOKEN_MIN_AMOUNT1_FIELD_NUMBER: _ClassVar[int]
    position_id: int
    sender: str
    amount0: str
    amount1: str
    token_min_amount0: str
    token_min_amount1: str

    def __init__(self, position_id: _Optional[int]=..., sender: _Optional[str]=..., amount0: _Optional[str]=..., amount1: _Optional[str]=..., token_min_amount0: _Optional[str]=..., token_min_amount1: _Optional[str]=...) -> None:
        ...

class MsgAddToPositionResponse(_message.Message):
    __slots__ = ['position_id', 'amount0', 'amount1']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT0_FIELD_NUMBER: _ClassVar[int]
    AMOUNT1_FIELD_NUMBER: _ClassVar[int]
    position_id: int
    amount0: str
    amount1: str

    def __init__(self, position_id: _Optional[int]=..., amount0: _Optional[str]=..., amount1: _Optional[str]=...) -> None:
        ...

class MsgWithdrawPosition(_message.Message):
    __slots__ = ['position_id', 'sender', 'liquidity_amount']
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    LIQUIDITY_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    position_id: int
    sender: str
    liquidity_amount: str

    def __init__(self, position_id: _Optional[int]=..., sender: _Optional[str]=..., liquidity_amount: _Optional[str]=...) -> None:
        ...

class MsgWithdrawPositionResponse(_message.Message):
    __slots__ = ['amount0', 'amount1']
    AMOUNT0_FIELD_NUMBER: _ClassVar[int]
    AMOUNT1_FIELD_NUMBER: _ClassVar[int]
    amount0: str
    amount1: str

    def __init__(self, amount0: _Optional[str]=..., amount1: _Optional[str]=...) -> None:
        ...

class MsgCollectSpreadRewards(_message.Message):
    __slots__ = ['position_ids', 'sender']
    POSITION_IDS_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    position_ids: _containers.RepeatedScalarFieldContainer[int]
    sender: str

    def __init__(self, position_ids: _Optional[_Iterable[int]]=..., sender: _Optional[str]=...) -> None:
        ...

class MsgCollectSpreadRewardsResponse(_message.Message):
    __slots__ = ['collected_spread_rewards']
    COLLECTED_SPREAD_REWARDS_FIELD_NUMBER: _ClassVar[int]
    collected_spread_rewards: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, collected_spread_rewards: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgCollectIncentives(_message.Message):
    __slots__ = ['position_ids', 'sender']
    POSITION_IDS_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    position_ids: _containers.RepeatedScalarFieldContainer[int]
    sender: str

    def __init__(self, position_ids: _Optional[_Iterable[int]]=..., sender: _Optional[str]=...) -> None:
        ...

class MsgCollectIncentivesResponse(_message.Message):
    __slots__ = ['collected_incentives', 'forfeited_incentives']
    COLLECTED_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    FORFEITED_INCENTIVES_FIELD_NUMBER: _ClassVar[int]
    collected_incentives: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]
    forfeited_incentives: _containers.RepeatedCompositeFieldContainer[_coin_pb2.Coin]

    def __init__(self, collected_incentives: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=..., forfeited_incentives: _Optional[_Iterable[_Union[_coin_pb2.Coin, _Mapping]]]=...) -> None:
        ...

class MsgFungifyChargedPositions(_message.Message):
    __slots__ = ['position_ids', 'sender']
    POSITION_IDS_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    position_ids: _containers.RepeatedScalarFieldContainer[int]
    sender: str

    def __init__(self, position_ids: _Optional[_Iterable[int]]=..., sender: _Optional[str]=...) -> None:
        ...

class MsgFungifyChargedPositionsResponse(_message.Message):
    __slots__ = ['new_position_id']
    NEW_POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    new_position_id: int

    def __init__(self, new_position_id: _Optional[int]=...) -> None:
        ...