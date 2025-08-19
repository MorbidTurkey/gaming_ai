"""
Data Retriever - Clean data extraction from APIs

This module takes metric definitions and retrieves clean DataFrames
ready for visualization.
"""

import pandas as pd
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class DataRetriever:
    """Retrieves and formats data from gaming APIs"""
    
    def __init__(self, apis):
        """
        Initialize with API instances
        
        Args:
            apis: Dictionary containing API instances (steam_api, twitch_api, etc.)
        """
        self.apis = apis
    
    def get_metric_data(self, metric_info: Dict[str, Any], game_name: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Retrieve data for a specific metric
        
        Args:
            metric_info: Metric configuration from MetricRegistry
            game_name: Optional game name for game-specific queries
            
        Returns:
            Tuple of (DataFrame, error_message). DataFrame is None if error occurred.
        """
        api_name = metric_info["api"]
        method_name = metric_info["method"]
        
        print(f"🔍 DATA RETRIEVER DEBUG:")
        print(f"   → API name: '{api_name}'")
        print(f"   → Method name: '{method_name}'")
        print(f"   → Game name: '{game_name}'")
        print(f"   → Has game_name: {bool(game_name)}")
        
        try:
            if api_name == "twitch":
                return self._get_twitch_data(method_name, metric_info)
            elif api_name == "steam":
                return self._get_steam_data(method_name, metric_info)
            elif api_name == "steamspy":
                return self._get_steamspy_data(method_name, metric_info)
            elif api_name == "rawg":
                return self._get_rawg_data(method_name, metric_info)
            elif api_name == "gamalytic" and game_name:
                return self._get_gamalytic_data(method_name, metric_info, game_name)
            elif api_name == "gamalytic_simple" and game_name:
                return self._get_simple_gamalytic_data(method_name, metric_info, game_name)
            elif api_name == "multi" and game_name:
                return self._get_game_stats(game_name, metric_info)
            else:
                return None, f"Unknown API: {api_name}"
                
        except Exception as e:
            logger.error(f"Error retrieving {api_name} data: {e}")
            return None, str(e)
    
    def _get_twitch_data(self, method_name: str, metric_info: Dict) -> Tuple[Optional[pd.DataFrame], str]:
        """Get Twitch data and convert to DataFrame"""
        print(f"🎯 RETRIEVING TWITCH DATA")
        
        if not hasattr(self.apis, 'twitch_api') or not self.apis.twitch_api.is_available:
            return None, "Unable to access Twitch API, please add an API key or check with your system admin."
        
        try:
            # Get method arguments with defaults
            method_args = metric_info.get("method_args", {"limit": 10})
            
            # Call the API method
            method = getattr(self.apis.twitch_api, method_name)
            raw_data = method(**method_args)
            
            print(f"📺 Raw Twitch data: {raw_data}")
            
            if not raw_data or not isinstance(raw_data, dict) or not raw_data.get("success"):
                return None, "Failed to retrieve Twitch data"
            
            games_data = raw_data.get("data", [])
            if not games_data:
                return None, "No Twitch games data returned"
            
            # Convert to DataFrame
            df = pd.DataFrame(games_data)
            
            # Ensure required columns exist
            data_format = metric_info["data_format"]
            x_col = data_format["x_column"]
            y_col = data_format["y_column"]
            
            if x_col not in df.columns or y_col not in df.columns:
                return None, f"Missing required columns: {x_col}, {y_col}"
            
            # Clean and format data
            df = df[[x_col, y_col]].copy()
            df = df.dropna()
            
            # Sort by viewer count (descending)
            df = df.sort_values(y_col, ascending=False)
            
            print(f"✅ Twitch DataFrame created: {len(df)} rows")
            print(f"📊 Columns: {list(df.columns)}")
            print(f"🔢 Sample data: {df.head(3).to_dict('records')}")
            
            return df, ""
            
        except Exception as e:
            print(f"❌ Twitch data error: {e}")
            return None, str(e)
    
    def _get_steam_data(self, method_name: str, metric_info: Dict) -> Tuple[Optional[pd.DataFrame], str]:
        """Get Steam data and convert to DataFrame"""
        print(f"🎯 RETRIEVING STEAM DATA")
        
        if not hasattr(self.apis, 'steam_api') or not self.apis.steam_api:
            return None, "Unable to access Steam API, please add an API key or check with your system admin."
        
        # Check if Steam API has valid key
        if not self.apis.steam_api.api_key:
            return None, "Unable to access Steam API, please add an API key or check with your system admin."
        
        try:
            # Get method arguments with defaults
            method_args = metric_info.get("method_args", {})
            
            # Call the API method
            method = getattr(self.apis.steam_api, method_name)
            raw_data = method(**method_args)
            
            print(f"🎮 Raw Steam data: {raw_data[:3] if raw_data else 'None'}")
            
            if not raw_data:
                return None, "No Steam data returned"
            
            # Convert to DataFrame
            df = pd.DataFrame(raw_data)
            
            # Ensure required columns exist
            data_format = metric_info["data_format"]
            x_col = data_format["x_column"]
            y_col = data_format["y_column"]
            
            if x_col not in df.columns or y_col not in df.columns:
                return None, f"Missing required columns: {x_col}, {y_col}"
            
            # Clean and format data
            df = df[[x_col, y_col]].copy()
            df = df.dropna()
            
            # Sort by player count (descending)
            df = df.sort_values(y_col, ascending=False)
            
            print(f"✅ Steam DataFrame created: {len(df)} rows")
            return df, ""
            
        except Exception as e:
            print(f"❌ Steam data error: {e}")
            return None, str(e)
    
    def _get_steamspy_data(self, method_name: str, metric_info: Dict) -> Tuple[Optional[pd.DataFrame], str]:
        """Get SteamSpy data and convert to DataFrame"""
        print(f"🎯 RETRIEVING STEAMSPY DATA")
        
        if not hasattr(self.apis, 'steamspy_api') or not self.apis.steamspy_api:
            return None, "SteamSpy API not available"
        
        try:
            # Get method arguments with defaults
            method_args = metric_info.get("method_args", {})
            
            # Call the API method
            method = getattr(self.apis.steamspy_api, method_name)
            raw_data = method(**method_args)
            
            if not raw_data:
                return None, "No SteamSpy data returned"
            
            # Convert to DataFrame
            df = pd.DataFrame(raw_data)
            
            # Ensure required columns exist
            data_format = metric_info["data_format"]
            x_col = data_format["x_column"]
            y_col = data_format["y_column"]
            
            if x_col not in df.columns or y_col not in df.columns:
                return None, f"Missing required columns: {x_col}, {y_col}"
            
            # Clean and format data
            df = df[[x_col, y_col]].copy()
            df = df.dropna()
            
            # Convert owners to millions for readability
            if y_col == "owners":
                df[y_col] = df[y_col] / 1_000_000
            
            # Sort by owners (descending)
            df = df.sort_values(y_col, ascending=False)
            
            print(f"✅ SteamSpy DataFrame created: {len(df)} rows")
            return df, ""
            
        except Exception as e:
            print(f"❌ SteamSpy data error: {e}")
            return None, str(e)
    
    def _get_rawg_data(self, method_name: str, metric_info: Dict) -> Tuple[Optional[pd.DataFrame], str]:
        """Get RAWG data and convert to DataFrame"""
        print(f"🎯 RETRIEVING RAWG DATA")
        
        if not hasattr(self.apis, 'rawg_api') or not self.apis.rawg_api.is_available:
            return None, "Unable to access RAWG API, please add an API key or check with your system admin."
        
        try:
            # Get method arguments with defaults
            method_args = metric_info.get("method_args", {})
            
            # Call the API method
            method = getattr(self.apis.rawg_api, method_name)
            raw_data = method(**method_args)
            
            if not raw_data:
                return None, "No RAWG data returned"
            
            # Convert to DataFrame
            df = pd.DataFrame(raw_data)
            
            # Ensure required columns exist
            data_format = metric_info["data_format"]
            x_col = data_format["x_column"]
            y_col = data_format["y_column"]
            
            if x_col not in df.columns or y_col not in df.columns:
                return None, f"Missing required columns: {x_col}, {y_col}"
            
            # Clean and format data
            df = df[[x_col, y_col]].copy()
            df = df.dropna()
            
            # Sort by rating (descending)
            df = df.sort_values(y_col, ascending=False)
            
            print(f"✅ RAWG DataFrame created: {len(df)} rows")
            return df, ""
            
        except Exception as e:
            print(f"❌ RAWG data error: {e}")
            return None, str(e)
    
    def _get_game_stats(self, game_name: str, metric_info: Dict) -> Tuple[Optional[pd.DataFrame], str]:
        """Get comprehensive stats for a specific game or similar games"""
        print(f"🎯 RETRIEVING GAME DATA FOR: {game_name}")
        
        # Check if this is a similar games query
        user_phrases = metric_info.get("user_phrases", [])
        is_similar_games = any("similar" in phrase or "other games" in phrase or "players" in phrase 
                              for phrase in user_phrases)
        
        if is_similar_games:
            return self._get_similar_games(game_name, metric_info)
        else:
            return self._get_individual_game_stats(game_name, metric_info)
    
    def _get_similar_games(self, game_name: str, metric_info: Dict) -> Tuple[Optional[pd.DataFrame], str]:
        """Get games similar to the specified game using Gamalytic API"""
        print(f"🎯 FINDING SIMILAR GAMES TO: {game_name}")
        
        # Try Gamalytic API for similar games (audience overlap data)
        if hasattr(self.apis, 'gamalytic_api') and self.apis.gamalytic_api.is_available:
            print(f"🔍 Using Gamalytic API for audience overlap games")
            try:
                result = self.apis.gamalytic_api.get_similar_games_by_players(game_name)
                if result.get("success") and result.get("data"):
                    game_data = result["data"]
                    games_data = []
                    
                    # First check for 'alsoPlayed' array (primary data source)
                    also_played = game_data.get("alsoPlayed", [])
                    if isinstance(also_played, list) and also_played:
                        print(f"✅ Found {len(also_played)} 'alsoPlayed' games")
                        for game in also_played[:10]:  # Limit to top 10
                            # Convert arrays to strings to avoid DataFrame length issues
                            genres_str = ", ".join(game.get("genres", [])) if game.get("genres") else ""
                            games_data.append({
                                "name": game.get("name", "Unknown Game"),
                                "steam_id": str(game.get("steamId", game.get("link", 0))),
                                "similarity_score": round(game.get("link", 0.5) * 10, 1),  # Use actual link score
                                "copies_sold": game.get("copiesSold", 0),
                                "revenue": game.get("revenue", 0),
                                "genres": genres_str,
                                "release_date": game.get("releaseDate", 0),
                                "price": game.get("price", 0)
                            })
                    
                    # If no 'alsoPlayed', check for 'audienceOverlap' array (secondary data source)
                    if not games_data:
                        audience_overlap = game_data.get("audienceOverlap", [])
                        if isinstance(audience_overlap, list) and audience_overlap:
                            print(f"✅ Found {len(audience_overlap)} 'audienceOverlap' games")
                            for game in audience_overlap[:10]:  # Limit to top 10
                                # Convert arrays to strings to avoid DataFrame length issues
                                genres_str = ", ".join(game.get("genres", [])) if game.get("genres") else ""
                                games_data.append({
                                    "name": game.get("name", "Unknown Game"),
                                    "steam_id": str(game.get("steamId", game.get("link", 0))),
                                    "similarity_score": round(game.get("link", 0.3) * 10, 1),  # Use actual link score
                                    "copies_sold": game.get("copiesSold", 0),
                                    "revenue": game.get("revenue", 0),
                                    "genres": genres_str,
                                    "release_date": game.get("releaseDate", 0),
                                    "price": game.get("price", 0)
                                })
                    
                    # If still no data, provide detailed debugging info
                    if not games_data:
                        print(f"🔍 No 'alsoPlayed' or 'audienceOverlap' found")
                        print(f"🎮 Available keys in response: {list(game_data.keys()) if isinstance(game_data, dict) else 'Not a dict'}")
                        if isinstance(game_data, dict):
                            for key, value in game_data.items():
                                if isinstance(value, list):
                                    print(f"  - {key}: {len(value)} items")
                                elif isinstance(value, dict):
                                    print(f"  - {key}: dict with keys {list(value.keys())}")
                                else:
                                    print(f"  - {key}: {type(value).__name__}")
                        return None, f"Game '{game_name}' found but no 'alsoPlayed' or 'audienceOverlap' data available"
                    
                    if games_data:
                        print(f"🔍 Creating DataFrame with {len(games_data)} rows")
                        print(f"🔍 Sample data: {games_data[0] if games_data else 'None'}")
                        
                        # Check for any list/array values that might cause issues
                        for i, game in enumerate(games_data):
                            for key, value in game.items():
                                if isinstance(value, (list, tuple)):
                                    print(f"⚠️  Row {i}, Key '{key}': Found array value {value}")
                                    games_data[i][key] = ", ".join(str(x) for x in value) if value else ""
                        
                        df = pd.DataFrame(games_data)
                        print(f"✅ Gamalytic also-played DataFrame created: {len(games_data)} rows")
                        print(f"📊 Columns: {list(df.columns)}")
                        return df, ""
                    else:
                        return None, "No similar games found in Gamalytic data"
                else:
                    error_msg = result.get("error", "Unknown error from Gamalytic API")
                    print(f"❌ Gamalytic API error: {error_msg}")
                    if "API key" in error_msg or "key required" in error_msg.lower():
                        return None, "Unable to access Gamalytic API, please add an API key or check with your system admin."
                    return None, f"Gamalytic API error: {error_msg}"
                    
            except Exception as e:
                print(f"❌ Error using Gamalytic API: {e}")
                print(f"🔍 Exception type: {type(e).__name__}")
                print(f"🔍 Exception details: {str(e)}")
                import traceback
                print(f"🔍 Full traceback: {traceback.format_exc()}")
                error_str = str(e)
                if "API key" in error_str or "key required" in error_str.lower():
                    return None, "Unable to access Gamalytic API, please add an API key or check with your system admin."
                return None, f"Error accessing Gamalytic API: {error_str}"
        else:
            return None, "Unable to access Gamalytic API, please add an API key or check with your system admin."
    
    def _get_individual_game_stats(self, game_name: str, metric_info: Dict) -> Tuple[Optional[pd.DataFrame], str]:
        """Get stats for an individual game"""
        print(f"🎯 RETRIEVING INDIVIDUAL GAME STATS FOR: {game_name}")
        
        stats = []
        
        # Try to get data from multiple APIs
        try:
            # Steam data
            if hasattr(self.apis, 'steam_api'):
                # This would require a method to search for specific games
                pass
            
            # RAWG data
            if hasattr(self.apis, 'rawg_api') and self.apis.rawg_api.is_available:
                game_details = self.apis.rawg_api.find_game_by_name(game_name)
                if game_details:
                    if 'rating' in game_details:
                        stats.append({"metric": "User Rating", "value": game_details['rating']})
                    if 'metacritic' in game_details:
                        stats.append({"metric": "Metacritic Score", "value": game_details['metacritic']})
                    if 'released' in game_details:
                        stats.append({"metric": "Release Year", "value": int(game_details['released'][:4])})
            
            if stats:
                df = pd.DataFrame(stats)
                print(f"✅ Game stats DataFrame created: {len(df)} rows")
                return df, ""
            else:
                return None, f"No stats found for {game_name}"
                
        except Exception as e:
            print(f"❌ Game stats error: {e}")
            return None, str(e)

    def _get_gamalytic_data(self, method_name: str, metric_info: Dict, game_name: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Get Gamalytic data and convert to DataFrame"""
        print(f"🎯 RETRIEVING GAMALYTIC DATA: {method_name} for {game_name}")
        
        if not hasattr(self.apis, 'gamalytic_api') or not self.apis.gamalytic_api.is_available:
            return None, "Unable to access Gamalytic API, please add an API key or check with your system admin."
        
        try:
            # Get method arguments with defaults
            method_args = metric_info.get("method_args", {})
            
            # Call the API method with game name
            method = getattr(self.apis.gamalytic_api, method_name)
            raw_data = method(game_name, **method_args)
            
            print(f"🎮 Raw Gamalytic data: {raw_data}")
            
            if not raw_data or not isinstance(raw_data, dict) or not raw_data.get("success"):
                error_msg = raw_data.get("error", "Failed to retrieve Gamalytic data") if raw_data else "Failed to retrieve Gamalytic data"
                if "API key" in error_msg or "key required" in error_msg.lower():
                    return None, "Unable to access Gamalytic API, please add an API key or check with your system admin."
                return None, error_msg
            
            # Handle complex response from get_similar_games_by_players
            if method_name == "get_similar_games_by_players":
                return self._process_similar_games_response(raw_data, metric_info)
            
            # Handle simple list response for other methods
            games_data = raw_data.get("data", [])
            if not games_data:
                return None, "No Gamalytic data returned"
            
            # Convert to DataFrame
            df = pd.DataFrame(games_data)
            
            # Ensure required columns exist
            data_format = metric_info["data_format"]
            x_col = data_format["x_column"]
            y_col = data_format["y_column"]
            
            if x_col not in df.columns or y_col not in df.columns:
                print(f"❌ Missing columns in Gamalytic data. Available: {list(df.columns)}")
                return None, f"Missing required columns: {x_col}, {y_col}"
            
            # Clean and format data
            df = df[[x_col, y_col]].copy()
            df = df.dropna()
            
            # Sort by the y column (descending by default)
            df = df.sort_values(y_col, ascending=False)
            
            print(f"✅ Gamalytic DataFrame created: {len(df)} rows")
            return df, ""
            
        except Exception as e:
            logger.error(f"Error retrieving Gamalytic data: {e}")
            print(f"❌ Error using Gamalytic API: {e}")
            error_str = str(e)
            if "API key" in error_str or "key required" in error_str.lower():
                return None, "Unable to access Gamalytic API, please add an API key or check with your system admin."
            return None, f"Error accessing Gamalytic API: {error_str}"
    
    def _process_similar_games_response(self, raw_data: Dict, metric_info: Dict) -> Tuple[Optional[pd.DataFrame], str]:
        """Process the complex response from get_similar_games_by_players API"""
        try:
            game_data = raw_data.get("data", {})
            games_data = []
            
            # First check for 'alsoPlayed' array (primary data source)
            also_played = game_data.get("alsoPlayed", [])
            if isinstance(also_played, list) and also_played:
                print(f"✅ Found {len(also_played)} 'alsoPlayed' games")
                for game in also_played[:10]:  # Limit to top 10
                    # Convert arrays to strings to avoid DataFrame length issues
                    genres_str = ", ".join(game.get("genres", [])) if game.get("genres") else ""
                    games_data.append({
                        "name": game.get("name", "Unknown Game"),
                        "steam_id": str(game.get("steamId", game.get("link", 0))),
                        "similarity_score": round(game.get("link", 0.5) * 10, 1),  # Use actual link score
                        "copies_sold": game.get("copiesSold", 0),
                        "revenue": game.get("revenue", 0),
                        "genres": genres_str,
                        "release_date": game.get("releaseDate", 0),
                        "price": game.get("price", 0)
                    })
            
            # If no 'alsoPlayed', check for 'audienceOverlap' array (secondary data source)
            if not games_data:
                audience_overlap = game_data.get("audienceOverlap", [])
                if isinstance(audience_overlap, list) and audience_overlap:
                    print(f"✅ Found {len(audience_overlap)} 'audienceOverlap' games")
                    for game in audience_overlap[:10]:  # Limit to top 10
                        # Convert arrays to strings to avoid DataFrame length issues
                        genres_str = ", ".join(game.get("genres", [])) if game.get("genres") else ""
                        games_data.append({
                            "name": game.get("name", "Unknown Game"),
                            "steam_id": str(game.get("steamId", game.get("link", 0))),
                            "similarity_score": round(game.get("link", 0.3) * 10, 1),  # Use actual link score
                            "copies_sold": game.get("copiesSold", 0),
                            "revenue": game.get("revenue", 0),
                            "genres": genres_str,
                            "release_date": game.get("releaseDate", 0),
                            "price": game.get("price", 0)
                        })
            
            if not games_data:
                print(f"🔍 No 'alsoPlayed' or 'audienceOverlap' found")
                print(f"🎮 Available keys in response: {list(game_data.keys()) if isinstance(game_data, dict) else 'Not a dict'}")
                return None, f"No similar games data found"
            
            print(f"🔍 Creating DataFrame with {len(games_data)} rows")
            print(f"🔍 Sample data: {games_data[0] if games_data else 'None'}")
            
            # Check for any list/array values that might cause issues
            for i, game in enumerate(games_data):
                for key, value in game.items():
                    if isinstance(value, (list, tuple)):
                        print(f"⚠️  Row {i}, Key '{key}': Found array value {value}")
                        games_data[i][key] = ", ".join(str(x) for x in value) if value else ""
            
            df = pd.DataFrame(games_data)
            print(f"✅ Gamalytic similar games DataFrame created: {len(games_data)} rows")
            print(f"📊 Columns: {list(df.columns)}")
            return df, ""
            
        except Exception as e:
            print(f"❌ Error processing similar games response: {e}")
            import traceback
            print(f"🔍 Full traceback: {traceback.format_exc()}")
            return None, f"Error processing similar games data: {str(e)}"
    
    def _get_simple_gamalytic_data(self, method_name: str, metric_info: Dict, game_name: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Simple Gamalytic handler that just returns game names - no complex DataFrame creation"""
        print(f"🎯 SIMPLE GAMALYTIC: {method_name} for {game_name}")
        
        if not hasattr(self.apis, 'gamalytic_api') or not self.apis.gamalytic_api.is_available:
            return None, "Gamalytic API key required"
        
        try:
            # Call the API method
            method = getattr(self.apis.gamalytic_api, method_name)
            result = method(game_name)
            
            if not result.get("success"):
                error_msg = result.get("error", "Unknown error")
                return None, error_msg
            
            # Get the game names list
            data = result.get("data", {})
            game_names = data.get("game_names", [])
            data_type = data.get("type", "unknown")
            
            if not game_names:
                return None, f"No game names found in {data_type} data"
            
            # Create a simple DataFrame with just the game names
            df_data = [{"game_name": name, "rank": i+1} for i, name in enumerate(game_names)]
            df = pd.DataFrame(df_data)
            
            print(f"✅ Simple Gamalytic result: {len(game_names)} games from {data_type}")
            print(f"📋 Games: {', '.join(game_names[:5])}{'...' if len(game_names) > 5 else ''}")
            
            return df, ""
            
        except Exception as e:
            print(f"❌ Simple Gamalytic error: {e}")
            return None, f"Error getting game data: {str(e)}"
