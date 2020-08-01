from ctypes import *
import os.path

dll = CDLL(os.path.abspath("discord_game_sdk.dll"))
DiscordCreate = dll.DiscordCreate 
    
DiscordClientId = c_int64
DiscordVersion = c_int32
DiscordSnowflake = c_int64
DiscordTimestamp = c_int64
DiscordUserId = DiscordSnowflake
DiscordLocale = c_char * 128
DiscordBranch = c_char * 4096
DiscordLobbyId = DiscordSnowflake
DiscordLobbySecret = c_char * 128
DiscordMetadataKey = c_char * 256
DiscordMetadataValue = c_char * 4096
DiscordNetworkPeerId = c_uint64
DiscordNetworkChannelId = c_uint8
DiscordPath = c_char * 4096
DiscordDateTime = c_char * 64

class DiscordUser(Structure):
    _fields_ = [
        ("id", DiscordUserId),
        ("username", c_char * 256),
        ("discriminator", c_char * 8),
        ("avatar", c_char * 128),
        ("bot", c_bool)
    ]
    
class DiscordOAuth2Token(Structure):
    _fields_ = [
        ("access_token", c_char * 128),
        ("scopes", c_char * 1024),
        ("expires", DiscordTimestamp)
    ]
    
class DiscordImageHandle(Structure):
    _fields_ = [
        ("type", c_int32),
        ("id", c_int64),
        ("size", c_uint32)
    ]
    
class DiscordImageDimensions(Structure):
    _fields_ = [
        ("width", c_uint32),
        ("height", c_uint32),
    ]
    
class DiscordActivityTimestamps(Structure):
    _fields_ = [
        ("start", DiscordTimestamp),
        ("end", DiscordTimestamp)
    ]
    
class DiscordActivityAssets(Structure):
    _fields_ = [
        ("large_image", c_char * 128),
        ("large_text", c_char * 128),
        ("small_image", c_char * 128),
        ("small_text", c_char * 128)
    ]
    
class DiscordPartySize(Structure):
    _fields_ = [
        ("current_size", c_int32),
        ("max_size", c_int32)
    ]
    
class DiscordActivityParty(Structure):
    _fields_ = [
        ("id", c_char * 128),
        ("size", DiscordPartySize)
    ]
    
class DiscordActivitySecrets(Structure):
    _fields_ = [
        ("char", c_char * 128),
        ("join", c_char * 128),
        ("spectate", c_char * 128)
    ]
    
class DiscordActivity(Structure):
    _fields_ = [
        ("type", c_int32),
        ("application_id", c_uint64),
        ("name", c_char * 128),
        ("state", c_char * 128),
        ("details", c_char * 128),
        ("timestamps", DiscordActivityTimestamps),
        ("assets", DiscordActivityAssets),
        ("party", DiscordActivityParty),
        ("secrets", DiscordActivitySecrets),
        ("instance", c_bool)
    ]
    
class DiscordPresence(Structure):
    _fields_ = [
        ("status", c_int32),
        ("activity", DiscordActivity)
    ]
    
class DiscordRelationship(Structure):
    _fields_ = [
        ("type", c_int32),
        ("user", DiscordUser),
        ("presence", DiscordPresence)
    ]
    
class DiscordLobby(Structure):
    _fields_ = [
        ("id", DiscordLobbyId),
        ("type", c_int32),
        ("owner_id", DiscordUserId),
        ("secret", DiscordLobbySecret),
        ("capacity", c_uint32),
        ("locked", c_bool)
    ]
    
"""class DiscordImeUnderline(Structure):
    _fields_ = [
        ("from", c_int32),
        ("to", c_int32),
        ("color", c_int32),
        ("background_color", c_uint32),
        ("thick", c_bool)
    ]
    
class DiscordRect(Structure):
    _fields_ = [
        ("left", c_int32),
        ("top", c_int32),
        ("right", c_int32),
        ("bottom", c_int32)
    ]"""
    
class DiscordFileStat(Structure):
    _fields_ = [
        ("filename", c_char * 260),
        ("size", c_uint64),
        ("last_modified", c_uint64)
    ]
    
class DiscordEntitlement(Structure):
    _fields_ = [
        ("id", DiscordSnowflake),
        ("type", c_int32),
        ("sku_id", DiscordSnowflake)
    ]
    
class DiscordSkuPrice(Structure):
    _fields_ = [
        ("amount", c_uint32),
        ("currency", c_char * 16)
    ]
    
