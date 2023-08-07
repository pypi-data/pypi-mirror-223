"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ...amino import amino_pb2 as amino_dot_amino__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ...cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'osmosis/concentrated-liquidity/tx.proto\x12%osmosis.concentratedliquidity.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x11amino/amino.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\x86\x04\n\x11MsgCreatePosition\x12#\n\x07pool_id\x18\x01 \x01(\x04B\x12\xf2\xde\x1f\x0eyaml:"pool_id"\x12!\n\x06sender\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12)\n\nlower_tick\x18\x03 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"lower_tick"\x12)\n\nupper_tick\x18\x04 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"upper_tick"\x12d\n\x0ftokens_provided\x18\x05 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12e\n\x11token_min_amount0\x18\x06 \x01(\tBJ\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x18yaml:"token_min_amount0"\x12e\n\x11token_min_amount1\x18\x07 \x01(\tBJ\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x18yaml:"token_min_amount1":\x1f\x8a\xe7\xb0*\x1aosmosis/cl-create-position"\xab\x03\n\x19MsgCreatePositionResponse\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id"\x12Q\n\x07amount0\x18\x02 \x01(\tB@\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount0"\x12Q\n\x07amount1\x18\x03 \x01(\tB@\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount1"\x12e\n\x11liquidity_created\x18\x05 \x01(\tBJ\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x18yaml:"liquidity_created"\x12)\n\nlower_tick\x18\x06 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"lower_tick"\x12)\n\nupper_tick\x18\x07 \x01(\x03B\x15\xf2\xde\x1f\x11yaml:"upper_tick""\xf9\x03\n\x10MsgAddToPosition\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id"\x12!\n\x06sender\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12R\n\x07amount0\x18\x03 \x01(\tBA\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0fyaml:"amount_0"\x12R\n\x07amount1\x18\x04 \x01(\tBA\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0fyaml:"amount_1"\x12e\n\x11token_min_amount0\x18\x05 \x01(\tBJ\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x18yaml:"token_min_amount0"\x12e\n\x11token_min_amount1\x18\x06 \x01(\tBJ\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x18yaml:"token_min_amount1":\x1f\x8a\xe7\xb0*\x1aosmosis/cl-add-to-position"\xed\x01\n\x18MsgAddToPositionResponse\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id"\x12Q\n\x07amount0\x18\x02 \x01(\tB@\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount0"\x12Q\n\x07amount1\x18\x03 \x01(\tB@\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount1""\xed\x01\n\x13MsgWithdrawPosition\x12+\n\x0bposition_id\x18\x01 \x01(\x04B\x16\xf2\xde\x1f\x12yaml:"position_id"\x12!\n\x06sender\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender"\x12c\n\x10liquidity_amount\x18\x03 \x01(\tBI\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x17yaml:"liquidity_amount":!\x8a\xe7\xb0*\x1cosmosis/cl-withdraw-position"\xc3\x01\n\x1bMsgWithdrawPositionResponse\x12Q\n\x07amount0\x18\x01 \x01(\tB@\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount0"\x12Q\n\x07amount1\x18\x02 \x01(\tB@\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount1""\x8b\x01\n\x17MsgCollectSpreadRewards\x12-\n\x0cposition_ids\x18\x01 \x03(\x04B\x17\xf2\xde\x1f\x13yaml:"position_ids"\x12!\n\x06sender\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender":\x1e\x8a\xe7\xb0*\x19osmosis/cl-col-sp-rewards"\xb4\x01\n\x1fMsgCollectSpreadRewardsResponse\x12\x90\x01\n\x18collected_spread_rewards\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBS\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"collected_spread_rewards"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins"\x8c\x01\n\x14MsgCollectIncentives\x12-\n\x0cposition_ids\x18\x01 \x03(\x04B\x17\xf2\xde\x1f\x13yaml:"position_ids"\x12!\n\x06sender\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender":"\x8a\xe7\xb0*\x1dosmosis/cl-collect-incentives"\xb4\x02\n\x1cMsgCollectIncentivesResponse\x12\x88\x01\n\x14collected_incentives\x18\x01 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBO\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"collected_incentives"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12\x88\x01\n\x14forfeited_incentives\x18\x02 \x03(\x0b2\x19.cosmos.base.v1beta1.CoinBO\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"forfeited_incentives"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins"\x99\x01\n\x1aMsgFungifyChargedPositions\x12-\n\x0cposition_ids\x18\x01 \x03(\x04B\x17\xf2\xde\x1f\x13yaml:"position_ids"\x12!\n\x06sender\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"sender":)\x8a\xe7\xb0*$osmosis/cl-fungify-charged-positions"Y\n"MsgFungifyChargedPositionsResponse\x123\n\x0fnew_position_id\x18\x01 \x01(\x04B\x1a\xf2\xde\x1f\x16yaml:"new_position_id"2\xee\x05\n\x03Msg\x12\x8c\x01\n\x0eCreatePosition\x128.osmosis.concentratedliquidity.v1beta1.MsgCreatePosition\x1a@.osmosis.concentratedliquidity.v1beta1.MsgCreatePositionResponse\x12\x92\x01\n\x10WithdrawPosition\x12:.osmosis.concentratedliquidity.v1beta1.MsgWithdrawPosition\x1aB.osmosis.concentratedliquidity.v1beta1.MsgWithdrawPositionResponse\x12\x89\x01\n\rAddToPosition\x127.osmosis.concentratedliquidity.v1beta1.MsgAddToPosition\x1a?.osmosis.concentratedliquidity.v1beta1.MsgAddToPositionResponse\x12\x9e\x01\n\x14CollectSpreadRewards\x12>.osmosis.concentratedliquidity.v1beta1.MsgCollectSpreadRewards\x1aF.osmosis.concentratedliquidity.v1beta1.MsgCollectSpreadRewardsResponse\x12\x95\x01\n\x11CollectIncentives\x12;.osmosis.concentratedliquidity.v1beta1.MsgCollectIncentives\x1aC.osmosis.concentratedliquidity.v1beta1.MsgCollectIncentivesResponseBDZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.concentrated_liquidity.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/types'
    _MSGCREATEPOSITION.fields_by_name['pool_id']._options = None
    _MSGCREATEPOSITION.fields_by_name['pool_id']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"pool_id"'
    _MSGCREATEPOSITION.fields_by_name['sender']._options = None
    _MSGCREATEPOSITION.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGCREATEPOSITION.fields_by_name['lower_tick']._options = None
    _MSGCREATEPOSITION.fields_by_name['lower_tick']._serialized_options = b'\xf2\xde\x1f\x11yaml:"lower_tick"'
    _MSGCREATEPOSITION.fields_by_name['upper_tick']._options = None
    _MSGCREATEPOSITION.fields_by_name['upper_tick']._serialized_options = b'\xf2\xde\x1f\x11yaml:"upper_tick"'
    _MSGCREATEPOSITION.fields_by_name['tokens_provided']._options = None
    _MSGCREATEPOSITION.fields_by_name['tokens_provided']._serialized_options = b'\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGCREATEPOSITION.fields_by_name['token_min_amount0']._options = None
    _MSGCREATEPOSITION.fields_by_name['token_min_amount0']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x18yaml:"token_min_amount0"'
    _MSGCREATEPOSITION.fields_by_name['token_min_amount1']._options = None
    _MSGCREATEPOSITION.fields_by_name['token_min_amount1']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x18yaml:"token_min_amount1"'
    _MSGCREATEPOSITION._options = None
    _MSGCREATEPOSITION._serialized_options = b'\x8a\xe7\xb0*\x1aosmosis/cl-create-position'
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['position_id']._options = None
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['amount0']._options = None
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['amount0']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount0"'
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['amount1']._options = None
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['amount1']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount1"'
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['liquidity_created']._options = None
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['liquidity_created']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x18yaml:"liquidity_created"'
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['lower_tick']._options = None
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['lower_tick']._serialized_options = b'\xf2\xde\x1f\x11yaml:"lower_tick"'
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['upper_tick']._options = None
    _MSGCREATEPOSITIONRESPONSE.fields_by_name['upper_tick']._serialized_options = b'\xf2\xde\x1f\x11yaml:"upper_tick"'
    _MSGADDTOPOSITION.fields_by_name['position_id']._options = None
    _MSGADDTOPOSITION.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _MSGADDTOPOSITION.fields_by_name['sender']._options = None
    _MSGADDTOPOSITION.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGADDTOPOSITION.fields_by_name['amount0']._options = None
    _MSGADDTOPOSITION.fields_by_name['amount0']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0fyaml:"amount_0"'
    _MSGADDTOPOSITION.fields_by_name['amount1']._options = None
    _MSGADDTOPOSITION.fields_by_name['amount1']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0fyaml:"amount_1"'
    _MSGADDTOPOSITION.fields_by_name['token_min_amount0']._options = None
    _MSGADDTOPOSITION.fields_by_name['token_min_amount0']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x18yaml:"token_min_amount0"'
    _MSGADDTOPOSITION.fields_by_name['token_min_amount1']._options = None
    _MSGADDTOPOSITION.fields_by_name['token_min_amount1']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x18yaml:"token_min_amount1"'
    _MSGADDTOPOSITION._options = None
    _MSGADDTOPOSITION._serialized_options = b'\x8a\xe7\xb0*\x1aosmosis/cl-add-to-position'
    _MSGADDTOPOSITIONRESPONSE.fields_by_name['position_id']._options = None
    _MSGADDTOPOSITIONRESPONSE.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _MSGADDTOPOSITIONRESPONSE.fields_by_name['amount0']._options = None
    _MSGADDTOPOSITIONRESPONSE.fields_by_name['amount0']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount0"'
    _MSGADDTOPOSITIONRESPONSE.fields_by_name['amount1']._options = None
    _MSGADDTOPOSITIONRESPONSE.fields_by_name['amount1']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount1"'
    _MSGWITHDRAWPOSITION.fields_by_name['position_id']._options = None
    _MSGWITHDRAWPOSITION.fields_by_name['position_id']._serialized_options = b'\xf2\xde\x1f\x12yaml:"position_id"'
    _MSGWITHDRAWPOSITION.fields_by_name['sender']._options = None
    _MSGWITHDRAWPOSITION.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGWITHDRAWPOSITION.fields_by_name['liquidity_amount']._options = None
    _MSGWITHDRAWPOSITION.fields_by_name['liquidity_amount']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x17yaml:"liquidity_amount"'
    _MSGWITHDRAWPOSITION._options = None
    _MSGWITHDRAWPOSITION._serialized_options = b'\x8a\xe7\xb0*\x1cosmosis/cl-withdraw-position'
    _MSGWITHDRAWPOSITIONRESPONSE.fields_by_name['amount0']._options = None
    _MSGWITHDRAWPOSITIONRESPONSE.fields_by_name['amount0']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount0"'
    _MSGWITHDRAWPOSITIONRESPONSE.fields_by_name['amount1']._options = None
    _MSGWITHDRAWPOSITIONRESPONSE.fields_by_name['amount1']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x0eyaml:"amount1"'
    _MSGCOLLECTSPREADREWARDS.fields_by_name['position_ids']._options = None
    _MSGCOLLECTSPREADREWARDS.fields_by_name['position_ids']._serialized_options = b'\xf2\xde\x1f\x13yaml:"position_ids"'
    _MSGCOLLECTSPREADREWARDS.fields_by_name['sender']._options = None
    _MSGCOLLECTSPREADREWARDS.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGCOLLECTSPREADREWARDS._options = None
    _MSGCOLLECTSPREADREWARDS._serialized_options = b'\x8a\xe7\xb0*\x19osmosis/cl-col-sp-rewards'
    _MSGCOLLECTSPREADREWARDSRESPONSE.fields_by_name['collected_spread_rewards']._options = None
    _MSGCOLLECTSPREADREWARDSRESPONSE.fields_by_name['collected_spread_rewards']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1fyaml:"collected_spread_rewards"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGCOLLECTINCENTIVES.fields_by_name['position_ids']._options = None
    _MSGCOLLECTINCENTIVES.fields_by_name['position_ids']._serialized_options = b'\xf2\xde\x1f\x13yaml:"position_ids"'
    _MSGCOLLECTINCENTIVES.fields_by_name['sender']._options = None
    _MSGCOLLECTINCENTIVES.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGCOLLECTINCENTIVES._options = None
    _MSGCOLLECTINCENTIVES._serialized_options = b'\x8a\xe7\xb0*\x1dosmosis/cl-collect-incentives'
    _MSGCOLLECTINCENTIVESRESPONSE.fields_by_name['collected_incentives']._options = None
    _MSGCOLLECTINCENTIVESRESPONSE.fields_by_name['collected_incentives']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"collected_incentives"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGCOLLECTINCENTIVESRESPONSE.fields_by_name['forfeited_incentives']._options = None
    _MSGCOLLECTINCENTIVESRESPONSE.fields_by_name['forfeited_incentives']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1byaml:"forfeited_incentives"\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins'
    _MSGFUNGIFYCHARGEDPOSITIONS.fields_by_name['position_ids']._options = None
    _MSGFUNGIFYCHARGEDPOSITIONS.fields_by_name['position_ids']._serialized_options = b'\xf2\xde\x1f\x13yaml:"position_ids"'
    _MSGFUNGIFYCHARGEDPOSITIONS.fields_by_name['sender']._options = None
    _MSGFUNGIFYCHARGEDPOSITIONS.fields_by_name['sender']._serialized_options = b'\xf2\xde\x1f\ryaml:"sender"'
    _MSGFUNGIFYCHARGEDPOSITIONS._options = None
    _MSGFUNGIFYCHARGEDPOSITIONS._serialized_options = b'\x8a\xe7\xb0*$osmosis/cl-fungify-charged-positions'
    _MSGFUNGIFYCHARGEDPOSITIONSRESPONSE.fields_by_name['new_position_id']._options = None
    _MSGFUNGIFYCHARGEDPOSITIONSRESPONSE.fields_by_name['new_position_id']._serialized_options = b'\xf2\xde\x1f\x16yaml:"new_position_id"'
    _globals['_MSGCREATEPOSITION']._serialized_start = 221
    _globals['_MSGCREATEPOSITION']._serialized_end = 739
    _globals['_MSGCREATEPOSITIONRESPONSE']._serialized_start = 742
    _globals['_MSGCREATEPOSITIONRESPONSE']._serialized_end = 1169
    _globals['_MSGADDTOPOSITION']._serialized_start = 1172
    _globals['_MSGADDTOPOSITION']._serialized_end = 1677
    _globals['_MSGADDTOPOSITIONRESPONSE']._serialized_start = 1680
    _globals['_MSGADDTOPOSITIONRESPONSE']._serialized_end = 1917
    _globals['_MSGWITHDRAWPOSITION']._serialized_start = 1920
    _globals['_MSGWITHDRAWPOSITION']._serialized_end = 2157
    _globals['_MSGWITHDRAWPOSITIONRESPONSE']._serialized_start = 2160
    _globals['_MSGWITHDRAWPOSITIONRESPONSE']._serialized_end = 2355
    _globals['_MSGCOLLECTSPREADREWARDS']._serialized_start = 2358
    _globals['_MSGCOLLECTSPREADREWARDS']._serialized_end = 2497
    _globals['_MSGCOLLECTSPREADREWARDSRESPONSE']._serialized_start = 2500
    _globals['_MSGCOLLECTSPREADREWARDSRESPONSE']._serialized_end = 2680
    _globals['_MSGCOLLECTINCENTIVES']._serialized_start = 2683
    _globals['_MSGCOLLECTINCENTIVES']._serialized_end = 2823
    _globals['_MSGCOLLECTINCENTIVESRESPONSE']._serialized_start = 2826
    _globals['_MSGCOLLECTINCENTIVESRESPONSE']._serialized_end = 3134
    _globals['_MSGFUNGIFYCHARGEDPOSITIONS']._serialized_start = 3137
    _globals['_MSGFUNGIFYCHARGEDPOSITIONS']._serialized_end = 3290
    _globals['_MSGFUNGIFYCHARGEDPOSITIONSRESPONSE']._serialized_start = 3292
    _globals['_MSGFUNGIFYCHARGEDPOSITIONSRESPONSE']._serialized_end = 3381
    _globals['_MSG']._serialized_start = 3384
    _globals['_MSG']._serialized_end = 4134