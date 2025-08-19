#!/usr/bin/env python3
"""
Debug script to test SteamSpy API and understand why player counts are 0
"""

from apis.steamspy_api import SteamSpyAPI
import json

def test_steamspy_data():
    """Test SteamSpy API to see what data we're getting"""
    
    print("🔍 Testing SteamSpy API...")
    api = SteamSpyAPI()
    
    print("\n1. Testing Action genre...")
    games = api.get_genre_data('Action')
    
    if games:
        print(f"✅ Found {len(games)} Action games")
        print("\n📊 Sample game data:")
        for i, game in enumerate(games[:5]):
            print(f"\n  Game {i+1}: {game.get('name', 'Unknown')}")
            print(f"    App ID: {game.get('appid', 'N/A')}")
            print(f"    Players 2 weeks: {game.get('players_2weeks', 'N/A')}")
            print(f"    CCU: {game.get('ccu', 'N/A')}")
            print(f"    Owners: {game.get('owners', 'N/A')}")
            print(f"    Average forever: {game.get('average_forever', 'N/A')}")
            print(f"    Average 2 weeks: {game.get('average_2weeks', 'N/A')}")
            
            # Show all available fields
            print(f"    All fields: {list(game.keys())}")
    else:
        print("❌ No games returned")
    
    print("\n2. Testing top 100 games in 2 weeks...")
    top_games = api.get_top_games_2weeks()
    
    if top_games:
        print(f"✅ Found {len(top_games)} top games")
        print("\n📊 Top 3 games:")
        for i, game in enumerate(top_games[:3]):
            print(f"\n  Game {i+1}: {game.get('name', 'Unknown')}")
            print(f"    Players 2 weeks: {game.get('players_2weeks', 'N/A')}")
            print(f"    CCU: {game.get('ccu', 'N/A')}")
            print(f"    Owners: {game.get('owners', 'N/A')}")
    else:
        print("❌ No top games returned")
    
    print("\n3. Testing specific game (Counter-Strike 2)...")
    cs2_data = api.get_app_details(730)  # CS2 app ID
    
    if cs2_data:
        print(f"✅ Found CS2 data")
        print(f"    Name: {cs2_data.get('name', 'Unknown')}")
        print(f"    Players 2 weeks: {cs2_data.get('players_2weeks', 'N/A')}")
        print(f"    CCU: {cs2_data.get('ccu', 'N/A')}")
        print(f"    Owners: {cs2_data.get('owners', 'N/A')}")
        print(f"    All fields: {list(cs2_data.keys())}")
    else:
        print("❌ No CS2 data returned")

if __name__ == "__main__":
    test_steamspy_data()