class DiscordSku(Structure):
    _fields_ = [
        ("id", DiscordSnowflake),
        ("type", c_int32),
        ("name", c_char * 256),
        ("price", DiscordSkuPrice)
    ]

class DiscordInputMode(Structure):
    _fields_ = [
        ("type", c_int32),
        ("shortcut", c_char * 256)
    ]
    
class DiscordUserAchievement(Structure):
    _fields_ = [
        ("user_id", DiscordSnowflake),
        ("achievement_id", DiscordSnowflake),
        ("percent_complete", c_uint8),
        ("unlocked_at", DiscordDateTime)
    ]

class IDiscordLobbyTransaction(Structure):
    pass
    
IDiscordLobbyTransaction._fields_ = [
    ("set_type", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyTransaction), c_int32)),
    ("set_owner", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyTransaction), DiscordUserId)),
    ("set_capacity", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyTransaction), c_uint32)),
    ("set_metadata", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyTransaction), DiscordMetadataKey, DiscordMetadataValue)),
    ("delete_metadata", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyTransaction), DiscordMetadataKey)),
    ("set_locked", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyTransaction), c_bool)),
]

class IDiscordLobbyMemberTransaction(Structure):
    pass
    
IDiscordLobbyMemberTransaction._fields_ = [
    ("set_metadata", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyMemberTransaction), DiscordMetadataKey, DiscordMetadataValue)),
    ("delete_metadata", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyMemberTransaction), DiscordMetadataKey))
]

class IDiscordLobbySearchQuery(Structure):
    pass
    
IDiscordLobbySearchQuery._fields_ = [
    ("filter", CFUNCTYPE(c_int32, POINTER(IDiscordLobbySearchQuery), DiscordMetadataKey, c_int32, c_int32, DiscordMetadataValue)),
    ("sort", CFUNCTYPE(c_int32, POINTER(IDiscordLobbySearchQuery), DiscordMetadataKey, c_int32, DiscordMetadataValue)),
    ("limit", CFUNCTYPE(c_int32, POINTER(IDiscordLobbySearchQuery), c_uint32)),
    ("distance", CFUNCTYPE(c_int32, POINTER(IDiscordLobbySearchQuery), c_int32))
]

IDiscordApplicationEvents = c_void_p
    
class IDiscordApplicationManager(Structure):
    pass
    
