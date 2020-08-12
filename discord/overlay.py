from . import sdk
from .enum import Result, ActivityActionType
from .event import bindEvents
from typing import Callable
import ctypes

class OverlayManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordOverlayEvents,
            self._OnToggle
        )
        
    def _OnToggle(self, event_data, locked):
        self.OnToggle(locked)
        
    def IsEnabled(self) -> bool:
        """
        Check whether the user has the overlay enabled or disabled.
        """
        enabled = ctypes.c_bool()
        self._internal.is_enabled(self._internal, enabled)
        return enabled.value
        
    def IsLocked(self) -> bool:
        """
        Check if the overlay is currently locked or unlocked
        """
        locked = ctypes.c_bool()
        self._internal.is_locked(self._internal, locked)
        return locked.value
        
    def SetLocked(self, locked: bool, callback: Callable[[Result], None]) -> None:
        """
        Locks or unlocks input in the overlay.
        """
        def CCallback(event_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.set_locked.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.set_locked(self._internal, locked, ctypes.c_void_p(), CCallback)
        
    def OpenActivityInvite(self, type: ActivityActionType, callback: Callable[[Result], None]) -> None:
        """
        Opens the overlay modal for sending game invitations to users, channels, and servers.
        """
        def CCallback(event_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.open_activity_invite.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.open_activity_invite(self._internal, type, ctypes.c_void_p(), CCallback)
        
    def OpenGuildInvite(self, code: str, callback: Callable[[Result], None]) -> None:
        """
        Opens the overlay modal for joining a Discord guild, given its invite code.
        """
        def CCallback(event_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.open_guild_invite.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        code = ctypes.c_char_p(code.encode("utf8"))
        self._internal.open_guild_invite(self._internal, code, ctypes.c_void_p(), CCallback)
        
    def OpenVoiceSettings(self, callback: Callable[[Result], None]) -> None:
        """
        Opens the overlay widget for voice settings for the currently connected application.
        """
        def CCallback(event_data, result):
            self._garbage.remove(CCallback)
            result = Result(result)
            callback(result)
            
        CCallback = self._internal.open_voice_settings.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.open_voice_settings(self._internal, ctypes.c_void_p(), CCallback)
        
    def OnToggle(self, locked: bool) -> None:
        """
        Fires when the overlay is locked or unlocked (a.k.a. opened or closed)
        """
        pass