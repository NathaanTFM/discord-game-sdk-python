from . import sdk
from .model import User, Activity
from .event import bindEvents
import ctypes

class ActivityManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordActivityEvents,
            self._OnActivityJoin,
            self._OnActivitySpectate,
            self._OnActivityJoinRequest,
            self._OnActivityInvite
        )
        
    def _OnActivityJoin(self, event_data, secret):
        self.OnActivityJoin(secret.decode("utf8"))
        
    def _OnActivitySpectate(self, event_data, secret):
        self.OnActivitySpectate(secret.decode("utf8"))
        
    def _OnActivityJoinRequest(self, event_data, user):
        self.OnActivityJoinRequest(User(internal = user.contents))
        
    def _OnActivityInvite(self, event_data, type, user, activity):
        self.OnActivityInvite(type, User(internal = user.contents), Activity(internal = activity.contents))
        
    def RegisterCommand(self, command):
        result = self._internal.register_command(self._internal, command.encode("utf8"))
        return result
        
    def RegisterSteam(self, steamId):
        result = self._internal.register_steam(self._internal, steamId)
        return result
        
    def UpdateActivity(self, activity, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.update_activity.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.update_activity(self._internal, activity._internal, ctypes.c_void_p(), CCallback)
        
    def ClearActivity(self, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.clear_activity.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.clear_activity(self._internal, ctypes.c_void_p(), CCallback)
        
    def SendRequestReply(self, userId, reply, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.send_request_reply.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.send_request_reply(self._internal, userId, reply, ctypes.c_void_p(), CCallback)
        
    def SendInvite(self, userId, type, content, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.send_invite.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.send_invite(self._internal, userId, type, content.encode("utf8"), ctypes.c_void_p(), CCallback)
        
    def AcceptInvite(self, userId, callback):
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.accept_invite.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.accept_invite(self._internal, userId, ctypes.c_void_p(), CCallback)
        
    def OnActivityJoin(self, joinSecret):
        pass
        
    def OnActivitySpectate(self, spectateSecret):
        pass
    
    def OnActivityJoinRequest(self, user):
        pass
        
    def OnActivityInvite(self, type, user, activity):
        pass
        