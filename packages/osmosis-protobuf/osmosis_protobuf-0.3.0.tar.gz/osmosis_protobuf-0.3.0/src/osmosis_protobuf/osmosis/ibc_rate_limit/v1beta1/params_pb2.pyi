from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['contract_address']
    CONTRACT_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    contract_address: str

    def __init__(self, contract_address: _Optional[str]=...) -> None:
        ...