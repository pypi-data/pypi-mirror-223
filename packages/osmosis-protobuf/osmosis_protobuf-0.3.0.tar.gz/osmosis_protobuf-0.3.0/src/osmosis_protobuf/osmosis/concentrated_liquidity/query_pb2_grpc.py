"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from ...osmosis.concentrated_liquidity import query_pb2 as osmosis_dot_concentrated__liquidity_dot_query__pb2

class QueryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Pools = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/Pools', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolsRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolsResponse.FromString)
        self.Params = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/Params', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ParamsRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ParamsResponse.FromString)
        self.UserPositions = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/UserPositions', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.UserPositionsRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.UserPositionsResponse.FromString)
        self.LiquidityPerTickRange = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/LiquidityPerTickRange', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityPerTickRangeRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityPerTickRangeResponse.FromString)
        self.LiquidityNetInDirection = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/LiquidityNetInDirection', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityNetInDirectionRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityNetInDirectionResponse.FromString)
        self.ClaimableSpreadRewards = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/ClaimableSpreadRewards', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableSpreadRewardsRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableSpreadRewardsResponse.FromString)
        self.ClaimableIncentives = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/ClaimableIncentives', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableIncentivesRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableIncentivesResponse.FromString)
        self.PositionById = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/PositionById', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PositionByIdRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PositionByIdResponse.FromString)
        self.PoolAccumulatorRewards = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/PoolAccumulatorRewards', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolAccumulatorRewardsRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolAccumulatorRewardsResponse.FromString)
        self.IncentiveRecords = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/IncentiveRecords', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.IncentiveRecordsRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.IncentiveRecordsResponse.FromString)
        self.TickAccumulatorTrackers = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/TickAccumulatorTrackers', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.TickAccumulatorTrackersRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.TickAccumulatorTrackersResponse.FromString)
        self.CFMMPoolIdLinkFromConcentratedPoolId = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/CFMMPoolIdLinkFromConcentratedPoolId', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.CFMMPoolIdLinkFromConcentratedPoolIdRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.CFMMPoolIdLinkFromConcentratedPoolIdResponse.FromString)
        self.UserUnbondingPositions = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/UserUnbondingPositions', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.UserUnbondingPositionsRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.UserUnbondingPositionsResponse.FromString)
        self.GetTotalLiquidity = channel.unary_unary('/osmosis.concentratedliquidity.v1beta1.Query/GetTotalLiquidity', request_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.GetTotalLiquidityRequest.SerializeToString, response_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.GetTotalLiquidityResponse.FromString)

class QueryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Pools(self, request, context):
        """Pools returns all concentrated liquidity pools
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Params(self, request, context):
        """Params returns concentrated liquidity module params.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserPositions(self, request, context):
        """UserPositions returns all concentrated postitions of some address.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LiquidityPerTickRange(self, request, context):
        """LiquidityPerTickRange returns the amount of liquidity per every tick range
        existing within the given pool
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LiquidityNetInDirection(self, request, context):
        """LiquidityNetInDirection returns liquidity net in the direction given.
        Uses the bound if specified, if not uses either min tick / max tick
        depending on the direction.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClaimableSpreadRewards(self, request, context):
        """ClaimableSpreadRewards returns the amount of spread rewards that can be
        claimed by a position with the given id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClaimableIncentives(self, request, context):
        """ClaimableIncentives returns the amount of incentives that can be claimed
        and how many would be forfeited by a position with the given id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PositionById(self, request, context):
        """PositionById returns a position with the given id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PoolAccumulatorRewards(self, request, context):
        """PoolAccumulatorRewards returns the pool-global accumulator rewards.
        Contains spread factor rewards and uptime rewards.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IncentiveRecords(self, request, context):
        """IncentiveRecords returns the incentive records for a given poolId
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TickAccumulatorTrackers(self, request, context):
        """TickAccumulatorTrackers returns the tick accumulator trackers.
        Contains spread factor and uptime accumulator trackers.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CFMMPoolIdLinkFromConcentratedPoolId(self, request, context):
        """CFMMPoolIdLinkFromConcentratedPoolId returns the pool id of the CFMM
        pool that is linked with the given concentrated pool.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UserUnbondingPositions(self, request, context):
        """UserUnbondingPositions returns the position and lock info of unbonding
        positions of the given address.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTotalLiquidity(self, request, context):
        """GetTotalLiquidity returns total liquidity across all cl pools.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {'Pools': grpc.unary_unary_rpc_method_handler(servicer.Pools, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolsRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolsResponse.SerializeToString), 'Params': grpc.unary_unary_rpc_method_handler(servicer.Params, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ParamsRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ParamsResponse.SerializeToString), 'UserPositions': grpc.unary_unary_rpc_method_handler(servicer.UserPositions, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.UserPositionsRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.UserPositionsResponse.SerializeToString), 'LiquidityPerTickRange': grpc.unary_unary_rpc_method_handler(servicer.LiquidityPerTickRange, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityPerTickRangeRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityPerTickRangeResponse.SerializeToString), 'LiquidityNetInDirection': grpc.unary_unary_rpc_method_handler(servicer.LiquidityNetInDirection, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityNetInDirectionRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityNetInDirectionResponse.SerializeToString), 'ClaimableSpreadRewards': grpc.unary_unary_rpc_method_handler(servicer.ClaimableSpreadRewards, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableSpreadRewardsRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableSpreadRewardsResponse.SerializeToString), 'ClaimableIncentives': grpc.unary_unary_rpc_method_handler(servicer.ClaimableIncentives, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableIncentivesRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableIncentivesResponse.SerializeToString), 'PositionById': grpc.unary_unary_rpc_method_handler(servicer.PositionById, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PositionByIdRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PositionByIdResponse.SerializeToString), 'PoolAccumulatorRewards': grpc.unary_unary_rpc_method_handler(servicer.PoolAccumulatorRewards, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolAccumulatorRewardsRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolAccumulatorRewardsResponse.SerializeToString), 'IncentiveRecords': grpc.unary_unary_rpc_method_handler(servicer.IncentiveRecords, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.IncentiveRecordsRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.IncentiveRecordsResponse.SerializeToString), 'TickAccumulatorTrackers': grpc.unary_unary_rpc_method_handler(servicer.TickAccumulatorTrackers, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.TickAccumulatorTrackersRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.TickAccumulatorTrackersResponse.SerializeToString), 'CFMMPoolIdLinkFromConcentratedPoolId': grpc.unary_unary_rpc_method_handler(servicer.CFMMPoolIdLinkFromConcentratedPoolId, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.CFMMPoolIdLinkFromConcentratedPoolIdRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.CFMMPoolIdLinkFromConcentratedPoolIdResponse.SerializeToString), 'UserUnbondingPositions': grpc.unary_unary_rpc_method_handler(servicer.UserUnbondingPositions, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.UserUnbondingPositionsRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.UserUnbondingPositionsResponse.SerializeToString), 'GetTotalLiquidity': grpc.unary_unary_rpc_method_handler(servicer.GetTotalLiquidity, request_deserializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.GetTotalLiquidityRequest.FromString, response_serializer=osmosis_dot_concentrated__liquidity_dot_query__pb2.GetTotalLiquidityResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('osmosis.concentratedliquidity.v1beta1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Query(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Pools(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/Pools', osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolsRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Params(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/Params', osmosis_dot_concentrated__liquidity_dot_query__pb2.ParamsRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.ParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UserPositions(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/UserPositions', osmosis_dot_concentrated__liquidity_dot_query__pb2.UserPositionsRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.UserPositionsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LiquidityPerTickRange(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/LiquidityPerTickRange', osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityPerTickRangeRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityPerTickRangeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LiquidityNetInDirection(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/LiquidityNetInDirection', osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityNetInDirectionRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.LiquidityNetInDirectionResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClaimableSpreadRewards(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/ClaimableSpreadRewards', osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableSpreadRewardsRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableSpreadRewardsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClaimableIncentives(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/ClaimableIncentives', osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableIncentivesRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.ClaimableIncentivesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PositionById(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/PositionById', osmosis_dot_concentrated__liquidity_dot_query__pb2.PositionByIdRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.PositionByIdResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PoolAccumulatorRewards(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/PoolAccumulatorRewards', osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolAccumulatorRewardsRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.PoolAccumulatorRewardsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IncentiveRecords(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/IncentiveRecords', osmosis_dot_concentrated__liquidity_dot_query__pb2.IncentiveRecordsRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.IncentiveRecordsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TickAccumulatorTrackers(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/TickAccumulatorTrackers', osmosis_dot_concentrated__liquidity_dot_query__pb2.TickAccumulatorTrackersRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.TickAccumulatorTrackersResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CFMMPoolIdLinkFromConcentratedPoolId(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/CFMMPoolIdLinkFromConcentratedPoolId', osmosis_dot_concentrated__liquidity_dot_query__pb2.CFMMPoolIdLinkFromConcentratedPoolIdRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.CFMMPoolIdLinkFromConcentratedPoolIdResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UserUnbondingPositions(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/UserUnbondingPositions', osmosis_dot_concentrated__liquidity_dot_query__pb2.UserUnbondingPositionsRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.UserUnbondingPositionsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTotalLiquidity(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/osmosis.concentratedliquidity.v1beta1.Query/GetTotalLiquidity', osmosis_dot_concentrated__liquidity_dot_query__pb2.GetTotalLiquidityRequest.SerializeToString, osmosis_dot_concentrated__liquidity_dot_query__pb2.GetTotalLiquidityResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)