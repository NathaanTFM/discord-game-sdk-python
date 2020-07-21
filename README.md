# WARNING: THIS IS A WORK-IN-PROGRESS

Please do not use it, except for testing purposes.

---

# Discord Game SDK for Python

This is **not** a module. This was made for **Python >= 3.7**

## Usage

Download it, unpack it, import it. Don't forget to add `discord_game_sdk.dll`. I don't know if I can redistribute it in that repo, and I don't know if it's backwards compatible, so here's the SHA1 hash: `a62307af643881ca7de75d3d49b09fc776eac42e`

## Examples

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

## To do

* **This code is a mess:** it need comments, type hinting, some cleaning
* **discord/sdk.py** isn't complete yet *(look for TODOs)*
* **ActivityManager:** should be working
* **RelationshipManager:** should be working
* **ImageManager:** should be working
* **UserManager:** should be working
* **ApplicationManager:** should be working but further testing would be appreciated (especially for the functions GetTicket and ValidateOrExit)
* **LobbyManager:** some functions are missing and some aren't tested
* **NetworkManager:** (almost) everything is missing
* **AchievementManager:** everything is missing
* **OverlayManager:** everything is missing
* **StorageManager:** everything is missing
* **StoreManager:** everything is missing
* **VoiceManager:** everything is missing