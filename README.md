# Discord Game SDK for Python

This is **not** a module. This was made for **Python >= 3.5** and **Discord Game SDK 2.5.6**

This is a **Work In Progress:** it might not work as expected or not work at all. This was made for testing purposes.

## Installation

- Download:
  - [Discord Game SDK (2.5.6)](https://dl-game-sdk.discordapp.net/2.5.6/discord_game_sdk.zip)
  - [Discord Game SDK for Python](https://github.com/NathaanTFM/discord-game-sdk-python/archive/master.zip)

- Grab the DLL from `discord_game_sdk.zip` in the `lib` directory and put it in your project directory
- Grab the `discord` directory from `master.zip` and put it in your project directory

## Documentation

If you need documentation, look at [**the official Game SDK docs**](https://discord.com/developers/docs/game-sdk/sdk-starter-guide) ; this was made following the official documentation.

## Features

* Should be working:
  * **ActivityManager**
  * **RelationshipManager**
  * **ImageManager**
  * **UserManager** 

* Should be working, but need more testing:
  * **ApplicationManager** (especially the functions `GetTicket` and `ValidateOrExit`)
  * **VoiceManager** (not tested at all)
  * **LobbyManager**
  * **NetworkManager**

* Not implemented, or not working:
  * **AchievementManager**
  * **OverlayManager**
  * **StorageManager**
  * **StoreManager**

## Contributing

The code needs **more comments, type hinting**. You can also implement the **missing features**, or add **more tests**. Feel free to open a **pull request**!

You can also **report issues**. Just open an issue and I will ll look into it!

## Examples

You can find more examples in the `examples/` directory.

Create a Discord instance

```python
from discord import Discord
from discord.enum import CreateFlags
import time

app = Discord(APPLICATION_ID, CreateFlags.Default)

# Don't forget to call RunCallbacks
while 1:
    time.sleep(1/10)
    app.RunCallbacks()
```

Get current user

```python
from discord import Discord
from discord.enum import CreateFlags
import time

app = Discord(APPLICATION_ID, CreateFlags.Default)

userManager = app.GetUserManager()
def onCurrUserUpdate():
    user = userManager.GetCurrentUser()
    print(f"Current user : {user.Username}#{user.Discriminator}")
    
userManager.OnCurrentUserUpdate = onCurrUserUpdate

# Don't forget to call RunCallbacks
while 1:
    time.sleep(1/10)
    app.RunCallbacks()
```

Set activity

```python
from discord import Discord
from discord.model import Activity
from discord.enum import Result, CreateFlags
import time

app = Discord(APPLICATION_ID, CreateFlags.Default)

activityManager = app.GetActivityManager()

activity = Activity()
activity.State = "Testing Game SDK"
activity.Party.Id = "my_super_party_id"
activity.Party.Size.CurrentSize = 4
activity.Party.Size.MaxSize = 8
activity.Secrets.Join = "my_super_secret"

def callback(result):
    if result == Result.Ok:
        print("Successfully set the activity!")
    else:
        raise Exception(result)
        
activityManager.UpdateActivity(activity, callback)

# Don't forget to call RunCallbacks
while 1:
    time.sleep(1/10)
    app.RunCallbacks()
```