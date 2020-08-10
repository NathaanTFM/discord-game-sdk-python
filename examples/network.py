# You need two discord instances running
# This is probably more a test than an example

# Discord is in the parent folder
import sys 
sys.path.insert(0, "..")

from discord import Discord
from discord.enum import CreateFlags, Result, ActivityJoinRequestReply
from discord.model import Activity
import discord.exception

import time, uuid, os

class Game:
    # We will set it dynamically
    ApplicationId = None
    
    def __init__(self, instanceId):
        self.instanceId = instanceId
        os.environ["DISCORD_INSTANCE_ID"] = str(self.instanceId)
        
        self.discord = Discord(Game.ApplicationId, CreateFlags.Default)
        
        self.networkManager = self.discord.GetNetworkManager()
        self.networkManager.OnRouteUpdate = self.onRouteUpdate
        self.networkManager.OnMessage = self.onMessage
        
        self.peerId = self.networkManager.GetPeerId()
        self.route = None
        self.connected = False
        
    def onRouteUpdate(self, route):
        self.route = route
        print(f"[Discord {self.instanceId}] Route: {self.route}")
        
        self.onRoute()
        
    def onMessage(self, peerId, channelId, data):
        print(f"[Discord {self.instanceId}] Received from {peerId} on channel {channelId}: {repr(data)}")
        
# We get the Application Id
with open("application_id.txt", "r") as file:
    Game.ApplicationId = int(file.read())
    
game0 = Game(0)
game1 = Game(1)

def onGame0Route():
    if not game1.connected:
        print(f"[Discord {game1.instanceId}] Connecting to other peer {game0.peerId} on route {game0.route}")
        game1.networkManager.OpenPeer(game0.peerId, game0.route)
        game1.networkManager.OpenChannel(game0.peerId, 0, True) # reliable channel
        game1.networkManager.OpenChannel(game0.peerId, 1, False) # unreliable channel
        game1.connected = True
    else:
        game1.networkManager.UpdatePeer(game1.peerId, game1.route)
    
def onGame1Route():
    if not game0.connected:
        print(f"[Discord {game0.instanceId}] Connecting to other peer {game1.peerId} on route {game1.route}")
        game0.networkManager.OpenPeer(game1.peerId, game1.route)
        game0.networkManager.OpenChannel(game1.peerId, 0, True) # reliable channel
        game0.networkManager.OpenChannel(game1.peerId, 1, False) # unreliable channel
        game0.connected = True
            
    else:
        game0.networkManager.UpdatePeer(game0.peerId, game0.route)

game0.onRoute = onGame0Route
game1.onRoute = onGame1Route

count = 0
nextPacket = 0

while 1:
    time.sleep(1/30)
    game0.discord.RunCallbacks()
    game1.discord.RunCallbacks()
    
    game0.networkManager.Flush()
    game1.networkManager.Flush()
    
    if game0.connected and game1.connected and time.time() > nextPacket:
        if count == 30:
            print(f"[Discord {game1.instanceId}] Closing connection to peer {game0.peerId}")
            game1.networkManager.ClosePeer(game0.peerId)
            
        # We stop after 40 (*2) sent packets.
        if count == 40:
            break
        
        else:
            game0.networkManager.SendMessage(game1.peerId, 0, ("reliable " + str(count)).encode("ascii"))
            print(f"[Discord {game0.instanceId}] Sent a packet to {game1.peerId} on channel 0")
            game0.networkManager.SendMessage(game1.peerId, 1, ("not reliable " + str(count)).encode("ascii"))
            print(f"[Discord {game0.instanceId}] Sent a packet to {game1.peerId} on channel 1")
            count += 1
        
            nextPacket = time.time() + 0.5
            