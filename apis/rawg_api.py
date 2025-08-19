"""
RAWG API Integration

RAWG is a comprehensive video game database with information about games,
platforms, genres, developers, and more. Provides free API access.

Free tier: 20,000 requests per month
Get your key at: https://rawg.io/apidocs
"""

import os
import requests
from typing import Dict, List, Optional
import time

class RAWGAPI:
    """RAWG Video Game Database API client"""
    
    def __init__(self):
        self.base_url = "https://api.rawg.io/api"
        self.api_key = os.getenv('RAWG_API_KEY')
        self.rate_limit_delay = 1  # 1 second between requests
        self.last_request_time = 0
        self.is_available = bool(self.api_key)
        
        if not self.api_key:
            print("ℹ️  RAWG API key not found - RAWG functions will be disabled")
            print("   Get a free key at: https://rawg.io/apidocs (20k requests/month)")
        else:
            print("✅ RAWG API key loaded - game database access available")
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to RAWG API with rate limiting"""
        if not self.is_available:
            return {"error": "RAWG API key not available"}
        
        self._rate_limit()
        
        if params is None:
            params = {}
        
        if self.api_key:
            params['key'] = self.api_key
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"RAWG API request failed: {e}")
            return {"error": str(e)}
    
    def search_games(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for games in RAWG database"""
        params = {
            "search": query,
            "page_size": limit
        }
        
        result = self._make_request("games", params)
        
        if "error" in result:
            return []
        
        games = []
        for game in result.get("results", []):
            games.append({
                "id": game.get("id"),
                "name": game.get("name"),
                "released": game.get("released"),
                "rating": game.get("rating"),
                "ratings_count": game.get("ratings_count"),
                "metacritic": game.get("metacritic"),
                "platforms": [p["platform"]["name"] for p in game.get("platforms", [])],
                "genres": [g["name"] for g in game.get("genres", [])],
                "developers": [d["name"] for d in game.get("developers", [])],
                "publishers": [p["name"] for p in game.get("publishers", [])],
                # "background_image": game.get("background_image"),  # Removed to avoid images in chat
                "playtime": game.get("playtime"),
                "tags": [t["name"] for t in game.get("tags", [])][:10]  # Limit tags
            })
        
        return games
    
    def get_game_details(self, game_id: int) -> Dict:
        """Get detailed information about a specific game"""
        result = self._make_request(f"games/{game_id}")
        
        if "error" in result:
            return result
        
        return {
            "id": result.get("id"),
            "name": result.get("name"),
            "description": result.get("description_raw", "")[:500] + "..." if result.get("description_raw") else "",
            "released": result.get("released"),
            "rating": result.get("rating"),
            "ratings_count": result.get("ratings_count"),
            "metacritic": result.get("metacritic"),
            "playtime": result.get("playtime"),
            "achievements_count": result.get("achievements_count"),
            "platforms": [p["platform"]["name"] for p in result.get("platforms", [])],
            "genres": [g["name"] for g in result.get("genres", [])],
            "developers": [d["name"] for d in result.get("developers", [])],
            "publishers": [p["name"] for p in result.get("publishers", [])],
            "esrb_rating": result.get("esrb_rating", {}).get("name") if result.get("esrb_rating") else None,
            "website": result.get("website"),
            "reddit_url": result.get("reddit_url"),
            # "background_image": result.get("background_image"),  # Removed to avoid images in chat
            "tags": [t["name"] for t in result.get("tags", [])][:15]
        }
    
    def get_trending_games(self, time_period: str = "week", limit: int = 20) -> List[Dict]:
        """Get trending games based on different time periods"""
        # RAWG doesn't have explicit trending, so we'll use ordering by different metrics
        order_map = {
            "week": "-added",  # Recently added
            "month": "-rating",  # Highest rated
            "year": "-released"  # Recently released
        }
        
        params = {
            "ordering": order_map.get(time_period, "-added"),
            "page_size": limit
        }
        
        result = self._make_request("games", params)
        
        if "error" in result:
            return []
        
        return self._format_game_list(result.get("results", []))
    
    def get_games_by_genre(self, genre: str, limit: int = 20) -> List[Dict]:
        """Get games by specific genre"""
        params = {
            "genres": genre.lower(),
            "page_size": limit,
            "ordering": "-rating"
        }
        
        result = self._make_request("games", params)
        
        if "error" in result:
            return []
        
        return self._format_game_list(result.get("results", []))
    
    def get_games_by_platform(self, platform: str, limit: int = 20) -> List[Dict]:
        """Get games by platform"""
        # Map common platform names to RAWG platform IDs
        platform_map = {
            "pc": "4",
            "playstation": "187",
            "xbox": "186",
            "nintendo": "7",
            "mobile": "21"
        }
        
        platform_id = platform_map.get(platform.lower())
        if not platform_id:
            return []
        
        params = {
            "platforms": platform_id,
            "page_size": limit,
            "ordering": "-rating"
        }
        
        result = self._make_request("games", params)
        
        if "error" in result:
            return []
        
        return self._format_game_list(result.get("results", []))
    
    def get_game_reviews(self, game_id: int, limit: int = 10) -> List[Dict]:
        """Get reviews for a specific game"""
        params = {"page_size": limit}
        
        result = self._make_request(f"games/{game_id}/reviews", params)
        
        if "error" in result:
            return []
        
        reviews = []
        for review in result.get("results", []):
            reviews.append({
                "id": review.get("id"),
                "text": review.get("text", "")[:200] + "..." if review.get("text") else "",
                "rating": review.get("rating"),
                "created": review.get("created"),
                "user": review.get("user", {}).get("username", "Anonymous")
            })
        
        return reviews
    
    def get_genres(self) -> List[Dict]:
        """Get all available game genres"""
        result = self._make_request("genres")
        
        if "error" in result:
            return []
        
        return [
            {
                "id": genre.get("id"),
                "name": genre.get("name"),
                "games_count": genre.get("games_count")
            }
            for genre in result.get("results", [])
        ]
    
    def get_platforms(self) -> List[Dict]:
        """Get all available gaming platforms"""
        result = self._make_request("platforms")
        
        if "error" in result:
            return []
        
        return [
            {
                "id": platform.get("id"),
                "name": platform.get("name"),
                "games_count": platform.get("games_count")
            }
            for platform in result.get("results", [])
        ]
    
    def _format_game_list(self, games: List[Dict]) -> List[Dict]:
        """Format a list of games consistently"""
        formatted = []
        for game in games:
            formatted.append({
                "id": game.get("id"),
                "name": game.get("name"),
                "released": game.get("released"),
                "rating": game.get("rating"),
                "metacritic": game.get("metacritic"),
                "platforms": [p["platform"]["name"] for p in game.get("platforms", [])],
                "genres": [g["name"] for g in game.get("genres", [])],
                # "background_image": game.get("background_image")  # Removed to avoid images in chat
            })
        
        return formatted
    
    def find_game_by_name(self, game_name: str) -> Optional[Dict]:
        """Find a game by name and return its details"""
        # First search for the game
        search_results = self.search_games(game_name, limit=5)
        
        if not search_results:
            return None
        
        # Look for exact match first, then best match
        exact_match = None
        best_match = None
        
        for game in search_results:
            if game["name"].lower() == game_name.lower():
                exact_match = game
                break
            elif game_name.lower() in game["name"].lower():
                if best_match is None:
                    best_match = game
        
        # Use exact match if found, otherwise use best match
        selected_game = exact_match or best_match or search_results[0]
        
        # Get full details for the selected game
        return self.get_game_details(selected_game["id"])
