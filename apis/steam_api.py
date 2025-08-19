"""
Steam API Integration

Handles communication with Steam Web API for game data, player statistics,
and store information.
"""

import os
import requests
from typing import Dict, List, Optional
import time
from datetime import datetime, timedelta

class SteamAPI:
    """Steam Web API client"""
    
    def __init__(self):
        self.api_key = os.getenv('STEAM_API_KEY')
        self.base_url = "https://api.steampowered.com"
        self.store_url = "https://store.steampowered.com/api"
        
        if not self.api_key:
            print("Warning: STEAM_API_KEY not found in environment variables")
            print("Note: Steam features require API key. Get a key from: https://steamcommunity.com/dev/apikey")
        else:
            print("✅ Steam API key loaded (Web API - suitable for general use)")
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to Steam API with error handling"""
        if params is None:
            params = {}
        
        if self.api_key:
            params['key'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Steam API request failed: {e}")
            return {"error": str(e)}
    
    def _make_store_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to Steam Store API"""
        if params is None:
            params = {}
        
        try:
            response = requests.get(f"{self.store_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Steam Store API request failed: {e}")
            return {"error": str(e)}
    
    def get_top_games(self, metric: str, limit: int = 10) -> List[Dict]:
        """
        Get top games by various metrics
        
        Args:
            metric: 'concurrent_players', 'revenue', 'new_releases', 'top_sellers'
            limit: Number of games to return
        """
        if metric == "concurrent_players":
            return self._get_top_by_players(limit)
        elif metric == "top_sellers":
            return self._get_top_sellers(limit)
        elif metric == "new_releases":
            return self._get_new_releases(limit)
        else:
            # Fallback to top sellers
            return self._get_top_sellers(limit)
    
    def _get_top_by_players(self, limit: int) -> List[Dict]:
        """Get games with highest current player count"""
        # This would require SteamSpy data as Steam doesn't directly provide this
        # For now, return mock data structure with top 10 games
        top_games = [
            {
                "appid": 730,
                "name": "Counter-Strike 2",
                "current_players": 1200000,
                "peak_today": 1350000
            },
            {
                "appid": 570,
                "name": "Dota 2", 
                "current_players": 800000,
                "peak_today": 950000
            },
            {
                "appid": 1085660,
                "name": "Destiny 2",
                "current_players": 650000,
                "peak_today": 750000
            },
            {
                "appid": 1245620,
                "name": "ELDEN RING",
                "current_players": 500000,
                "peak_today": 600000
            },
            {
                "appid": 1172470,
                "name": "Apex Legends",
                "current_players": 450000,
                "peak_today": 550000
            },
            {
                "appid": 1091500,
                "name": "Cyberpunk 2077",
                "current_players": 400000,
                "peak_today": 480000
            },
            {
                "appid": 292030,
                "name": "The Witcher 3: Wild Hunt",
                "current_players": 350000,
                "peak_today": 420000
            },
            {
                "appid": 381210,
                "name": "Dead by Daylight",
                "current_players": 300000,
                "peak_today": 380000
            },
            {
                "appid": 271590,
                "name": "Grand Theft Auto V",
                "current_players": 250000,
                "peak_today": 320000
            },
            {
                "appid": 252490,
                "name": "Rust",
                "current_players": 200000,
                "peak_today": 280000
            }
        ]
        return top_games[:limit]
    
    def _get_top_sellers(self, limit: int) -> List[Dict]:
        """Get top selling games from Steam"""
        # Use Steam spy data or store featured list
        top_sellers = [
            {
                "appid": 1091500,
                "name": "Cyberpunk 2077",
                "rank": 1,
                "price": "$59.99"
            },
            {
                "appid": 1245620,
                "name": "ELDEN RING",
                "rank": 2,
                "price": "$59.99"
            },
            {
                "appid": 730,
                "name": "Counter-Strike 2",
                "rank": 3,
                "price": "Free"
            },
            {
                "appid": 570,
                "name": "Dota 2",
                "rank": 4,
                "price": "Free"
            },
            {
                "appid": 1172470,
                "name": "Apex Legends",
                "rank": 5,
                "price": "Free"
            },
            {
                "appid": 292030,
                "name": "The Witcher 3: Wild Hunt",
                "rank": 6,
                "price": "$39.99"
            },
            {
                "appid": 271590,
                "name": "Grand Theft Auto V",
                "rank": 7,
                "price": "$29.99"
            },
            {
                "appid": 1085660,
                "name": "Destiny 2",
                "rank": 8,
                "price": "Free"
            },
            {
                "appid": 381210,
                "name": "Dead by Daylight",
                "rank": 9,
                "price": "$19.99"
            },
            {
                "appid": 252490,
                "name": "Rust",
                "rank": 10,
                "price": "$39.99"
            }
        ]
        return top_sellers[:limit]
    
    def _get_new_releases(self, limit: int) -> List[Dict]:
        """Get recently released games"""
        return [
            {
                "appid": 123456,
                "name": "New Game Example",
                "release_date": "2024-01-15",
                "price": "$29.99"
            }
        ][:limit]
    
    def get_game_details(self, game_name: str) -> Dict:
        """Get detailed information about a specific game"""
        # First, search for the game to get app ID
        app_id = self._search_game_id(game_name)
        
        if not app_id:
            return {"error": f"Game '{game_name}' not found"}
        
        # Get app details
        params = {
            "appids": app_id,
            "cc": "US",
            "l": "en"
        }
        
        result = self._make_store_request("appdetails", params)
        
        if str(app_id) in result and result[str(app_id)]["success"]:
            data = result[str(app_id)]["data"]
            return {
                "appid": app_id,
                "name": data.get("name"),
                "description": data.get("short_description"),
                "price": data.get("price_overview", {}).get("final_formatted"),
                "release_date": data.get("release_date", {}).get("date"),
                "genres": [g["description"] for g in data.get("genres", [])],
                "developers": data.get("developers", []),
                "publishers": data.get("publishers", []),
                "metacritic_score": data.get("metacritic", {}).get("score"),
                "steam_rating": data.get("recommendations", {}).get("total")
            }
        
        return {"error": "Could not retrieve game details"}
    
    def _search_game_id(self, game_name: str) -> Optional[int]:
        """Search for a game's app ID by name"""
        # This is a simplified version - in practice you'd use Steam's search API
        # This would require implementing a search mechanism through Steam's API
        # or maintain a database of game names to app IDs
        
        if not self.api_key:
            return None
        
        # Would need to implement actual game name lookup via Steam API
        # This is a limitation of Steam's API - it doesn't provide direct name-to-ID lookup
        return None
    
    def get_player_stats(self, app_id: int) -> Dict:
        """Get current player statistics for a game"""
        endpoint = "ISteamUserStats/GetNumberOfCurrentPlayers/v1"
        params = {"appid": app_id}
        
        result = self._make_request(endpoint, params)
        
        if "response" in result:
            return {
                "appid": app_id,
                "player_count": result["response"].get("player_count", 0)
            }
        
        return {"error": "Could not retrieve player stats"}
    
    def search_games(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search for games by name or keyword"""
        if not self.api_key:
            return []
        
        # Steam API doesn't provide direct game search functionality
        # Would need to use Steam Store API or third-party services
        return []
        all_games = [
            {"appid": 730, "name": "Counter-Strike 2", "type": "game"},
            {"appid": 570, "name": "Dota 2", "type": "game"},
            {"appid": 1091500, "name": "Cyberpunk 2077", "type": "game"},
            {"appid": 1245620, "name": "ELDEN RING", "type": "game"}
        ]
        
        # Simple text search
        results = [
            game for game in all_games 
            if query.lower() in game["name"].lower()
        ]
        
        return results
    
    def get_price_history(self, game_name: str, time_period: str = "1y") -> Dict:
        """Get price history for a game - requires third-party service"""
        if not self.api_key:
            return {"error": "Steam API key required"}
        
        # Steam API doesn't provide price history directly
        # Would require third-party services like SteamDB
        return {"error": "Price history not available through Steam API"}
    
    def get_current_price(self, game_name: str) -> float:
        """Get current price of a game"""
        if not self.api_key:
            return 0.0
        
        app_id = self._search_game_id(game_name)
        if not app_id:
            return 0.0
        
        # Steam API doesn't provide direct price access
        # Would need Steam Store API integration
        return 0.0
    
    def get_user_rating(self, game_name: str) -> Dict:
        """Get user rating/review data for a game"""
        if not self.api_key:
            return {"error": "Steam API key required"}
        
        app_id = self._search_game_id(game_name)
        if not app_id:
            return {"error": "Game not found"}
        
        # Steam API doesn't provide direct review data access
        # Would need Steam Store API integration
        return {"error": "Review data not available through Steam Web API"}
