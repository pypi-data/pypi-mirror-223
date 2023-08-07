import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import osmosis
from .... import cosmos
from .... import google
import google.protobuf.any_pb2
from .... import cosmos_proto
import google.protobuf.timestamp_pb2

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.ParamsRequest, osmosis.poolmanager.v1beta1.query_pb2.ParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EstimateSwapExactAmountIn(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EstimateSinglePoolSwapExactAmountIn(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.EstimateSinglePoolSwapExactAmountInRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EstimateSwapExactAmountOut(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutResponse]') -> None:
        pass

    @abc.abstractmethod
    async def EstimateSinglePoolSwapExactAmountOut(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.EstimateSinglePoolSwapExactAmountOutRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutResponse]') -> None:
        pass

    @abc.abstractmethod
    async def NumPools(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.NumPoolsRequest, osmosis.poolmanager.v1beta1.query_pb2.NumPoolsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Pool(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.PoolRequest, osmosis.poolmanager.v1beta1.query_pb2.PoolResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AllPools(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.AllPoolsRequest, osmosis.poolmanager.v1beta1.query_pb2.AllPoolsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def SpotPrice(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.SpotPriceRequest, osmosis.poolmanager.v1beta1.query_pb2.SpotPriceResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalPoolLiquidity(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.TotalPoolLiquidityRequest, osmosis.poolmanager.v1beta1.query_pb2.TotalPoolLiquidityResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TotalLiquidity(self, stream: 'grpclib.server.Stream[osmosis.poolmanager.v1beta1.query_pb2.TotalLiquidityRequest, osmosis.poolmanager.v1beta1.query_pb2.TotalLiquidityResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.poolmanager.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.ParamsRequest, osmosis.poolmanager.v1beta1.query_pb2.ParamsResponse), '/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountIn': grpclib.const.Handler(self.EstimateSwapExactAmountIn, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInResponse), '/osmosis.poolmanager.v1beta1.Query/EstimateSinglePoolSwapExactAmountIn': grpclib.const.Handler(self.EstimateSinglePoolSwapExactAmountIn, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.EstimateSinglePoolSwapExactAmountInRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInResponse), '/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountOut': grpclib.const.Handler(self.EstimateSwapExactAmountOut, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutResponse), '/osmosis.poolmanager.v1beta1.Query/EstimateSinglePoolSwapExactAmountOut': grpclib.const.Handler(self.EstimateSinglePoolSwapExactAmountOut, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.EstimateSinglePoolSwapExactAmountOutRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutResponse), '/osmosis.poolmanager.v1beta1.Query/NumPools': grpclib.const.Handler(self.NumPools, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.NumPoolsRequest, osmosis.poolmanager.v1beta1.query_pb2.NumPoolsResponse), '/osmosis.poolmanager.v1beta1.Query/Pool': grpclib.const.Handler(self.Pool, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.PoolRequest, osmosis.poolmanager.v1beta1.query_pb2.PoolResponse), '/osmosis.poolmanager.v1beta1.Query/AllPools': grpclib.const.Handler(self.AllPools, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.AllPoolsRequest, osmosis.poolmanager.v1beta1.query_pb2.AllPoolsResponse), '/osmosis.poolmanager.v1beta1.Query/SpotPrice': grpclib.const.Handler(self.SpotPrice, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.SpotPriceRequest, osmosis.poolmanager.v1beta1.query_pb2.SpotPriceResponse), '/osmosis.poolmanager.v1beta1.Query/TotalPoolLiquidity': grpclib.const.Handler(self.TotalPoolLiquidity, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.TotalPoolLiquidityRequest, osmosis.poolmanager.v1beta1.query_pb2.TotalPoolLiquidityResponse), '/osmosis.poolmanager.v1beta1.Query/TotalLiquidity': grpclib.const.Handler(self.TotalLiquidity, grpclib.const.Cardinality.UNARY_UNARY, osmosis.poolmanager.v1beta1.query_pb2.TotalLiquidityRequest, osmosis.poolmanager.v1beta1.query_pb2.TotalLiquidityResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/Params', osmosis.poolmanager.v1beta1.query_pb2.ParamsRequest, osmosis.poolmanager.v1beta1.query_pb2.ParamsResponse)
        self.EstimateSwapExactAmountIn = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountIn', osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInResponse)
        self.EstimateSinglePoolSwapExactAmountIn = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/EstimateSinglePoolSwapExactAmountIn', osmosis.poolmanager.v1beta1.query_pb2.EstimateSinglePoolSwapExactAmountInRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountInResponse)
        self.EstimateSwapExactAmountOut = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/EstimateSwapExactAmountOut', osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutResponse)
        self.EstimateSinglePoolSwapExactAmountOut = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/EstimateSinglePoolSwapExactAmountOut', osmosis.poolmanager.v1beta1.query_pb2.EstimateSinglePoolSwapExactAmountOutRequest, osmosis.poolmanager.v1beta1.query_pb2.EstimateSwapExactAmountOutResponse)
        self.NumPools = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/NumPools', osmosis.poolmanager.v1beta1.query_pb2.NumPoolsRequest, osmosis.poolmanager.v1beta1.query_pb2.NumPoolsResponse)
        self.Pool = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/Pool', osmosis.poolmanager.v1beta1.query_pb2.PoolRequest, osmosis.poolmanager.v1beta1.query_pb2.PoolResponse)
        self.AllPools = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/AllPools', osmosis.poolmanager.v1beta1.query_pb2.AllPoolsRequest, osmosis.poolmanager.v1beta1.query_pb2.AllPoolsResponse)
        self.SpotPrice = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/SpotPrice', osmosis.poolmanager.v1beta1.query_pb2.SpotPriceRequest, osmosis.poolmanager.v1beta1.query_pb2.SpotPriceResponse)
        self.TotalPoolLiquidity = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/TotalPoolLiquidity', osmosis.poolmanager.v1beta1.query_pb2.TotalPoolLiquidityRequest, osmosis.poolmanager.v1beta1.query_pb2.TotalPoolLiquidityResponse)
        self.TotalLiquidity = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolmanager.v1beta1.Query/TotalLiquidity', osmosis.poolmanager.v1beta1.query_pb2.TotalLiquidityRequest, osmosis.poolmanager.v1beta1.query_pb2.TotalLiquidityResponse)