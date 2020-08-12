class Result:
    Ok = 0
    ServiceUnavailable = 1
    InvalidVersion = 2
    LockFailed = 3
    InternalError = 4
    InvalidPayload = 5
    InvalidCommand = 6
    InvalidPermissions = 7
    NotFetched = 8
    NotFound = 9
    Conflict = 10
    InvalidSecret = 11
    InvalidJoinSecret = 12
    NoEligibleActivity = 13
    InvalidInvite = 14
    NotAuthenticated = 15
    InvalidAccessToken = 16
    ApplicationMismatch = 17
    InvalidDataUrl = 18
    InvalidBase64 = 19
    NotFiltered = 20
    LobbyFull = 21
    InvalidLobbySecret = 22
    InvalidFilename = 23
    InvalidFileSize = 24
    InvalidEntitlement = 25
    NotInstalled = 26
    NotRunning = 27
    InsufficientBuffer = 28
    PurchaseCanceled = 29
    InvalidGuild = 30
    InvalidEvent = 31
    InvalidChannel = 32
    InvalidOrigin = 33
    RateLimited = 34
    OAuth2Error = 35
    SelectChannelTimeout = 36
    GetGuildTimeout = 37
    SelectVoiceForceRequired = 38
    CaptureShortcutAlreadyListening = 39
    UnauthorizedForAchievement = 40
    InvalidGiftCode = 41
    PurchaseError = 42
    TransactionAborted = 43
    #DrawingInitFailed = 44
    
class LogLevel:
    Error = 0
    Warning = 1
    Info = 2
    Debug = 3
    
class CreateFlags:
    Default = 0
    NoRequireDiscord = 1

class UserFlag:
    Partner = 2
    HypeSquadEvents = 4
    HypeSquadHouse1 = 64
    HypeSquadHouse2 = 128
    HypeSquadHouse3 = 256
    
class PremiumType:
    None_ = 0
    Tier1 = 1
    Tier2 = 2
    
class ActivityType:
    Playing = 0
    Streaming = 1
    Listening = 2
    Custom = 4
    
class ActivityJoinRequestReply:
    No = 0
    Yes = 1
    Ignore = 2
    
class ActivityActionType:
    Join = 1
    Spectate = 2
    
class RelationshipType:
    None_ = 0
    Friend = 1
    Blocked = 2
    PendingIncoming = 3
    PendingOutgoing = 4
    Implicit = 5
    
class Status:
    Offline = 0
    Online = 1
    Idle = 2
    DoNotDisturb = 3
    
class ImageType:
    User = 0
    
class LobbyType:
    Private = 1
    Public = 2
    
class LobbySearchComparison:
    LessThanOrEqual = -2
    LessThan = -1
    Equal = 0
    GreaterThan = 1
    GreaterThanOrEqual = 2
    NotEqual = 3
    
class LobbySearchCast:
    String = 1
    Number = 2
    
class LobbySearchDistance:
    Local = 0
    Default = 1
    Extended = 2
    Global = 3
    
class InputModeType:
    VoiceActivity = 0
    PushToTalk = 1
    
class SkuType:
    Application = 1
    DLC = 2
    Consumable = 3
    Bundle = 4
    
class EntitlementType:
    Purchase = 1
    PremiumSubscription = 2
    DeveloperGift = 3
    TestModePurchase = 4
    FreePurchase = 5
    UserGift = 6
    PremiumPurchase = 7