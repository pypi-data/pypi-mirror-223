from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from cosmos.base.v1beta1 import coin_pb2 as _coin_pb2
from osmosis.valset_pref.v1beta1 import state_pb2 as _state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class MsgSetValidatorSetPreference(_message.Message):
    __slots__ = ['delegator', 'preferences']
    DELEGATOR_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    delegator: str
    preferences: _containers.RepeatedCompositeFieldContainer[_state_pb2.ValidatorPreference]

    def __init__(self, delegator: _Optional[str]=..., preferences: _Optional[_Iterable[_Union[_state_pb2.ValidatorPreference, _Mapping]]]=...) -> None:
        ...

class MsgSetValidatorSetPreferenceResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgDelegateToValidatorSet(_message.Message):
    __slots__ = ['delegator', 'coin']
    DELEGATOR_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    delegator: str
    coin: _coin_pb2.Coin

    def __init__(self, delegator: _Optional[str]=..., coin: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class MsgDelegateToValidatorSetResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgUndelegateFromValidatorSet(_message.Message):
    __slots__ = ['delegator', 'coin']
    DELEGATOR_FIELD_NUMBER: _ClassVar[int]
    COIN_FIELD_NUMBER: _ClassVar[int]
    delegator: str
    coin: _coin_pb2.Coin

    def __init__(self, delegator: _Optional[str]=..., coin: _Optional[_Union[_coin_pb2.Coin, _Mapping]]=...) -> None:
        ...

class MsgUndelegateFromValidatorSetResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgRedelegateValidatorSet(_message.Message):
    __slots__ = ['delegator', 'preferences']
    DELEGATOR_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    delegator: str
    preferences: _containers.RepeatedCompositeFieldContainer[_state_pb2.ValidatorPreference]

    def __init__(self, delegator: _Optional[str]=..., preferences: _Optional[_Iterable[_Union[_state_pb2.ValidatorPreference, _Mapping]]]=...) -> None:
        ...

class MsgRedelegateValidatorSetResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgWithdrawDelegationRewards(_message.Message):
    __slots__ = ['delegator']
    DELEGATOR_FIELD_NUMBER: _ClassVar[int]
    delegator: str

    def __init__(self, delegator: _Optional[str]=...) -> None:
        ...

class MsgWithdrawDelegationRewardsResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...

class MsgDelegateBondedTokens(_message.Message):
    __slots__ = ['delegator', 'lockID']
    DELEGATOR_FIELD_NUMBER: _ClassVar[int]
    LOCKID_FIELD_NUMBER: _ClassVar[int]
    delegator: str
    lockID: int

    def __init__(self, delegator: _Optional[str]=..., lockID: _Optional[int]=...) -> None:
        ...

class MsgDelegateBondedTokensResponse(_message.Message):
    __slots__ = []

    def __init__(self) -> None:
        ...