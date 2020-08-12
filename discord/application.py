from . import sdk
from .model import OAuth2Token
from .enum import Result
from typing import Callable, Optional
import ctypes

class SignedAppTicket:
    def __init__(self):
        self.application_id = None
        self.user = None
        self.entitlements = None
        self.timestamp = None

class ApplicationManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = None
        
    def GetCurrentLocale(self) -> str:
        """
        Get the locale the current user has Discord set to.
        """
        locale = sdk.DiscordLocale()
        self._internal.get_current_locale(self._internal, locale)
        return locale.value.decode("utf8")
        
    def GetCurrentBranch(self) -> str:
        """
        Get the name of pushed branch on which the game is running.
        """
        branch = sdk.DiscordBranch()
        self._internal.get_current_branch(self._internal, branch)
        return branch.value.decode("utf8")
        
    def GetOAuth2Token(self, callback: Callable[[Result, Optional[OAuth2Token]], None]) -> None:
        """
        Retrieve an oauth2 bearer token for the current user.
        
        Returns discord.enum.Result (int) and OAuth2Token (str) via callback.
        """
        def CCallback(callback_data, result, oauth2_token):
            self._garbage.remove(CCallback)
            if result == Result.Ok:
                callback(result, OAuth2Token(copy = oauth2_token.contents))
            else:
                callback(result, None)
            
        CCallback = self._internal.get_oauth2_token.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.get_oauth2_token(self._internal, ctypes.c_void_p(), CCallback)
        
    def ValidateOrExit(self, callback: Callable[[Result], None]) -> None:
        """
        Checks if the current user has the entitlement to run this game.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.validate_or_exit.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.validate_or_exit(self._internal, ctypes.c_void_p(), CCallback)
        
    def GetTicket(self, callback: Callable[[Result, Optional[str]], None]) -> None:
        """
        Get the signed app ticket for the current user.
        
        Returns discord.Enum.Result (int) and str via callback.
        """
        def CCallback(callback_data, result, data):
            self._garbage.remove(CCallback)
            if result == Result.Ok:
                callback(result, data.contents.value.decode("utf8"))
            else:
                callback(result, None)
            
        CCallback = self._internal.get_ticket.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.get_ticket(self._internal, ctypes.c_void_p(), CCallback)