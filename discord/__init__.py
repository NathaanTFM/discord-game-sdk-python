from . import sdk
from .activity import ActivityManager
from .relationship import RelationshipManager
from .image import ImageManager
from .user import UserManager
from .lobby import LobbyManager
from .network import NetworkManager
from .overlay import OverlayManager
from .application import ApplicationManager
from .storage import StorageManager
from .store import StoreManager
from .voice import VoiceManager
from .achievement import AchievementManager
from .enum import Result
import ctypes
    
class Discord:
    def __init__(self, clientId, flags):
        self._activityManager = ActivityManager()
        self._relationshipManager = RelationshipManager()
        self._imageManager = ImageManager()
        self._userManager = UserManager()
        self._lobbyManager = LobbyManager()
        self._networkManager = NetworkManager()
        self._overlayManager = OverlayManager()
        self._applicationManager = ApplicationManager()
        self._storageManager = StorageManager()
        self._storeManager = StoreManager()
        self._voiceManager = VoiceManager()
        self._achievementManager = AchievementManager()
        
        self._garbage = []
        
        version = sdk.DiscordVersion(2)
        
        params = sdk.DiscordCreateParams()
        params.client_id = clientId
        params.flags = flags
        
        sdk.DiscordCreateParamsSetDefault(params)
        params.activity_events = self._activityManager._events
        params.relationship_events = self._relationshipManager._events
        params.image_events = self._imageManager._events
        params.user_events = self._userManager._events
        params.lobby_events = self._lobbyManager._events
        params.network_events = self._networkManager._events
        params.overlay_events = self._overlayManager._events
        params.application_events = self._applicationManager._events
        params.storage_events = self._storageManager._events
        params.store_events = self._storeManager._events
        params.voice_events = self._voiceManager._events
        params.achievement_events = self._achievementManager._events
        
        ptr = (ctypes.POINTER(sdk.IDiscordCore))()
        
        self.core = None
        
        result = sdk.DiscordCreate(version, params, ctypes.byref(ptr))
        if result != Result.Ok:
            raise Exception(result)
        
        self.core = ptr.contents
        
    def __del__(self):
        if self.core:
            self.core.destroy(self.core)
        
    def SetLogHook(self, min_level, hook):
        def CHook(hook_data, level, message):
            hook(level, message.decode("utf8"))
            
        CHook = self.core.set_log_hook.argtypes[-1](CHook)
        self._garbage.append(CHook)
        
        self.core.set_log_hook(self.core, min_level, ctypes.c_void_p(), CHook)
        
    def RunCallbacks(self):
        return self.core.run_callbacks(self.core)
        
    def GetActivityManager(self):
        if not self._activityManager._internal:
            self._activityManager._internal = self.core.get_activity_manager(self.core).contents
        
        return self._activityManager
        
    def GetRelationshipManager(self):
        if not self._relationshipManager._internal:
            self._relationshipManager._internal = self.core.get_relationship_manager(self.core).contents
        
        return self._relationshipManager
        
    def GetImageManager(self):
        if not self._imageManager._internal:
            self._imageManager._internal = self.core.get_image_manager(self.core).contents
        
        return self._imageManager
        
    def GetUserManager(self):
        if not self._userManager._internal:
            self._userManager._internal = self.core.get_user_manager(self.core).contents
        
        return self._userManager
        
    def GetLobbyManager(self):
        if not self._lobbyManager._internal:
            self._lobbyManager._internal = self.core.get_lobby_manager(self.core).contents
        
        return self._lobbyManager
        
    def GetNetworkManager(self):
        if not self._networkManager._internal:
            self._networkManager._internal = self.core.get_network_manager(self.core).contents
        
        return self._networkManager
        
    def GetOverlayManager(self):
        if not self._overlayManager._internal:
            self._overlayManager._internal = self.core.get_overlay_manager(self.core).contents
        
        return self._overlayManager
        
    def GetApplicationManager(self):
        if not self._applicationManager._internal:
            self._applicationManager._internal = self.core.get_application_manager(self.core).contents
        
        return self._applicationManager
        
    def GetStorageManager(self):
        if not self._storageManager._internal:
            self._storageManager._internal = self.core.get_storage_manager(self.core).contents
        
        return self._storageManager
        
    def GetStoreManager(self):
        if not self._storeManager._internal:
            self._storeManager._internal = self.core.get_store_manager(self.core).contents
        
        return self._storeManager
        
    def GetVoiceManager(self):
        if not self._voiceManager._internal:
            self._voiceManager._internal = self.core.get_voice_manager(self.core).contents
        
        return self._voiceManager
        
    def GetAchievementManager(self):
        if not self._achievementManager._internal:
            self._achievementManager._internal = self.core.get_achievement_manager(self.core).contents
        
        return self._achievementManager
        