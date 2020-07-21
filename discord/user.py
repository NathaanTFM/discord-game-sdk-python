from . import sdk
from .model import User
from .enum import Result
from .event import bindEvents
import ctypes

class UserManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordUserEvents,
            self._OnCurrentUserUpdate
        )
        
    def _OnCurrentUserUpdate(self, event_data):
        self.OnCurrentUserUpdate()
        
    def GetCurrentUser(self):
        user = sdk.DiscordUser()
        result = self._internal.get_current_user(self._internal, user)
        if result != Result.Ok:
            raise Exception(result)
            
        return User(internal = user)
        
    def GetUser(self, userId, callback):
        def CCallback(callback_data, result, user):
            self._garbage.remove(CCallback)
            if result == Result.Ok:
                callback(result, User(internal = user.contents))
            else:
                callback(result, None)
                
        CCallback = self._internal.get_user.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.get_user(self._internal, userId, ctypes.c_void_p(), CCallback)
        
    def GetCurrentUserPremiumType(self):
        premiumType = ctypes.c_int32()
        result = self._internal.get_current_user_premium_type(self._internal, premiumType)
        if result != Result.Ok:
            raise Exception(result)
            
        return premiumType.value
        
    def CurrentUserHasFlag(self, flag):
        hasFlag = ctypes.c_bool()
        result = self._internal.current_user_has_flag(self._internal, flag, hasFlag)
        if result != Result.Ok:
            raise Exception(result)
            
        return hasFlag.value
        
    def OnCurrentUserUpdate(self):
        pass
        