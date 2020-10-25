from . import sdk
from .model import Rect, ImeUnderline
from .enum import Result, ActivityActionType, KeyVariant, MouseButton
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
        
    #
    # The followings function are not documented.
    # Their documentation will be added as the official updates.
    #
    
    def InitDrawingDxgi(self, swapchain: ctypes.c_void_p, useMessageForwarding: bool) -> None:
        result = Result(self._internal.init_drawing_dxgi(self._internal, swapchain, useMessageForwarding))
        if result != Result.Ok:
            raise getException(result)
            
    def OnPresent(self):
        self._internal.on_present(self._internal)
        
    def ForwardMessage(self, message: ctypes.c_void_p) -> None:
        self._internal.forward_message(self._internal, message)
        
    def KeyEvent(self, down: bool, keyCode: str, variant: KeyVariant) -> None:
        keyCode = ctypes.c_char_p(keyCode.encode("utf8"))
        self._internal.key_event(self._internal, down, keyCode, variant)
        
    def CharEvent(self, character: str) -> None:
        character = ctypes.c_char_p(character.encode("utf8"))
        self._internal.char_event(self._internal, character)
        
    def MouseButtonEvent(self, down: int, clickCount: int, which: MouseButton, x: int, y: int) -> None:
        self._internal.mouse_button_event(self._internal, down, clickCount, which, x, y)
        
    def MouseMotionEvent(self, x: int, y: int) -> None:
        self._internal.mouse_motion_event(self._internal, x, y)
        
    def ImeCommitText(self, text: str) -> None:
        text = ctypes.c_char_p(text.encode("utf8"))
        self._internal.ime_commit_text(self._internal, text)
        
    def ImeSetComposition(self, text: str, underlines: ImeUnderline, from_: int, to: int) -> None:
        text = ctypes.c_char_p(text.encode("utf8"))
        self._internal.ime_set_composition(self._internal, text, underlines, ctypes.sizeof(underlines), from_, to) # TODO: check sizeof argument
        
    def ImeCancelComposition(self) -> None:
        self._internal.ime_cancel_composition(self._internal)
        
    def SetImeCompositionRangeCallback(self, callback: Callable[[int, int, Rect], None]) -> None:
        def CCallback(on_ime_composition_range_changed_data, from_, to, bounds, bounds_length):
            self._garbage.remove(CCallback)
            callback(from_, to, Rect(copy = bounds))
            
        CCallback = self._internal.set_ime_composition_range_callback.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.set_ime_composition_range_callback(self._internal, ctypes.c_void_p(), CCallback)
        
    def SetImeSelectionBoundsCallback(self, callback: Callable[[Rect, Rect, bool], None]) -> None:
        def CCallback(on_ime_selection_bounds_changed_data, anchor, focus, is_anchor_first):
            self._garbage.remove(CCallback)
            callback(Rect(internal = anchor), Rect(internal = focus), is_anchor_first)
            
        CCallback = self._internal.set_ime_selection_bounds_callback.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.set_ime_selection_bounds_callback(self._internal, ctypes.c_void_p(), CCallback)
        
    def IsPointInsideClickZone(self, x: int, y: int) -> None:
        point_inside_click_zone = ctypes.c_bool()
        self._internal.is_point_inside_click_zone(self._internal, x, y)
        return point_inside_click_zone.value