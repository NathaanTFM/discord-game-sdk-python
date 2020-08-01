from . import sdk
from .model import Lobby, User
from .enum import Result
from .event import bindEvents
import ctypes

class LobbyTransaction:
    def __init__(self, internal):
        self._internal = internal
        
    def SetType(self, type):
        result = self._internal.set_type(self._internal, type)
        if result != Result.Ok:
            raise Exception(result)
            
    def SetOwner(self, userId):
        result = self._internal.set_owner(self._internal, userId)
        if result != Result.Ok:
            raise Exception(result)
        
    def SetCapacity(self, capacity):
        result = self._internal.set_capacity(self._internal, capacity)
        if result != Result.Ok:
            raise Exception(result)
        
    def SetMetadata(self, key, value):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        metadataValue.value = value.encode("utf8")
        
        result = self._internal.set_metadata(self._internal, metadataKey, metadataValue)
        if result != Result.Ok:
            raise Exception(result)
    
    def DeleteMetadata(self, key):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
            
        result = self._internal.delete_metadata(self._internal, metadataKey)
        if result != Result.Ok:
            raise Exception(result)
    
    def SetLocked(self, locked):
        result = self._internal.set_locked(self._internal, locked)
        if result != Result.Ok:
            raise Exception(result)
    
class LobbyMemberTransaction:
    def __init__(self, internal):
        self._internal = internal
        
    def SetMetadata(self, key, value):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        metadataValue.value = value.encode("utf8")
        
        result = self._internal.set_metadata(self._internal, metadataKey, metadataValue)
        if result != Result.Ok:
            raise Exception(result)
    
    def DeleteMetadata(self, key):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        result = self._internal.delete_metadata(self._internal, metadataKey)
        if result != Result.Ok:
            raise Exception(result)
    
