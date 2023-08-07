import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
from .... import cosmos
from .... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def Params(self, stream: 'grpclib.server.Stream[osmosis.ibc_rate_limit.v1beta1.query_pb2.ParamsRequest, osmosis.ibc_rate_limit.v1beta1.query_pb2.ParamsResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.ibcratelimit.v1beta1.Query/Params': grpclib.const.Handler(self.Params, grpclib.const.Cardinality.UNARY_UNARY, osmosis.ibc_rate_limit.v1beta1.query_pb2.ParamsRequest, osmosis.ibc_rate_limit.v1beta1.query_pb2.ParamsResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Params = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.ibcratelimit.v1beta1.Query/Params', osmosis.ibc_rate_limit.v1beta1.query_pb2.ParamsRequest, osmosis.ibc_rate_limit.v1beta1.query_pb2.ParamsResponse)