IDiscordApplicationManager._fields_ = [
    ("validate_or_exit", CFUNCTYPE(None, POINTER(IDiscordApplicationManager), c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("get_current_locale", CFUNCTYPE(None, POINTER(IDiscordApplicationManager), POINTER(DiscordLocale))),
    ("get_current_branch", CFUNCTYPE(None, POINTER(IDiscordApplicationManager), POINTER(DiscordBranch))),
    ("get_oauth2_token", CFUNCTYPE(None, POINTER(IDiscordApplicationManager), c_void_p, CFUNCTYPE(None, c_void_p, c_int32, POINTER(DiscordOAuth2Token)))),
    ("get_ticket", CFUNCTYPE(None, POINTER(IDiscordApplicationManager), c_void_p, CFUNCTYPE(None, c_void_p, c_int32, c_char_p))),
]

class IDiscordUserEvents(Structure):
    _fields_ = [
        ("on_current_user_update", CFUNCTYPE(None, c_void_p))
    ]

class IDiscordUserManager(Structure):
    pass
    
IDiscordUserManager._fields_ = [
    ("get_current_user", CFUNCTYPE(c_int32, POINTER(IDiscordUserManager), POINTER(DiscordUser))),
    ("get_user", CFUNCTYPE(None, POINTER(IDiscordUserManager), DiscordUserId, c_void_p, CFUNCTYPE(None, c_void_p, c_int32, POINTER(DiscordUser)))),
    ("get_current_user_premium_type", CFUNCTYPE(c_int32, POINTER(IDiscordUserManager), POINTER(c_int32))),
    ("current_user_has_flag", CFUNCTYPE(c_int32, POINTER(IDiscordUserManager), c_int32, POINTER(c_bool))),
]
    
IDiscordImageEvents = c_void_p

class IDiscordImageManager(Structure):
    pass
    
IDiscordImageManager._fields_ = [
    ("fetch", CFUNCTYPE(None, POINTER(IDiscordImageManager), DiscordImageHandle, c_bool, c_void_p, CFUNCTYPE(None, c_void_p, c_int32, DiscordImageHandle))),
    ("get_dimensions", CFUNCTYPE(c_int32, POINTER(IDiscordImageManager), DiscordImageHandle, POINTER(DiscordImageDimensions))),
    ("get_data", CFUNCTYPE(c_int32, POINTER(IDiscordImageManager), DiscordImageHandle, POINTER(c_uint8), c_uint32)),
]

class IDiscordActivityEvents(Structure):
    _fields_ = [
        ("on_activity_join", CFUNCTYPE(None, c_void_p, c_char_p)),
        ("on_activity_spectate", CFUNCTYPE(None, c_void_p, c_char_p)),
        ("on_activity_join_request", CFUNCTYPE(None, c_void_p, POINTER(DiscordUser))),
        ("on_activity_invite", CFUNCTYPE(None, c_void_p, c_int32, POINTER(DiscordUser), POINTER(DiscordActivity)))
    ]

class IDiscordActivityManager(Structure):
    pass
    
IDiscordActivityManager._fields_ = [
    ("register_command", CFUNCTYPE(c_int32, POINTER(IDiscordActivityManager), c_char_p)),
    ("register_steam", CFUNCTYPE(c_int32, POINTER(IDiscordActivityManager), c_int32)),
    ("update_activity", CFUNCTYPE(None, POINTER(IDiscordActivityManager), POINTER(DiscordActivity), c_void_p, CFUNCTYPE(None, c_void_p, c_uint32))),
    ("clear_activity", CFUNCTYPE(None, POINTER(IDiscordActivityManager), c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("send_request_reply", CFUNCTYPE(None, POINTER(IDiscordActivityManager), DiscordUserId, c_int32, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("send_invite", CFUNCTYPE(None, POINTER(IDiscordActivityManager), DiscordUserId, c_int32, c_char_p, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("accept_invite", CFUNCTYPE(None, POINTER(IDiscordActivityManager), DiscordUserId, c_void_p, CFUNCTYPE(None, c_void_p, c_int32)))
]
class IDiscordRelationshipEvents(Structure):
    _fields_ = [
        ("on_refresh", CFUNCTYPE(None, c_void_p)),
        ("on_relationship_update", CFUNCTYPE(None, c_void_p, POINTER(DiscordRelationship)))
    ]

class IDiscordRelationshipManager(Structure):
    pass
    
IDiscordRelationshipManager._fields_ = [
    ("filter", CFUNCTYPE(None, POINTER(IDiscordRelationshipManager), c_void_p, CFUNCTYPE(c_bool, c_void_p, POINTER(DiscordRelationship)))),
    ("count", CFUNCTYPE(c_int32, POINTER(IDiscordRelationshipManager), POINTER(c_int32))),
    ("get", CFUNCTYPE(c_int32, POINTER(IDiscordRelationshipManager), DiscordUserId, POINTER(DiscordRelationship))),
    ("get_at", CFUNCTYPE(c_int32, POINTER(IDiscordRelationshipManager), c_uint32, POINTER(DiscordRelationship)))
]
    
class IDiscordLobbyEvents(Structure):
    _fields_ = [
        ("on_lobby_update", CFUNCTYPE(None, c_void_p, c_int64)),
        ("on_lobby_delete", CFUNCTYPE(None, c_void_p, c_int64, c_uint32)),
        ("on_member_connect", CFUNCTYPE(None, c_void_p, c_int64, c_int64)),
        ("on_member_update", CFUNCTYPE(None, c_void_p, c_int64, c_int64)),
        ("on_member_disconnect", CFUNCTYPE(None, c_void_p, c_int64, c_int64)),
        ("on_lobby_message", CFUNCTYPE(None, c_void_p, c_int64, c_int64, POINTER(c_uint8), c_uint32)),
        ("on_speaking", CFUNCTYPE(None, c_void_p, c_int64, c_int64, c_bool)),
        ("on_network_message", CFUNCTYPE(None, c_void_p, c_int64, c_int64, c_uint8, POINTER(c_uint8), c_uint32))
    ]
    
class IDiscordLobbyManager(Structure):
    pass
    
IDiscordLobbyManager._fields_ = [
    ("get_lobby_create_transaction", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), POINTER(POINTER(IDiscordLobbyTransaction)))),
    ("get_lobby_update_transaction", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, POINTER(POINTER(IDiscordLobbyTransaction)))),
    ("get_member_update_transaction", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordUserId, POINTER(POINTER(IDiscordLobbyTransaction)))),
    ("create_lobby", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), POINTER(IDiscordLobbyTransaction), c_void_p, CFUNCTYPE(None, c_void_p, c_int32, POINTER(DiscordLobby)))),
    ("update_lobby", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbyId, POINTER(IDiscordLobbyTransaction), c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("delete_lobby", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbyId, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("connect_lobby", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordLobbySecret, c_void_p, CFUNCTYPE(None, c_void_p, c_int32, POINTER(DiscordLobby)))),
    ("connect_lobby_with_activity_secret", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbySecret, c_void_p, CFUNCTYPE(None, c_void_p, c_int32, POINTER(DiscordLobby)))),
    ("disconnect_lobby", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbyId, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("get_lobby", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, POINTER(DiscordLobby))),
    ("get_lobby_activity_secret", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, POINTER(DiscordLobbySecret))),
    ("get_lobby_metadata_value", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordMetadataKey, POINTER(DiscordMetadataValue))),
    ("get_lobby_metadata_key", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, c_int32, POINTER(DiscordMetadataKey))),
    ("lobby_metadata_count", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, POINTER(c_int32))),
    ("member_count", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, POINTER(c_int32))),
    ("get_member_user_id", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, c_int32, POINTER(DiscordUserId))),
    ("get_member_user", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordUserId, POINTER(DiscordUser))),
    ("get_member_metadata_value", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordUserId, DiscordMetadataKey, POINTER(DiscordMetadataValue))),
    ("get_member_metadata_key", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordUserId, c_int32, POINTER(DiscordMetadataKey))),
    ("member_metadata_count", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordUserId, POINTER(c_int32))),
    ("update_member", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordUserId, POINTER(IDiscordLobbyMemberTransaction), c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("send_lobby_message", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbyId, POINTER(c_uint8), c_uint32, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("get_search_query", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), POINTER(POINTER(IDiscordLobbySearchQuery)))),
    ("search", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), POINTER(IDiscordLobbySearchQuery), c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("lobby_count", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), POINTER(c_int32))),
    ("get_lobby_id", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), c_int32, POINTER(DiscordLobbyId))),
    ("connect_voice", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbyId, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("disconnect_voice", CFUNCTYPE(None, POINTER(IDiscordLobbyManager), DiscordLobbyId, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("connect_network", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId)),
    ("disconnect_network", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId)),
    ("flush_network", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager))),
    ("open_network_channel", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, c_uint8, c_bool)),
    ("send_network_message", CFUNCTYPE(c_int32, POINTER(IDiscordLobbyManager), DiscordLobbyId, DiscordUserId, c_uint8, POINTER(c_uint8), c_uint32)),
]