class LobbySearchQuery:
    def __init__(self, internal):
        self._internal = internal
        
    def Filter(self, key, comp, cast, value):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        metadataValue.value = value.encode("utf8")
        
        result = self._internal.filter(self._internal, metadataKey, comp, cast, metadataValue)
        if result != Result.Ok:
            raise Exception(result)
    
    def Sort(self, key, cast, value):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        metadataValue.value = value.encode("utf8")
        
        result = self._internal.sort(self._internal, metadataKey, cast, metadataValue)
        if result != Result.Ok:
            raise Exception(result)
    
    def Limit(self, limit):
        result = self._internal.limit(self._internal, limit)
        if result != Result.Ok:
            raise Exception(result)
    
    def Distance(self, distance):
        result = self._internal.distance(self._internal, distance)
        if result != Result.Ok:
            raise Exception(result)
    
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
        
    def GetLobbyCreateTransaction(self):
        transaction = ctypes.POINTER(sdk.IDiscordLobbyTransaction)()
        result = self._internal.get_lobby_create_transaction(self._internal, transaction)
        if result != Result.Ok:
            raise Exception(result)
            
        return LobbyTransaction(internal = transaction.contents)
        
    def GetLobbyUpdateTransaction(self, lobbyId):
        transaction = ctypes.POINTER(sdk.IDiscordLobbyTransaction)()
        result = self._internal.get_lobby_update_transaction(self._internal, lobbyId, transaction)
        if result != Result.Ok:
            raise Exception(result)
            
        return LobbyTransaction(internal = transaction.contents)
        
    def GetMemberUpdateTransaction(self, lobbyId, userId):
        transaction = ctypes.POINTER(sdk.IDiscordLobbyMemberTransaction)()
        result = self._internal.get_member_update_transaction(self._internal, lobbyId, userId, transaction)
        if result != Result.Ok:
            raise Exception(result)
            
        return LobbyMemberTransaction(internal = transaction.contents)
        
    def CreateLobby(self, transaction, callback):
        def CCallback(callback_data, result, lobby):
            self._garbage.remove(CCallback)
            if result == Result.Ok:
                callback(result, Lobby(copy = lobby.contents))
            else:
                callback(result, None)
                
        CCallback = self._internal.create_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.create_lobby(self._internal, transaction._internal, ctypes.c_void_p(), CCallback)
        
    def UpdateLobby(self, lobbyId, transaction, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.update_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.update_lobby(self._internal, lobbyId, transaction._internal, ctypes.c_void_p(), CCallback)
        
    def DeleteLobby(self, lobbyId, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.delete_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.delete_lobby(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def ConnectLobby(self, lobbyId, lobbySecret, callback):
        def CCallback(callback_data, result, lobby):
            self._garbage.remove(CCallback)
            if result == Result.Ok:
                callback(result, Lobby(copy = lobby.contents))
            else:
                callback(result, None)
            
        CCallback = self._internal.connect_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        _lobbySecret = sdk.DiscordLobbySecret()
        _lobbySecret.value = lobbySecret.encode("utf8")
        
        self._internal.connect_lobby(self._internal, lobbyId, _lobbySecret, ctypes.c_void_p(), CCallback)
        
    def ConnectLobbyWithActivitySecret(self, activitySecret, callback):
        def CCallback(callback_data, result, lobby):
            self._garbage.remove(CCallback)
            if result == Result.Ok:
                callback(result, Lobby(copy = lobby.contents))
            else:
                callback(result, None)
            
        CCallback = self._internal.connect_lobby_with_activity_secret.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        _activitySecret = sdk.DiscordLobbySecret()
        _activitySecret.value = activitySecret.encode("utf8")
        
        self._internal.connect_lobby_with_activity_secret(self._internal, _activitySecret, ctypes.c_void_p(), CCallback)
        
    def GetLobbyActivitySecret(self, lobbyId):
        lobbySecret = sdk.DiscordLobbySecret()
        
        result = self._internal.get_lobby_activity_secret(self._internal, lobbyId, lobbySecret)
        if result != result.Ok:
            raise Exception(result)
            
        return lobbySecret.value.decode("utf8")
        
    def DisconnectLobby(self, lobbyId, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.disconnect_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.disconnect_lobby(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def GetLobby(self, lobbyId):
        lobby = sdk.DiscordLobby()
        
        result = self._internal.get_lobby(self._internal, lobbyId, lobby)
        if result != Result.Ok:
            raise Exception(result)
            
        return Lobby(internal = lobby)
        
    def LobbyMetadataCount(self, lobbyId):
        count = sdk.c_int32()
        
        result = self._internal.lobby_metadata_count(self._internal, lobbyId, count)
        if result != Result.Ok:
            raise Exception(result)
            
        return count.value
        
    def GetLobbyMetadataKey(self, lobbyId, index):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        
        result = self._internal.get_lobby_metadata_key(self._internal, lobbyId, index, metadataKey)
        if result != Result.Ok:
            raise Exception(result)
            
        return metadataKey.value.decode("utf8")
        
    def GetLobbyMetadataValue(self, lobbyId, key):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        
        result = self._internal.get_lobby_metadata_value(self._internal, lobbyId, metadataKey, metadataValue)
        if result != Result.Ok:
            raise Exception(result)
            
        return metadataValue.value.decode("utf8")
        
    def MemberCount(self, lobbyId):
        count = sdk.c_int32()
        
        result = self._internal.member_count(self._internal, lobbyId, count)
        if result != Result.Ok:
            raise Exception(result)
            
        return count.value
        
    def GetMemberUserId(self, lobbyId, index):
        userId = sdk.DiscordUserId()
        
        result = self._internal.get_member_user_id(self._internal, lobbyId, index, userId)
        if result != Result.Ok:
            raise Exception(result)
            
        return userId.value
        
    def GetMemberUser(self, lobbyId, userId):
        user = sdk.DiscordUser()
        
        result = self._internal.get_member_user(self._internal, lobbyId, userId, user)
        if result != Result.Ok:
            raise Exception(result)
            
        return User(internal = user)
        
    def MemberMetadataCount(self, lobbyId, userId):
        count = sdk.c_int32()
        
        result = self._internal.member_metadata_count(self._internal, lobbyId, userId, count)
        if result != Result.Ok:
            raise Exception(result)
            
        return count.value
        
    def GetMemberMetadataKey(self, lobbyId, userId, index):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        
        result = self._internal.get_member_metadata_key(self._internal, lobbyId, userId, index, metadataKey)
        if result != Result.Ok:
            raise Exception(result)
            
        return metadataKey.value.decode("utf8")
        
    def GetMemberMetadataValue(self, lobbyId, userId, key):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        
        result = self._internal.get_member_metadata_value(self._internal, lobbyId, userId, metadataKey, metadataValue)
        if result != Result.Ok:
            raise Exception(result)
            
        return metadataValue.value.decode("utf8")
        
    def UpdateMember(self, lobbyId, userId, transaction, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.update_member.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.update_member(self._internal, lobbyId, userId, transaction._internal, ctypes.c_void_p(), CCallback)
        
    def SendLobbyMessage(self, lobbyId, data, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.send_lobby_message.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        data = data.encode("utf8")
        data = (ctypes.c_uint8 * len(data))(*data)
        self._internal.send_lobby_message(self._internal, lobbyId, data, len(data), ctypes.c_void_p(), CCallback)
        
    def GetSearchQuery(self):
        search_query = (ctypes.POINTER(sdk.IDiscordLobbySearchQuery))()
        result = self._internal.get_search_query(self._internal, ctypes.byref(search_query))
        if result != Result.Ok:
            raise Exception(result)
            
        return LobbySearchQuery(internal = search_query.contents)
        
    def Search(self, search, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.search.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.search(self._internal, search._internal, ctypes.c_void_p(), CCallback)
        
    def LobbyCount(self):
        count = sdk.c_int32()
        self._internal.lobby_count(self._internal, count)
        return count.value
        
    def GetLobbyId(self, index):
        lobbyId = sdk.DiscordLobbyId()
        
        result = self._internal.get_lobby_id(self._internal, index, lobbyId)
        if result != Result.Ok:
            raise Exception(result)
            
        return lobbyId.value
        
    def ConnectVoice(self, lobbyId, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.connect_voice.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.connect_voice(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def DisconnectVoice(self, lobbyId, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.disconnect_voice.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.disconnect_voice(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def OnLobbyUpdate(self, lobbyId):
        pass
        
    def OnLobbyDelete(self, lobbyId, reason):
        pass
        
    def OnMemberConnect(self, lobbyId, userId):
        pass
        
    def OnMemberUpdate(self, lobbyId, userId):
        pass
        
    def OnMemberDisconnect(self, lobbyId, userId):
        pass
        
    def OnLobbyMessage(self, lobbyId, userId, message):
        pass
        
    def OnSpeaking(self, lobbyId, userId, speaking):
        pass
        
    def ConnectNetwork(self, lobbyId):
        result = self._internal.connect_network(self._internal, lobbyId)
        if result != Result.Ok:
            raise Exception(result)
        
    def DisconnectNetwork(self, lobbyId):
        result = self._internal.disconnect_network(self._internal, lobbyId)
        if result != Result.Ok:
            raise Exception(result)
            
    def FlushNetwork(self):
        result = self._internal.flush_network(self._internal)
        if result != Result.Ok:
            raise Exception(result)
            
    def OpenNetworkChannel(self, lobbyId, channelId, reliable):
        result = self._internal.open_network_channel(self._internal, lobbyId, channelId, reliable)
        if result != Result.Ok:
            raise Exception(result)
            
    def SendNetworkMessage(self, lobbyId, userId, channelId, data):
        data = (ctypes.c_uint8 * len(data))(*data)
        result = self._internal.send_network_message(self._internal, lobbyId, userId, channelId, data, len(data))
        if result != Result.Ok:
            raise Exception(result)
            
    def OnNetworkMessage(self, lobbyId, userId, channelId, data):
        pass
        