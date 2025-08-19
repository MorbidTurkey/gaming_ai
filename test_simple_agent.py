"""
Test script for the new simple agent workflow
"""

from utils.simple_gaming_agent import SimpleGamingAgent
from utils.metric_registry import MetricRegistry
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

print("🧪 Testing simple agent workflow...")

# Initialize simple agent
apis = APIs()
simple_agent = SimpleGamingAgent(apis)

# Test queries
test_queries = [
    "What are the most popular games on Twitch?",
    "What other games do players of Total War Attila play?",
    "What are similar games to Counter-Strike?",
    "Show me the top Steam games",
    "Unknown query that won't match"
]

for query in test_queries:
    print(f"\n🎯 TESTING QUERY: {query}")
    response_text, visualization = simple_agent.respond(query)
    print(f"📝 Response: {response_text[:100]}...")
    print(f"📊 Visualization: {'✅ Success' if visualization and visualization.get('success') else '❌ None'}")
    print("-" * 80)
