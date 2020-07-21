# discord is in the parent folder
import sys 
sys.path.insert(0, "..")

# we can now import it
from discord import Discord
from discord.enum import CreateFlags, Result, Status, RelationshipType
from discord.model import Activity
import time, random

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
relationshipManager = app.GetRelationshipManager()

# events
def onRefresh():
    print("[onRefresh]")
    
    # we filter friends
    relationshipManager.Filter(lambda relationship: relationship.Type == RelationshipType.Friend)

    # we get how many friends we have!!
    friendCount = relationshipManager.Count()
    friends = []
    print("you have " + str(friendCount) + " friends!")
    
    for n in range(friendCount):
        # we get the friend at index n
        friend = relationshipManager.GetAt(n)
        
        # we add it to the list
        friends.append(friend)
        
        # we show it
        print(f"{friend.User.Username}#{friend.User.Discriminator}")
        
    if len(friends):
        print()
        
        # we get the friend with a random friend, by his ID
        randomFriend = random.choice(friends)
        print("fetching " + str(randomFriend.User.Id))
        
        friend = relationshipManager.Get(randomFriend.User.Id)
        print("we found %s" % friend.User.Username)
    
    # let's get implicit relationships
    relationshipManager.Filter(lambda relationship: relationship.Type == RelationshipType.Implicit)
    
    print()
    print("implicit relationships:")
    for n in range(relationshipManager.Count()):
        relationship = relationshipManager.GetAt(n)
        print(f"  {relationship.User.Username}#{relationship.User.Discriminator}")
    
def onRelationshipUpdate(relationship):
    print("[onRelationshipUpdate]")
    print("relationship", relationship.User.Username)
    
# bind events
relationshipManager.OnRefresh = onRefresh
relationshipManager.OnRelationshipUpdate = onRelationshipUpdate

while 1:
    time.sleep(1/10)
    app.RunCallbacks()
    