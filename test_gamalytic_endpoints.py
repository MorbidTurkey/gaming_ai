#!/usr/bin/env python3
"""
Test script to verify Gamalytic API connectivity and endpoints
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GAMALYTIC_API_KEY")
base_url = "https://api.gamalytic.com"

print(f"🔑 API Key: {'✅ Found' if api_key else '❌ Missing'}")
print(f"🌐 Base URL: {base_url}")

if not api_key:
    print("❌ No API key found, exiting")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Test different endpoint patterns
endpoints_to_test = [
    "",  # Root endpoint
    "steam-games/list",
    "steam-games",
    "game/730",  # CS2
    "games",
    "games/730",
    "api/steam-games/list",
    "api/game/730"
]

for endpoint in endpoints_to_test:
    url = f"{base_url}/{endpoint}" if endpoint else base_url
    print(f"\n🔍 Testing: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS!")
            try:
                data = response.json()
                print(f"   📊 Response keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                if isinstance(data, list):
                    print(f"   📊 Response: Array with {len(data)} items")
            except:
                print(f"   📊 Response: {response.text[:200]}...")
        elif response.status_code == 404:
            print(f"   ❌ Not Found")
        elif response.status_code == 401:
            print(f"   🔐 Unauthorized - API key issue")
        elif response.status_code == 403:
            print(f"   🚫 Forbidden - Access denied")
        else:
            print(f"   ⚠️  Status {response.status_code}: {response.text[:100]}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ Timeout")
    except requests.exceptions.ConnectionError:
        print(f"   🌐 Connection Error")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n🏁 Test complete")
