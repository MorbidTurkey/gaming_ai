"""
Intelligent Gaming Agent - Uses AI to understand intent and dynamically route queries

This agent             "steamspy": {
                "api": self.apis.steamspy_api,
                "capabilities": ["ownership", "owners", "most_owned", "genre_analysis_fallback", "genres_fallback"],
                "methods": {
                    "ownership": "get_app_details",
                    "owners": "get_app_details",
                    "most_owned": "get_top_owned_games",
                    "genre_analysis_fallback": "analyze_genre_popularity",
                    "genres_fallback": "analyze_genre_popularity"
                }
            }l language understanding to:
1. Parse user intent from queries
2. Dynamically select appropriate APIs and methods
3. Handle flexible query variations without predefined patterns
"""

import re
from typing import Tuple, Optional, Dict, Any, List
import pandas as pd
from utils.api_usage_tracker import APIUsageTracker

class IntelligentGamingAgent:
    """AI-powered gaming agent that understands intent"""
    
    def __init__(self, apis):
        """
        Initialize with API instances
        
        Args:
            apis: Object containing API instances (steam_api, twitch_api, etc.)
        """
        self.apis = apis
        self.usage_tracker = APIUsageTracker()  # Add usage tracking
        
        # Vibrant color palette for charts
        self.color_palette = [
            '#FF6B6B',  # Vibrant Red
            '#4ECDC4',  # Vibrant Teal  
            '#45B7D1',  # Vibrant Blue
            '#FFA07A',  # Light Salmon
            '#98D8C8',  # Mint Green
            '#F7DC6F',  # Light Gold
            '#BB8FCE',  # Light Purple
            '#85C1E9',  # Light Blue
            '#F8C471',  # Light Orange
            '#82E0AA',  # Light Green
            '#F1948A',  # Light Pink
            '#AED6F1'   # Powder Blue
        ]
        
        # Color theme palettes
        self.color_themes = {
            "vibrant": [
                '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8C471', '#82E0AA'
            ],
            "ocean": [
                '#006994', '#0582CA', '#00A6FB', '#0CB0DA', '#40E0D0',
                '#48CAE4', '#51CAF0', '#61A5C2', '#89C2D9', '#A2D2FF'
            ],
            "sunset": [
                '#FF6B35', '#F7931E', '#FFD23F', '#06FFA5', '#118AB2',
                '#EE6C4D', '#F38BA8', '#A663CC', '#4CC9F0', '#7209B7'
            ],
            "pastel": [
                '#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF',
                '#E6E6FA', '#F0E68C', '#DDA0DD', '#98FB98', '#F5DEB3'
            ],
            "fire": [
                '#FF0000', '#FF4500', '#FF6347', '#FF7F50', '#FFA500',
                '#FFD700', '#FFFF00', '#ADFF2F', '#00FF00', '#00FA9A'
            ],
            "nature": [
                '#228B22', '#32CD32', '#90EE90', '#98FB98', '#00FA9A',
                '#40E0D0', '#48D1CC', '#87CEEB', '#87CEFA', '#B0E0E6'
            ]
        }
        
        self.current_theme = "vibrant"
        
        # Available data sources and their capabilities
        self.data_sources = {
            "steam": {
                "api": self.apis.steam_api,
                "capabilities": ["top_games", "player_count", "concurrent_players", "rankings"],
                "methods": {
                    "top_games": "get_top_games",
                    "player_count": "get_top_games", 
                    "concurrent_players": "get_top_games",
                    "rankings": "get_top_games"
                }
            },
            "twitch": {
                "api": self.apis.twitch_api,
                "capabilities": ["top_games", "viewer_count", "streaming", "popular"],
                "methods": {
                    "top_games": "get_top_games",
                    "viewer_count": "get_top_games",
                    "streaming": "get_top_games",
                    "popular": "get_top_games"
                }
            },
            "gamalytic": {
                "api": self.apis.gamalytic_api,
                "capabilities": ["also_played", "genre_analysis", "genres", "genre_stats"],
                "methods": {
                    "also_played": "get_other_games_players_play",
                    "genre_analysis": "get_genre_stats",
                    "genres": "get_genre_stats",
                    "genre_stats": "get_genre_stats"
                }
            },
            "steamspy": {
                "api": self.apis.steamspy_api,
                "capabilities": ["ownership", "owners", "most_owned", "genre_analysis", "genres"],
                "methods": {
                    "ownership": "get_top_owned_games",
                    "owners": "get_top_owned_games",
                    "most_owned": "get_top_owned_games",
                    "genre_analysis": "analyze_genre_popularity",
                    "genres": "analyze_genre_popularity"
                }
            }
        }
    
    def set_color_theme(self, theme_name: str):
        """Set the color theme for charts"""
        if theme_name in self.color_themes:
            self.current_theme = theme_name
            self.color_palette = self.color_themes[theme_name]
            print(f"🎨 Color theme changed to: {theme_name}")
        else:
            print(f"❌ Unknown color theme: {theme_name}")
    
    def respond(self, user_query: str) -> Tuple[str, Optional[Dict]]:
        """
        Process user query using AI interpretation
        
        Args:
            user_query: User's natural language query
            
        Returns:
            Tuple of (text_response, visualization_dict)
        """
        print(f"🧠 INTELLIGENT AGENT PROCESSING: {user_query}")
        
        # Step 1: Parse intent from the query
        intent = self._parse_intent(user_query)
        
        if not intent:
            return self._handle_unknown_query(user_query)
        
        print(f"🎯 Parsed intent: {intent}")
        
        # Step 2: Execute the intent
        try:
            result = self._execute_intent(intent, user_query)
            return result
        except Exception as e:
            print(f"❌ Error executing intent: {e}")
            return f"Sorry, I encountered an error processing your request: {str(e)}", None
    
    def _parse_intent(self, query: str) -> Optional[Dict]:
        """
        Parse user intent from natural language query
        
        Returns:
            Dict with platform, data_type, action, game_name (if specific game query)
        """
        query_lower = query.lower()
        
        # Extract platform
        platform = None
        if any(word in query_lower for word in ["steam"]):
            platform = "steam"
        elif any(word in query_lower for word in ["twitch", "streaming", "streamer"]):
            platform = "twitch"
        elif any(word in query_lower for word in ["gamalytic", "similar", "also play", "audience overlap"]):
            platform = "gamalytic"
        elif any(word in query_lower for word in ["steamspy", "ownership", "owned"]):
            platform = "steamspy"
        
        # Extract data type and action
        data_type = None
        action = None
        
        # Genre analysis queries
        if any(word in query_lower for word in ["genre", "genres", "category", "categories", "type", "types"]):
            data_type = "genre_analysis"
            action = "genres"
            platform = platform or "gamalytic"  # Default to gamalytic for genre analysis
        
        # Game rankings/lists
        elif any(word in query_lower for word in ["top", "best", "popular", "most", "ranking", "chart"]):
            data_type = "rankings"
            if any(word in query_lower for word in ["games", "titles"]):
                action = "top_games"
            elif any(word in query_lower for word in ["player", "concurrent", "playing"]):
                action = "player_count" 
            elif any(word in query_lower for word in ["viewer", "watching", "streaming"]):
                action = "viewer_count"
            elif any(word in query_lower for word in ["owned", "ownership"]):
                action = "ownership"
        
        # Similar/related games
        elif any(phrase in query_lower for phrase in ["similar", "also play", "other games", "related", "like"]):
            data_type = "also_played"
            action = "also_played"
            platform = platform or "gamalytic"  # Default to gamalytic for also_played games
        
        # Specific game queries - extract game name
        game_name = None
        game_patterns = [
            # "What other games do [GameName] players play?"
            r"what (?:other )?games? do ([a-zA-Z0-9\s:'-]+?) players? (?:also )?play",
            # "[GameName] players also play" or "players of [GameName]"
            r"([a-zA-Z0-9\s:'-]+?) players? (?:also )?play",
            # "games like [GameName]" or "similar to [GameName]"
            r"(?:games? (?:like|similar to)|similar to) ([a-zA-Z0-9\s:'-]+?)(?:\s|$)",
            # "for [GameName]" or "about [GameName]"
            r"(?:for|about|of) ([a-zA-Z0-9\s:'-]+?)(?:\s+players?|\s+also|\s*$)"
        ]
        
        for pattern in game_patterns:
            match = re.search(pattern, query_lower)
            if match:
                potential_game = match.group(1).strip()
                # Filter out common non-game words and phrases
                excluded_words = ["steam", "twitch", "what", "which", "the", "most", "top", "popular", "other", "games", "do"]
                if potential_game not in excluded_words and len(potential_game) > 2:
                    game_name = potential_game
                    break
        
        # Auto-detect platform if not specified but we have a game
        if game_name and not platform:
            # Default to steam for game queries unless it's clearly an also_played query
            if data_type == "also_played":
                platform = "gamalytic"
            else:
                platform = "steam"
        
        # Default to steam for general game queries
        if not platform and any(word in query_lower for word in ["games", "gaming"]):
            platform = "steam"
        
        # Extract requested count (top 5, top 10, etc.)
        count = 10  # default
        count_match = re.search(r'top\s+(\d+)', query_lower)
        if count_match:
            count = int(count_match.group(1))
            print(f"🔢 Extracted count: {count} from query")
        
        if not platform or not action:
            return None
        
        return {
            "platform": platform,
            "data_type": data_type,
            "action": action,
            "game_name": game_name,
            "count": count,
            "original_query": query
        }
    
    def _execute_intent(self, intent: Dict, original_query: str) -> Tuple[str, Optional[Dict]]:
        """Execute the parsed intent"""
        
        platform = intent["platform"]
        action = intent["action"]
        game_name = intent.get("game_name")
        count = intent.get("count", 10)  # Get requested count, default to 10
        
        # Get the appropriate API and method
        if platform not in self.data_sources:
            return f"Sorry, I don't have access to {platform} data.", None
        
        api_info = self.data_sources[platform]
        api = api_info["api"]
        
        if action not in api_info["capabilities"]:
            return f"Sorry, I can't get {action} data from {platform}.", None
        
        method_name = api_info["methods"][action]
        method = getattr(api, method_name)
        
        # Execute the method with appropriate parameters
        try:
            print(f"🔧 EXECUTING: platform={platform}, action={action}, method_name={method_name}")
            
            # Special handling for genre analysis
            if action == "genres":
                if platform == "gamalytic":
                    print(f"🎭 Gamalytic genre analysis query")
                    result = method()  # Call get_genre_stats()
                    
                    # If Gamalytic fails, fallback to SteamSpy
                    if not result.get("success") and "steamspy" in self.data_sources:
                        print(f"⚠️ Gamalytic failed, falling back to SteamSpy")
                        steamspy_api = self.data_sources["steamspy"]["api"]
                        result = steamspy_api.analyze_genre_popularity()
                        if isinstance(result, list):
                            # Convert to expected format
                            result = {"success": True, "data": result}
                        
                elif platform == "steamspy":
                    print(f"🎭 SteamSpy genre analysis query")
                    result = method()  # Call analyze_genre_popularity()
                    if isinstance(result, list):
                        # Convert to expected format for consistency
                        result = {"success": True, "data": result}
            elif game_name:
                # Game-specific query
                print(f"🎮 Game-specific query for: {game_name}")
                if platform == "gamalytic":
                    result = method(game_name)
                else:
                    # For other APIs, get general data and filter
                    if platform == "steam":
                        print(f"🔧 Calling Steam API: {method_name}(metric='concurrent_players', limit={count})")
                        result = method(metric="concurrent_players", limit=count)
                    elif platform == "twitch":
                        print(f"🔧 Calling Twitch API: {method_name}(limit={count})")
                        result = method(limit=count)
                    else:
                        print(f"🔧 Calling {platform} API: {method_name}()")
                        result = method()
            else:
                # General query
                print(f"🔧 General query for {platform}")
                if platform == "steam":
                    print(f"🔧 Calling Steam API: {method_name}(metric='concurrent_players', limit={count})")
                    result = method(metric="concurrent_players", limit=count)
                elif platform == "twitch":
                    print(f"🔧 Calling Twitch API: {method_name}(limit={count})")
                    result = method(limit=count)
                else:
                    print(f"🔧 Calling {platform} API: {method_name}()")
                    result = method()
            
            # Track API usage
            print(f"📊 Tracking API usage for: {platform}")
            self.usage_tracker.track_api_call(platform, 1)
            
            print(f"✅ API call successful, result type: {type(result)}")
            print(f"📊 API result preview: {str(result)[:200]}...")
            
            return self._format_response(result, intent, original_query)
            
        except Exception as e:
            print(f"❌ API call failed: {e}")
            return f"Sorry, I couldn't get {action} data from {platform}: {str(e)}", None
    
    def _format_response(self, data: Dict, intent: Dict, original_query: str) -> Tuple[str, Optional[Dict]]:
        """Format the API response into a user-friendly response"""
        
        if not data or ("success" in data and not data["success"]):
            error_msg = data.get("error", "Unknown error") if data else "No data returned"
            return f"Sorry, I couldn't get the requested data: {error_msg}", None
        
        platform = intent["platform"]
        action = intent["action"]
        game_name = intent.get("game_name")
        
        # Handle different response formats
        
        # Genre analysis (check this FIRST before general list handling)
        if action == "genres":
            if platform == "gamalytic" and "data" in data:
                # Gamalytic genre stats response
                genre_stats = data["data"]
                
                if not genre_stats:
                    return "No genre statistics found.", None
                
                # Format response text focusing on real player metrics from Gamalytic
                response = "📊 **Most Popular Game Genres Analysis**\n\n"
                response += "Based on real player activity and market data:\n\n"
                
                # Gamalytic should return genre-grouped statistics
                for i, (genre_name, stats) in enumerate(genre_stats.items() if isinstance(genre_stats, dict) else [], 1):
                    if i > 10:  # Limit to top 10 genres
                        break
                        
                    response += f"{i}. **{genre_name}**\n"
                    
                    # Show meaningful metrics from Gamalytic
                    players = stats.get("players", 0)
                    copies_sold = stats.get("copiesSold", 0)
                    revenue = stats.get("revenue", 0)
                    avg_playtime = stats.get("avgPlaytime", 0)
                    total_games = stats.get("totalGames", 0)
                    
                    if players > 0:
                        response += f"   • Active Players: {players:,}\n"
                    if copies_sold > 0:
                        response += f"   • Total Copies Sold: {copies_sold:,}\n"
                    if revenue > 0:
                        response += f"   • Revenue: ${revenue:,.0f}\n"
                    if avg_playtime > 0:
                        response += f"   • Average Playtime: {avg_playtime:.1f} hours\n"
                    if total_games > 0:
                        response += f"   • Games in Genre: {total_games:,}\n"
                    
                    response += "\n"
                
                # Create DataFrame for visualization
                df_data = []
                for genre_name, stats in (genre_stats.items() if isinstance(genre_stats, dict) else [])[:8]:
                    df_data.append({
                        "genre": genre_name,
                        "total_players": stats.get("players", 0),
                        "total_games": stats.get("totalGames", 0),
                        "avg_players": stats.get("players", 0) / max(stats.get("totalGames", 1), 1)
                    })
                
                df = pd.DataFrame(df_data)
                viz_config = self._create_genre_visualization(df)
                return response, viz_config
                
            elif isinstance(data.get("data"), list):
                # SteamSpy genre analysis response (fallback) - data wrapped in success format
                genre_data = data["data"]
                
                if not genre_data:
                    return "No genre data found.", None
                
                # Format response text focusing on popularity metrics
                response = "📊 **Most Popular Game Genres Analysis**\n\n"
                response += "Based on ownership and player activity from top games:\n\n"
                
                for i, genre in enumerate(genre_data[:10], 1):
                    genre_name = genre.get("genre", "Unknown")
                    primary_activity = genre.get("primary_activity", 0)
                    total_ccu = genre.get("total_ccu", 0)
                    total_players_2weeks = genre.get("total_players_2weeks", 0)
                    total_games = genre.get("total_games", 0)
                    estimated_owners = genre.get("estimated_total_owners", 0)
                    avg_activity = genre.get("avg_players_per_game", 0)
                    
                    response += f"{i}. **{genre_name}**\n"
                    
                    # Show meaningful metrics based on what's available
                    if estimated_owners > 0:
                        response += f"   • Total Estimated Ownership: {estimated_owners:,}\n"
                    if total_ccu > 0:
                        response += f"   • Peak Concurrent Users: {total_ccu:,}\n"
                    if total_players_2weeks > 0:
                        response += f"   • Active Players (2 weeks): {total_players_2weeks:,}\n"
                    if primary_activity > 0 and primary_activity != estimated_owners:
                        response += f"   • Activity Score: {primary_activity:,}\n"
                        
                    response += f"   • Games in Genre: {total_games:,}\n"
                    
                    if avg_activity > 0:
                        if estimated_owners > 0:
                            response += f"   • Avg Ownership per Game: {avg_activity:,.0f}\n"
                        else:
                            response += f"   • Avg Activity per Game: {avg_activity:,.0f}\n"
                    
                    # Add top games in this genre
                    top_games = genre.get("top_games", [])[:3]
                    if top_games:
                        response += "   • Top Games: "
                        top_names = [game.get("name", "Unknown") for game in top_games]
                        response += ", ".join(top_names) + "\n"
                    response += "\n"
                
                # Create DataFrame for visualization
                df_data = []
                for genre in genre_data[:8]:  # Show top 8 genres in chart
                    df_data.append({
                        "genre": genre.get("genre", "Unknown"),
                        "total_players": genre.get("primary_activity", 0),  # Use primary activity metric
                        "total_games": genre.get("total_games", 0),
                        "avg_players": genre.get("avg_players_per_game", 0)
                    })
                
                df = pd.DataFrame(df_data)
                viz_config = self._create_genre_visualization(df)
                return response, viz_config
        
        elif platform == "gamalytic" and "data" in data:
            # Gamalytic responses
            game_data = data["data"]
            if "game_names" in game_data:
                games = game_data["game_names"]
                game_type = game_data.get("type", "related")
                
                response = f"Here are games that {game_name} players also play:\n\n"
                for i, game in enumerate(games[:10], 1):
                    response += f"{i}. {game}\n"
                
                # Create simple list visualization (no chart needed)
                return response, None
        
        elif isinstance(data, list) and data:
            # Direct list responses (like Steam API)
            games_data = data
            
            # Create DataFrame for visualization
            df = pd.DataFrame(games_data)
            
            # Format response text
            response = f"Here are the top {platform.title()} games:\n\n"
            for i, game in enumerate(games_data[:10], 1):
                name = game.get("name", "Unknown")
                if platform == "steam":
                    count = game.get("current_players", game.get("player_count", 0))
                    response += f"{i}. {name} - {count:,} players\n"
                elif platform == "twitch":
                    count = game.get("viewer_count", 0)
                    response += f"{i}. {name} - {count:,} viewers\n"
                else:
                    response += f"{i}. {name}\n"
            
            # Create visualization
            viz_config = self._create_visualization_config(df, platform, action)
            return response, viz_config

        elif "success" in data and data["success"] and "data" in data:
            # Standard API responses with success field
            games_data = data["data"]
            
            if isinstance(games_data, list) and games_data:
                # Create DataFrame for visualization
                df = pd.DataFrame(games_data)
                
                # Format response text
                response = f"Here are the top {platform.title()} games:\n\n"
                for i, game in enumerate(games_data[:10], 1):
                    name = game.get("name", "Unknown")
                    if platform == "steam":
                        count = game.get("current_players", game.get("player_count", 0))
                        response += f"{i}. {name} - {count:,} players\n"
                    elif platform == "twitch":
                        count = game.get("viewer_count", 0)
                        response += f"{i}. {name} - {count:,} viewers\n"
                    else:
                        response += f"{i}. {name}\n"
                
                # Create visualization
                viz_config = self._create_visualization_config(df, platform, action)
                return response, viz_config
                
        # Fallback for other response formats
        return f"I found some data but couldn't format it properly. Raw response: {str(data)[:200]}...", None
    
    def _create_visualization_config(self, df: pd.DataFrame, platform: str, action: str) -> Dict:
        """Create visualization configuration"""
        
        # Import plotly here to avoid circular imports
        import plotly.graph_objects as go
        
        # Determine columns based on platform
        if platform == "steam":
            x_col = "name"
            y_col = "current_players" if "current_players" in df.columns else "player_count"
            y_title = "Current Players"
        elif platform == "twitch":
            x_col = "name"
            y_col = "viewer_count"
            y_title = "Viewers"
        else:
            return None
        
        # Create the actual Plotly figure
        fig = go.Figure()
        
        # Generate colors for each bar
        colors = []
        current_palette = self.color_themes.get(self.current_theme, self.color_palette)
        for i in range(min(10, len(df))):
            colors.append(current_palette[i % len(current_palette)])
        
        # Add bar chart with vibrant colors
        fig.add_trace(go.Bar(
            x=df[x_col][:10],  # Top 10 only
            y=df[y_col][:10],
            name=y_title,
            marker_color=colors,
            marker_line_color='rgba(255, 255, 255, 0.8)',
            marker_line_width=1.5,
            text=df[y_col][:10],  # Add value labels
            textposition='auto',
            textfont=dict(color='white', size=10)
        ))
        
        # Update layout for dark theme
        fig.update_layout(
            title=f"Top {platform.title()} Games",
            xaxis_title="Games",
            yaxis_title=y_title,
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#2d2d2d',
            font=dict(color='#ffffff'),
            xaxis=dict(tickangle=45),
            height=500
        )
        
        return fig.to_dict()
    
    def _create_genre_visualization(self, df: pd.DataFrame) -> Dict:
        """Create visualization for genre analysis"""
        
        import plotly.graph_objects as go
        
        # Create the actual Plotly figure
        fig = go.Figure()
        
        # Generate colors for each bar
        colors = []
        current_palette = self.color_themes.get(self.current_theme, self.color_palette)
        for i in range(len(df)):
            colors.append(current_palette[i % len(current_palette)])
        
        # Determine what metric we're showing based on the data
        max_players = df['total_players'].max() if len(df) > 0 else 0
        
        # Choose appropriate label based on data magnitude
        if max_players > 1000000:
            y_title = "Total Ownership/Activity"
            text_values = [f"{val:,.0f}" for val in df['total_players']]
        elif max_players > 1000:
            y_title = "Activity Score"
            text_values = [f"{val:,.0f}" for val in df['total_players']]
        else:
            y_title = "Popularity Score"
            text_values = [f"{val:.0f}" for val in df['total_players']]
        
        # Add bar chart for primary activity metric
        fig.add_trace(go.Bar(
            x=df['genre'],
            y=df['total_players'],
            name='Genre Popularity',
            marker_color=colors,
            marker_line_color='rgba(255, 255, 255, 0.8)',
            marker_line_width=1.5,
            text=text_values,
            textposition='auto',
            textfont=dict(color='white', size=10),
            hovertemplate='<b>%{x}</b><br>' + y_title + ': %{y:,.0f}<br>Games: %{customdata}<extra></extra>',
            customdata=df['total_games']
        ))
        
        # Update layout for dark theme
        fig.update_layout(
            title="Most Popular Game Genres by Player Activity & Ownership",
            xaxis_title="Game Genres",
            yaxis_title=y_title,
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#2d2d2d',
            font=dict(color='#ffffff'),
            xaxis=dict(tickangle=45),
            height=500,
            showlegend=False
        )
        
        return fig.to_dict()
    
    def _handle_unknown_query(self, query: str) -> Tuple[str, None]:
        """Handle queries that couldn't be parsed"""
        
        # Provide helpful suggestions
        suggestions = [
            "• 'What are the top games on Steam?' - for Steam player rankings",
            "• 'Most popular games on Twitch' - for Twitch viewer counts", 
            "• 'What other games do Elden Ring players also play?' - for games players also play",
            "• 'Most owned games on Steam' - for ownership statistics"
        ]
        
        response = "I couldn't understand that query. Here are some things you can ask:\n\n"
        response += "\n".join(suggestions)
        
        return response, None
    
    def get_api_usage_summary(self):
        """Get API usage summary for dashboard gauges"""
        try:
            return {
                "success": True,
                "data": self.usage_tracker.get_usage_summary()
            }
        except Exception as e:
            print(f"❌ Error getting API usage summary: {e}")
            return {
                "success": False,
                "error": str(e)
            }
