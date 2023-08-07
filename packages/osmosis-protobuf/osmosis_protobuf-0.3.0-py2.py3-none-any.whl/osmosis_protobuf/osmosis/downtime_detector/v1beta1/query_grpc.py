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
import google.protobuf.duration_pb2
import google.protobuf.timestamp_pb2

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def RecoveredSinceDowntimeOfLength(self, stream: 'grpclib.server.Stream[osmosis.downtime_detector.v1beta1.query_pb2.RecoveredSinceDowntimeOfLengthRequest, osmosis.downtime_detector.v1beta1.query_pb2.RecoveredSinceDowntimeOfLengthResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.downtimedetector.v1beta1.Query/RecoveredSinceDowntimeOfLength': grpclib.const.Handler(self.RecoveredSinceDowntimeOfLength, grpclib.const.Cardinality.UNARY_UNARY, osmosis.downtime_detector.v1beta1.query_pb2.RecoveredSinceDowntimeOfLengthRequest, osmosis.downtime_detector.v1beta1.query_pb2.RecoveredSinceDowntimeOfLengthResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.RecoveredSinceDowntimeOfLength = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.downtimedetector.v1beta1.Query/RecoveredSinceDowntimeOfLength', osmosis.downtime_detector.v1beta1.query_pb2.RecoveredSinceDowntimeOfLengthRequest, osmosis.downtime_detector.v1beta1.query_pb2.RecoveredSinceDowntimeOfLengthResponse)