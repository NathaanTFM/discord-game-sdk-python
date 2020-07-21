# discord is in the parent folder
import sys 
sys.path.insert(0, "..")

# we can now import it
from discord import Discord
from discord.enum import CreateFlags, Result, ActivityJoinRequestReply
from discord.model import Activity
import time, uuid

# we get the application id from a file
with open("application_id.txt", "r") as file:
    applicationId = int(file.read())

# debug callback
def debugCallback(debug, result, *args):
    if result == Result.Ok:
        print(debug, "success")
    else:
        print(debug, "failure", result, args)
        
# we create the discord instance
app = Discord(applicationId,  CreateFlags.Default)
activityManager = app.GetActivityManager()

# events
def onActivityJoin(secret):
    print("[onActivityJoin]")
    print("Secret", secret)
    
def onActivitySpectate(secret):
    print("[onActivitySpectate]")
    print("Secret", secret)
    
def onActivityJoinRequest(user):
    print("[onActivityJoinRequest]")
    print("User", user.Username)
    
    activityManager.SendRequestReply(user.Id, ActivityJoinRequestReply.Yes, lambda result: debugCallback("SendRequestReply", result)) 
    
def onActivityInvite(type, user, activity):
    print("[onActivityInvite]")
    print("Type", type)
    print("User", user.Username)
    print("Activity", activity.State)
    
    activityManager.AcceptInvite(user.Id, lambda result: debugCallback("AcceptInvite", result))
    
# bind events
activityManager.OnActivityJoin = onActivityJoin
activityManager.OnActivitySpectate = onActivitySpectate
activityManager.OnActivityJoinRequest = onActivityJoinRequest
activityManager.OnActivityInvite = onActivityInvite

# we create an activity
activity = Activity()
activity.State = "Testing Game SDK"
activity.Party.Id = str(uuid.uuid4())
activity.Party.Size.CurrentSize = 4
activity.Party.Size.MaxSize = 8
activity.Secrets.Join = str(uuid.uuid4())

# we update the activity
activityManager.UpdateActivity(activity, lambda result: debugCallback("UpdateActivity", result))

# we set the command
activityManager.RegisterCommand("iexplore.exe http://www.example.com/")

timer = 0

while 1:
    time.sleep(1/10)
    app.RunCallbacks()
    
    timer += 1
    if timer == 600: # clear activity after 60 seconds
        activityManager.ClearActivity(lambda result: debugCallback("ClearActivity", result))