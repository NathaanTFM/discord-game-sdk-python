from . import sdk
from .model import Lobby
from .enum import Result
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
        self._events = None
        
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
                callback(result, Lobby(internal = lobby.contents))
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
            
        CCallback = self._internal.update_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.delete_lobby(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def ConnectLobby(self, lobbyId, lobbySecret, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.update_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.connect_lobby(self._internal, lobbyId, lobbySecret, ctypes.c_void_p(), CCallback)
        
    def ConnectLobbyWithActivitySecret(self, activitySecret, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.update_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.connect_lobby_with_activity_secret(self._internal, activitySecret, ctypes.c_void_p(), CCallback)
        
    def GetLobbyActivitySecret(self, lobbyId):
        raise NotImplementedError
        
    def DisconnectLobby(self, lobbyId, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.update_lobby.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.disconnect_lobby(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def GetLobby(self, lobbyId):
        lobby = sdk.DiscordLobby()
        
        result = self._internal.get_lobby(self._internal, lobbyId, lobby)
        if result != result.Ok:
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
        
        result = self._internal.get_lobby_metadata_value(self._internal, lobbyId, index, metadataKey)
        if result != Result.Ok:
            raise Exception(result)
            
        return metadataKey.value
        
    def GetLobbyMetadataValue(self, lobbyId, key):
        metadataKey = sdk.DiscordMetadataKey()
        metadataKey.value = key.encode("utf8")
        
        metadataValue = sdk.DiscordMetadataValue()
        
        result = self._internal.get_lobby_metadata_value(self._internal, lobbyId, metadataKey, metadataValue)
        if result != Result.Ok:
            raise Exception(result)
            
        return metadataValue.value
        
    def MemberCount(self, lobbyId):
        raise NotImplementedError
        
    def GetMemberUserId(self, lobbyId, index):
        raise NotImplementedError
        
    def GetMemberUser(self, lobbyId, userId):
        raise NotImplementedError
        
    def MemberMetadataCount(self, lobbyId, userId):
        raise NotImplementedError
        
    def GetMemberMetadataKey(self, lobbyId, userId, index):
        raise NotImplementedError
        
    def GetMemberMetadataValue(self, lobbyId, userId, key):
        raise NotImplementedError
        
    def UpdateMember(self, lobbyId, userId, transaction, callback):
        raise NotImplementedError
        
    def SendLobbyMessage(self, lobbyId, data, callback):
        raise NotImplementedError
        
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
            
        CCallback = self._internal.search.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.connect_voice(self._internal, lobbyId, ctypes.c_void_p(), CCallback)
        
    def DisconnectVoice(self, lobbyId, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.search.argtypes[-1](CCallback)
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
        result = None
        if result != Result.Ok:
            raise Exception(Result)
        
    def DisconnectNetwork(self, lobbyId):
        result = None
        if result != Result.Ok:
            raise Exception(Result)
            
    def FlushNetwork(self):
        result = None
        if result != Result.Ok:
            raise Exception(Result)
            
    def OpenNetworkChannel(self, lobbyId, channelId, reliable):
        result = None
        if result != Result.Ok:
            raise Exception(Result)
            
    def SendNetworkMessage(self, lobbyId, userId, channelId, reliable):
        result = None
        if result != Result.Ok:
            raise Exception(Result)
            
    def OnNetworkMessage(self, lobbyId, userId, channelId, data):
        pass