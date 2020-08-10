from . import sdk
from .enum import Result
from .exception import getException
from .event import bindEvents
import ctypes

class NetworkManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordNetworkEvents,
            self._OnMessage,
            self._OnRouteUpdate
        )
        
    def _OnMessage(self, event_data, peer_id, channel_id, data, data_length):
        data = bytes(data[:data_length])
        self.OnMessage(peer_id, channel_id, data)
        
    def _OnRouteUpdate(self, event_data, route_data):
        self.OnRouteUpdate(route_data.decode("utf8"))
        
    def GetPeerId(self) -> int:
        """
        Get the networking peer ID for the current user, allowing other users to send packets to them.
        """
        peerId = sdk.DiscordNetworkPeerId()
        self._internal.get_peer_id(self._internal, peerId)
        return peerId.value
        
    def Flush(self) -> None:
        """
        Flushes the network
        """
        result = self._internal.flush(self._internal)
        if result != Result.Ok:
            raise getException(result)
            
    def OpenChannel(self, peerId: int, channelId: int, reliable: bool) -> None:
        """
        Opens a channel to a user with their given peer ID on the given channel number.
        """
        result = self._internal.open_channel(self._internal, peerId, channelId, reliable)
        if result != Result.Ok:
            raise getException(result)
        
    def OpenPeer(self, peerId: int, route: str) -> None:
        """
        Opens a network connection to another Discord user.
        """
        route_data = ctypes.create_string_buffer(route.encode("utf8"))
        result = self._internal.open_peer(self._internal, peerId, route_data)
        if result != Result.Ok:
            raise getException(result)
        
    def UpdatePeer(self, peerId: int, route: str) -> None:
        """
        Updates the network connection to another Discord user.
        """
        result = self._internal.update_peer(self._internal, peerId, route)
        if result != Result.Ok:
            raise getException(result)
        
    def SendMessage(self, peerId: int, channelId: int, data: bytes) -> None:
        """
        Sends data to a given peer ID through the given channel.
        """
        data = (ctypes.c_uint8 * len(data))(*data)
        result = self._internal.send_message(self._internal, peerId, channelId, data, len(data))
        if result != Result.Ok:
            raise getException(result)
        
    def CloseChannel(self, peerId: int, channelId: int) -> None:
        """
        Close the connection to a given user by peerId on the given channel.
        """
        result = self._internal.close_channel(self._internal, peerId, channelId)
        if result != Result.Ok:
            raise getException(result)
        
    def ClosePeer(self, peerId: int) -> None:
        """
        Disconnects the network session to another Discord user.
        """
        result = self._internal.close_peer(self._internal, peerId)
        if result != Result.Ok:
            raise getException(result)
        
    def OnMessage(self, peerId: int, channelId: int, data: bytes) -> None:
        """
        Fires when you receive data from another user.
        """
        pass
        
    def OnRouteUpdate(self, route: str) -> None:
        """
        Fires when your networking route has changed.
        """
        pass
        