"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....cosmos.gov.v1 import gov_pb2 as cosmos_dot_gov_dot_v1_dot_gov__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from ....cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from ....amino import amino_pb2 as amino_dot_amino__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16cosmos/gov/v1/tx.proto\x12\rcosmos.gov.v1\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x17cosmos/gov/v1/gov.proto\x1a\x14gogoproto/gogo.proto\x1a\x19cosmos_proto/cosmos.proto\x1a\x19google/protobuf/any.proto\x1a\x17cosmos/msg/v1/msg.proto\x1a\x11amino/amino.proto"\x8b\x02\n\x11MsgSubmitProposal\x12&\n\x08messages\x18\x01 \x03(\x0b2\x14.google.protobuf.Any\x12=\n\x0finitial_deposit\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12*\n\x08proposer\x18\x03 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12\x10\n\x08metadata\x18\x04 \x01(\t\x12\r\n\x05title\x18\x05 \x01(\t\x12\x0f\n\x07summary\x18\x06 \x01(\t:1\x82\xe7\xb0*\x08proposer\x8a\xe7\xb0*\x1fcosmos-sdk/v1/MsgSubmitProposal"0\n\x19MsgSubmitProposalResponse\x12\x13\n\x0bproposal_id\x18\x01 \x01(\x04"\xa7\x01\n\x14MsgExecLegacyContent\x12E\n\x07content\x18\x01 \x01(\x0b2\x14.google.protobuf.AnyB\x1e\xca\xb4-\x1acosmos.gov.v1beta1.Content\x12\x11\n\tauthority\x18\x02 \x01(\t:5\x82\xe7\xb0*\tauthority\x8a\xe7\xb0*"cosmos-sdk/v1/MsgExecLegacyContent"\x1e\n\x1cMsgExecLegacyContentResponse"\xc0\x01\n\x07MsgVote\x12)\n\x0bproposal_id\x18\x01 \x01(\x04B\x14\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01\x12\'\n\x05voter\x18\x02 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x12)\n\x06option\x18\x03 \x01(\x0e2\x19.cosmos.gov.v1.VoteOption\x12\x10\n\x08metadata\x18\x04 \x01(\t:$\x82\xe7\xb0*\x05voter\x8a\xe7\xb0*\x15cosmos-sdk/v1/MsgVote"\x11\n\x0fMsgVoteResponse"\xd9\x01\n\x0fMsgVoteWeighted\x12)\n\x0bproposal_id\x18\x01 \x01(\x04B\x14\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01\x12\'\n\x05voter\x18\x02 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x122\n\x07options\x18\x03 \x03(\x0b2!.cosmos.gov.v1.WeightedVoteOption\x12\x10\n\x08metadata\x18\x04 \x01(\t:,\x82\xe7\xb0*\x05voter\x8a\xe7\xb0*\x1dcosmos-sdk/v1/MsgVoteWeighted"\x19\n\x17MsgVoteWeightedResponse"\xc7\x01\n\nMsgDeposit\x12)\n\x0bproposal_id\x18\x01 \x01(\x04B\x14\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01\x12+\n\tdepositor\x18\x02 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x124\n\x06amount\x18\x03 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01:+\x82\xe7\xb0*\tdepositor\x8a\xe7\xb0*\x18cosmos-sdk/v1/MsgDeposit"\x14\n\x12MsgDepositResponse"\xa8\x01\n\x0fMsgUpdateParams\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14cosmos.AddressString\x120\n\x06params\x18\x02 \x01(\x0b2\x15.cosmos.gov.v1.ParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01:6\x82\xe7\xb0*\tauthority\x8a\xe7\xb0*#cosmos-sdk/x/gov/v1/MsgUpdateParams"\x19\n\x17MsgUpdateParamsResponse2\x8a\x04\n\x03Msg\x12\\\n\x0eSubmitProposal\x12 .cosmos.gov.v1.MsgSubmitProposal\x1a(.cosmos.gov.v1.MsgSubmitProposalResponse\x12e\n\x11ExecLegacyContent\x12#.cosmos.gov.v1.MsgExecLegacyContent\x1a+.cosmos.gov.v1.MsgExecLegacyContentResponse\x12>\n\x04Vote\x12\x16.cosmos.gov.v1.MsgVote\x1a\x1e.cosmos.gov.v1.MsgVoteResponse\x12V\n\x0cVoteWeighted\x12\x1e.cosmos.gov.v1.MsgVoteWeighted\x1a&.cosmos.gov.v1.MsgVoteWeightedResponse\x12G\n\x07Deposit\x12\x19.cosmos.gov.v1.MsgDeposit\x1a!.cosmos.gov.v1.MsgDepositResponse\x12V\n\x0cUpdateParams\x12\x1e.cosmos.gov.v1.MsgUpdateParams\x1a&.cosmos.gov.v1.MsgUpdateParamsResponse\x1a\x05\x80\xe7\xb0*\x01B-Z+github.com/cosmos/cosmos-sdk/x/gov/types/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.gov.v1.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z+github.com/cosmos/cosmos-sdk/x/gov/types/v1'
    _MSGSUBMITPROPOSAL.fields_by_name['initial_deposit']._options = None
    _MSGSUBMITPROPOSAL.fields_by_name['initial_deposit']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _MSGSUBMITPROPOSAL.fields_by_name['proposer']._options = None
    _MSGSUBMITPROPOSAL.fields_by_name['proposer']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGSUBMITPROPOSAL._options = None
    _MSGSUBMITPROPOSAL._serialized_options = b'\x82\xe7\xb0*\x08proposer\x8a\xe7\xb0*\x1fcosmos-sdk/v1/MsgSubmitProposal'
    _MSGEXECLEGACYCONTENT.fields_by_name['content']._options = None
    _MSGEXECLEGACYCONTENT.fields_by_name['content']._serialized_options = b'\xca\xb4-\x1acosmos.gov.v1beta1.Content'
    _MSGEXECLEGACYCONTENT._options = None
    _MSGEXECLEGACYCONTENT._serialized_options = b'\x82\xe7\xb0*\tauthority\x8a\xe7\xb0*"cosmos-sdk/v1/MsgExecLegacyContent'
    _MSGVOTE.fields_by_name['proposal_id']._options = None
    _MSGVOTE.fields_by_name['proposal_id']._serialized_options = b'\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01'
    _MSGVOTE.fields_by_name['voter']._options = None
    _MSGVOTE.fields_by_name['voter']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGVOTE._options = None
    _MSGVOTE._serialized_options = b'\x82\xe7\xb0*\x05voter\x8a\xe7\xb0*\x15cosmos-sdk/v1/MsgVote'
    _MSGVOTEWEIGHTED.fields_by_name['proposal_id']._options = None
    _MSGVOTEWEIGHTED.fields_by_name['proposal_id']._serialized_options = b'\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01'
    _MSGVOTEWEIGHTED.fields_by_name['voter']._options = None
    _MSGVOTEWEIGHTED.fields_by_name['voter']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGVOTEWEIGHTED._options = None
    _MSGVOTEWEIGHTED._serialized_options = b'\x82\xe7\xb0*\x05voter\x8a\xe7\xb0*\x1dcosmos-sdk/v1/MsgVoteWeighted'
    _MSGDEPOSIT.fields_by_name['proposal_id']._options = None
    _MSGDEPOSIT.fields_by_name['proposal_id']._serialized_options = b'\xea\xde\x1f\x0bproposal_id\xa8\xe7\xb0*\x01'
    _MSGDEPOSIT.fields_by_name['depositor']._options = None
    _MSGDEPOSIT.fields_by_name['depositor']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGDEPOSIT.fields_by_name['amount']._options = None
    _MSGDEPOSIT.fields_by_name['amount']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _MSGDEPOSIT._options = None
    _MSGDEPOSIT._serialized_options = b'\x82\xe7\xb0*\tdepositor\x8a\xe7\xb0*\x18cosmos-sdk/v1/MsgDeposit'
    _MSGUPDATEPARAMS.fields_by_name['authority']._options = None
    _MSGUPDATEPARAMS.fields_by_name['authority']._serialized_options = b'\xd2\xb4-\x14cosmos.AddressString'
    _MSGUPDATEPARAMS.fields_by_name['params']._options = None
    _MSGUPDATEPARAMS.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01'
    _MSGUPDATEPARAMS._options = None
    _MSGUPDATEPARAMS._serialized_options = b'\x82\xe7\xb0*\tauthority\x8a\xe7\xb0*#cosmos-sdk/x/gov/v1/MsgUpdateParams'
    _MSG._options = None
    _MSG._serialized_options = b'\x80\xe7\xb0*\x01'
    _globals['_MSGSUBMITPROPOSAL']._serialized_start = 219
    _globals['_MSGSUBMITPROPOSAL']._serialized_end = 486
    _globals['_MSGSUBMITPROPOSALRESPONSE']._serialized_start = 488
    _globals['_MSGSUBMITPROPOSALRESPONSE']._serialized_end = 536
    _globals['_MSGEXECLEGACYCONTENT']._serialized_start = 539
    _globals['_MSGEXECLEGACYCONTENT']._serialized_end = 706
    _globals['_MSGEXECLEGACYCONTENTRESPONSE']._serialized_start = 708
    _globals['_MSGEXECLEGACYCONTENTRESPONSE']._serialized_end = 738
    _globals['_MSGVOTE']._serialized_start = 741
    _globals['_MSGVOTE']._serialized_end = 933
    _globals['_MSGVOTERESPONSE']._serialized_start = 935
    _globals['_MSGVOTERESPONSE']._serialized_end = 952
    _globals['_MSGVOTEWEIGHTED']._serialized_start = 955
    _globals['_MSGVOTEWEIGHTED']._serialized_end = 1172
    _globals['_MSGVOTEWEIGHTEDRESPONSE']._serialized_start = 1174
    _globals['_MSGVOTEWEIGHTEDRESPONSE']._serialized_end = 1199
    _globals['_MSGDEPOSIT']._serialized_start = 1202
    _globals['_MSGDEPOSIT']._serialized_end = 1401
    _globals['_MSGDEPOSITRESPONSE']._serialized_start = 1403
    _globals['_MSGDEPOSITRESPONSE']._serialized_end = 1423
    _globals['_MSGUPDATEPARAMS']._serialized_start = 1426
    _globals['_MSGUPDATEPARAMS']._serialized_end = 1594
    _globals['_MSGUPDATEPARAMSRESPONSE']._serialized_start = 1596
    _globals['_MSGUPDATEPARAMSRESPONSE']._serialized_end = 1621
    _globals['_MSG']._serialized_start = 1624
    _globals['_MSG']._serialized_end = 2146