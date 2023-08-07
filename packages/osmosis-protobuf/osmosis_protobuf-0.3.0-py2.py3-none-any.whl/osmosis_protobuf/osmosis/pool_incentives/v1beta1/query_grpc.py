import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
import google.protobuf.duration_pb2
from .... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def GaugeIds(self, stream: 'grpclib.server.Stream[osmosis.pool_incentives.v1beta1.query_pb2.QueryGaugeIdsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryGaugeIdsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DistrInfo(self, stream: 'grpclib.server.Stream[osmosis.pool_incentives.v1beta1.query_pb2.QueryDistrInfoRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryDistrInfoResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.pool_incentives.v1beta1.query_pb2.QueryParamsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryParamsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LockableDurations(self, stream: 'grpclib.server.Stream[osmosis.pool_incentives.v1beta1.query_pb2.QueryLockableDurationsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryLockableDurationsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def IncentivizedPools(self, stream: 'grpclib.server.Stream[osmosis.pool_incentives.v1beta1.query_pb2.QueryIncentivizedPoolsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryIncentivizedPoolsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ExternalIncentiveGauges(self, stream: 'grpclib.server.Stream[osmosis.pool_incentives.v1beta1.query_pb2.QueryExternalIncentiveGaugesRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryExternalIncentiveGaugesResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.poolincentives.v1beta1.Query/GaugeIds': grpclib.const.Handler(self.GaugeIds, grpclib.const.Cardinality.UNARY_UNARY, osmosis.pool_incentives.v1beta1.query_pb2.QueryGaugeIdsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryGaugeIdsResponse), '/osmosis.poolincentives.v1beta1.Query/DistrInfo': grpclib.const.Handler(self.DistrInfo, grpclib.const.Cardinality.UNARY_UNARY, osmosis.pool_incentives.v1beta1.query_pb2.QueryDistrInfoRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryDistrInfoResponse), '/osmosis.poolincentives.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.pool_incentives.v1beta1.query_pb2.QueryParamsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryParamsResponse), '/osmosis.poolincentives.v1beta1.Query/LockableDurations': grpclib.const.Handler(self.LockableDurations, grpclib.const.Cardinality.UNARY_UNARY, osmosis.pool_incentives.v1beta1.query_pb2.QueryLockableDurationsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryLockableDurationsResponse), '/osmosis.poolincentives.v1beta1.Query/IncentivizedPools': grpclib.const.Handler(self.IncentivizedPools, grpclib.const.Cardinality.UNARY_UNARY, osmosis.pool_incentives.v1beta1.query_pb2.QueryIncentivizedPoolsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryIncentivizedPoolsResponse), '/osmosis.poolincentives.v1beta1.Query/ExternalIncentiveGauges': grpclib.const.Handler(self.ExternalIncentiveGauges, grpclib.const.Cardinality.UNARY_UNARY, osmosis.pool_incentives.v1beta1.query_pb2.QueryExternalIncentiveGaugesRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryExternalIncentiveGaugesResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.GaugeIds = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolincentives.v1beta1.Query/GaugeIds', osmosis.pool_incentives.v1beta1.query_pb2.QueryGaugeIdsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryGaugeIdsResponse)
        self.DistrInfo = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolincentives.v1beta1.Query/DistrInfo', osmosis.pool_incentives.v1beta1.query_pb2.QueryDistrInfoRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryDistrInfoResponse)
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolincentives.v1beta1.Query/Params', osmosis.pool_incentives.v1beta1.query_pb2.QueryParamsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryParamsResponse)
        self.LockableDurations = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolincentives.v1beta1.Query/LockableDurations', osmosis.pool_incentives.v1beta1.query_pb2.QueryLockableDurationsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryLockableDurationsResponse)
        self.IncentivizedPools = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolincentives.v1beta1.Query/IncentivizedPools', osmosis.pool_incentives.v1beta1.query_pb2.QueryIncentivizedPoolsRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryIncentivizedPoolsResponse)
        self.ExternalIncentiveGauges = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.poolincentives.v1beta1.Query/ExternalIncentiveGauges', osmosis.pool_incentives.v1beta1.query_pb2.QueryExternalIncentiveGaugesRequest, osmosis.pool_incentives.v1beta1.query_pb2.QueryExternalIncentiveGaugesResponse)