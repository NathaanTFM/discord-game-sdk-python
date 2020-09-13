from . import sdk
from .model import Lobby, User
from .enum import Result, LobbyType, LobbySearchComparison, LobbySearchCast, LobbySearchDistance
from .event import bindEvents
from .exception import getException
from typing import Callable, Optional
import ctypes

class LobbyTransaction:
    def __init__(self, internal):
        self._internal = internal
        
    def SetType(self, type: LobbyType) -> None:
        """
        Marks a lobby as private or public.
        """
        result = Result(self._internal.set_type(self._internal, type))
        if result != Result.Ok:
            raise getException(result)
            
    def SetOwner(self, userId: int) -> None:
        """
        Sets a new owner for the lobby.
        """
        result = Result(self._internal.set_owner(self._internal, userId))
        if result != Result.Ok:
            raise getException(result)
        
    def SetCapacity(self, capacity: int) -> None:
        """
        Sets a new capacity for the lobby.
        """
        result = Result(self._internal.set_capacity(self._internal, capacity))
        if result != Result.Ok:
            raise getException(result)
        
    def SetMetadata(self, key: str, value: str) -> None:
        """
        Sets metadata value under a given key name for the lobby.
        """
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        metadataValue.value = value.encode("utf8")
        
        result = Result(self._internal.set_metadata(self._internal, metadataKey, metadataValue))
        if result != Result.Ok:
            raise getException(result)
    
    def DeleteMetadata(self, key: str) -> None:
        """
        Deletes the lobby metadata for a key.
        """
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
            
        result = Result(self._internal.delete_metadata(self._internal, metadataKey))
        if result != Result.Ok:
            raise getException(result)
    
    def SetLocked(self, locked: bool) -> None:
        """
        Sets the lobby to locked or unlocked.
        """
        result = Result(self._internal.set_locked(self._internal, locked))
        if result != Result.Ok:
            raise getException(result)
    
class LobbyMemberTransaction:
    def __init__(self, internal):
        self._internal = internal
        
    def SetMetadata(self, key: str, value: str) -> None:
        """
        Sets metadata value under a given key name for the current user.
        """
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        metadataValue.value = value.encode("utf8")
        
        result = Result(self._internal.set_metadata(self._internal, metadataKey, metadataValue))
        if result != Result.Ok:
            raise getException(result)
    
    def DeleteMetadata(self, key: str) -> None:
        """
        Sets metadata value under a given key name for the current user.
        """
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        result = Result(self._internal.delete_metadata(self._internal, metadataKey))
        if result != Result.Ok:
            raise getException(result)
    
class LobbySearchQuery:
    def __init__(self, internal):
        self._internal = internal
        
    def Filter(self, key: str, comp: LobbySearchComparison, cast: LobbySearchCast, value: str) -> None:
        """
        Filters lobbies based on metadata comparison. 
        """
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        metadataValue.value = value.encode("utf8")
        
        result = Result(self._internal.filter(self._internal, metadataKey, comp, cast, metadataValue))
        if result != Result.Ok:
            raise getException(result)
    
    def Sort(self, key: str, cast: LobbySearchCast, value: str) -> None:
        """
        Sorts the filtered lobbies based on "near-ness" to a given value.
        """
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        metadataValue.value = value.encode("utf8")
        
        result = Result(self._internal.sort(self._internal, metadataKey, cast, metadataValue))
        if result != Result.Ok:
            raise getException(result)
    
    def Limit(self, limit: int) -> None:
        """
        Limits the number of lobbies returned in a search.
        """
        result = Result(self._internal.limit(self._internal, limit))
        if result != Result.Ok:
            raise getException(result)
    
    def Distance(self, distance: LobbySearchDistance) -> None:
        """
        Filters lobby results to within certain regions relative to the user's location.
        """
        result = Result(self._internal.distance(self._internal, distance))
        if result != Result.Ok:
            raise getException(result)
    
class LobbyManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordLobbyEvents,
            self._OnLobbyUpdate,
            self._OnLobbyDelete,
            self._OnMemberConnect,
            self._OnMemberUpdate,
            self._OnMemberDisconnect,
            self._OnLobbyMessage,
            self._OnSpeaking,
            self._OnNetworkMessage
        )
        
    def _OnLobbyUpdate(self, event_data, lobby_id):
        self.OnLobbyUpdate(lobby_id)
        
    def _OnLobbyDelete(self, event_data, lobby_id, reason):
        self.OnLobbyDelete(lobby_id, reason)
        
    def _OnMemberConnect(self, event_data, lobby_id, user_id):
        self.OnMemberConnect(lobby_id, user_id)
        
    def _OnMemberUpdate(self, event_data, lobby_id, user_id):
        self.OnMemberUpdate(lobby_id, user_id)
        
    def _OnMemberDisconnect(self, event_data, lobby_id, user_id):
        self.OnMemberDisconnect(lobby_id, user_id)
        
    def _OnLobbyMessage(self, event_data, lobby_id, user_id, data, data_length):
        message = bytes(data[:data_length]).decode("utf8")
        self.OnLobbyMessage(lobby_id, user_id, message)
        
    def _OnSpeaking(self, event_data, lobby_id, user_id, speaking):
        self.OnSpeaking(lobby_id, user_id, speaking)
        
    def _OnNetworkMessage(self, event_data, lobby_id, user_id, channel_id, data, data_length):
        data = bytes(data[:data_length])
        self.OnNetworkMessage(lobby_id, user_id, channel_id, data)
        
    def GetLobbyCreateTransaction(self) -> LobbyTransaction:
        """
        Gets a Lobby transaction used for creating a new lobby
        """
        transaction = ctypes.POINTER(sdk.IDiscordLobbyTransaction)()
        result = Result(self._internal.get_lobby_create_transaction(self._internal, transaction))
        if result != Result.Ok:
            raise getException(result)
            
        return LobbyTransaction(internal = transaction.contents)
        
    def GetLobbyUpdateTransaction(self, lobbyId: int) -> LobbyTransaction:
        """
        Gets a lobby transaction used for updating an existing lobby.
        """
        transaction = ctypes.POINTER(sdk.IDiscordLobbyTransaction)()
        result = Result(self._internal.get_lobby_update_transaction(self._internal, lobbyId, transaction))
        if result != Result.Ok:
            raise getException(result)
            
        return LobbyTransaction(internal = transaction.contents)
        
    def GetMemberUpdateTransaction(self, lobbyId: int, userId: int) -> LobbyMemberTransaction:
        """
        Gets a new member transaction for a lobby member in a given lobby.
        """
        transaction = ctypes.POINTER(sdk.IDiscordLobbyMemberTransaction)()
        result = Result(self._internal.get_member_update_transaction(self._internal, lobbyId, userId, transaction))
        if result != Result.Ok:
            raise getException(result)
            
        return LobbyMemberTransaction(internal = transaction.contents)
        
    def CreateLobby(self, transaction: LobbyTransaction, callback: Callable[[Result, Optional[Lobby]], None]) -> None:
        """
        Creates a lobby.
        
        Returns discord.enum.Result (int) and Lobby via callback.
        """
        def CCallback(callback_data, result, lobby):
            self._garbage.remove(CCallback)
            result = Result(result)
            if result == Result.Ok:
                callback(result, Lobby(copy = lobby.contents))
            else:
                callback(result, None)
                
        CCallback = self._internal.create_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.create_lobby(self._internal, transaction._internal, ctypes.c_void_p(), CCallback)
        
    def UpdateLobby(self, lobbyId: int, transaction: LobbyTransaction, callback: Callable[[Result], None]) -> None:
        """
        Updates a lobby with data from the given transaction.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.update_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.update_lobby(self._internal, lobbyId, transaction._internal, ctypes.c_void_p(), CCallback)
        
    def DeleteLobby(self, lobbyId: int, callback: Callable[[Result], None]) -> None:
        """
        Deletes a given lobby.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.delete_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.delete_lobby(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def ConnectLobby(self, lobbyId: int, lobbySecret: str, callback: Callable[[Result], None]) -> None:
        """
        Connects the current user to a given lobby.
        """
        def CCallback(callback_data, result, lobby):
            self._garbage.remove(CCallback)
            result = Result(result)
            if result == Result.Ok:
                callback(result, Lobby(copy = lobby.contents))
            else:
                callback(result, None)
            
        CCallback = self._internal.connect_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        _lobbySecret = sdk.DiscordLobbySecret()
        _lobbySecret.value = lobbySecret.encode("utf8")
        
        self._internal.connect_lobby(self._internal, lobbyId, _lobbySecret, ctypes.c_void_p(), CCallback)
        
    def ConnectLobbyWithActivitySecret(self, activitySecret: str, callback: Callable[[Result, Optional[Lobby]], None]) -> None:
        """
        Connects the current user to a lobby; requires the special activity secret from the lobby which is a concatenated lobbyId and secret.
        """
        def CCallback(callback_data, result, lobby):
            self._garbage.remove(CCallback)
            result = Result(result)
            if result == Result.Ok:
                callback(result, Lobby(copy = lobby.contents))
            else:
                callback(result, None)
            
        CCallback = self._internal.connect_lobby_with_activity_secret.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        _activitySecret = sdk.DiscordLobbySecret()
        _activitySecret.value = activitySecret.encode("utf8")
        
        self._internal.connect_lobby_with_activity_secret(self._internal, _activitySecret, ctypes.c_void_p(), CCallback)
        
    def GetLobbyActivitySecret(self, lobbyId: int) -> str:
        """
        Gets the special activity secret for a given lobby.
        """
        lobbySecret = sdk.DiscordLobbySecret()
        
        result = self._internal.get_lobby_activity_secret(self._internal, lobbyId, lobbySecret)
        if result != Result.Ok:
            raise getException(result)
            
        return lobbySecret.value.decode("utf8")
        
    def DisconnectLobby(self, lobbyId: int, callback: Callable[[Result], None]) -> None:
        """
        Disconnects the current user from a lobby.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.disconnect_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.disconnect_lobby(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def GetLobby(self, lobbyId: int) -> Lobby:
        """
        Gets the lobby object for a given lobby id.
        """
        lobby = sdk.DiscordLobby()
        
        result = Result(self._internal.get_lobby(self._internal, lobbyId, lobby))
        if result != Result.Ok:
            raise getException(result)
            
        return Lobby(internal = lobby)
        
    def LobbyMetadataCount(self, lobbyId: int) -> int:
        """
        Returns the number of metadata key/value pairs on a given lobby.
        """
        count = ctypes.c_int32()
        
        result = Result(self._internal.lobby_metadata_count(self._internal, lobbyId, count))
        if result != Result.Ok:
            raise getException(result)
            
        return count.value
        
    def GetLobbyMetadataKey(self, lobbyId: int, index: int) -> str:
        """
        Returns the key for the lobby metadata at the given index.
        """
        metadataKey = sdk.DiscordMetadataKey()
        
        result = Result(self._internal.get_lobby_metadata_key(self._internal, lobbyId, index, metadataKey))
        if result != Result.Ok:
            raise getException(result)
            
        return metadataKey.value.decode("utf8")
        
    def GetLobbyMetadataValue(self, lobbyId: int, key: str) -> str:
        """
        Returns lobby metadata value for a given key and id.
        """
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        
        result = Result(self._internal.get_lobby_metadata_value(self._internal, lobbyId, metadataKey, metadataValue))
        if result != Result.Ok:
            raise getException(result)
            
        return metadataValue.value.decode("utf8")
        
    def MemberCount(self, lobbyId: int) -> int:
        """
        Get the number of members in a lobby.
        """
        count = ctypes.c_int32()
        
        result = Result(self._internal.member_count(self._internal, lobbyId, count))
        if result != Result.Ok:
            raise getException(result)
            
        return count.value
        
    def GetMemberUserId(self, lobbyId: int, index: int) -> int:
        """
        Gets the user id of the lobby member at the given index.
        """
        userId = sdk.DiscordUserId()
        
        result = Result(self._internal.get_member_user_id(self._internal, lobbyId, index, userId))
        if result != Result.Ok:
            raise getException(result)
            
        return userId.value
        
    def GetMemberUser(self, lobbyId: int, userId: int) -> User:
        """
        Gets the user object for a given user id.
        """
        user = sdk.DiscordUser()
        
        result = Result(self._internal.get_member_user(self._internal, lobbyId, userId, user))
        if result != Result.Ok:
            raise getException(result)
            
        return User(internal = user)
        
    def MemberMetadataCount(self, lobbyId: int, userId: int) -> int:
        """
        Gets the number of metadata key/value pairs for the given lobby member.
        """
        count = ctypes.c_int32()
        
        result = Result(self._internal.member_metadata_count(self._internal, lobbyId, userId, count))
        if result != Result.Ok:
            raise getException(result)
            
        return count.value
        
    def GetMemberMetadataKey(self, lobbyId: int, userId: int, index: int) -> str:
        """
        Gets the key for the lobby metadata at the given index on a lobby member.
        """
        metadataKey = sdk.DiscordMetadataKey()
        
        result = Result(self._internal.get_member_metadata_key(self._internal, lobbyId, userId, index, metadataKey))
        if result != Result.Ok:
            raise getException(result)
            
        return metadataKey.value.decode("utf8")
        
    def GetMemberMetadataValue(self, lobbyId: int, userId: int, key: str) -> str:
        """
        Returns user metadata for a given key.
        """
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        
        result = Result(self._internal.get_member_metadata_value(self._internal, lobbyId, userId, metadataKey, metadataValue))
        if result != Result.Ok:
            raise getException(result)
            
        return metadataValue.value.decode("utf8")
        
    def UpdateMember(self, lobbyId: int, userId: int, transaction: LobbyMemberTransaction, callback: Callable[[Result], None]) -> None:
        """
        Updates lobby member info for a given member of the lobby.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.update_member.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.update_member(self._internal, lobbyId, userId, transaction._internal, ctypes.c_void_p(), CCallback)
        
    def SendLobbyMessage(self, lobbyId: int, data: str, callback: Callable[[Result], None]) -> None:
        """
        Sends a message to the lobby on behalf of the current user.
        
        Returns Discord.result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.send_lobby_message.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        data = data.encode("utf8")
        data = (ctypes.c_uint8 * len(data))(*data)
        self._internal.send_lobby_message(self._internal, lobbyId, data, len(data), ctypes.c_void_p(), CCallback)
        
    def GetSearchQuery(self) -> LobbySearchQuery:
        """
        Creates a search object to search available lobbies.
        """
        search_query = (ctypes.POINTER(sdk.IDiscordLobbySearchQuery))()
        result = Result(self._internal.get_search_query(self._internal, ctypes.byref(search_query)))
        if result != Result.Ok:
            raise getException(result)
            
        return LobbySearchQuery(internal = search_query.contents)
        
    def Search(self, search: LobbySearchQuery, callback: Callable[[Result], None]) -> None:
        """
        Searches available lobbies based on the search criteria chosen in the LobbySearchQuery member functions.
        
        Lobbies that meet the criteria are then globally filtered, and can be accessed via iteration with LobbyCount() and GetLobbyId(). The callback fires when the list of lobbies is stable and ready for iteration.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.search.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.search(self._internal, search._internal, ctypes.c_void_p(), CCallback)
        
    def LobbyCount(self) -> int:
        """
        Get the number of lobbies that match the search.
        """
        count = ctypes.c_int32()
        self._internal.lobby_count(self._internal, count)
        return count.value
        
    def GetLobbyId(self, index: int) -> int:
        """
        Returns the id for the lobby at the given index.
        """
        
        lobbyId = sdk.DiscordLobbyId()
        
        result = Result(self._internal.get_lobby_id(self._internal, index, lobbyId))
        if result != Result.Ok:
            raise getException(result)
            
        return lobbyId.value
        
    def ConnectVoice(self, lobbyId: int, callback: Callable[[Result], None]) -> None:
        """
        Connects to the voice channel of the current lobby.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.connect_voice.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.connect_voice(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def DisconnectVoice(self, lobbyId: int, callback: Callable[[Result], None]) -> None:
        """
        Disconnects from the voice channel of a given lobby.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.disconnect_voice.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.disconnect_voice(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def OnLobbyUpdate(self, lobbyId: int) -> None:
        """
        Fires when a lobby is updated.
        """
        pass
        
    def OnLobbyDelete(self, lobbyId: int, reason: str) -> None:
        """
        Fired when a lobby is deleted.
        """
        pass
        
    def OnMemberConnect(self, lobbyId: int, userId: int) -> None:
        """
        Fires when a new member joins the lobby.
        """
        pass
        
    def OnMemberUpdate(self, lobbyId: int, userId: int) -> None:
        """
        Fires when data for a lobby member is updated.
        """
        pass
        
    def OnMemberDisconnect(self, lobbyId: int, userId: int) -> None:
        """
        Fires when a member leaves the lobby.
        """
        pass
        
    def OnLobbyMessage(self, lobbyId: int, userId: int, message: str) -> None:
        """
        Fires when a message is sent to the lobby.
        """
        pass
        
    def OnSpeaking(self, lobbyId: int, userId: int, speaking: bool) -> None:
        """
        Fires when a user connected to voice starts or stops speaking.
        """
        pass
        
    def ConnectNetwork(self, lobbyId: int) -> None:
        """
        Connects to the networking layer for the given lobby ID.
        """
        result = Result(self._internal.connect_network(self._internal, lobbyId))
        if result != Result.Ok:
            raise getException(result)
        
    def DisconnectNetwork(self, lobbyId: int) -> None:
        """
        Disconnects from the networking layer for the given lobby ID.
        """
        result = Result(self._internal.disconnect_network(self._internal, lobbyId))
        if result != Result.Ok:
            raise getException(result)
            
    def FlushNetwork(self) -> None:
        """
        Flushes the network. Call this when you're done sending messages.
        """
        result = Result(self._internal.flush_network(self._internal))
        if result != Result.Ok:
            raise getException(result)
            
    def OpenNetworkChannel(self, lobbyId: int, channelId: int, reliable: bool) -> None:
        """
        Opens a network channel to all users in a lobby on the given channel number. No need to iterate over everyone!
        """
        result = Result(self._internal.open_network_channel(self._internal, lobbyId, channelId, reliable))
        if result != Result.Ok:
            raise getException(result)
            
    def SendNetworkMessage(self, lobbyId: int, userId: int, channelId: int, data: bytes) -> None:
        """
        Sends a network message to the given user ID that is a member of the given lobby ID over the given channel ID.
        """
        data = (ctypes.c_uint8 * len(data))(*data)
        result = Result(self._internal.send_network_message(self._internal, lobbyId, userId, channelId, data, len(data)))
        if result != Result.Ok:
            raise getException(result)
            
    def OnNetworkMessage(self, lobbyId: int, userId: int, channelId: int, data: bytes) -> None:
        """
        Fires when the user receives a message from the lobby's networking layer.
        """
        pass
        