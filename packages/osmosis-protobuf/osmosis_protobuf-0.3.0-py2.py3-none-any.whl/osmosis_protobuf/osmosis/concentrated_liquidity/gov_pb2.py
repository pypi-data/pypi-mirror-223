"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(osmosis/concentrated-liquidity/gov.proto\x12%osmosis.concentratedliquidity.v1beta1\x1a\x14gogoproto/gogo.proto"\xc2\x01\n(CreateConcentratedLiquidityPoolsProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12d\n\x0cpool_records\x18\x03 \x03(\x0b21.osmosis.concentratedliquidity.v1beta1.PoolRecordB\x1b\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"pool_records":\x0c\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01"\xc0\x01\n\x1bTickSpacingDecreaseProposal\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12o\n\x1fpool_id_to_tick_spacing_records\x18\x03 \x03(\x0b2@.osmosis.concentratedliquidity.v1beta1.PoolIdToTickSpacingRecordB\x04\xc8\xde\x1f\x00:\x0c\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01"L\n\x19PoolIdToTickSpacingRecord\x12\x0f\n\x07pool_id\x18\x01 \x01(\x04\x12\x18\n\x10new_tick_spacing\x18\x02 \x01(\x04:\x04\xe8\xa0\x1f\x01"\xd5\x02\n\nPoolRecord\x12!\n\x06denom0\x18\x01 \x01(\tB\x11\xf2\xde\x1f\ryaml:"denom0"\x12!\n\x06denom1\x18\x02 \x01(\tB\x11\xf2\xde\x1f\ryaml:"denom1"\x12-\n\x0ctick_spacing\x18\x03 \x01(\x04B\x17\xf2\xde\x1f\x13yaml:"tick_spacing"\x12m\n\x15exponent_at_price_one\x18\x04 \x01(\tBN\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x1cyaml:"exponent_at_price_one"\x12]\n\rspread_factor\x18\x05 \x01(\tBF\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"spread_factor":\x04\xe8\xa0\x1f\x01BDZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/typesb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'osmosis.concentrated_liquidity.gov_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'ZBgithub.com/osmosis-labs/osmosis/v16/x/concentrated-liquidity/types'
    _CREATECONCENTRATEDLIQUIDITYPOOLSPROPOSAL.fields_by_name['pool_records']._options = None
    _CREATECONCENTRATEDLIQUIDITYPOOLSPROPOSAL.fields_by_name['pool_records']._serialized_options = b'\xc8\xde\x1f\x00\xf2\xde\x1f\x13yaml:"pool_records"'
    _CREATECONCENTRATEDLIQUIDITYPOOLSPROPOSAL._options = None
    _CREATECONCENTRATEDLIQUIDITYPOOLSPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01'
    _TICKSPACINGDECREASEPROPOSAL.fields_by_name['pool_id_to_tick_spacing_records']._options = None
    _TICKSPACINGDECREASEPROPOSAL.fields_by_name['pool_id_to_tick_spacing_records']._serialized_options = b'\xc8\xde\x1f\x00'
    _TICKSPACINGDECREASEPROPOSAL._options = None
    _TICKSPACINGDECREASEPROPOSAL._serialized_options = b'\x88\xa0\x1f\x00\x98\xa0\x1f\x00\xe8\xa0\x1f\x01'
    _POOLIDTOTICKSPACINGRECORD._options = None
    _POOLIDTOTICKSPACINGRECORD._serialized_options = b'\xe8\xa0\x1f\x01'
    _POOLRECORD.fields_by_name['denom0']._options = None
    _POOLRECORD.fields_by_name['denom0']._serialized_options = b'\xf2\xde\x1f\ryaml:"denom0"'
    _POOLRECORD.fields_by_name['denom1']._options = None
    _POOLRECORD.fields_by_name['denom1']._serialized_options = b'\xf2\xde\x1f\ryaml:"denom1"'
    _POOLRECORD.fields_by_name['tick_spacing']._options = None
    _POOLRECORD.fields_by_name['tick_spacing']._serialized_options = b'\xf2\xde\x1f\x13yaml:"tick_spacing"'
    _POOLRECORD.fields_by_name['exponent_at_price_one']._options = None
    _POOLRECORD.fields_by_name['exponent_at_price_one']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xf2\xde\x1f\x1cyaml:"exponent_at_price_one"'
    _POOLRECORD.fields_by_name['spread_factor']._options = None
    _POOLRECORD.fields_by_name['spread_factor']._serialized_options = b'\xc8\xde\x1f\x00\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Dec\xf2\xde\x1f\x14yaml:"spread_factor"'
    _POOLRECORD._options = None
    _POOLRECORD._serialized_options = b'\xe8\xa0\x1f\x01'
    _globals['_CREATECONCENTRATEDLIQUIDITYPOOLSPROPOSAL']._serialized_start = 106
    _globals['_CREATECONCENTRATEDLIQUIDITYPOOLSPROPOSAL']._serialized_end = 300
    _globals['_TICKSPACINGDECREASEPROPOSAL']._serialized_start = 303
    _globals['_TICKSPACINGDECREASEPROPOSAL']._serialized_end = 495
    _globals['_POOLIDTOTICKSPACINGRECORD']._serialized_start = 497
    _globals['_POOLIDTOTICKSPACINGRECORD']._serialized_end = 573
    _globals['_POOLRECORD']._serialized_start = 576
    _globals['_POOLRECORD']._serialized_end = 917