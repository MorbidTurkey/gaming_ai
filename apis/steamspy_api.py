"""
SteamSpy API Integration

Handles communication with SteamSpy API for game statistics,
player data, and market analysis.
"""

import requests
from typing import Dict, List, Optional
import time
from datetime import datetime, timedelta

class SteamSpyAPI:
    """SteamSpy API client for game statistics"""
    
    def __init__(self):
        self.base_url = "https://steamspy.com/api.php"
        self.rate_limit_delay = 1  # 1 second between requests
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def _make_request(self, params: Dict) -> Dict:
        """Make a request to SteamSpy API with rate limiting"""
        self._rate_limit()
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"SteamSpy API request failed: {e}")
            return {"error": str(e)}
    
    def get_top_games(self, limit: int = 100) -> List[Dict]:
        """Get top games by player count"""
        params = {
            "request": "top100in2weeks"
        }
        
        result = self._make_request(params)
        
        if "error" in result:
            return []
        
        # Convert to list and limit results
        games = []
        for appid, data in list(result.items())[:limit]:
            if appid.isdigit():
                games.append({
                    "appid": int(appid),
                    "name": data.get("name", "Unknown"),
                    "owners": data.get("owners", "0"),
                    "players_2weeks": data.get("players_2weeks", 0),
                    "players_forever": data.get("players_forever", 0),
                    "average_playtime": data.get("average_forever", 0),
                    "median_playtime": data.get("median_forever", 0)
                })
        
        return games
    
    def get_game_data(self, game_name: str) -> Dict:
        """Get detailed data for a specific game"""
        # First try to find the game by name
        app_id = self._find_appid_by_name(game_name)
        
        if not app_id:
            return {"error": f"Game '{game_name}' not found"}
        
        return self.get_game_data_by_appid(app_id)
    
    def get_game_data_by_appid(self, app_id: int) -> Dict:
        """Get data for a game by its Steam app ID"""
        params = {
            "request": "appdetails",
            "appid": app_id
        }
        
        result = self._make_request(params)
        
        if "error" in result or not result:
            return {"error": f"No data found for app ID {app_id}"}
        
        return {
            "appid": app_id,
            "name": result.get("name", "Unknown"),
            "developer": result.get("developer", "Unknown"),
            "publisher": result.get("publisher", "Unknown"),
            "owners": result.get("owners", "0"),
            "players_forever": result.get("players_forever", 0),
            "players_2weeks": result.get("players_2weeks", 0),
            "average_playtime_forever": result.get("average_forever", 0),
            "average_playtime_2weeks": result.get("average_2weeks", 0),
            "median_playtime_forever": result.get("median_forever", 0),
            "median_playtime_2weeks": result.get("median_2weeks", 0),
            "price": result.get("price", "0"),
            "initial_price": result.get("initialprice", "0"),
            "discount": result.get("discount", 0),
            "languages": result.get("languages", ""),
            "genre": result.get("genre", ""),
            "tags": result.get("tags", {}),
            "positive_ratings": result.get("positive", 0),
            "negative_ratings": result.get("negative", 0),
            "score_rank": result.get("score_rank", 0),
            "userscore": result.get("userscore", 0)
        }
    
    def _find_appid_by_name(self, game_name: str) -> Optional[int]:
        """Find a game's app ID by searching for its name"""
        # Get all games and search through them
        params = {"request": "all"}
        result = self._make_request(params)
        
        if "error" in result:
            return None
        
        game_name_lower = game_name.lower()
        
        for appid, data in result.items():
            if appid.isdigit() and isinstance(data, dict):
                if data.get("name", "").lower() == game_name_lower:
                    return int(appid)
        
        # If exact match not found, try partial match
        for appid, data in result.items():
            if appid.isdigit() and isinstance(data, dict):
                if game_name_lower in data.get("name", "").lower():
                    return int(appid)
        
        return None
    
    def get_genre_data(self, genre: str) -> List[Dict]:
        """Get games by genre"""
        params = {
            "request": "genre",
            "genre": genre
        }
        
        result = self._make_request(params)
        
        if "error" in result:
            return []
        
        games = []
        for appid, data in result.items():
            if appid.isdigit():
                games.append({
                    "appid": int(appid),
                    "name": data.get("name", "Unknown"),
                    "owners": data.get("owners", "0"),
                    "players_2weeks": data.get("players_2weeks", 0),
                    "score_rank": data.get("score_rank", 0)
                })
        
        return games
    
    def get_tag_data(self, tag: str) -> List[Dict]:
        """Get games by tag"""
        params = {
            "request": "tag",
            "tag": tag
        }
        
        result = self._make_request(params)
        
        if "error" in result:
            return []
        
        games = []
        for appid, data in result.items():
            if appid.isdigit():
                games.append({
                    "appid": int(appid),
                    "name": data.get("name", "Unknown"),
                    "owners": data.get("owners", "0"),
                    "players_2weeks": data.get("players_2weeks", 0)
                })
        
        return games
    
    def search_games(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search games by name"""
        # Get all games and filter by query
        params = {"request": "all"}
        result = self._make_request(params)
        
        if "error" in result:
            return []
        
        query_lower = query.lower()
        games = []
        
        for appid, data in result.items():
            if appid.isdigit() and isinstance(data, dict):
                name = data.get("name", "").lower()
                if query_lower in name:
                    games.append({
                        "appid": int(appid),
                        "name": data.get("name", "Unknown"),
                        "owners": data.get("owners", "0"),
                        "players_2weeks": data.get("players_2weeks", 0)
                    })
        
        return games[:50]  # Limit results
    
    def get_player_history(self, game_name: str, time_period: str = "30d") -> Dict:
        """Get historical player data - not available through SteamSpy API"""
        # SteamSpy doesn't provide historical data
        return {"error": "Historical player data not available through SteamSpy API"}
    
    def get_current_players(self, game_name: str) -> int:
        """Get current player count for a game"""
        data = self.get_game_data(game_name)
        return data.get("players_2weeks", 0) if "error" not in data else 0

    def analyze_genre_popularity(self) -> List[Dict]:
        """
        Analyze the most popular genres by getting top games and grouping by genre
        This provides better data than the genre endpoint which has limited fields
        """
        print("🔍 Getting top games for genre analysis...")
        
        # Get top 100 games by players in last 2 weeks (better data)
        top_games = self.get_top_games_by_players_2weeks()
        
        if not top_games:
            print("❌ No top games data available, falling back to genre endpoint")
            return self._analyze_genre_via_genre_endpoint()
        
        # Group games by genre and calculate statistics
        genre_stats = {}
        
        for game in top_games:
            # Skip games without genre data
            if not game.get("tags"):
                continue
                
            # Parse tags to find genres
            tags = game.get("tags", {})
            game_genres = []
            
            # Common genre tags from Steam
            genre_keywords = {
                "Action": ["Action"],
                "Adventure": ["Adventure"],
                "RPG": ["RPG", "Role-Playing"],
                "Strategy": ["Strategy", "Real Time Strategy", "Turn-Based Strategy"],
                "Simulation": ["Simulation", "Sim"],
                "Sports": ["Sports"],
                "Racing": ["Racing"],
                "Shooter": ["Shooter", "First-Person Shooter", "Third-Person Shooter"],
                "Puzzle": ["Puzzle"],
                "Indie": ["Indie", "Independent"],
                "Casual": ["Casual"],
                "Multiplayer": ["Multiplayer", "Co-op", "Online"],
                "Early Access": ["Early Access"],
                "Free to Play": ["Free to Play", "F2P"],
                "Horror": ["Horror"],
                "Fighting": ["Fighting"],
                "Platformer": ["Platformer", "2D Platformer"],
                "MMO": ["MMO", "MMORPG", "Massively Multiplayer"]
            }
            
            # Find matching genres for this game
            for genre_name, keywords in genre_keywords.items():
                for keyword in keywords:
                    if any(keyword.lower() in tag_name.lower() for tag_name in tags.keys()):
                        if genre_name not in game_genres:
                            game_genres.append(genre_name)
                        break
            
            # If no specific genre found, try to categorize by name or default to Action
            if not game_genres:
                game_name = game.get("name", "").lower()
                if any(word in game_name for word in ["rpg", "role", "fantasy"]):
                    game_genres = ["RPG"]
                elif any(word in game_name for word in ["strategy", "war", "civilization"]):
                    game_genres = ["Strategy"]
                elif any(word in game_name for word in ["racing", "drive", "car"]):
                    game_genres = ["Racing"]
                elif any(word in game_name for word in ["sport", "football", "basketball", "soccer"]):
                    game_genres = ["Sports"]
                else:
                    game_genres = ["Action"]  # Default genre
            
            # Add this game to each of its genres
            for genre in game_genres:
                if genre not in genre_stats:
                    genre_stats[genre] = {
                        "genre": genre,
                        "total_games": 0,
                        "total_players_2weeks": 0,
                        "total_ccu": 0,
                        "games": []
                    }
                
                genre_stats[genre]["total_games"] += 1
                genre_stats[genre]["total_players_2weeks"] += game.get("players_2weeks", 0)
                genre_stats[genre]["total_ccu"] += game.get("ccu", 0)
                genre_stats[genre]["games"].append(game)
        
        # Convert to list and calculate final metrics
        result = []
        for genre_name, stats in genre_stats.items():
            total_games = stats["total_games"]
            total_players_2weeks = stats["total_players_2weeks"]
            total_ccu = stats["total_ccu"]
            
            # Use CCU as primary metric, fallback to players_2weeks
            primary_activity = total_ccu if total_ccu > 0 else total_players_2weeks
            avg_activity = primary_activity / total_games if total_games > 0 else 0
            
            # Calculate estimated owners
            total_owners = 0
            for game in stats["games"]:
                owners_str = game.get("owners", "0")
                if " .. " in owners_str:
                    try:
                        parts = owners_str.split(" .. ")
                        min_owners = int(parts[0].replace(",", ""))
                        max_owners = int(parts[1].replace(",", ""))
                        estimated_owners = (min_owners + max_owners) // 2
                        total_owners += estimated_owners
                    except:
                        pass
            
            result.append({
                "genre": genre_name,
                "total_games": total_games,
                "total_players_2weeks": total_players_2weeks,
                "total_ccu": total_ccu,
                "primary_activity": primary_activity,
                "avg_players_per_game": avg_activity,
                "estimated_total_owners": total_owners,
                "top_games": sorted(stats["games"], 
                                  key=lambda x: x.get("ccu", 0) if x.get("ccu", 0) > 0 else x.get("players_2weeks", 0), 
                                  reverse=True)[:5]
            })
        
        # Sort by primary activity metric
        result.sort(key=lambda x: x["primary_activity"], reverse=True)
        
        print(f"✅ Analyzed {len(result)} genres from {len(top_games)} top games")
        return result
    
    def _analyze_genre_via_genre_endpoint(self) -> List[Dict]:
        """
        Fallback method using the genre endpoint (limited data)
        """
        print("🔍 Using genre endpoint fallback...")
        
        # Common Steam genres to analyze
        popular_genres = [
            "Action", "Adventure", "RPG", "Strategy", "Simulation", 
            "Sports", "Racing", "Shooter", "Puzzle", "Indie",
            "Casual", "Multiplayer", "Early Access", "Free to Play",
            "Horror", "Fighting", "Platformer", "MMO"
        ]
        
        genre_stats = []
        
        for genre in popular_genres:
            print(f"🔍 Analyzing genre: {genre}")
            games = self.get_genre_data(genre)
            
            if games:
                # For genre endpoint, we only have limited data
                # Use estimated owners as primary metric since player counts are often 0
                total_owners = 0
                total_games = len(games)
                
                for game in games:
                    owners_str = game.get("owners", "0")
                    if " .. " in owners_str:
                        try:
                            parts = owners_str.split(" .. ")
                            min_owners = int(parts[0].replace(",", ""))
                            max_owners = int(parts[1].replace(",", ""))
                            estimated_owners = (min_owners + max_owners) // 2
                            total_owners += estimated_owners
                        except:
                            pass
                
                genre_stats.append({
                    "genre": genre,
                    "total_games": total_games,
                    "total_players_2weeks": 0,  # Not reliable from genre endpoint
                    "total_ccu": 0,  # Not available from genre endpoint
                    "primary_activity": total_owners,  # Use ownership as activity metric
                    "avg_players_per_game": total_owners / total_games if total_games > 0 else 0,
                    "estimated_total_owners": total_owners,
                    "top_games": sorted(games, key=lambda x: x.get("score_rank", 999999))[:5]  # Sort by score rank
                })
                
                # Rate limiting
                time.sleep(1)
        
        # Sort by total owners (primary activity metric for fallback)
        genre_stats.sort(key=lambda x: x["primary_activity"], reverse=True)
        
        return genre_stats
    
    def get_top_games_by_players_2weeks(self, limit: int = 100) -> List[Dict]:
        """Get top games by players in last 2 weeks with detailed data"""
        params = {
            "request": "top100in2weeks"
        }
        
        result = self._make_request(params)
        
        if "error" in result:
            print(f"❌ Error getting top games: {result['error']}")
            return []
        
        # Convert dict to list of games
        games = []
        for app_id, game_data in result.items():
            if isinstance(game_data, dict):
                game_data["appid"] = app_id
                games.append(game_data)
        
        return games[:limit]
