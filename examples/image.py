# discord is in the parent folder
import sys 
sys.path.insert(0, "..")

# we can now import it
from discord import Discord
from discord.enum import CreateFlags, Result, ImageType
from discord.model import ImageHandle
from PIL import Image
import time, uuid

# we get the application id from a file
with open("application_id.txt", "r") as file:
    applicationId = int(file.read())

# we create the discord instance
app = Discord(applicationId,  CreateFlags.Default)
userManager = app.GetUserManager()
imageManager = app.GetImageManager()

# callbacks
def onImageLoaded(result, handle):
    if result != Result.Ok:
        print("failed to fetch the image (result " + str(result) + ")")
    else:
        print("fetched the image!")
        print("handle:", handle.Type, handle.Id, handle.Size)
        
        dimensions = imageManager.GetDimensions(handle)
        print("dimensions:", dimensions.Width, dimensions.Height)
        
        # we load the image
        data = imageManager.GetData(handle)
        im = Image.frombytes("RGBA", (dimensions.Width, dimensions.Height), data)
        im.show()
        
# events
def onCurrentUserUpdate():
    user = userManager.GetCurrentUser()
    print(f"hello, {user.Username}#{user.Discriminator}!")
    
    # we create an handle
    handle = ImageHandle()
    handle.Type = ImageType.User
    handle.Id = user.Id
    handle.Size = 256
    
    # we fetch the image
    imageManager.Fetch(handle, True, onImageLoaded)
    
# bind events
userManager.OnCurrentUserUpdate = onCurrentUserUpdate

while 1:
    time.sleep(1/10)
    app.RunCallbacks()
    