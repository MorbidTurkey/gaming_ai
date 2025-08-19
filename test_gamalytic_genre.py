#!/usr/bin/env python3
"""
Test Gamalytic API Genre Stats vs SteamSpy Genre Analysis

This script tests the new Gamalytic-based approach for genre analysis
to verify it provides better data than the SteamSpy approach.
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from apis.gamalytic_api import GamalyticAPI
from apis.steamspy_api import SteamSpyAPI

def test_gamalytic_genre_stats():
    """Test the new Gamalytic genre stats endpoint"""
    print("🧪 Testing Gamalytic Genre Stats...")
    print("=" * 50)
    
    gamalytic = GamalyticAPI()
    
    if not gamalytic.is_available:
        print("❌ Gamalytic API not available (no API key)")
        return False
    
    try:
        result = gamalytic.get_genre_stats()
        print(f"📊 Gamalytic result: {result}")
        
        if result.get("success"):
            print("✅ Gamalytic genre stats successful!")
            data = result.get("data", {})
            print(f"📈 Data type: {type(data)}")
            if isinstance(data, dict):
                print(f"📋 Available genres: {list(data.keys())[:5]}...")  # Show first 5
            elif isinstance(data, list):
                print(f"📋 Number of genre entries: {len(data)}")
            return True
        else:
            print(f"❌ Gamalytic failed: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Gamalytic exception: {str(e)}")
        return False

def test_steamspy_comparison():
    """Test SteamSpy genre analysis for comparison"""
    print("\n🧪 Testing SteamSpy Genre Analysis (for comparison)...")
    print("=" * 50)
    
    steamspy = SteamSpyAPI()
    
    try:
        result = steamspy.analyze_genre_popularity()
        print(f"📊 SteamSpy result type: {type(result)}")
        
        if isinstance(result, list) and len(result) > 0:
            print(f"✅ SteamSpy returned {len(result)} genres")
            
            # Check data quality
            first_genre = result[0]
            print(f"📋 First genre structure: {first_genre.keys()}")
            
            # Check for meaningful player data
            has_real_data = False
            for genre in result[:3]:
                activity = genre.get("primary_activity", 0)
                ccu = genre.get("total_ccu", 0)
                players_2w = genre.get("total_players_2weeks", 0)
                
                if activity > 0 or ccu > 0 or players_2w > 0:
                    has_real_data = True
                    break
            
            if has_real_data:
                print("✅ SteamSpy has meaningful player activity data")
            else:
                print("❌ SteamSpy genre data lacks meaningful player activity metrics")
                
            return True
        else:
            print(f"❌ SteamSpy failed or returned empty data")
            return False
    except Exception as e:
        print(f"❌ SteamSpy exception: {str(e)}")
        return False

def main():
    """Run the comparison test"""
    print("🎮 Testing Genre Analysis APIs")
    print("=" * 60)
    
    gamalytic_success = test_gamalytic_genre_stats()
    steamspy_success = test_steamspy_comparison()
    
    print("\n📊 COMPARISON RESULTS:")
    print("=" * 60)
    
    if gamalytic_success and steamspy_success:
        print("✅ Both APIs working - Gamalytic preferred for real player metrics")
        print("💡 Recommendation: Use Gamalytic for genre analysis")
    elif gamalytic_success:
        print("✅ Gamalytic working, SteamSpy has issues")
        print("💡 Recommendation: Definitely use Gamalytic")
    elif steamspy_success:
        print("❌ Gamalytic unavailable, SteamSpy working but limited data")
        print("💡 Recommendation: Use SteamSpy as fallback only")
    else:
        print("❌ Both APIs have issues")
        print("💡 Recommendation: Need to investigate API connectivity")

if __name__ == "__main__":
    main()
