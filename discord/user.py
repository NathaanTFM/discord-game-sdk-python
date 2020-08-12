from . import sdk
from .model import User
from .enum import Result, PremiumType, UserFlag
from .event import bindEvents
from .exception import getException
from typing import Callable
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
        
    def GetCurrentUser(self) -> User:
        """
        Fetch information about the currently connected user account.
        """
        user = sdk.DiscordUser()
        result = Result(self._internal.get_current_user(self._internal, user))
        if result != Result.Ok:
            raise getException(result)
            
        return User(internal = user)
        
    def GetUser(self, userId: int, callback: Callable) -> None:
        """
        Get user information for a given id.
        
        Returns discord.enum.Result (int) and User via callback.
        """
        def CCallback(callback_data, result, user):
            self._garbage.remove(CCallback)
            result = Result(result)
            if result == Result.Ok:
                callback(result, User(copy = user.contents))
            else:
                callback(result, None)
                
        CCallback = self._internal.get_user.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.get_user(self._internal, userId, ctypes.c_void_p(), CCallback)
        
    def GetCurrentUserPremiumType(self) -> PremiumType:
        """
        Get the PremiumType for the currently connected user.
        """
        premiumType = ctypes.c_int32()
        result = Result(self._internal.get_current_user_premium_type(self._internal, premiumType))
        if result != Result.Ok:
            raise getException(result)
            
        return PremiumType(premiumType.value)
        
    def CurrentUserHasFlag(self, flag: UserFlag) -> bool:
        """
        See whether or not the current user has a certain UserFlag on their account.
        """
        hasFlag = ctypes.c_bool()
        result = Result(self._internal.current_user_has_flag(self._internal, flag, hasFlag))
        if result != Result.Ok:
            raise getException(result)
            
        return hasFlag.value
        
    def OnCurrentUserUpdate(self) -> None:
        """
        Fires when the User struct of the currently connected user changes.
        """
        pass
        