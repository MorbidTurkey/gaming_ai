#!/usr/bin/env python3
"""
Test script to search for Elden Ring specifically in Gamalytic
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GAMALYTIC_API_KEY")
base_url = "https://api.gamalytic.com"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Test search for Elden Ring
print("🔍 Searching for 'Elden Ring' in Gamalytic database...")

search_url = f"{base_url}/steam-games/list"
params = {"search": "Elden Ring", "limit": 10}

try:
    response = requests.get(search_url, headers=headers, params=params, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response structure: {list(data.keys())}")
        
        result = data.get("result", [])
        print(f"Found {len(result)} games")
        
        for i, game in enumerate(result):
            print(f"  {i+1}. {game.get('name', 'Unknown')} (ID: {game.get('steamId', 'N/A')})")
            
        if result:
            # Test getting details for the first game found
            first_game = result[0]
            game_id = first_game.get("steamId")
            if game_id:
                print(f"\n🎮 Getting details for game ID {game_id}...")
                details_url = f"{base_url}/game/{game_id}"
                
                details_response = requests.get(details_url, headers=headers, timeout=10)
                print(f"Details status: {details_response.status_code}")
                
                if details_response.status_code == 200:
                    details_data = details_response.json()
                    also_played = details_data.get("alsoPlayed", [])
                    audience_overlap = details_data.get("audienceOverlap", [])
                    
                    print(f"✅ alsoPlayed games: {len(also_played)}")
                    print(f"✅ audienceOverlap games: {len(audience_overlap)}")
                    
                    if also_played:
                        print(f"First 3 'also played' games:")
                        for game in also_played[:3]:
                            print(f"  - {game.get('name', 'Unknown')}")
                    
                    if audience_overlap:
                        print(f"First 3 'audience overlap' games:")
                        for game in audience_overlap[:3]:
                            print(f"  - {game.get('name', 'Unknown')}")
        else:
            print("❌ No games found for 'Elden Ring'")
            print("Let's try other search terms...")
            
            # Try alternative searches
            alt_searches = ["Elden", "Dark Souls", "Counter-Strike"]
            for search_term in alt_searches:
                print(f"\n🔍 Trying '{search_term}'...")
                alt_response = requests.get(search_url, headers=headers, 
                                          params={"search": search_term, "limit": 3}, timeout=10)
                if alt_response.status_code == 200:
                    alt_data = alt_response.json()
                    alt_result = alt_data.get("result", [])
                    print(f"   Found {len(alt_result)} games")
                    for game in alt_result:
                        print(f"     - {game.get('name', 'Unknown')} (ID: {game.get('steamId', 'N/A')})")
    else:
        print(f"❌ Search failed: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\n🏁 Search test complete")
