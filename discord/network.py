from . import sdk

class NetworkManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = None
        
    def GetPeerId(self):
        peerId = sdk.DiscordNetworkPeerId()
        self._internal.get_peer_id(self._internal, peerId)
        return peerId.value
        
    # TODO