"""
Metric Registry - Defines available metrics from each API

This module maps user queries to specific data that can be retrieved from APIs
and defines how to extract and format that data.
"""

from typing import Dict, List, Any, Optional
import pandas as pd

class MetricRegistry:
    """Registry of all available metrics from gaming APIs"""
    
    def __init__(self):
        self.metrics = {
            # TWITCH METRICS
            "twitch_top_games": {
                "description": "Most popular games on Twitch by viewer count",
                "api": "twitch",
                "method": "get_top_games",
                "user_phrases": [
                    "twitch popular games", "twitch top games", "most watched twitch",
                    "popular on twitch", "trending twitch", "twitch viewer count",
                    "streaming games", "twitch rankings"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "name",
                    "y_column": "viewer_count",
                    "x_title": "Games",
                    "y_title": "Current Viewers",
                    "title_template": "Most Popular Games on Twitch"
                }
            },
            
            # STEAM METRICS
            "steam_top_games": {
                "description": "Top games on Steam by concurrent players",
                "api": "steam",
                "method": "get_top_games",
                "method_args": {"metric": "concurrent_players", "limit": 10},
                "user_phrases": [
                    "steam top games", "steam popular", "steam player count",
                    "most played steam", "steam concurrent", "steam rankings",
                    "top steam games", "steam charts"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "name",
                    "y_column": "current_players",
                    "x_title": "Games",
                    "y_title": "Current Players",
                    "title_template": "Top Games on Steam by Player Count"
                }
            },
            
            # STEAMSPY METRICS
            "steamspy_top_owned": {
                "description": "Most owned games on Steam",
                "api": "steamspy",
                "method": "get_top_games",
                "method_args": {"limit": 10},
                "user_phrases": [
                    "most owned games", "steamspy owners", "game ownership",
                    "steam ownership", "most owned steam", "popular ownership",
                    "ownership statistics", "steamspy statistics", "ownership data"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "name",
                    "y_column": "owners",
                    "x_title": "Games",
                    "y_title": "Estimated Owners (millions)",
                    "title_template": "Most Owned Games on Steam"
                }
            },
            
            # RAWG METRICS
            "rawg_top_rated": {
                "description": "Highest rated games from RAWG",
                "api": "rawg",
                "method": "search_games",
                "method_args": {"ordering": "-rating", "page_size": 10},
                "user_phrases": [
                    "best rated games", "highest rated", "top rated games",
                    "best games", "game ratings", "rawg ratings"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "name",
                    "y_column": "rating",
                    "x_title": "Games",
                    "y_title": "Rating (out of 5)",
                    "title_template": "Highest Rated Games"
                }
            },
            
            # GAME COMPARISON METRICS
            "game_stats": {
                "description": "Individual game statistics",
                "api": "multi",
                "user_phrases": [
                    "game stats", "game statistics", "tell me about",
                    "game details", "game info", "analyze game"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "metric",
                    "y_column": "value",
                    "x_title": "Metrics",
                    "y_title": "Values",
                    "title_template": "Game Statistics"
                }
            },
            
            # SIMPLE GAMALYTIC - WHAT OTHER GAMES DO PLAYERS PLAY
            "other_games_players_play": {
                "description": "What other games do players of this game also play",
                "api": "gamalytic_simple",  # Use special handler
                "method": "get_other_games_players_play",
                "user_phrases": [
                    "what other games", "other games players", "also play", "players also play",
                    "what games do players", "games players play", "what do players also play"
                ],
                "chart_type": "list",  # Just return a list, no chart
                "data_format": {
                    "response_type": "game_names_list",
                    "title_template": "Other games that {game_name} players also play"
                }
            },
            
            "gamalytic_game_analysis": {
                "description": "Comprehensive game analysis from Gamalytic",
                "api": "gamalytic",
                "method": "get_game_details",
                "user_phrases": [
                    "detailed analysis", "comprehensive analysis", "game analysis",
                    "full breakdown", "complete stats", "deep dive", "market analysis",
                    "detailed stats", "thorough analysis", "gamalytic data"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "metric",
                    "y_column": "value", 
                    "x_title": "Metrics",
                    "y_title": "Values",
                    "title_template": "Comprehensive Analysis: {game_name}"
                }
            },
            
            "gamalytic_playtime_distribution": {
                "description": "Player playtime distribution patterns",
                "api": "gamalytic",
                "method": "get_game_details", 
                "user_phrases": [
                    "playtime distribution", "playtime patterns", "how long do players",
                    "player engagement", "session length", "time spent playing",
                    "engagement metrics", "playtime breakdown", "player hours"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "time_range",
                    "y_column": "percentage",
                    "x_title": "Playtime Ranges",
                    "y_title": "Percentage of Players",
                    "title_template": "Playtime Distribution for {game_name}"
                }
            },
            
            # TWITCH ANALYTICS METRICS
            "twitch_extension_analytics": {
                "description": "Extension analytics report from Twitch Analytics API",
                "api": "twitch",
                "method": "get_extension_analytics",
                "user_phrases": [
                    "extension analytics", "extension performance", "extension metrics",
                    "extension insights", "extension engagement", "extension revenue",
                    "extension downloads", "extension usage", "extension stats"
                ],
                "chart_type": "line", 
                "data_format": {
                    "x_column": "date",
                    "y_column": "metric_value",
                    "x_title": "Date",
                    "y_title": "Metric Value",
                    "title_template": "Extension Analytics: {extension_name}"
                }
            },
            
            "twitch_game_analytics": {
                "description": "Game analytics report from Twitch Analytics API",
                "api": "twitch", 
                "method": "get_game_analytics",
                "user_phrases": [
                    "game analytics", "viewership analytics", "streaming analytics",
                    "twitch game metrics", "game viewership", "streaming metrics",
                    "broadcast analytics", "viewer analytics", "stream performance"
                ],
                "chart_type": "line",
                "data_format": {
                    "x_column": "date",
                    "y_column": "view_count",
                    "x_title": "Date", 
                    "y_title": "View Count",
                    "title_template": "Game Analytics: {game_name}"
                }
            },
            
            "twitch_bits_leaderboard": {
                "description": "Bits leaderboard for channel monetization analysis",
                "api": "twitch",
                "method": "get_bits_leaderboard", 
                "user_phrases": [
                    "bits leaderboard", "top contributors", "channel points", "bits analytics",
                    "monetization analytics", "top donors", "bits revenue", "supporter metrics"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "user_name",
                    "y_column": "score",
                    "x_title": "Contributors",
                    "y_title": "Bits Contributed",
                    "title_template": "Top Bits Contributors"
                }
            },
            
            "twitch_extension_transactions": {
                "description": "Extension transaction analytics for monetization tracking",
                "api": "twitch",
                "method": "get_extension_transactions",
                "user_phrases": [
                    "extension transactions", "extension revenue", "bits transactions",
                    "monetization tracking", "extension earnings", "transaction analytics",
                    "extension monetization", "bits revenue analytics"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "product_type",
                    "y_column": "amount", 
                    "x_title": "Product Type",
                    "y_title": "Revenue Amount",
                    "title_template": "Extension Transaction Analytics"
                }
            },
            
            # LEGACY SIMILAR GAMES (now redirects to Gamalytic)
            "similar_games": {
                "description": "Games similar to a specific game (redirects to Gamalytic)",
                "api": "gamalytic",
                "method": "get_game_details",
                "user_phrases": [
                    "similar games", "games like", "similar to", "recommendations",
                    "games similar to", "find similar", "like this game"
                ],
                "chart_type": "bar",
                "data_format": {
                    "x_column": "name",
                    "y_column": "copiesSold",
                    "x_title": "Similar Games",
                    "y_title": "Estimated Copies Sold",
                    "title_template": "Games Similar to {game_name}"
                }
            }
        }
    
    def find_metric(self, user_query: str) -> Optional[str]:
        """
        Find the best matching metric for a user query
        
        Args:
            user_query: User's natural language query
            
        Returns:
            Metric key if found, None otherwise
        """
        user_query_lower = user_query.lower()
        user_words = set(user_query_lower.split())
        
        # Score each metric based on phrase matches
        best_metric = None
        best_score = 0
        
        for metric_key, metric_info in self.metrics.items():
            score = 0
            for phrase in metric_info["user_phrases"]:
                phrase_lower = phrase.lower()
                
                # First check exact phrase match (highest score)
                if phrase_lower in user_query_lower:
                    score += len(phrase.split()) * 2  # Double score for exact match
                    continue
                
                # Then check if all words in phrase are in query (partial match)
                phrase_words = set(phrase_lower.split())
                if phrase_words.issubset(user_words):
                    score += len(phrase_words)  # Score based on number of matching words
            
            if score > best_score:
                best_score = score
                best_metric = metric_key
        
        return best_metric if best_score > 0 else None
    
    def get_metric_info(self, metric_key: str) -> Optional[Dict]:
        """Get information about a specific metric"""
        return self.metrics.get(metric_key)
    
    def list_all_metrics(self) -> Dict[str, str]:
        """Get a list of all available metrics with descriptions"""
        return {key: info["description"] for key, info in self.metrics.items()}

    def extract_game_name(self, user_query: str) -> Optional[str]:
        """
        Extract game name from user queries for game-specific analysis
        
        Args:
            user_query: User's query
            
        Returns:
            Game name if detected, None otherwise
        """
        query_lower = user_query.lower()
        
        # Pattern 1: "What other games do players of [GAME] play"
        if "players of" in query_lower:
            parts = query_lower.split("players of")
            if len(parts) > 1:
                game_part = parts[1].strip()
                # Remove common words at the end
                game_part = game_part.replace(" play", "").replace(" also play", "").replace("?", "").strip()
                if game_part:
                    return game_part.title()
        
        # Pattern 2: "Similar games to [GAME]"
        if "similar" in query_lower and "to" in query_lower:
            parts = query_lower.split(" to ")
            if len(parts) > 1:
                game_part = parts[1].strip()
                game_part = game_part.replace("?", "").strip()
                if game_part:
                    return game_part.title()
        
        # Pattern 3: "Games like [GAME]"
        if "games like" in query_lower:
            parts = query_lower.split("games like")
            if len(parts) > 1:
                game_part = parts[1].strip()
                game_part = game_part.replace("?", "").strip()
                if game_part:
                    return game_part.title()
        
        # Pattern 4: "Tell me about [GAME]", "Statistics for [GAME]"
        game_indicators = [
            "tell me about", "stats for", "statistics for", "analyze",
            "information about", "details about", "data on", "data about"
        ]
        
        for indicator in game_indicators:
            if indicator in query_lower:
                # Extract text after the indicator
                parts = query_lower.split(indicator)
                if len(parts) > 1:
                    game_name = parts[1].strip()
                    # Clean up common words
                    game_name = game_name.replace("the game", "").replace("game", "").replace("?", "").strip()
                    if game_name:
                        return game_name.title()
        
        # Pattern 5: Look for known game titles in the query
        known_games = [
            "counter-strike", "counter strike", "cs2", "cs:go", "csgo",
            "total war attila", "total war", "attila",
            "league of legends", "lol", "dota 2", "dota",
            "world of warcraft", "wow", "valorant", "apex legends",
            "fortnite", "call of duty", "cod", "overwatch",
            "minecraft", "grand theft auto", "gta", "the witcher",
            "cyberpunk", "red dead redemption", "elden ring",
            "steam deck", "battlefield", "fifa", "madden",
            "rocket league", "among us", "fall guys", "pubg",
            "destiny", "warframe", "path of exile", "diablo",
            "civilization", "crusader kings", "europa universalis",
            "age of empires", "starcraft", "hearthstone"
        ]
        
        for game in known_games:
            if game in query_lower:
                # Return the proper capitalization
                if game == "counter-strike" or game == "counter strike":
                    return "Counter-Strike"
                elif game == "cs2":
                    return "Counter-Strike 2"
                elif game == "cs:go" or game == "csgo":
                    return "Counter-Strike: Global Offensive"
                elif game == "total war attila":
                    return "Total War: Attila"
                elif game == "total war":
                    return "Total War"
                elif game == "attila":
                    return "Total War: Attila"
                elif game == "league of legends" or game == "lol":
                    return "League of Legends"
                elif game == "dota 2" or game == "dota":
                    return "Dota 2"
                elif game == "valorant":
                    return "VALORANT"
                elif game == "apex legends":
                    return "Apex Legends"
                elif game == "call of duty" or game == "cod":
                    return "Call of Duty"
                elif game == "grand theft auto" or game == "gta":
                    return "Grand Theft Auto"
                elif game == "the witcher":
                    return "The Witcher 3"
                elif game == "cyberpunk":
                    return "Cyberpunk 2077"
                elif game == "red dead redemption":
                    return "Red Dead Redemption 2"
                elif game == "elden ring":
                    return "Elden Ring"
                elif game == "rocket league":
                    return "Rocket League"
                elif game == "among us":
                    return "Among Us"
                elif game == "fall guys":
                    return "Fall Guys"
                elif game == "pubg":
                    return "PLAYERUNKNOWN'S BATTLEGROUNDS"
                elif game == "path of exile":
                    return "Path of Exile"
                elif game == "age of empires":
                    return "Age of Empires"
                elif game == "crusader kings":
                    return "Crusader Kings III"
                elif game == "europa universalis":
                    return "Europa Universalis IV"
                else:
                    return game.title()
        
        return None
