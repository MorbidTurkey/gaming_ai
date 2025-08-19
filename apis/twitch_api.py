"""
Twitch API Integration

Provides gaming streaming data, game popularity on Twitch,
top streamers, and viewer statistics.

Requires Twitch Developer App registration at: https://dev.twitch.tv/
"""

import os
import requests
from typing import Dict, List, Optional
import time

class TwitchAPI:
    """Twitch API client for streaming and gaming data"""
    
    def __init__(self):
        self.base_url = "https://api.twitch.tv/helix"
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.access_token = None
        self.rate_limit_delay = 1
        self.last_request_time = 0
        self.is_available = bool(self.client_id and self.client_secret)
        
        if not self.is_available:
            print("ℹ️  Twitch API credentials not found - Twitch functions will be disabled")
            print("   Get credentials at: https://dev.twitch.tv/console/apps")
        else:
            print("✅ Twitch API credentials loaded - streaming data available")
            self._get_access_token()
    
    def _get_access_token(self):
        """Get OAuth access token for Twitch API"""
        if not self.is_available:
            return
        
        auth_url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        
        try:
            response = requests.post(auth_url, params=params)
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            print("✅ Twitch access token obtained")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to get Twitch access token: {e}")
            self.is_available = False
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make a request to Twitch API with rate limiting"""
        if not self.is_available or not self.access_token:
            return {"error": "Twitch API not available"}
        
        self._rate_limit()
        
        if params is None:
            params = {}
        
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", 
                                  params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Twitch API request failed: {e}")
            return {"error": str(e)}
    
    def get_top_games(self, limit: int = 20) -> Dict:
        """Get top games currently being streamed on Twitch with viewer counts"""
        params = {"first": min(limit, 100)}  # Twitch API limit
        
        result = self._make_request("games/top", params)
        
        if "error" in result:
            return {"success": False, "error": result["error"]}
        
        games = []
        for game in result.get("data", []):
            game_id = game.get("id")
            game_name = game.get("name")
            
            # Get current viewer count for this game by fetching streams
            viewer_count = self._get_game_viewer_count(game_id)
            
            games.append({
                "id": game_id,
                "name": game_name,
                # "box_art_url": game.get("box_art_url"),  # Removed to avoid images in chat
                "igdb_id": game.get("igdb_id"),
                "viewer_count": viewer_count
            })
        
        return {"success": True, "data": games}
    
    def _get_game_viewer_count(self, game_id: str) -> int:
        """Get total viewer count for a specific game"""
        try:
            params = {"game_id": game_id, "first": 100}
            result = self._make_request("streams", params)
            
            if "error" in result:
                return 0
            
            total_viewers = sum(stream.get("viewer_count", 0) for stream in result.get("data", []))
            return total_viewers
        except:
            return 0
    
    def get_game_streams(self, game_name: str, limit: int = 10) -> Dict:
        """Get current streams for a specific game"""
        # First, get game ID
        game_result = self._make_request("games", {"name": game_name})
        
        if "error" in game_result or not game_result.get("data"):
            return {"error": f"Game '{game_name}' not found"}
        
        game_id = game_result["data"][0]["id"]
        
        # Get streams for this game
        params = {
            "game_id": game_id,
            "first": min(limit, 100)
        }
        
        streams_result = self._make_request("streams", params)
        
        if "error" in streams_result:
            return streams_result
        
        streams = []
        total_viewers = 0
        
        for stream in streams_result.get("data", []):
            stream_data = {
                "user_name": stream.get("user_name"),
                "title": stream.get("title"),
                "viewer_count": stream.get("viewer_count", 0),
                "language": stream.get("language"),
                # "thumbnail_url": stream.get("thumbnail_url"),  # Removed to avoid images in chat
                "started_at": stream.get("started_at")
            }
            streams.append(stream_data)
            total_viewers += stream_data["viewer_count"]
        
        return {
            "game": game_name,
            "total_streams": len(streams),
            "total_viewers": total_viewers,
            "streams": streams
        }
    
    def get_game_analytics(self, game_name: str) -> Dict:
        """Get analytics for a game on Twitch"""
        streams_data = self.get_game_streams(game_name, 100)
        
        if "error" in streams_data:
            return streams_data
        
        streams = streams_data["streams"]
        
        if not streams:
            return {
                "game": game_name,
                "total_streams": 0,
                "total_viewers": 0,
                "average_viewers_per_stream": 0,
                "top_languages": [],
                "peak_streams": 0
            }
        
        # Calculate analytics
        viewer_counts = [s["viewer_count"] for s in streams]
        languages = {}
        
        for stream in streams:
            lang = stream["language"]
            languages[lang] = languages.get(lang, 0) + 1
        
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "game": game_name,
            "total_streams": len(streams),
            "total_viewers": sum(viewer_counts),
            "average_viewers_per_stream": sum(viewer_counts) / len(viewer_counts) if viewer_counts else 0,
            "max_viewers_single_stream": max(viewer_counts) if viewer_counts else 0,
            "min_viewers_single_stream": min(viewer_counts) if viewer_counts else 0,
            "top_languages": [{"language": lang, "streams": count} for lang, count in top_languages]
        }
    
    def get_top_streamers(self, game_name: str = None, limit: int = 10) -> List[Dict]:
        """Get top streamers, optionally filtered by game"""
        params = {"first": min(limit, 100)}
        
        if game_name:
            # Get game ID first
            game_result = self._make_request("games", {"name": game_name})
            if "data" in game_result and game_result["data"]:
                params["game_id"] = game_result["data"][0]["id"]
        
        result = self._make_request("streams", params)
        
        if "error" in result:
            return []
        
        streamers = []
        for stream in result.get("data", []):
            streamers.append({
                "user_name": stream.get("user_name"),
                "display_name": stream.get("user_login"),
                "title": stream.get("title"),
                "viewer_count": stream.get("viewer_count"),
                "game_name": stream.get("game_name"),
                "language": stream.get("language"),
                # "thumbnail_url": stream.get("thumbnail_url"),  # Removed to avoid images in chat
                "started_at": stream.get("started_at")
            })
        
        return streamers
    
    def compare_games_popularity(self, game_names: List[str]) -> Dict:
        """Compare the streaming popularity of multiple games"""
        comparison = {}
        
        for game in game_names:
            analytics = self.get_game_analytics(game)
            if "error" not in analytics:
                comparison[game] = {
                    "total_streams": analytics["total_streams"],
                    "total_viewers": analytics["total_viewers"],
                    "average_viewers_per_stream": analytics["average_viewers_per_stream"]
                }
        
        return {
            "comparison": comparison,
            "most_streams": max(comparison.items(), key=lambda x: x[1]["total_streams"])[0] if comparison else None,
            "most_viewers": max(comparison.items(), key=lambda x: x[1]["total_viewers"])[0] if comparison else None
        }
    
    def get_streaming_trends(self) -> Dict:
        """Get overall streaming trends on Twitch"""
        top_games = self.get_top_games(20)
        
        if not top_games:
            return {"error": "Could not fetch streaming trends"}
        
        # Get detailed data for top 5 games
        detailed_trends = []
        
        for game in top_games[:5]:
            analytics = self.get_game_analytics(game["name"])
            if "error" not in analytics:
                detailed_trends.append({
                    "game": game["name"],
                    "streams": analytics["total_streams"],
                    "viewers": analytics["total_viewers"],
                    "avg_viewers": analytics["average_viewers_per_stream"]
                })
        
        return {
            "top_games": [game["name"] for game in top_games[:10]],
            "detailed_trends": detailed_trends,
            "total_games_tracked": len(top_games)
        }
