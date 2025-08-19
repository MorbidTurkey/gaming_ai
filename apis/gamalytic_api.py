"""
Gamalytic API Client - Gaming Market Analysis API
Provides real-time gaming industry data, market analysis, and predictions.
"""
import os
import time
import requests
from typing import Dict, List, Optional


class GamalyticAPI:
    """
    Gamalytic API for gaming market analysis and insights
    
    This API provides:
    - Market analysis and size data
    - Genre performance analytics
    - Gaming trends and predictions
    - Competitor analysis
    - Influencer and streaming data
    """
    
    def __init__(self):
        """Initialize the Gamalytic API client"""
        self.api_key = os.getenv("GAMALYTIC_API_KEY")
        self.base_url = "https://api.gamalytic.com"  # Fixed: removed /v1 based on documentation
        
        # Rate limiting
        self.rate_limit_delay = 1.0  # 1 second between requests
        self.last_request_time = 0
        
        # Circuit breaker for failed endpoints
        self.failed_endpoints = set()  # Track endpoints that consistently fail
        self.endpoint_failures = {}   # Track failure count per endpoint
        self.max_failures = 3        # Max failures before circuit breaker kicks in
        
        # Check if API is available
        self.is_available = bool(self.api_key)
        
        if not self.is_available:
            print("⚠️  Gamalytic API key not found. Market analysis features will be unavailable.")
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to Gamalytic API with rate limiting and circuit breaker"""
        if not self.is_available:
            return {"error": "Gamalytic API key not available"}
        
        # Circuit breaker: check if endpoint has failed too many times
        if endpoint in self.failed_endpoints:
            print(f"🚫 Circuit breaker: Skipping {endpoint} (too many failures)")
            return {"error": f"Endpoint {endpoint} disabled due to repeated failures"}
        
        self._rate_limit()
        
        if params is None:
            params = {}
        
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key  # Use X-API-Key format like user's working script
        
        try:
            print(f"🌐 Making Gamalytic API request to: {endpoint}")
            response = requests.get(f"{self.base_url}/{endpoint}", 
                                  params=params, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Gamalytic API response received ({response.status_code})")
                # Reset failure count on success
                if endpoint in self.endpoint_failures:
                    del self.endpoint_failures[endpoint]
                return response.json()
            elif response.status_code == 401:
                print(f"❌ Gamalytic API authentication failed ({response.status_code})")
                self._record_failure(endpoint)
                return {"error": "Invalid API key"}
            elif response.status_code == 429:
                print(f"⚠️ Gamalytic API rate limit exceeded ({response.status_code})")
                return {"error": "Rate limit exceeded"}
            elif response.status_code == 404:
                print(f"❌ Gamalytic API endpoint not found ({response.status_code})")
                self._record_failure(endpoint)
                return {"error": "Endpoint not found"}
            else:
                print(f"❌ Gamalytic API request failed ({response.status_code})")
                self._record_failure(endpoint)
                return {"error": f"API request failed with status {response.status_code}"}
                
        except requests.RequestException as e:
            print(f"❌ Gamalytic API request error: {str(e)}")
            self._record_failure(endpoint)
            return {"error": f"Request failed: {str(e)}"}
    
    def _record_failure(self, endpoint: str):
        """Record a failure for an endpoint and enable circuit breaker if needed"""
        if endpoint not in self.endpoint_failures:
            self.endpoint_failures[endpoint] = 0
        
        self.endpoint_failures[endpoint] += 1
        
        if self.endpoint_failures[endpoint] >= self.max_failures:
            self.failed_endpoints.add(endpoint)
            print(f"🚫 Circuit breaker activated for {endpoint} (failed {self.endpoint_failures[endpoint]} times)")
    
    def reset_circuit_breaker(self, endpoint: str = None):
        """Reset circuit breaker for a specific endpoint or all endpoints"""
        if endpoint:
            self.failed_endpoints.discard(endpoint)
            if endpoint in self.endpoint_failures:
                del self.endpoint_failures[endpoint]
            print(f"✅ Circuit breaker reset for {endpoint}")
        else:
            self.failed_endpoints.clear()
            self.endpoint_failures.clear()
            print("✅ All circuit breakers reset")
    
    def get_genre_analysis(self, genres: List[str]) -> Dict:
        """Get analysis data for specific game genres"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for genre analysis"}
        
        # This would make actual API call when key is available
        params = {"genres": genres}
        response = self._make_request("genre-analysis", params)
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def get_market_analysis(self, region: str = "global") -> Dict:
        """Get market analysis for a specific region"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for market analysis"}
        
        # This would make actual API call when key is available
        params = {"region": region}
        response = self._make_request("market-analysis", params)
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def get_trends_data(self, time_period: str = "1y") -> Dict:
        """Get gaming industry trends over time"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for trends data"}
        
        # This would make actual API call when key is available
        params = {"period": time_period}
        response = self._make_request("trends", params)
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def get_competitor_analysis(self, company: str) -> Dict:
        """Get competitive analysis for a gaming company"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for competitor analysis"}
        
        endpoint = f"companies/{company}/analysis"
        response = self._make_request(endpoint)
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def get_game_performance_prediction(self, game_data: Dict) -> Dict:
        """Get performance prediction for a game based on its characteristics"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for performance predictions"}
        
        endpoint = "predictions/performance"
        response = self._make_request(endpoint, game_data)
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def get_influencer_data(self, platform: str = "twitch") -> Dict:
        """Get gaming influencer and streaming data"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for influencer data"}
        
        endpoint = f"influencers/{platform}"
        response = self._make_request(endpoint)
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def get_game_audience_overlap_by_id(self, game_id: str, comparison_game_ids: List[str] = None) -> Dict:
        """Get audience overlap percentages between games using game IDs"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for audience overlap analysis"}
        
        # Based on the API documentation, this should be the correct endpoint structure
        endpoint = f"game/{game_id}/audience-overlap"
        params = {}
        
        if comparison_game_ids:
            params["comparison_games"] = comparison_game_ids
        
        response = self._make_request(endpoint, params)
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def search_game_by_name(self, game_name: str) -> Dict:
        """Search for a game by name to get its ID for use in other endpoints"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for game search"}
        
        # This might be under /steam-games/list with search parameters
        endpoint = "steam-games/list"
        params = {
            "search": game_name,
            "limit": 10
        }
        response = self._make_request(endpoint, params)
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def get_game_audience_overlap(self, primary_game: str, comparison_games: List[str]) -> Dict:
        """Get audience overlap percentages between games (legacy method - requires game name to ID lookup)"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for audience overlap analysis"}
        
        # This method would need to:
        # 1. Search for primary game to get its ID
        # 2. Search for comparison games to get their IDs  
        # 3. Call the actual audience overlap endpoint with IDs
        
        # For now, return an informative error
        return {
            "success": False, 
            "error": "Game name to ID lookup not implemented. Use get_game_audience_overlap_by_id() with specific game IDs instead."
        }
    
    def get_game_by_name(self, game_name: str) -> Dict:
        """Get game ID from game name via steam-games list endpoint"""
        if not self.is_available:
            return {"success": False, "error": "Unable to access Gamalytic API, please add an API key or check with your system admin."}
        
        # Use the working endpoint: steam-games/list
        print(f"🔍 Searching for game: {game_name}")
        response = self._make_request("steam-games/list", {"search": game_name, "limit": 10})
        
        if "error" in response:
            return {"success": False, "error": response["error"]}
        
        return {"success": True, "data": response}
    
    def get_other_games_players_play(self, game_name: str) -> Dict:
        """Get what other games players of this game also play - Simple approach like user's script"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required"}
        
        # Step 1: Find the Steam ID for the game
        steam_id = self._find_steam_id_for_game(game_name)
        if not steam_id:
            return {"success": False, "error": f"Could not find Steam ID for '{game_name}'"}
        
        print(f"🎮 Found Steam ID {steam_id} for '{game_name}'")
        
        # Step 2: Get game data using the exact same approach as user's script
        url = f"game/{steam_id}"
        headers = {"Accept": "application/json", "X-API-Key": self.api_key}
        
        try:
            response = self._make_request(url, {})
            if "error" in response:
                return {"success": False, "error": response["error"]}
            
            # Step 3: Extract game names from alsoPlayed array
            also_played = response.get("alsoPlayed", [])
            if also_played:
                game_names = [game.get("name", "Unknown") for game in also_played]
                return {"success": True, "data": {"game_names": game_names, "type": "alsoPlayed"}}
            
            # Fallback to audienceOverlap if no alsoPlayed
            audience_overlap = response.get("audienceOverlap", [])
            if audience_overlap:
                game_names = [game.get("name", "Unknown") for game in audience_overlap]
                return {"success": True, "data": {"game_names": game_names, "type": "audienceOverlap"}}
            
            return {"success": False, "error": f"No 'alsoPlayed' or 'audienceOverlap' data found for '{game_name}'"}
            
        except Exception as e:
            return {"success": False, "error": f"API request failed: {str(e)}"}
    
    def _find_steam_id_for_game(self, game_name: str) -> str:
        """Find Steam ID for a game name using Steam API (free) instead of Gamalytic API"""
        
        # First check if the input is already a Steam ID (all digits)
        if game_name.isdigit():
            print(f"🎯 Input '{game_name}' appears to be a Steam ID already")
            return game_name
        
        # Try to use Steam API to find the game ID
        # This would require importing the Steam API client and using it
        # For now, we'll implement a basic approach that could be enhanced
        
        # Import here to avoid circular imports
        try:
            from apis.steam_api import SteamAPI
            steam_api = SteamAPI()
            
            # Use Steam's search functionality if available
            # This is a placeholder - we'd need to implement steam search
            print(f"🔍 Searching Steam API for game: {game_name}")
            
            # For now, fallback to a simple lookup table for common games
            # This could be expanded or replaced with actual Steam API search
            common_games = {
                "elden ring": "1245620",
                "dota 2": "570", 
                "counter-strike 2": "730",
                "counter-strike": "730",
                "cs2": "730",
                "pubg": "578080",
                "apex legends": "1172470",
                "cyberpunk 2077": "1091500",
                "the witcher 3": "292030",
                "witcher 3": "292030",
                "terraria": "105600",
                "left 4 dead 2": "550",
                "l4d2": "550",
                "grand theft auto v": "271590",
                "gta v": "271590",
                "gta 5": "271590",
                "total war rome ii": "214950",
                "rome total war 2": "214950",
                "total war rome 2": "214950",
                "rome 2": "214950",
                "destiny 2": "1085660",
                "rainbow six siege": "359550",
                "r6": "359550",
                "valorant": "1172470",  # Note: Valorant is on Epic/Riot, not Steam
                "minecraft": "None",     # Minecraft is not on Steam
                "fortnite": "None",      # Fortnite is not on Steam  
                "league of legends": "None", # LoL is not on Steam
                "call of duty warzone": "1962663",
                "cod warzone": "1962663",
                "warzone": "1962663",
                "rust": "252490",
                "among us": "945360",
                "fall guys": "1097150",
                "rocket league": "252950",
                "team fortress 2": "440",
                "tf2": "440",
                "garry's mod": "4000",
                "gmod": "4000",
                "half-life 2": "220",
                "portal 2": "620",
                "skyrim": "72850",
                "elder scrolls v skyrim": "72850",
                "fallout 4": "377160",
                "dark souls 3": "374320",
                "sekiro": "814380",
                "bloodborne": "None",   # PS4 exclusive
                "horizon zero dawn": "1151640",
                "monster hunter world": "582010",
                "red dead redemption 2": "1174180",
                "rdr2": "1174180",
                "assassin's creed valhalla": "2208920"
            }
            
            game_name_lower = game_name.lower()
            print(f"🔍 Looking for: '{game_name_lower}'")
            
            # First try exact match
            if game_name_lower in common_games:
                steam_id = common_games[game_name_lower]
                if steam_id != "None":  # Game is on Steam
                    print(f"🎯 Found Steam ID {steam_id} for '{game_name}' in lookup table")
                    return steam_id
                else:
                    print(f"❌ '{game_name}' is not available on Steam")
                    return None
                    
            # Try fuzzy matching for common variations
            print(f"🔍 Exact match failed, trying fuzzy matching...")
            for game_key, steam_id in common_games.items():
                if steam_id == "None":
                    continue
                    
                # Check if the input contains key words from the game name
                game_words = set(game_key.split())
                input_words = set(game_name_lower.split())
                
                print(f"   Comparing '{game_name_lower}' vs '{game_key}': input_words={input_words}, game_words={game_words}")
                
                # If most words match, consider it a match
                common_words = game_words.intersection(input_words)
                if len(common_words) >= min(2, len(game_words) - 1):
                    print(f"🎯 Found fuzzy match: '{game_name}' → '{game_key}' (Steam ID: {steam_id})")
                    return steam_id
                
        except ImportError:
            print("⚠️ Steam API not available, using fallback lookup")
        
        # If all else fails, could fall back to Gamalytic search as last resort
        # But we'll avoid this to reduce API usage as requested
        print(f"❌ Could not find Steam ID for '{game_name}'")
        return None

    def get_genre_stats(self) -> Dict:
        """Get global game stats grouped by genre using /steam-games/genres/stats endpoint"""
        if not self.is_available:
            return {"success": False, "error": "Gamalytic API key required for genre statistics"}
        
        try:
            # Use the proper endpoint from master API reference
            response = self._make_request("steam-games/genres/stats", {})
            
            if "error" in response:
                return {"success": False, "error": response["error"]}
            
            # The response should contain genre-grouped statistics with real player metrics
            return {"success": True, "data": response}
            
        except Exception as e:
            print(f"❌ Error getting genre stats from Gamalytic: {str(e)}")
            return {"success": False, "error": f"Failed to get genre statistics: {str(e)}"}
