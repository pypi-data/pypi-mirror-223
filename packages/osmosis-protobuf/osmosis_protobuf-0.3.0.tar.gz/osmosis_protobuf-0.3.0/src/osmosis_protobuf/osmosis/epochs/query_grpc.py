import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from ... import gogoproto
from ... import google
from ... import cosmos
from ... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def EpochInfos(self, stream: 'grpclib.server.Stream[osmosis.epochs.query_pb2.QueryEpochsInfoRequest, osmosis.epochs.query_pb2.QueryEpochsInfoResponse]') -> None:
        pass

    @abc.abstractmethod
    async def CurrentEpoch(self, stream: 'grpclib.server.Stream[osmosis.epochs.query_pb2.QueryCurrentEpochRequest, osmosis.epochs.query_pb2.QueryCurrentEpochResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.epochs.v1beta1.Query/EpochInfos': grpclib.const.Handler(self.EpochInfos, grpclib.const.Cardinality.UNARY_UNARY, osmosis.epochs.query_pb2.QueryEpochsInfoRequest, osmosis.epochs.query_pb2.QueryEpochsInfoResponse), '/osmosis.epochs.v1beta1.Query/CurrentEpoch': grpclib.const.Handler(self.CurrentEpoch, grpclib.const.Cardinality.UNARY_UNARY, osmosis.epochs.query_pb2.QueryCurrentEpochRequest, osmosis.epochs.query_pb2.QueryCurrentEpochResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.EpochInfos = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.epochs.v1beta1.Query/EpochInfos', osmosis.epochs.query_pb2.QueryEpochsInfoRequest, osmosis.epochs.query_pb2.QueryEpochsInfoResponse)
        self.CurrentEpoch = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.epochs.v1beta1.Query/CurrentEpoch', osmosis.epochs.query_pb2.QueryCurrentEpochRequest, osmosis.epochs.query_pb2.QueryCurrentEpochResponse)