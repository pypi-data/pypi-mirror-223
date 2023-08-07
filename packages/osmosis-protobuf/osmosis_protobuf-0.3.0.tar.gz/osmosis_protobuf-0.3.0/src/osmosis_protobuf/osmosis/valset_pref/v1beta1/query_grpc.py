import abc
import typing
import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server
from .... import gogoproto
from .... import google
from .... import osmosis

class QueryBase(abc.ABC):

    @abc.abstractmethod
    async def UserValidatorPreferences(self, stream: 'grpclib.server.Stream[osmosis.valset_pref.v1beta1.query_pb2.UserValidatorPreferencesRequest, osmosis.valset_pref.v1beta1.query_pb2.UserValidatorPreferencesResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {'/osmosis.valsetpref.v1beta1.Query/UserValidatorPreferences': grpclib.const.Handler(self.UserValidatorPreferences, grpclib.const.Cardinality.UNARY_UNARY, osmosis.valset_pref.v1beta1.query_pb2.UserValidatorPreferencesRequest, osmosis.valset_pref.v1beta1.query_pb2.UserValidatorPreferencesResponse)}

class QueryStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.UserValidatorPreferences = grpclib.client.UnaryUnaryMethod(channel, '/osmosis.valsetpref.v1beta1.Query/UserValidatorPreferences', osmosis.valset_pref.v1beta1.query_pb2.UserValidatorPreferencesRequest, osmosis.valset_pref.v1beta1.query_pb2.UserValidatorPreferencesResponse)