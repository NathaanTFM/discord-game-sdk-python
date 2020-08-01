from . import sdk
import ctypes

class Model:
    def __init__(self, **kwargs):
        self._internal = kwargs.get("internal", self._struct_())
        if "copy" in kwargs:
            ctypes.memmove(ctypes.byref(self._internal), ctypes.byref(kwargs["copy"]), ctypes.sizeof(self._struct_))
            
        self._fields = {}
        
        for name, field, ftype in self._fields_:
            self._fields[name] = (field, ftype)
            if issubclass(ftype, Model):
                setattr(self, "_" + field, ftype(internal = getattr(self._internal, field)))
                
    def __getattribute__(self, key):
        if key.startswith("_"):
            return super().__getattribute__(key)
        else:
            field = self._fields[key]
            value = getattr(self._internal, field[0])
            if field[1] == int:
                return int(value)
            elif field[1] == str:
                return value.decode("utf8")
            elif field[1] == bool:
                return bool(value)
            elif issubclass(field[1], Model):
                return getattr(self, "_" + field[0])
            else:
                raise TypeError(field[1])
                    
    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            field = self._fields[key]
            if field[1] == int:
                value = int(value)
                setattr(self._internal, field[0], value)
            elif field[1] == str:
                value = value.encode("utf8")
                setattr(self._internal, field[0], value)
            elif field[1] == bool:
                value = bool(value)
                setattr(self._internal, field[0], value)
            elif issubclass(field[1], Model):
                setattr(self, "_" + field[0], value)
                setattr(self._internal, field[0], value._internal)
            else:
                raise TypeError(field[1])
            
class User(Model):
    _struct_ = sdk.DiscordUser
    _fields_ = [
        ("Id", "id", int),
        ("Username", "username", str),
        ("Discriminator", "discriminator", str),
        ("Avatar", "avatar", str),
        ("Bot", "bot", bool)
    ]

class ActivityTimestamps(Model):
    _struct_ = sdk.DiscordActivityTimestamps
    _fields_ = [
        ("Start", "start", int),
        ("End", "end", int)
    ]
    
class ActivityAssets(Model):
    _struct_ = sdk.DiscordActivityAssets
    _fields_ = [
        ("LargeImage", "large_image", str),
        ("LargeText", "large_text", str),
        ("SmallImage", "small_image", str),
        ("SmallText", "small_text", str)
    ]
    
class PartySize(Model):
    _struct_ = sdk.DiscordPartySize
    _fields_ = [
        ("CurrentSize", "current_size", int),
        ("MaxSize", "max_size", int)
    ]
    
class ActivityParty(Model):
    _struct_ = sdk.DiscordActivityParty
    _fields_ = [
        ("Id", "id", str),
        ("Size", "size", PartySize)
    ]
        
class ActivitySecrets(Model):
    _struct_ = sdk.DiscordActivitySecrets
    _fields_ = [
        ("Match", "match", str),
        ("Join", "join", str),
        ("Spectate", "spectate", str)
    ]
    
class Activity(Model):
    _struct_ = sdk.DiscordActivity
    _fields_ = [
        ("ApplicationId", "application_id", int),
        ("Name", "name", str),
        ("State", "state", str),
        ("Details", "details", str),
        ("Timestamps", "timestamps", ActivityTimestamps),
        ("Assets", "assets", ActivityAssets),
        ("Party", "party", ActivityParty),
        ("Secrets", "secrets", ActivitySecrets),
        ("Instance", "instance", bool)
    ]
    
class Presence(Model):
    _struct_ = sdk.DiscordPresence 
    _fields_ = [
        ("Status", "status", int),
        ("Activity", "activity", Activity)
    ]
    
class Relationship(Model):
    _struct_ = sdk.DiscordRelationship
    _fields_ = [
        ("Type", "type", int),
        ("User", "user", User),
        ("Presence", "presence", Presence)
    ]
    

class ImageDimensions(Model):
    _struct_ = sdk.DiscordImageDimensions
    _fields_ = [
        ("Width", "width", int),
        ("Height", "height", int)
    ]
    
class ImageHandle(Model):
    _struct_ = sdk.DiscordImageHandle
    _fields_ = [
        ("Type", "type", int),
        ("Id", "id", int),
        ("Size", "size", int)
    ]
    
class OAuth2Token(Model):
    _struct_ = sdk.DiscordOAuth2Token
    _fields_ = [
        ("AccessToken", "access_token", str),
        ("Scopes", "scopes", str),
        ("Expires", "expires", int)
    ]
    
class Lobby(Model):
    _struct_ = sdk.DiscordLobby
    _fields_ = [
        ("Id", "id", int),
        ("Type", "type", int),
        ("OwnerId", "owner_id", int),
        ("Secret", "secret", str),
        ("Capacity", "capacity", int),
        ("Locked", "locked", bool)
    ]