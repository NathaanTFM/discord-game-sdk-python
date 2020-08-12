from .enum import Result
from .model import UserAchievement
from .event import bindEvents
from .exception import getException
from . import sdk
from typing import Callable
import ctypes

class AchievementManager:
    def __init__(self):
        self._internal = None
        self._garbage = []
        self._events = bindEvents(sdk.IDiscordAchievementEvents,
            self._OnUserAchievementUpdate
        )
        
    def _OnUserAchievementUpdate(self, event_data, user_achievement):
        self.OnUserAchievementUpdate(UserAchievement(copy = user_achievement.contents))
        
    def SetUserAchievement(self, achievementId: int, percentComplete: int, callback: Callable) -> None:
        """
        Updates the current user's status for a given achievement.
        
        Returns discord.enum.Result via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.set_user_achievement.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.set_user_achievement(self._internal, achievementId, percentComplete, ctypes.c_void_p(), CCallback)
        
    def FetchUserAchievements(self, callback: Callable) -> None:
        """
        Loads a stable list of the current user's achievements to iterate over.
        
        Returns discord.enum.Result via callback.
        """
        def CCallback(callback_data, result):
            self._garbage.remove(CCallback)
            callback(result)
            
        CCallback = self._internal.fetch_user_achievements.argtypes[-1](CCallback)
        self._garbage.append(CCallback) # prevent it from being garbage collected
        
        self._internal.fetch_user_achievements(self._internal, ctypes.c_void_p(), CCallback)
        
    def CountUserAchievements(self) -> int:
        """
        Counts the list of a user's achievements for iteration.
        """
        count = ctypes.c_int32()
        self._internal.count_user_achievements(self._internal, count)
        return count.value
        
    def GetUserAchievementAt(self, index: int) -> UserAchievement:
        """
        Gets the user's achievement at a given index of their list of achievements.
        """
        achievement = sdk.DiscordUserAchievement()
        result = self._internal.get_user_achievement_at(self._internal, index, achievement)
        if result != Result.Ok:
            raise getException(result)
            
        return UserAchievement(internal = achievement)
        
    def GetUserAchievement(self, achievementId: int) -> None:
        """
        Gets the user achievement for the given achievement id. 
        """
        achievement = sdk.DiscordUserAchievement()
        result = self._internal.get_user_achievement(self._internal, achievementId, achievement)
        if result != Result.Ok:
            raise getException(result)
            
        return UserAchievement(internal = achievement)
        
    def OnUserAchievementUpdate(self, achievement: UserAchievement) -> None:
        """
        Fires when an achievement is updated for the currently connected user
        """
        pass