class IDiscordNetworkEvents(Structure):
    _fields_ = [
        ("on_message", CFUNCTYPE(None, c_void_p, DiscordNetworkPeerId, DiscordNetworkChannelId, POINTER(c_uint8), c_uint32)),
        ("on_route_update", CFUNCTYPE(None, c_void_p, c_char_p))
    ]

class IDiscordNetworkManager(Structure):
    pass
    
IDiscordNetworkManager._fields_ = [
    ("get_peer_id", CFUNCTYPE(None, POINTER(IDiscordNetworkManager), POINTER(DiscordNetworkPeerId))),
    ("flush", CFUNCTYPE(c_int32, POINTER(IDiscordNetworkManager))),
    ("open_peer", CFUNCTYPE(c_int32, POINTER(IDiscordNetworkManager), DiscordNetworkPeerId, c_char_p)),
    ("update_peer", CFUNCTYPE(c_int32, POINTER(IDiscordNetworkManager), DiscordNetworkPeerId, c_char_p)),
    ("close_peer", CFUNCTYPE(c_int32, POINTER(IDiscordNetworkManager), DiscordNetworkPeerId)),
    ("open_channel", CFUNCTYPE(c_int32, POINTER(IDiscordNetworkManager), DiscordNetworkPeerId, DiscordNetworkChannelId, c_bool)),
    ("close_channel", CFUNCTYPE(c_int32, POINTER(IDiscordNetworkManager), DiscordNetworkPeerId, DiscordNetworkChannelId)),
    ("send_message", CFUNCTYPE(c_int32, POINTER(IDiscordNetworkManager), DiscordNetworkPeerId, DiscordNetworkChannelId, POINTER(c_uint8), c_uint32))
]

