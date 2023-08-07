"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from .....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9osmosis/cosmwasmpool/v1beta1/model/module_query_msg.proto\x12\x1cosmosis.cosmwasmpool.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\xa1\x01\n\x11CalcOutAmtGivenIn\x121\n\x08token_in\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12\x17\n\x0ftoken_out_denom\x18\x02 \x01(\t\x12@\n\x08swap_fee\x18\x03 \x01(\tB.\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec"p\n\x18CalcOutAmtGivenInRequest\x12T\n\x15calc_out_amt_given_in\x18\x01 \x01(\x0b2/.osmosis.cosmwasmpool.v1beta1.CalcOutAmtGivenInB\x04\xc8\xde\x1f\x00"O\n\x19CalcOutAmtGivenInResponse\x122\n\ttoken_out\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00"\xa1\x01\n\x11CalcInAmtGivenOut\x122\n\ttoken_out\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12\x16\n\x0etoken_in_denom\x18\x02 \x01(\t\x12@\n\x08swap_fee\x18\x03 \x01(\tB.\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec"p\n\x18CalcInAmtGivenOutRequest\x12T\n\x15calc_in_amt_given_out\x18\x01 \x01(\x0b2/.osmosis.cosmwasmpool.v1beta1.CalcInAmtGivenOutB\x04\xc8\xde\x1f\x00"N\n\x19CalcInAmtGivenOutResponse\x121\n\x08token_in\x18\x01 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00BAZ?github.com/osmosis-labs/osmosis/v16/x/cosmwasmpool/cosmwasm/msgb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.cosmwasmpool.v1beta1.model.module_query_msg_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z?github.com/osmosis-labs/osmosis/v16/x/cosmwasmpool/cosmwasm/msg'
    _CALCOUTAMTGIVENIN.fields_by_name['token_in']._options = None
    _CALCOUTAMTGIVENIN.fields_by_name['token_in']._serialized_options = b'\xc8\xde\x1f\x00'
    _CALCOUTAMTGIVENIN.fields_by_name['swap_fee']._options = None
    _CALCOUTAMTGIVENIN.fields_by_name['swap_fee']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec'
    _CALCOUTAMTGIVENINREQUEST.fields_by_name['calc_out_amt_given_in']._options = None
    _CALCOUTAMTGIVENINREQUEST.fields_by_name['calc_out_amt_given_in']._serialized_options = b'\xc8\xde\x1f\x00'
    _CALCOUTAMTGIVENINRESPONSE.fields_by_name['token_out']._options = None
    _CALCOUTAMTGIVENINRESPONSE.fields_by_name['token_out']._serialized_options = b'\xc8\xde\x1f\x00'
    _CALCINAMTGIVENOUT.fields_by_name['token_out']._options = None
    _CALCINAMTGIVENOUT.fields_by_name['token_out']._serialized_options = b'\xc8\xde\x1f\x00'
    _CALCINAMTGIVENOUT.fields_by_name['swap_fee']._options = None
    _CALCINAMTGIVENOUT.fields_by_name['swap_fee']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec'
    _CALCINAMTGIVENOUTREQUEST.fields_by_name['calc_in_amt_given_out']._options = None
    _CALCINAMTGIVENOUTREQUEST.fields_by_name['calc_in_amt_given_out']._serialized_options = b'\xc8\xde\x1f\x00'
    _CALCINAMTGIVENOUTRESPONSE.fields_by_name['token_in']._options = None
    _CALCINAMTGIVENOUTRESPONSE.fields_by_name['token_in']._serialized_options = b'\xc8\xde\x1f\x00'
    _globals['_CALCOUTAMTGIVENIN']._serialized_start = 146
    _globals['_CALCOUTAMTGIVENIN']._serialized_end = 307
    _globals['_CALCOUTAMTGIVENINREQUEST']._serialized_start = 309
    _globals['_CALCOUTAMTGIVENINREQUEST']._serialized_end = 421
    _globals['_CALCOUTAMTGIVENINRESPONSE']._serialized_start = 423
    _globals['_CALCOUTAMTGIVENINRESPONSE']._serialized_end = 502
    _globals['_CALCINAMTGIVENOUT']._serialized_start = 505
    _globals['_CALCINAMTGIVENOUT']._serialized_end = 666
    _globals['_CALCINAMTGIVENOUTREQUEST']._serialized_start = 668
    _globals['_CALCINAMTGIVENOUTREQUEST']._serialized_end = 780
    _globals['_CALCINAMTGIVENOUTRESPONSE']._serialized_start = 782
    _globals['_CALCINAMTGIVENOUTRESPONSE']._serialized_end = 860