"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....osmosis.gamm.v1beta1 import genesis_pb2 as osmosis_dot_gamm_dot_v1beta1_dot_genesis__pb2
from ....osmosis.gamm.v1beta1 import shared_pb2 as osmosis_dot_gamm_dot_v1beta1_dot_shared__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1eosmosis/gamm/v1beta1/gov.proto\x12\x14osmosis.gamm.v1beta1\x1a\x14gogoproto/gogo.proto\x1a"osmosis/gamm/v1beta1/genesis.proto\x1a!osmosis/gamm/v1beta1/shared.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x11amino/amino.proto"\xea\x01\n\x1fReplaceMigrationRecordsProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12K\n\x07records\x18\x03 \x03(\x0b24.osmosis.gamm.v1beta1.BalancerToConcentratedPoolLinkB\x04\xc8\xde\x1f\x00:V\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*\'osmosis/ReplaceMigrationRecordsProposal"\xe8\x01\n\x1eUpdateMigrationRecordsProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12K\n\x07records\x18\x03 \x03(\x0b24.osmosis.gamm.v1beta1.BalancerToConcentratedPoolLinkB\x04\xc8\xde\x1f\x00:U\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*&osmosis/UpdateMigrationRecordsProposalB2Z0github.com/osmosis-labs/osmosis/v16/x/gamm/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.gamm.v1beta1.gov_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/osmosis-labs/osmosis/v16/x/gamm/types'
    _REPLACEMIGRATIONRECORDSPROPOSAL.fields_by_name['records']._options = None
    _REPLACEMIGRATIONRECORDSPROPOSAL.fields_by_name['records']._serialized_options = b'\xc8\xde\x1f\x00'
    _REPLACEMIGRATIONRECORDSPROPOSAL._options = None
    _REPLACEMIGRATIONRECORDSPROPOSAL._serialized_options = b"\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*'osmosis/ReplaceMigrationRecordsProposal"
    _UPDATEMIGRATIONRECORDSPROPOSAL.fields_by_name['records']._options = None
    _UPDATEMIGRATIONRECORDSPROPOSAL.fields_by_name['records']._serialized_options = b'\xc8\xde\x1f\x00'
    _UPDATEMIGRATIONRECORDSPROPOSAL._options = None
    _UPDATEMIGRATIONRECORDSPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01\xca\xb4-\x1acosmos.gov.v1beta1.Content\x8a\xe7\xb0*&osmosis/UpdateMigrationRecordsProposal'
    _globals['_REPLACEMIGRATIONRECORDSPROPOSAL']._serialized_start = 196
    _globals['_REPLACEMIGRATIONRECORDSPROPOSAL']._serialized_end = 430
    _globals['_UPDATEMIGRATIONRECORDSPROPOSAL']._serialized_start = 433
    _globals['_UPDATEMIGRATIONRECORDSPROPOSAL']._serialized_end = 665