class IDiscordOverlayEvents(Structure):
    _fields_ = [
        ("on_toggle", CFUNCTYPE(None, c_void_p, c_bool))
    ]
    
class IDiscordOverlayManager(Structure):
    pass
    
IDiscordOverlayManager._fields_ = [
    ("is_enabled", CFUNCTYPE(None, POINTER(IDiscordOverlayManager), POINTER(c_bool))),
    ("is_locked", CFUNCTYPE(None, POINTER(IDiscordOverlayManager), POINTER(c_bool))),
    ("set_locked", CFUNCTYPE(None, POINTER(IDiscordOverlayManager), c_bool, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("open_activity_invite", CFUNCTYPE(None, POINTER(IDiscordOverlayManager), c_int32, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("open_guild_invite", CFUNCTYPE(None, POINTER(IDiscordOverlayManager), c_char_p, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("open_voice_settings", CFUNCTYPE(None, POINTER(IDiscordOverlayManager), c_void_p, CFUNCTYPE(None, c_void_p, c_int32)))
]

IDiscordStorageEvents = c_void_p
    
class IDiscordStorageManager(Structure):
    pass
    
IDiscordStorageManager._fields_ = [
    ("read", CFUNCTYPE(c_int32, POINTER(IDiscordStorageManager), c_char_p, POINTER(c_uint8), c_uint32, POINTER(c_uint32))),
    ("read_async", CFUNCTYPE(None, POINTER(IDiscordStorageManager), c_char_p, c_void_p, CFUNCTYPE(None, c_void_p, c_int32, POINTER(c_uint8), c_uint32))),
    ("read_async_partial", CFUNCTYPE(None, POINTER(IDiscordStorageManager), c_char_p, c_uint64, c_uint64, c_void_p, CFUNCTYPE(None, c_void_p, c_int32, POINTER(c_uint8), c_uint32))),
    ("write", CFUNCTYPE(c_int32, POINTER(IDiscordStorageManager), c_char_p, POINTER(c_uint8), c_uint32)),
    ("write_async", CFUNCTYPE(None, POINTER(IDiscordStorageManager), c_char_p, POINTER(c_uint8), c_uint32, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("delete_", CFUNCTYPE(c_int32, POINTER(IDiscordStorageManager), c_char_p)),
    ("exists", CFUNCTYPE(c_int32, POINTER(IDiscordStorageManager), c_char_p, POINTER(c_bool))),
    ("count", CFUNCTYPE(None, POINTER(IDiscordStorageManager), POINTER(c_int32))),
    ("stat", CFUNCTYPE(c_int32, POINTER(IDiscordStorageManager), c_char_p, POINTER(DiscordFileStat))),
    ("stat_at", CFUNCTYPE(c_int32, POINTER(IDiscordStorageManager), c_int32, POINTER(DiscordFileStat))),
    ("get_path", CFUNCTYPE(c_int32, POINTER(IDiscordStorageManager), POINTER(DiscordPath)))
]

class IDiscordStoreEvents(Structure):
    _fields_ = [
        ("on_entitlement_create", CFUNCTYPE(None, c_void_p, POINTER(DiscordEntitlement))),
        ("on_entitlement_delete", CFUNCTYPE(None, c_void_p, POINTER(DiscordEntitlement)))
    ]
    
class IDiscordStoreManager(Structure):
    pass # TODO

class IDiscordVoiceEvents(Structure):
    _fields_ = [
        ("on_settings_update", CFUNCTYPE(None, c_void_p))
    ]
    
class IDiscordVoiceManager(Structure):
    pass
    
IDiscordVoiceManager._fields_ = [
    ("get_input_mode", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), POINTER(DiscordInputMode))),
    ("set_input_mode", CFUNCTYPE(None, POINTER(IDiscordVoiceManager), DiscordInputMode, c_void_p, CFUNCTYPE(None, c_void_p, c_int32))),
    ("is_self_mute", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), POINTER(c_bool))),
    ("set_self_mute", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), c_bool)),
    ("is_self_deaf", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), POINTER(c_bool))),
    ("set_self_deaf", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), c_bool)),
    ("is_local_mute", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), DiscordSnowflake, POINTER(c_bool))),
    ("set_local_mute", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), DiscordSnowflake, c_bool)),
    ("get_local_volume", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), DiscordSnowflake, POINTER(c_uint8))),
    ("set_local_volume", CFUNCTYPE(c_int32, POINTER(IDiscordVoiceManager), DiscordSnowflake, POINTER(c_uint8)))
]
    
