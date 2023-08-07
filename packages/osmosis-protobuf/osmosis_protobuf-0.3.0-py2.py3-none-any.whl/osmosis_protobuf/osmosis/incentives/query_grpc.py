import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from ... import gogoproto
from ... import google
import google.protobuf.duration_pb2
from ... import cosmos
from ... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def ModuleToDistributeCoins(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.ModuleToDistributeCoinsRequest, osmosis.incentives.query_pb2.ModuleToDistributeCoinsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def GaugeByID(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.GaugeByIDRequest, osmosis.incentives.query_pb2.GaugeByIDResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Gauges(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.GaugesRequest, osmosis.incentives.query_pb2.GaugesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ActiveGauges(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.ActiveGaugesRequest, osmosis.incentives.query_pb2.ActiveGaugesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def ActiveGaugesPerDenom(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.ActiveGaugesPerDenomRequest, osmosis.incentives.query_pb2.ActiveGaugesPerDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UpcomingGauges(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.UpcomingGaugesRequest, osmosis.incentives.query_pb2.UpcomingGaugesResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UpcomingGaugesPerDenom(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.UpcomingGaugesPerDenomRequest, osmosis.incentives.query_pb2.UpcomingGaugesPerDenomResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RewardsEst(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.RewardsEstRequest, osmosis.incentives.query_pb2.RewardsEstResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LockableDurations(self, stream: 'grpclib.server.Stream[osmosis.incentives.query_pb2.QueryLockableDurationsRequest, osmosis.incentives.query_pb2.QueryLockableDurationsResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.incentives.Query/ModuleToDistributeCoins': grpclib.const.Handler(self.ModuleToDistributeCoins, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.ModuleToDistributeCoinsRequest, osmosis.incentives.query_pb2.ModuleToDistributeCoinsResponse), '/osmosis.incentives.Query/GaugeByID': grpclib.const.Handler(self.GaugeByID, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.GaugeByIDRequest, osmosis.incentives.query_pb2.GaugeByIDResponse), '/osmosis.incentives.Query/Gauges': grpclib.const.Handler(self.Gauges, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.GaugesRequest, osmosis.incentives.query_pb2.GaugesResponse), '/osmosis.incentives.Query/ActiveGauges': grpclib.const.Handler(self.ActiveGauges, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.ActiveGaugesRequest, osmosis.incentives.query_pb2.ActiveGaugesResponse), '/osmosis.incentives.Query/ActiveGaugesPerDenom': grpclib.const.Handler(self.ActiveGaugesPerDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.ActiveGaugesPerDenomRequest, osmosis.incentives.query_pb2.ActiveGaugesPerDenomResponse), '/osmosis.incentives.Query/UpcomingGauges': grpclib.const.Handler(self.UpcomingGauges, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.UpcomingGaugesRequest, osmosis.incentives.query_pb2.UpcomingGaugesResponse), '/osmosis.incentives.Query/UpcomingGaugesPerDenom': grpclib.const.Handler(self.UpcomingGaugesPerDenom, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.UpcomingGaugesPerDenomRequest, osmosis.incentives.query_pb2.UpcomingGaugesPerDenomResponse), '/osmosis.incentives.Query/RewardsEst': grpclib.const.Handler(self.RewardsEst, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.RewardsEstRequest, osmosis.incentives.query_pb2.RewardsEstResponse), '/osmosis.incentives.Query/LockableDurations': grpclib.const.Handler(self.LockableDurations, grpclib.const.Cardinality.UNARY_UNARY, osmosis.incentives.query_pb2.QueryLockableDurationsRequest, osmosis.incentives.query_pb2.QueryLockableDurationsResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.ModuleToDistributeCoins = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/ModuleToDistributeCoins', osmosis.incentives.query_pb2.ModuleToDistributeCoinsRequest, osmosis.incentives.query_pb2.ModuleToDistributeCoinsResponse)
        self.GaugeByID = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/GaugeByID', osmosis.incentives.query_pb2.GaugeByIDRequest, osmosis.incentives.query_pb2.GaugeByIDResponse)
        self.Gauges = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/Gauges', osmosis.incentives.query_pb2.GaugesRequest, osmosis.incentives.query_pb2.GaugesResponse)
        self.ActiveGauges = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/ActiveGauges', osmosis.incentives.query_pb2.ActiveGaugesRequest, osmosis.incentives.query_pb2.ActiveGaugesResponse)
        self.ActiveGaugesPerDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/ActiveGaugesPerDenom', osmosis.incentives.query_pb2.ActiveGaugesPerDenomRequest, osmosis.incentives.query_pb2.ActiveGaugesPerDenomResponse)
        self.UpcomingGauges = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/UpcomingGauges', osmosis.incentives.query_pb2.UpcomingGaugesRequest, osmosis.incentives.query_pb2.UpcomingGaugesResponse)
        self.UpcomingGaugesPerDenom = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/UpcomingGaugesPerDenom', osmosis.incentives.query_pb2.UpcomingGaugesPerDenomRequest, osmosis.incentives.query_pb2.UpcomingGaugesPerDenomResponse)
        self.RewardsEst = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/RewardsEst', osmosis.incentives.query_pb2.RewardsEstRequest, osmosis.incentives.query_pb2.RewardsEstResponse)
        self.LockableDurations = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.incentives.Query/LockableDurations', osmosis.incentives.query_pb2.QueryLockableDurationsRequest, osmosis.incentives.query_pb2.QueryLockableDurationsResponse)