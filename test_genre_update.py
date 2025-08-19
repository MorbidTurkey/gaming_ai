#!/usr/bin/env python3
"""
Test the updated genre analysis approach
"""

from apis.steamspy_api import SteamSpyAPI

def test_updated_genre_analysis():
    """Test the updated genre analysis"""
    
    print("🔍 Testing updated genre analysis...")
    api = SteamSpyAPI()
    
    # Test the new analyze_genre_popularity method
    genre_stats = api.analyze_genre_popularity()
    
    if genre_stats:
        print(f"✅ Found {len(genre_stats)} genre statistics")
        print("\n📊 Top 5 genres:")
        for i, genre in enumerate(genre_stats[:5]):
            print(f"\n  {i+1}. {genre['genre']}")
            print(f"     Primary Activity: {genre['primary_activity']:,}")
            print(f"     Total Games: {genre['total_games']:,}")
            print(f"     Estimated Owners: {genre['estimated_total_owners']:,}")
            print(f"     Players 2 weeks: {genre['total_players_2weeks']:,}")
            print(f"     CCU: {genre['total_ccu']:,}")
            
            top_games = genre.get('top_games', [])[:2]
            if top_games:
                print(f"     Top games: {', '.join([g.get('name', 'Unknown') for g in top_games])}")
    else:
        print("❌ No genre statistics returned")

if __name__ == "__main__":
    test_updated_genre_analysis()
