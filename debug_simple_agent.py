#!/usr/bin/env python3
"""
Debug script to test the simple gaming agent
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from utils.simple_gaming_agent import SimpleGamingAgent
from apis.steam_api import SteamAPI
from apis.steamspy_api import SteamSpyAPI  
from apis.rawg_api import RAWGAPI
from apis.twitch_api import TwitchAPI
from apis.gamalytic_api import GamalyticAPI

# Initialize APIs for simple agent
class APIs:
    def __init__(self):
        self.steam_api = SteamAPI()
        self.steamspy_api = SteamSpyAPI()
        self.rawg_api = RAWGAPI()
        self.twitch_api = TwitchAPI()
        self.gamalytic_api = GamalyticAPI()

print("🔧 Initializing APIs...")
print(f"🔑 Gamalytic API Key: {'✅ Found' if os.getenv('GAMALYTIC_API_KEY') else '❌ Missing'}")
apis = APIs()
print("🤖 Initializing Simple Gaming Agent...")
simple_agent = SimpleGamingAgent(apis)

print("🎯 Testing: What other games do Elden Ring players also play?")
try:
    response, viz = simple_agent.respond('What other games do Elden Ring players also play?')
    print(f'✅ Response: {response}')
    print(f'📊 Visualization: {viz}')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    print(f'📍 Traceback: {traceback.format_exc()}')
