"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from ...cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5osmosis/concentrated-liquidity/incentive_record.proto\x12%osmosis.concentratedliquidity.v1beta1\x1a\x19cosmos_proto/cosmos.proto\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1ecosmos/base/v1beta1/coin.proto"\xa0\x02\n\x0fIncentiveRecord\x12-\n\x0cincentive_id\x18\x01 \x01(\x04B\x17\xf2\xde\x1f\x13yaml:"incentive_id"\x12\x0f\n\x07pool_id\x18\x02 \x01(\x04\x12\x7f\n\x15incentive_record_body\x18\x04 \x01(\x0b2:.osmosis.concentratedliquidity.v1beta1.IncentiveRecordBodyB$\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"incentive_record_body"\x12L\n\nmin_uptime\x18\x05 \x01(\x0b2\x19.google.protobuf.DurationB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"min_uptime"\x98\xdf\x1f\x01"\xc8\x02\n\x13IncentiveRecordBody\x12\x82\x01\n\x0eremaining_coin\x18\x01 \x01(\x0b2\x1c.cosmos.base.v1beta1.DecCoinBL\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"remaining_coins"\xaa\xdf\x1f*github.com/cosmos/cosmos-sdk/types.DecCoin\x12]\n\remission_rate\x18\x02 \x01(\tBF\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"emission_rate"\x12M\n\nstart_time\x18\x03 \x01(\x0b2\x1a.google.protobuf.TimestampB\x1d\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01BDZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.concentrated_liquidity.incentive_record_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/types'
    _INCENTIVERECORD.fields_by_name['incentive_id']._options = None
    _INCENTIVERECORD.fields_by_name['incentive_id']._serialized_options = b'\xf2\xde\x1f\x13yaml:"incentive_id"'
    _INCENTIVERECORD.fields_by_name['incentive_record_body']._options = None
    _INCENTIVERECORD.fields_by_name['incentive_record_body']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x1cyaml:"incentive_record_body"'
    _INCENTIVERECORD.fields_by_name['min_uptime']._options = None
    _INCENTIVERECORD.fields_by_name['min_uptime']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"min_uptime"\x98\xdf\x1f\x01'
    _INCENTIVERECORDBODY.fields_by_name['remaining_coin']._options = None
    _INCENTIVERECORDBODY.fields_by_name['remaining_coin']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x16yaml:"remaining_coins"\xaa\xdf\x1f*github.com/cosmos/cosmos-sdk/types.DecCoin'
    _INCENTIVERECORDBODY.fields_by_name['emission_rate']._options = None
    _INCENTIVERECORDBODY.fields_by_name['emission_rate']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"emission_rate"'
    _INCENTIVERECORDBODY.fields_by_name['start_time']._options = None
    _INCENTIVERECORDBODY.fields_by_name['start_time']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x11yaml:"start_time"\x90\xdf\x1f\x01'
    _globals['_INCENTIVERECORD']._serialized_start = 243
    _globals['_INCENTIVERECORD']._serialized_end = 531
    _globals['_INCENTIVERECORDBODY']._serialized_start = 534
    _globals['_INCENTIVERECORDBODY']._serialized_end = 862