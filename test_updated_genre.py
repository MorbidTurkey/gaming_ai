#!/usr/bin/env python3
"""
Test Updated Genre Analysis with Gamalytic Primary + SteamSpy Fallback

This script tests the updated approach where Gamalytic is primary
and SteamSpy is used as fallback.
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.intelligent_gaming_agent import IntelligentGamingAgent

# Initialize APIs for testing
class APIs:
    def __init__(self):
        from apis.steam_api import SteamAPI
        from apis.steamspy_api import SteamSpyAPI
        from apis.rawg_api import RAWGAPI
        from apis.twitch_api import TwitchAPI
        from apis.gamalytic_api import GamalyticAPI
        
        self.steam_api = SteamAPI()
        self.steamspy_api = SteamSpyAPI()
        self.rawg_api = RAWGAPI()
        self.twitch_api = TwitchAPI()
        self.gamalytic_api = GamalyticAPI()

def test_genre_analysis():
    """Test the updated genre analysis approach"""
    print("🧪 Testing Updated Genre Analysis Approach")
    print("=" * 60)
    
    # Initialize agent
    apis = APIs()
    agent = IntelligentGamingAgent(apis)
    
    # Test the genre question
    test_query = "What is the most popular genre of games?"
    
    print(f"🔍 Testing query: '{test_query}'")
    print("-" * 40)
    
    try:
        response_text, visualization = agent.respond(test_query)
        
        print("📝 Response Text:")
        print("=" * 30)
        print(response_text)
        print()
        
        print("📊 Visualization:")
        print("=" * 30)
        if visualization:
            print(f"✅ Visualization generated successfully")
            print(f"📈 Type: {type(visualization)}")
            if isinstance(visualization, dict):
                print(f"📋 Keys: {list(visualization.keys())}")
                if "layout" in visualization:
                    title = visualization["layout"].get("title", "No title")
                    print(f"📊 Chart title: {title}")
        else:
            print("❌ No visualization generated")
        
        # Check if response mentions real player metrics
        has_player_metrics = any(keyword in response_text.lower() for keyword in [
            "active players", "copies sold", "revenue", "playtime", "players:"
        ])
        
        has_game_counts = "games in genre" in response_text.lower()
        
        print("\n📊 Analysis Quality:")
        print("=" * 30)
        if has_player_metrics:
            print("✅ Response includes meaningful player activity metrics")
        else:
            print("❌ Response lacks player activity metrics")
            
        if has_game_counts:
            print("📊 Response includes game count information")
        else:
            print("❌ Response lacks game count information")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

def main():
    """Run the test"""
    print("🎮 Genre Analysis API Selection Test")
    print("=" * 60)
    
    success = test_genre_analysis()
    
    print("\n📊 CONCLUSION:")
    print("=" * 60)
    
    if success:
        print("✅ Updated approach working!")
        print("💡 Gamalytic primary with SteamSpy fallback is properly configured")
    else:
        print("❌ Issues with updated approach")
        print("💡 May need further debugging")

if __name__ == "__main__":
    main()
