from . import sdk
from .model import InputMode
from .enum import Result
from .event import bindEvents
from .exception import getException
from typing import Callable
import ctypes

class VoiceManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordVoiceEvents,
            self._OnCurrentUserUpdate
        )
        
    def _OnCurrentUserUpdate(self, event_data):
        self.OnCurrentUserUpdate()
        
    def GetInputMode(self) -> InputMode:
        """
        Get the current voice input mode for the user
        """
        input_mode = sdk.DiscordInputMode()
        result = self._internal.get_input_mode(self._internal, input_mode)
        if result != Result.Ok:
            raise getException(result)
            
        return InputMode(internal = input_mode)
        
    def SetInputMode(self, inputMode: InputMode, callback: Callable) -> None:
        """
        Sets a new voice input mode for the uesr.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.set_input_mode.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.set_input_mode(self._internal, inputMode._internal, ctypes.c_void_p(), CCallback)
        
    def IsSelfMute(self) -> bool:
        """
        Whether the connected user is currently muted.
        """
        mute = ctypes.c_bool()
        result = self._internal.is_self_mute(self._internal, mute)
        if result != Result.Ok:
            raise getException(result)
            
        return mute.value
        
    def SetSelfMute(self, mute: bool) -> None:
        """
        Mutes or unmutes the currently connected user.
        """
        result = self._internal.set_self_mute(self._internal, mute)
        if result != Result.Ok:
            raise getException(result)
        
    def IsSelfDeaf(self) -> bool:
        """
        Whether the connected user is currently deafened.
        """
        deaf = ctypes.c_bool()
        result = self._internal.is_self_deaf(self._internal, deaf)
        if result != Result.Ok:
            raise getException(result)
            
        return deaf.value
        
    def SetSelfDeaf(self, deaf: bool) -> None:
        """
        Deafens or undefeans the currently connected user.
        """
        result = self._internal.set_self_deaf(self._internal, deaf)
        if result != Result.Ok:
            raise getException(result)
        
    def IsLocalMute(self, userId: int) -> bool:
        """
        Whether the given user is currently muted by the connected user.
        """
        mute = ctypes.c_bool()
        result = self._internal.is_local_mute(self._internal, userId, mute)
        if result != Result.Ok:
            raise getException(result)
            
        return mute.value
        
    def SetLocalMute(self, userId: int, mute: bool) -> None:
        """
        Mutes or unmutes the given user for the currently connected user.
        """
        result = self._internal.set_local_mute(self._internal, userId, mute)
        if result != Result.Ok:
            raise getException(result)
        
    def GetLocalVolume(self, userId: int) -> int:
        """
        Gets the local volume for a given user.
        """
        volume = ctypes.c_uint8()
        result = self._internal.get_local_volume(self._internal, userId, volume)
        if result != Result.Ok:
            raise getException(result)
            
        return volume.value
        
    def SetLocalVolume(self, userId: int, volume: int) -> None:
        """
        Sets the local volume for a given user. 
        """
        result = self._internal.set_local_volume(self._internal, userId, volume)
        if result != Result.Ok:
            raise getException(result)
            
    def OnCurrentUserUpdate(self) -> None:
        # This event is not documented anywhere (yet?)
        pass