class IDiscordAchievementEvents(Structure):
    _fields_ = [
        ("on_user_achievement_update", CFUNCTYPE(None, c_void_p, POINTER(DiscordUserAchievement)))
    ]
    
class IDiscordAchievementManager(Structure):
    pass # TODO

IDiscordCoreEvents = c_void_p
    
class IDiscordCore(Structure):
    pass
    
IDiscordCore._fields_ = [
    ("destroy", CFUNCTYPE(None, POINTER(IDiscordCore))),
    ("run_callbacks", CFUNCTYPE(c_int32, POINTER(IDiscordCore))),
    ("set_log_hook", CFUNCTYPE(None, POINTER(IDiscordCore), c_int32, c_void_p, CFUNCTYPE(None, c_void_p, c_int32, c_char_p))),
    ("get_application_manager", CFUNCTYPE(POINTER(IDiscordApplicationManager), POINTER(IDiscordCore))),
    ("get_user_manager", CFUNCTYPE(POINTER(IDiscordUserManager), POINTER(IDiscordCore))),
    ("get_image_manager", CFUNCTYPE(POINTER(IDiscordImageManager), POINTER(IDiscordCore))),
    ("get_activity_manager", CFUNCTYPE(POINTER(IDiscordActivityManager), POINTER(IDiscordCore))),
    ("get_relationship_manager", CFUNCTYPE(POINTER(IDiscordRelationshipManager), POINTER(IDiscordCore))),
    ("get_lobby_manager", CFUNCTYPE(POINTER(IDiscordLobbyManager), POINTER(IDiscordCore))),
    ("get_network_manager", CFUNCTYPE(POINTER(IDiscordNetworkManager), POINTER(IDiscordCore))),
    ("get_overlay_manager", CFUNCTYPE(POINTER(IDiscordOverlayManager), POINTER(IDiscordCore))),
    ("get_storage_manager", CFUNCTYPE(POINTER(IDiscordStorageManager), POINTER(IDiscordCore))),
    ("get_store_manager", CFUNCTYPE(POINTER(IDiscordStoreManager), POINTER(IDiscordCore))),
    ("get_voice_manager", CFUNCTYPE(POINTER(IDiscordVoiceManager), POINTER(IDiscordCore))),
    ("get_achievement_manager", CFUNCTYPE(POINTER(IDiscordAchievementManager), POINTER(IDiscordCore))),
]
    
class DiscordCreateParams(Structure):
    _fields_ = [
        ("client_id", DiscordClientId),
        ("flags", c_uint64),
        ("events", POINTER(IDiscordCoreEvents)),
        ("event_data", c_void_p),
        ("application_events", POINTER(IDiscordApplicationEvents)),
        ("application_version", DiscordVersion),
        ("user_events", POINTER(IDiscordUserEvents)),
        ("user_version", DiscordVersion),
        ("image_events", POINTER(IDiscordImageEvents)),
        ("image_version", DiscordVersion),
        ("activity_events", POINTER(IDiscordActivityEvents)),
        ("activity_version", DiscordVersion),
        ("relationship_events", POINTER(IDiscordRelationshipEvents)),
        ("relationship_version", DiscordVersion),
        ("lobby_events", POINTER(IDiscordLobbyEvents)),
        ("lobby_version", DiscordVersion),
        ("network_events", POINTER(IDiscordNetworkEvents)),
        ("network_version", DiscordVersion),
        ("overlay_events", POINTER(IDiscordOverlayEvents)),
        ("overlay_version", DiscordVersion),
        ("storage_events", POINTER(IDiscordStorageEvents)),
        ("storage_version", DiscordVersion),
        ("store_events", POINTER(IDiscordStoreEvents)),
        ("store_version", DiscordVersion),
        ("voice_events", POINTER(IDiscordVoiceEvents)),
        ("voice_version", DiscordVersion),
        ("achievement_events", POINTER(IDiscordAchievementEvents)),
        ("achievement_version", DiscordVersion)
    ]

def DiscordCreateParamsSetDefault(params):
    params.application_version = 1
    params.user_version = 1
    params.image_version = 1
    params.activity_version = 1
    params.relationship_version = 1
    params.lobby_version = 1
    params.network_version = 1
    params.overlay_version = 1
    params.storage_version = 1
    params.store_version = 1
    params.voice_version = 1
    params.achievement_version = 1
