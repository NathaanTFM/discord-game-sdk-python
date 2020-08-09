from . import sdk
from .model import User, Activity
from .event import bindEvents
from .enum import Result, ActivityJoinRequestReply, ActivityActionType
from typing import Callable
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
        self.OnActivityJoinRequest(User(copy = user.contents))
        
    def _OnActivityInvite(self, event_data, type, user, activity):
        self.OnActivityInvite(type, User(copy = user.contents), Activity(copy = activity.contents))
        
    def RegisterCommand(self, command: str) -> Result:
        """
        Registers a command by which Discord can launch your game.
        """
        result = self._internal.register_command(self._internal, command.encode("utf8"))
        return result
        
    def RegisterSteam(self, steamId: int) -> Result:
        """
        Registers your game's Steam app id for the protocol `steam://run-game-id/<id>`.
        """
        result = self._internal.register_steam(self._internal, steamId)
        return result
        
    def UpdateActivity(self, activity: Activity, callback: Callable) -> None:
        """
        Set a user's presence in Discord to a new activity.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.update_activity.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.update_activity(self._internal, activity._internal, ctypes.c_void_p(), CCallback)
        
    def ClearActivity(self, callback: Callable) -> None:
        """
        Clears a user's presence in Discord to make it show nothing.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.clear_activity.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.clear_activity(self._internal, ctypes.c_void_p(), CCallback)
        
    def SendRequestReply(self, userId: int, reply: ActivityJoinRequestReply, callback: Callable) -> None:
        """
        Sends a reply to an Ask to Join request.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.send_request_reply.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.send_request_reply(self._internal, userId, reply, ctypes.c_void_p(), CCallback)
        
    def SendInvite(self, userId: int, type: ActivityActionType, content: str, callback: Callable) -> None:
        """
        Sends a game invite to a given user.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.send_invite.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.send_invite(self._internal, userId, type, content.encode("utf8"), ctypes.c_void_p(), CCallback)
        
    def AcceptInvite(self, userId: int, callback: Callable) -> None:
        """
        Accepts a game invitation from a given userId.
        
        Returns discord.enum.Result (int) via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.accept_invite.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.accept_invite(self._internal, userId, ctypes.c_void_p(), CCallback)
        
    def OnActivityJoin(self, joinSecret: str) -> None:
        """
        Fires when a user accepts a game chat invite or receives confirmation from Asking to Join.
        """
        pass
        
    def OnActivitySpectate(self, spectateSecret: str) -> None:
        """
        Fires when a user accepts a spectate chat invite or clicks the Spectate button on a user's profile.
        """
        pass
    
    def OnActivityJoinRequest(self, user: User) -> None:
        """
        Fires when a user asks to join the current user's game.
        """
        pass
        
    def OnActivityInvite(self, type: ActivityActionType, user: User, activity: Activity) -> None:
        """
        Fires when the user receives a join or spectate invite.
        """
        pass
        