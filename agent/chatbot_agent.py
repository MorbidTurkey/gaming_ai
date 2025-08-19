"""
Gaming AI Chatbot Agent

This module contains the main agent class that handles:
- Natural language processing with OpenAI
- API calls to gaming data sources
- Visualization generation
- Conversation memory management
"""

import json
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

import openai
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

from apis.steam_api import SteamAPI
from apis.steamspy_api import SteamSpyAPI
from apis.gamalytic_api import GamalyticAPI
from apis.rawg_api import RAWGAPI
from apis.twitch_api import TwitchAPI
from utils.visualization import VisualizationGenerator
from utils.api_usage_tracker import APIUsageTracker

# Load environment variables
load_dotenv()

@dataclass
class ConversationTurn:
    """Represents a single turn in the conversation"""
    timestamp: datetime
    user_message: str
    agent_response: str
    function_calls: List[str]
    visualization: Optional[Dict] = None

class GamingChatbotAgent:
    """
    Main chatbot agent for gaming industry questions and analysis
    """
    
    def __init__(self):
        """Initialize the agent with API clients and conversation memory"""
        # Initialize OpenAI
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
        self.client = openai.OpenAI(api_key=api_key)
        
        # Initialize API clients
        self.steam_api = SteamAPI()
        self.steamspy_api = SteamSpyAPI()
        self.gamalytic_api = GamalyticAPI()
        self.rawg_api = RAWGAPI()
        self.twitch_api = TwitchAPI()
        
        # Initialize visualization generator
        self.viz_generator = VisualizationGenerator()
        
        # Initialize API usage tracker
        self.usage_tracker = APIUsageTracker()
        
        # Conversation memory
        self.conversation_history: List[ConversationTurn] = []
        
        # Define available functions for OpenAI function calling
        self.available_functions = {
            "get_steam_top_games": self.get_steam_top_games,
            "get_game_details": self.get_game_details,
            "get_player_count_data": self.get_player_count_data,
            "generate_visualization": self.generate_visualization,
            "search_games": self.search_games,
            "get_price_history": self.get_price_history,
            "compare_games": self.compare_games,
            "get_comprehensive_game_analysis": self.get_comprehensive_game_analysis
        }
        
        # Add Gamalytic functions only if API key is available
        if self.gamalytic_api.is_available:
            self.available_functions["get_genre_analysis"] = self.get_genre_analysis
            self.available_functions["get_market_analysis"] = self.get_market_analysis
            self.available_functions["get_trends_data"] = self.get_trends_data
            self.available_functions["get_game_audience_overlap"] = self.get_game_audience_overlap
            self.available_functions["get_similar_games_by_players"] = self.get_similar_games_by_players
            print("✅ Gamalytic functions enabled")
        else:
            print("ℹ️  Gamalytic functions disabled (no API key)")
        
        # Add RAWG functions only if API key is available
        if self.rawg_api.is_available:
            self.available_functions["search_rawg_games"] = self.search_rawg_games
            self.available_functions["get_game_metadata"] = self.get_game_metadata
            self.available_functions["get_game_reviews"] = self.get_game_reviews
            print("✅ RAWG functions enabled")
        else:
            print("ℹ️  RAWG functions disabled (no API key)")
        
        # Add Twitch functions only if API keys are available
        if self.twitch_api.is_available:
            self.available_functions["get_twitch_top_games"] = self.get_twitch_top_games
            self.available_functions["get_game_streams"] = self.get_game_streams
            self.available_functions["get_streaming_stats"] = self.get_streaming_stats
            print("✅ Twitch functions enabled")
        else:
            print("ℹ️  Twitch functions disabled (no API keys)")
        
        # Add usage tracking functions
        self.available_functions["get_api_usage_summary"] = self.get_api_usage_summary
        self.available_functions["get_usage_gauges"] = self.get_usage_gauges
        self.available_functions["reset_monthly_usage"] = self.reset_monthly_usage
    
    def set_color_theme(self, theme_name: str):
        """Set the color theme for chart visualizations"""
        if hasattr(self, 'viz_generator'):
            self.viz_generator.set_color_theme(theme_name)
            print(f"🎨 Chatbot visualization theme set to: {theme_name}")
        else:
            print("❌ Visualization generator not initialized")
        
        # Function definitions for OpenAI (using tools format)
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_steam_top_games",
                    "description": "Get top games from Steam by various metrics",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "metric": {
                                "type": "string",
                                "enum": ["concurrent_players", "revenue", "new_releases", "top_sellers"],
                                "description": "The metric to sort games by"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of games to return (default 10)",
                                "default": 10
                            }
                        },
                        "required": ["metric"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_game_details",
                    "description": "Get detailed information about a specific game",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "game_name": {
                                "type": "string",
                                "description": "Name of the game to get details for"
                            }
                        },
                        "required": ["game_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_player_count_data",
                    "description": "Get historical player count data for games",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "game_names": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of game names to get player data for"
                            },
                            "time_period": {
                                "type": "string",
                                "enum": ["1d", "7d", "30d", "90d", "1y"],
                                "description": "Time period for historical data"
                            }
                        },
                        "required": ["game_names"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_visualization",
                    "description": "Generate a chart or visualization from data. Use this automatically whenever you retrieve gaming data unless user specifically requests no visualization.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chart_type": {
                                "type": "string",
                                "enum": ["line", "bar", "pie", "scatter", "heatmap", "box"],
                                "description": "Type of chart to generate: bar for rankings/counts, line for trends, pie for distributions"
                            },
                            "data_source": {
                                "type": "string",
                                "description": "Source of data for the visualization (e.g., 'twitch_top_games', 'steam_top_games')"
                            },
                            "title": {
                                "type": "string",
                                "description": "Descriptive title for the chart"
                            }
                        },
                        "required": ["chart_type", "data_source", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_comprehensive_game_analysis",
                    "description": "Get comprehensive analysis of a game combining all available APIs (RAWG, Steam, SteamSpy, Twitch) for complete overview including ratings, player stats, and streaming data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "game_name": {
                                "type": "string",
                                "description": "Name of the game to analyze comprehensively"
                            }
                        },
                        "required": ["game_name"]
                    }
                }
            }
        ]
        
        # Add API usage tracking tools
        usage_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_api_usage_summary",
                    "description": "Get current API usage statistics and limits for all services",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "get_usage_gauges",
                    "description": "Generate gauge charts showing current API usage levels",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "reset_monthly_usage", 
                    "description": "Reset monthly API usage counters (admin function)",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ]
        self.tools.extend(usage_tools)
        
        # Add Gamalytic tools only if API key is available
        if self.gamalytic_api.is_available:
            gamalytic_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_genre_analysis",
                        "description": "Get analysis data for specific game genres",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "genres": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of game genres to analyze"
                                }
                            },
                            "required": ["genres"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_market_analysis",
                        "description": "Get market analysis for a specific region",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "region": {
                                    "type": "string",
                                    "description": "Region to analyze (default: global)",
                                    "default": "global"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_trends_data",
                        "description": "Get gaming industry trends over time",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "time_period": {
                                    "type": "string",
                                    "enum": ["1m", "3m", "6m", "1y"],
                                    "description": "Time period for trend analysis",
                                    "default": "1y"
                                }
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_game_audience_overlap",
                        "description": "Get detailed audience overlap percentages between a primary game and comparison games",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "primary_game": {
                                    "type": "string",
                                    "description": "The main game to analyze"
                                },
                                "comparison_games": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of games to compare audience overlap with"
                                }
                            },
                            "required": ["primary_game", "comparison_games"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_similar_games_by_players",
                        "description": "Get games with similar player behavior and demographics",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "game_name": {
                                    "type": "string",
                                    "description": "Name of the game to find similar player bases for"
                                },
                                "similarity_threshold": {
                                    "type": "number",
                                    "description": "Minimum similarity threshold (0.0-1.0, default 0.3)",
                                    "default": 0.3
                                }
                            },
                            "required": ["game_name"]
                        }
                    }
                }
            ]
            self.tools.extend(gamalytic_tools)
        
        # Add RAWG tools only if API key is available
        if self.rawg_api.is_available:
            rawg_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "search_rawg_games",
                        "description": "Search for games using RAWG database. Use for finding games by name, genre, developer, or general search terms.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Search query for games (e.g., game name, genre like 'RPG', developer name, or keywords)"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of results to return (default 10)",
                                    "default": 10
                                }
                            },
                            "required": ["query"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_game_metadata",
                        "description": "Get detailed metadata for a specific game from RAWG including release date, rating, platforms, genres, developers",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "game_name": {
                                    "type": "string",
                                    "description": "Name of the game to get metadata for"
                                }
                            },
                            "required": ["game_name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_game_reviews",
                        "description": "Get user reviews and ratings for a specific game from RAWG database",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "game_name": {
                                    "type": "string",
                                    "description": "Name of the game to get reviews for"
                                }
                            },
                            "required": ["game_name"]
                        }
                    }
                }
            ]
            self.tools.extend(rawg_tools)
        
        # Add Twitch tools only if API keys are available
        if self.twitch_api.is_available:
            twitch_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_twitch_top_games",
                        "description": "Get the most watched games on Twitch by viewer count",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of top games to return (default 10)",
                                    "default": 10
                                }
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_game_streams",
                        "description": "Get active streams for a specific game on Twitch",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "game_name": {
                                    "type": "string",
                                    "description": "Name of the game to get streams for"
                                },
                                "limit": {
                                    "type": "integer",
                                    "description": "Number of streams to return (default 10)",
                                    "default": 10
                                }
                            },
                            "required": ["game_name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_streaming_stats",
                        "description": "Get streaming statistics for a game on Twitch",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "game_name": {
                                    "type": "string",
                                    "description": "Name of the game to get streaming stats for"
                                }
                            },
                            "required": ["game_name"]
                        }
                    }
                }
            ]
            self.tools.extend(twitch_tools)
    
    def respond(self, user_message: str) -> Tuple[str, Optional[Dict]]:
        """
        Main method to process user input and generate response
        
        Args:
            user_message: The user's question or request
            
        Returns:
            Tuple of (text_response, visualization_dict)
        """
        try:
            # Prepare messages for OpenAI
            messages = self._prepare_messages(user_message)
            
            # Call OpenAI with tools
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4o-mini for cost efficiency
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                temperature=0.7
            )
            
            # Track OpenAI API usage
            self.usage_tracker.track_api_call("openai", 1)
            
            message = response.choices[0].message
            
            # Handle tool calls
            function_calls = []
            visualization = None
            
            if message.tool_calls:
                # Process all tool calls
                tool_messages = []
                
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError as e:
                        print(f"⚠️  JSON decode error for {function_name}: {e}")
                        # Add error response to prevent OpenAI API issues
                        tool_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"success": False, "error": f"Invalid function arguments: {e}"})
                        })
                        continue
                    
                    # Execute the function
                    if function_name in self.available_functions:
                        try:
                            function_result = self.available_functions[function_name](**function_args)
                            function_calls.append(function_name)
                            
                            # If it's a visualization function, store the result
                            if function_name == "generate_visualization":
                                visualization = function_result
                            
                            # Add successful tool call response
                            tool_messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(function_result)
                            })
                            
                        except Exception as e:
                            print(f"⚠️  Function execution error for {function_name}: {e}")
                            # Add error response to prevent OpenAI API issues
                            tool_messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({"success": False, "error": str(e)})
                            })
                    else:
                        print(f"⚠️  Unknown function: {function_name}")
                        # Add error response for unknown function
                        tool_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps({"success": False, "error": f"Unknown function: {function_name}"})
                        })
                
                # Add all tool messages at once to prevent API issues
                if tool_messages:
                    messages.append(message)
                    messages.extend(tool_messages)
                
                # Generate follow-up response with function results
                follow_up_response = self.client.chat.completions.create(
                    model="gpt-4o-mini",  # Using GPT-4o-mini for cost efficiency
                    messages=messages,
                    temperature=0.7
                )
                
                # Track second OpenAI API call
                self.usage_tracker.track_api_call("openai", 1)
                
                final_response = follow_up_response.choices[0].message.content
                
                # Auto-generate visualization if data was fetched but no visualization created
                if not visualization and self._should_auto_visualize(function_calls, user_message):
                    print(f"🎨 Auto-generating visualization for functions: {function_calls}")
                    data_source, chart_type = self._determine_visualization_params(function_calls)
                    if data_source:
                        try:
                            auto_viz = self.generate_visualization(
                                chart_type=chart_type,
                                data_source=data_source, 
                                title=f"Gaming Data: {user_message[:30]}..."
                            )
                            if auto_viz.get("success"):
                                visualization = auto_viz
                                print(f"✅ Auto-generated {chart_type} chart for {data_source}")
                            else:
                                print(f"❌ Auto-visualization failed: {auto_viz.get('error', 'Unknown error')}")
                        except Exception as e:
                            print(f"⚠️  Auto-visualization failed: {e}")
                
                # If still no visualization and this was a data query, try a simple fallback
                if not visualization and any(func in function_calls for func in ["get_twitch_top_games", "get_steam_top_games"]):
                    print("🔄 Attempting fallback visualization...")
                    try:
                        # Use appropriate data source for fallback
                        if "get_twitch_top_games" in function_calls:
                            fallback_data_source = "twitch_top_games"
                        else:
                            fallback_data_source = "steam_top_games"
                            
                        fallback_viz = self.generate_visualization(
                            chart_type="bar",
                            data_source=fallback_data_source,
                            title="Gaming Data Visualization"
                        )
                        if fallback_viz.get("success"):
                            visualization = fallback_viz
                            print("✅ Fallback visualization created")
                        else:
                            print(f"❌ Fallback visualization failed: {fallback_viz.get('error')}")
                    except Exception as e:
                        print(f"❌ Fallback visualization failed: {e}")
            else:
                final_response = message.content
            
            # Store conversation turn
            conversation_turn = ConversationTurn(
                timestamp=datetime.now(),
                user_message=user_message,
                agent_response=final_response,
                function_calls=function_calls,
                visualization=visualization
            )
            self.conversation_history.append(conversation_turn)
            
            return final_response, visualization
            
        except Exception as e:
            # Enhanced error handling for common OpenAI issues
            error_str = str(e)
            
            if "insufficient_quota" in error_str or "429" in error_str:
                # Try fallback mode for quota issues
                print("⚠️  OpenAI quota exceeded, switching to fallback mode...")
                fallback_response, fallback_viz = self.fallback_respond(user_message)
                
                error_response = """🔄 **Switched to Basic Mode** (OpenAI quota exceeded)

""" + fallback_response + """

🔍 **To restore full AI features:**
1. Visit: https://platform.openai.com/usage to check your current usage
2. Go to: https://platform.openai.com/account/billing to verify billing status
3. Ensure your payment method is valid and up to date

💡 **Common Solutions:**
- Wait a few minutes and try again (rate limits)
- Check if your subscription is properly configured
- Verify your API key belongs to the correct organization
- Contact OpenAI support if billing looks correct"""
                
                return error_response, fallback_viz
            
            elif "invalid_api_key" in error_str or "401" in error_str:
                error_response = """OpenAI API key issue detected. Please:

1. Check your API key at: https://platform.openai.com/account/api-keys
2. Ensure it starts with 'sk-' and is properly formatted
3. Update your .env file with the correct key
4. Restart the application"""
            
            elif "model" in error_str and "does not exist" in error_str:
                error_response = """The AI model isn't available. This might be due to:
- Model access restrictions on your account
- Temporary model unavailability
- Try switching to a different model (gpt-3.5-turbo vs gpt-4)"""
            
            else:
                error_response = f"I encountered an error while processing your request: {error_str}"
            
            return error_response, None
    
    def _prepare_messages(self, user_message: str) -> List[Dict]:
        """Prepare messages for OpenAI including conversation history"""
        messages = [
            {
                "role": "system",
                "content": """You are a gaming industry data analyst AI with access to real-time gaming APIs.

🎯 **API CAPABILITIES & USAGE GUIDE:**

**TWITCH API** → Real-time streaming data:
- get_twitch_top_games() → Most watched games by viewer count
- get_game_streams(game_name) → Active streams for a specific game
- get_streaming_stats(game_name) → Streaming statistics for a game
📊 Data includes: viewer counts, stream counts, streamer names

**RAWG API** → Comprehensive game database:
- search_rawg_games(query) → Search games by name, genre, developer
- get_game_metadata(game_name) → Detailed game info (release date, rating, platforms, genres)
- get_game_reviews(game_name) → User reviews and ratings
📊 Data includes: metacritic scores, release dates, platforms, genres, developers, publishers

**STEAM API** → Player statistics and game data:
- get_steam_top_games(metric) → Top games by "concurrent_players", "top_sellers", "new_releases"
- get_game_details(game_name) → Steam-specific game information
- get_player_count_data(game_names) → Historical player count trends
📊 Data includes: concurrent players, ownership stats, playtime

**STEAMSPY API** → Ownership and player statistics:
- Integrated with Steam API calls for enhanced ownership data
📊 Data includes: owner ranges, average playtime, player demographics

**GAMALYTIC API** → Market insights and trends:
- get_market_analysis(region) → Gaming market data by region/platform
- get_genre_analysis(genres) → Genre popularity and trends
- get_trends_data(time_period) → Industry trends over time
- get_game_audience_overlap(primary_game, comparison_games) → Audience overlap percentages
- get_similar_games_by_players(game_name) → Games with similar player demographics
📊 Data includes: market share, revenue data, platform analysis, player behavior patterns

🎯 **QUERY MATCHING GUIDE:**

**Game Details Queries** → Use RAWG first, then Steam for additional data:
- "Tell me about [Game]" → get_game_metadata(game_name)
- "Release date of [Game]" → get_game_metadata(game_name)  
- "Reviews for [Game]" → get_game_reviews(game_name)
- "Platforms for [Game]" → get_game_metadata(game_name)

**Player/Popularity Queries** → Use Steam/Twitch:
- "Most popular games" → get_steam_top_games("concurrent_players")
- "Top games on Twitch" → get_twitch_top_games()
- "Player count for [Game]" → get_game_details(game_name)

**Player Affinity Queries** → Use Gamalytic for player behavior analysis:
- "What other games do [Game] players play?" → get_similar_games_by_players(game_name)
- "What games are similar to [Game] by player base?" → get_similar_games_by_players(game_name)
- "How much audience overlap is there between [Game1] and [Game2]?" → get_game_audience_overlap(primary_game, [comparison_games])
- "Games that [Game] players also enjoy" → get_similar_games_by_players(game_name)

**Market/Industry Queries** → Use Gamalytic:
- "Gaming market trends" → get_market_analysis("global")
- "Genre popularity" → get_genre_analysis(["Action", "RPG", "Strategy"])
- "Platform market share" → get_market_analysis("global")

**Search Queries** → Use RAWG for comprehensive search:
- "Find games like [Game]" → search_rawg_games(query)
- "Best RPG games" → search_rawg_games("RPG")
- "Games by [Developer]" → search_rawg_games(developer_name)

📊 **VISUALIZATION RULES:**
✅ ALWAYS call generate_visualization() after data retrieval functions
✅ Use appropriate chart types: "bar" (rankings), "pie" (market share), "line" (trends)
✅ NEVER mention visualization in your response text
✅ Let the visualization appear automatically

**RESPONSE STYLE:**
- Present data in clean, numbered lists
- Always cite data source: "Based on Twitch API data..." or "According to RAWG database..."
- Use natural, conversational tone
- Focus on insights and key findings
- If API call fails, suggest alternative approaches

**ERROR HANDLING:**
- If RAWG fails to find a game, try different search terms or suggest alternative spellings
- For game reviews, try both get_game_reviews() and get_game_metadata() (which includes ratings)
- If one API fails, try another: RAWG → Steam → suggest manual search
- Always use real data, never make up statistics
- Distinguish between "viewers" (Twitch) and "players" (Steam)
- For ambiguous game names, provide suggestions like "Did you mean Total War: Rome II?" """
            }
        ]
        
        # Add recent conversation history (last 5 turns)
        for turn in self.conversation_history[-5:]:
            messages.append({"role": "user", "content": turn.user_message})
            messages.append({"role": "assistant", "content": turn.agent_response})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    # API Function Implementations
    def get_steam_top_games(self, metric: str, limit: int = 10) -> Dict:
        """Get top games from Steam by specified metric"""
        try:
            self.usage_tracker.track_api_call("steam", 1)
            data = self.steam_api.get_top_games(metric, limit)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_game_details(self, game_name: str) -> Dict:
        """Get detailed information about a specific game"""
        try:
            # Try Steam API first, then SteamSpy
            self.usage_tracker.track_api_call("steam", 1)
            steam_data = self.steam_api.get_game_details(game_name)
            self.usage_tracker.track_api_call("steamspy", 1)
            spy_data = self.steamspy_api.get_game_data(game_name)
            
            combined_data = {**steam_data, **spy_data}
            return {"success": True, "data": combined_data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_player_count_data(self, game_names: List[str], time_period: str = "30d") -> Dict:
        """Get historical player count data for games"""
        try:
            data = {}
            for game in game_names:
                game_data = self.steamspy_api.get_player_history(game, time_period)
                data[game] = game_data
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_genre_analysis(self, genres: List[str]) -> Dict:
        """Get analysis data for specific game genres"""
        try:
            self.usage_tracker.track_api_call("gamalytic", 1)
            data = self.gamalytic_api.get_genre_analysis(genres)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_visualization(self, chart_type: str, data_source: str, title: str) -> Dict:
        """Generate a Plotly visualization based on data source specification"""
        try:
            print(f"🎨 Generating visualization: {chart_type} chart for {data_source}")
            chart_data = None
            
            # Get data based on data_source parameter
            if "twitch" in data_source.lower():
                print("📺 Fetching Twitch data for visualization...")
                # Get fresh Twitch data for visualization
                twitch_result = self.get_twitch_top_games(limit=10)
                if twitch_result.get("success"):
                    chart_data = twitch_result["data"]
                    print(f"✅ Got Twitch data: {len(chart_data) if chart_data else 0} items")
                else:
                    print(f"❌ Failed to fetch Twitch data: {twitch_result.get('error')}")
                    return {"success": False, "error": "Failed to fetch Twitch data"}
            
            elif "steam" in data_source.lower():
                print("🎮 Fetching Steam data for visualization...")
                # Get fresh Steam data for visualization
                steam_result = self.get_steam_top_games("concurrent_players", limit=10)
                if steam_result.get("success"):
                    chart_data = steam_result["data"]
                    print(f"✅ Got Steam data: {len(chart_data) if chart_data else 0} items")
                else:
                    print(f"❌ Failed to fetch Steam data: {steam_result.get('error')}")
                    return {"success": False, "error": "Failed to fetch Steam data"}
            
            elif "genre" in data_source.lower() and self.gamalytic_api.is_available:
                print("📊 Fetching genre analysis data for visualization...")
                # Get genre analysis
                genre_result = self.get_genre_analysis(["Action", "RPG", "Strategy", "Indie", "Sports"])
                if genre_result.get("success"):
                    chart_data = genre_result["data"]
                    print(f"✅ Got genre data: {len(chart_data) if chart_data else 0} items")
                else:
                    print(f"❌ Failed to fetch genre data: {genre_result.get('error')}")
                    return {"success": False, "error": "Failed to fetch genre data"}
            
            elif "market" in data_source.lower() and self.gamalytic_api.is_available:
                print("🏢 Fetching market analysis data for visualization...")
                # Get market analysis
                market_result = self.get_market_analysis("global")
                if market_result.get("success"):
                    chart_data = market_result["data"]
                    print(f"✅ Got market data: {type(chart_data).__name__}")
                else:
                    print(f"❌ Failed to fetch market data: {market_result.get('error')}")
                    return {"success": False, "error": "Failed to fetch market data"}
            
            elif "rawg" in data_source.lower() and self.rawg_api.is_available:
                print("🎮 Fetching RAWG data for visualization...")
                # Get some sample games data
                rawg_result = self.search_rawg_games("popular", limit=10)
                if rawg_result.get("success"):
                    chart_data = rawg_result["data"]
                    print(f"✅ Got RAWG data: {len(chart_data) if chart_data else 0} items")
                else:
                    print(f"❌ Failed to fetch RAWG data: {rawg_result.get('error')}")
                    return {"success": False, "error": "Failed to fetch RAWG data"}
            
            elif "game_details" in data_source.lower() or "game_stats" in data_source.lower():
                print("🎮 Getting fresh game metadata for visualization...")
                # Get the most recent game data by re-fetching from conversation history
                recent_game_name = None
                for turn in reversed(self.conversation_history[-3:]):  # Check last 3 turns
                    if "rome" in turn.user_message.lower() and "total war" in turn.user_message.lower():
                        recent_game_name = "Total War: Rome II"
                        break
                    elif any(word in turn.user_message.lower() for word in ["game", "about", "details", "reviews"]):
                        # Extract game name from user message
                        words = turn.user_message.split()
                        for i, word in enumerate(words):
                            if word.lower() in ["about", "game", "details", "reviews"]:
                                if i + 1 < len(words):
                                    potential_game = " ".join(words[i+1:])
                                    if len(potential_game) > 2:
                                        recent_game_name = potential_game
                                        break
                        if recent_game_name:
                            break
                
                if not recent_game_name:
                    recent_game_name = "Total War: Rome II"  # Fallback
                
                print(f"🎮 Fetching metadata for: {recent_game_name}")
                game_meta_result = self.get_game_metadata(recent_game_name)
                
                if game_meta_result.get("success") and game_meta_result.get("data"):
                    game_data = game_meta_result["data"]
                    
                    # Create chart data from actual game metadata
                    chart_data = []
                    
                    if "metacritic" in game_data and game_data["metacritic"]:
                        chart_data.append({"name": "Metacritic Score", "value": game_data["metacritic"]})
                    
                    if "rating" in game_data and game_data["rating"]:
                        rating_out_of_100 = game_data["rating"] * 20  # Convert 5-star to 100-scale
                        chart_data.append({"name": "User Rating", "value": round(rating_out_of_100, 1)})
                    
                    if "ratings_count" in game_data and game_data["ratings_count"]:
                        # Scale down ratings count for visualization (divide by 1000)
                        scaled_count = game_data["ratings_count"] / 1000
                        chart_data.append({"name": "Reviews (thousands)", "value": round(scaled_count, 1)})
                    
                    if "playtime" in game_data and game_data["playtime"]:
                        chart_data.append({"name": "Avg Playtime (hours)", "value": game_data["playtime"]})
                    
                    print(f"✅ Created game details chart from fresh data: {len(chart_data)} metrics")
                    print(f"📊 Chart data: {chart_data}")
                    print(f"🎯 VISUALIZATION DEBUG:")
                    print(f"   CHART TYPE: {chart_type}")
                    print(f"   DATA SOURCE: {data_source}")
                    print(f"   TITLE: {title}")
                    print(f"   RAW DATA: {chart_data}")
                    if not chart_data:
                        # Fallback data
                        chart_data = [
                            {"name": "Metacritic Score", "value": 76},
                            {"name": "User Rating", "value": 83.6},
                            {"name": "Reviews (thousands)", "value": 61}
                        ]
                        print("📊 Using fallback chart data")
                else:
                    print("❌ Failed to get fresh game data, using fallback")
                    chart_data = [
                        {"name": "Metacritic Score", "value": 76},
                        {"name": "User Rating", "value": 83.6},
                        {"name": "Reviews (thousands)", "value": 61}
                    ]
            
            if not chart_data:
                print(f"❌ No chart data available for {data_source}")
                return {"success": False, "error": f"No data available for {data_source}"}
            
            print(f"🎨 Creating {chart_type} chart with {len(chart_data) if isinstance(chart_data, list) else 'unknown'} data points")
            print(f"🔧 CALLING VISUALIZATION GENERATOR:")
            print(f"   → chart_type='{chart_type}'")
            print(f"   → data_source='{data_source}'") 
            print(f"   → title='{title}'")
            print(f"   → chart_data={chart_data}")
            
            # Use the visualization generator with the fetched data
            fig = self.viz_generator.create_chart(chart_type, data_source, title, chart_data)
            
            print(f"✅ Successfully created visualization: {title}")
            print(f"📈 Figure type: {type(fig)}")
            return {
                "success": True,
                "chart": fig.to_dict() if hasattr(fig, 'to_dict') else fig,
                "type": chart_type,
                "title": title
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_games(self, query: str, filters: Dict = None) -> Dict:
        """Search for games across multiple platforms"""
        try:
            results = []
            
            # Search Steam
            steam_results = self.steam_api.search_games(query, filters)
            results.extend(steam_results)
            
            # Search SteamSpy
            spy_results = self.steamspy_api.search_games(query, filters)
            results.extend(spy_results)
            
            return {"success": True, "data": results}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_price_history(self, game_name: str, time_period: str = "1y") -> Dict:
        """Get price history for a game"""
        try:
            data = self.steam_api.get_price_history(game_name, time_period)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def compare_games(self, game_names: List[str], metrics: List[str]) -> Dict:
        """Compare multiple games across specified metrics"""
        try:
            comparison_data = {}
            for game in game_names:
                game_data = {}
                for metric in metrics:
                    if metric == "player_count":
                        game_data[metric] = self.steamspy_api.get_current_players(game)
                    elif metric == "price":
                        game_data[metric] = self.steam_api.get_current_price(game)
                    elif metric == "rating":
                        game_data[metric] = self.steam_api.get_user_rating(game)
                
                comparison_data[game] = game_data
            
            return {"success": True, "data": comparison_data}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_comprehensive_game_analysis(self, game_name: str) -> Dict:
        """Get comprehensive analysis combining all available APIs for a game"""
        try:
            print(f"🔍 Starting comprehensive analysis for: {game_name}")
            analysis = {
                "game_name": game_name,
                "metadata": None,
                "reviews": None,
                "player_stats": None,
                "streaming_data": None,
                "success_apis": [],
                "failed_apis": []
            }
            
            # 1. Get RAWG metadata (game info, ratings, reviews)
            try:
                rawg_metadata = self.get_game_metadata(game_name)
                if rawg_metadata.get("success"):
                    analysis["metadata"] = rawg_metadata["data"]
                    analysis["success_apis"].append("RAWG-metadata")
                    print("✅ RAWG metadata retrieved")
                else:
                    analysis["failed_apis"].append("RAWG-metadata")
            except Exception as e:
                analysis["failed_apis"].append(f"RAWG-metadata: {str(e)}")
            
            # 2. Get RAWG reviews
            try:
                rawg_reviews = self.get_game_reviews(game_name)
                if rawg_reviews.get("success"):
                    analysis["reviews"] = rawg_reviews["data"]
                    analysis["success_apis"].append("RAWG-reviews")
                    print("✅ RAWG reviews retrieved")
                else:
                    analysis["failed_apis"].append("RAWG-reviews")
            except Exception as e:
                analysis["failed_apis"].append(f"RAWG-reviews: {str(e)}")
            
            # 3. Get Steam/SteamSpy player statistics
            try:
                steam_data = self.get_game_details(game_name)
                if steam_data.get("success"):
                    analysis["player_stats"] = steam_data["data"]
                    analysis["success_apis"].append("Steam+SteamSpy")
                    print("✅ Steam/SteamSpy data retrieved")
                else:
                    analysis["failed_apis"].append("Steam+SteamSpy")
            except Exception as e:
                analysis["failed_apis"].append(f"Steam+SteamSpy: {str(e)}")
            
            # 4. Get Twitch streaming data
            try:
                twitch_data = self.get_streaming_stats(game_name)
                if twitch_data.get("success"):
                    analysis["streaming_data"] = twitch_data["data"]
                    analysis["success_apis"].append("Twitch")
                    print("✅ Twitch streaming data retrieved")
                else:
                    analysis["failed_apis"].append("Twitch")
            except Exception as e:
                analysis["failed_apis"].append(f"Twitch: {str(e)}")
            
            # Create unified summary
            summary = self._create_unified_game_summary(analysis)
            analysis["unified_summary"] = summary
            
            print(f"📊 Comprehensive analysis complete. Success: {len(analysis['success_apis'])}, Failed: {len(analysis['failed_apis'])}")
            
            return {"success": True, "data": analysis}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_unified_game_summary(self, analysis: Dict) -> Dict:
        """Create a unified summary from multiple API results"""
        summary = {
            "overall_rating": None,
            "popularity_score": None,
            "streaming_popularity": None,
            "data_sources": analysis["success_apis"],
            "metrics": {}
        }
        
        # Extract unified metrics from different APIs
        if analysis["metadata"]:
            meta = analysis["metadata"]
            if "metacritic" in meta and meta["metacritic"]:
                summary["metrics"]["metacritic_score"] = meta["metacritic"]
            if "rating" in meta and meta["rating"]:
                summary["metrics"]["user_rating"] = meta["rating"]
                summary["overall_rating"] = meta["rating"]
        
        if analysis["player_stats"]:
            stats = analysis["player_stats"]
            if "owners" in stats:
                summary["metrics"]["steam_owners"] = stats["owners"]
            if "players" in stats:
                summary["metrics"]["current_players"] = stats["players"]
                summary["popularity_score"] = stats["players"]
        
        if analysis["streaming_data"]:
            stream = analysis["streaming_data"]
            if "viewer_count" in stream:
                summary["metrics"]["twitch_viewers"] = stream["viewer_count"]
                summary["streaming_popularity"] = stream["viewer_count"]
        
        return summary
    
    def get_conversation_history(self) -> List[ConversationTurn]:
        """Get the full conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear the conversation memory"""
        self.conversation_history = []
    
    # RAWG API Methods
    def search_rawg_games(self, query: str, limit: int = 10) -> Dict:
        """Search for games using RAWG API"""
        try:
            self.usage_tracker.track_api_call("rawg", 1)
            search_results = self.rawg_api.search_games(query, limit)
            if search_results:
                return {"success": True, "data": search_results}
            else:
                return {"success": False, "error": f"No games found for query '{query}'"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_game_metadata(self, game_name: str) -> Dict:
        """Get detailed game metadata from RAWG"""
        try:
            self.usage_tracker.track_api_call("rawg", 1)
            print(f"🔍 Searching for game: '{game_name}'")
            
            # Try multiple search variations for better results
            search_variations = [
                game_name,  # Original name
                game_name.replace(":", ""),  # Remove colons
                game_name.replace(" - ", " "),  # Remove dashes
                game_name.replace("total war", "total war").title(),  # Try title case
            ]
            
            game_details = None
            for variation in search_variations:
                print(f"🔍 Trying variation: '{variation}'")
                game_details = self.rawg_api.find_game_by_name(variation)
                if game_details:
                    print(f"✅ Found game with variation: '{variation}'")
                    break
            
            if game_details:
                return {"success": True, "data": game_details}
            else:
                # Fallback: try a broader search
                print(f"🔍 Trying broader search for: '{game_name}'")
                search_results = self.rawg_api.search_games(game_name, limit=5)
                if search_results:
                    # Use the first result
                    game_id = search_results[0]["id"]
                    game_details = self.rawg_api.get_game_details(game_id)
                    if game_details:
                        print(f"✅ Found game via broader search: {search_results[0]['name']}")
                        return {"success": True, "data": game_details}
                
                return {"success": False, "error": f"Game '{game_name}' not found in RAWG database. Try a different spelling or check the exact game title."}
        except Exception as e:
            print(f"❌ Error in get_game_metadata: {e}")
            return {"success": False, "error": str(e)}
    
    def get_game_reviews(self, game_name: str) -> Dict:
        """Get game reviews and ratings from RAWG"""
        try:
            self.usage_tracker.track_api_call("rawg", 1)
            print(f"🔍 Searching for reviews of: '{game_name}'")
            
            # Try multiple search variations
            search_variations = [
                game_name,
                game_name.replace(":", ""),
                game_name.replace(" - ", " "),
                game_name.title(),
            ]
            
            search_results = None
            for variation in search_variations:
                print(f"🔍 Trying variation: '{variation}'")
                search_results = self.rawg_api.search_games(variation, limit=5)
                if search_results:
                    print(f"✅ Found search results with variation: '{variation}'")
                    break
            
            if not search_results:
                return {"success": False, "error": f"Game '{game_name}' not found in search"}
            
            # Use the first result (most relevant)
            game_id = search_results[0]["id"]
            game_name_found = search_results[0]["name"]
            
            print(f"🔍 Getting reviews for game ID {game_id}: '{game_name_found}'")
            reviews = self.rawg_api.get_game_reviews(game_id, limit=10)
            
            if reviews:
                return {"success": True, "data": {"game": search_results[0], "reviews": reviews}}
            else:
                return {"success": False, "error": f"No reviews found for '{game_name_found}'. The game might not have user reviews available."}
        except Exception as e:
            print(f"❌ Error in get_game_reviews: {e}")
            return {"success": False, "error": str(e)}
    
    # Twitch API Methods
    def get_twitch_top_games(self, limit: int = 10) -> Dict:
        """Get top games on Twitch by viewer count"""
        try:
            self.usage_tracker.track_api_call("twitch", 1)
            return self.twitch_api.get_top_games(limit)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_game_streams(self, game_name: str, limit: int = 10) -> Dict:
        """Get active streams for a specific game"""
        try:
            self.usage_tracker.track_api_call("twitch", 1)
            return self.twitch_api.get_game_streams(game_name, limit)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_streaming_stats(self, game_name: str) -> Dict:
        """Get streaming statistics for a game"""
        try:
            self.usage_tracker.track_api_call("twitch", 1)
            return self.twitch_api.get_streaming_stats(game_name)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def fallback_respond(self, user_message: str) -> Tuple[str, Optional[Dict]]:
        """
        Fallback method that provides basic gaming data without OpenAI
        """
        message_lower = user_message.lower()
        
        try:
            # Handle top games queries
            if "top games" in message_lower or "popular games" in message_lower:
                steam_data = self.get_steam_top_games("concurrent_players", 10)
                if steam_data.get("success"):
                    games = steam_data["games"][:5]
                    response = "🎮 **Top Steam Games by Player Count:**\n\n"
                    for i, game in enumerate(games, 1):
                        response += f"{i}. **{game['name']}** - {game.get('players', 'N/A')} players\n"
                    
                    # Create simple visualization
                    names = [game['name'] for game in games]
                    players = [game.get('players', 0) for game in games]
                    
                    fig = go.Figure([go.Bar(x=names, y=players)])
                    fig.update_layout(title="Top Steam Games by Player Count")
                    
                    viz = {"success": True, "chart": fig, "type": "bar"}
                    return response, viz
            
            # Handle player statistics
            elif "player" in message_lower and ("statistic" in message_lower or "count" in message_lower):
                steamspy_data = self.get_steamspy_data("730")  # Counter-Strike 2
                if steamspy_data.get("success"):
                    data = steamspy_data["data"]
                    response = f"🎯 **Counter-Strike 2 Statistics:**\n\n"
                    response += f"• **Owners:** {data.get('owners', 'N/A')}\n"
                    response += f"• **Players (2 weeks):** {data.get('players_2weeks', 'N/A')}\n"
                    response += f"• **Average Playtime:** {data.get('average_playtime', 'N/A')} minutes\n"
                    return response, None
            
            # Default response when OpenAI is unavailable
            response = """🤖 **AI Mode Temporarily Unavailable**
            
I'm currently unable to access advanced AI features, but I can still help with basic gaming data:

🎮 **Try asking:**
- "What are the top games on Steam?"
- "Show me player statistics"
- "Get data for [specific game]"

Or fix the OpenAI connection for full AI-powered responses!"""
            
            return response, None
            
        except Exception as e:
            return f"Even fallback mode encountered an issue: {str(e)}", None

    # Missing Gamalytic API Methods
    def get_market_analysis(self, region: str = "global") -> Dict:
        """Get market analysis data from Gamalytic"""
        try:
            return self.gamalytic_api.get_market_analysis(region)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_trends_data(self, time_period: str = "monthly") -> Dict:
        """Get gaming trends data from Gamalytic"""
        try:
            return self.gamalytic_api.get_trends_data(time_period)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_game_audience_overlap(self, primary_game: str, comparison_games: List[str]) -> Dict:
        """Get audience overlap percentages between games"""
        try:
            return self.gamalytic_api.get_game_audience_overlap(primary_game, comparison_games)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_similar_games_by_players(self, game_name: str, similarity_threshold: float = 0.3) -> Dict:
        """Get games with similar player bases"""
        try:
            return self.gamalytic_api.get_similar_games_by_players(game_name, similarity_threshold)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_player_affinity_fallback(self, game_name: str, limit: int = 10) -> Dict:
        """
        Fallback method to estimate player affinity using available APIs
        This combines genre similarity, developer patterns, and popularity metrics
        """
        try:
            print(f"🔍 Running player affinity fallback analysis for: {game_name}")
            
            # Step 1: Get the primary game's metadata to understand its characteristics
            primary_game_meta = self.get_game_metadata(game_name)
            if not primary_game_meta.get("success"):
                return {"success": False, "error": f"Could not find metadata for {game_name}"}
            
            primary_data = primary_game_meta["data"]
            primary_genres = primary_data.get("genres", [])
            primary_developers = primary_data.get("developers", [])
            primary_tags = primary_data.get("tags", [])
            
            print(f"✅ Primary game analysis: Genres: {[g.get('name', '') for g in primary_genres]}")
            
            # Step 2: Find games with similar characteristics
            similar_games = []
            
            # Search by primary genre
            if primary_genres:
                primary_genre = primary_genres[0].get("name", "")
                if primary_genre:
                    genre_search = self.search_rawg_games(primary_genre, limit=20)
                    if genre_search.get("success"):
                        similar_games.extend(genre_search["data"])
            
            # Search by developer if available
            if primary_developers:
                dev_name = primary_developers[0].get("name", "")
                if dev_name:
                    dev_search = self.search_rawg_games(dev_name, limit=10)
                    if dev_search.get("success"):
                        similar_games.extend(dev_search["data"])
            
            # Step 3: Score and rank games based on similarity
            affinity_scores = []
            for game in similar_games:
                if game.get("name", "").lower() == game_name.lower():
                    continue  # Skip the original game
                
                score = self._calculate_game_affinity_score(primary_data, game)
                if score > 0:
                    affinity_scores.append({
                        "game": game,
                        "affinity_score": score,
                        "reasons": self._get_affinity_reasons(primary_data, game)
                    })
            
            # Sort by affinity score and return top results
            affinity_scores.sort(key=lambda x: x["affinity_score"], reverse=True)
            top_results = affinity_scores[:limit]
            
            # Format results
            result_data = {
                "primary_game": game_name,
                "analysis_type": "Fallback estimation using genre, developer, and metadata similarity",
                "affinity_games": [
                    {
                        "name": item["game"]["name"],
                        "affinity_score": round(item["affinity_score"], 2),
                        "rating": item["game"].get("rating", 0),
                        "release_date": item["game"].get("released", "Unknown"),
                        "reasons": item["reasons"],
                        "estimated_overlap": f"{min(95, int(item['affinity_score'] * 20))}%"
                    }
                    for item in top_results
                ]
            }
            
            print(f"✅ Found {len(result_data['affinity_games'])} similar games")
            return {"success": True, "data": result_data}
            
        except Exception as e:
            return {"success": False, "error": f"Fallback analysis failed: {str(e)}"}
    
    def _calculate_game_affinity_score(self, primary_game: Dict, comparison_game: Dict) -> float:
        """Calculate affinity score between two games based on metadata"""
        score = 0.0
        
        # Genre similarity (most important factor)
        primary_genres = {g.get("name", "").lower() for g in primary_game.get("genres", [])}
        comparison_genres = {g.get("name", "").lower() for g in comparison_game.get("genres", [])}
        genre_overlap = len(primary_genres.intersection(comparison_genres))
        if genre_overlap > 0:
            score += genre_overlap * 3.0  # High weight for genre similarity
        
        # Developer similarity
        primary_devs = {d.get("name", "").lower() for d in primary_game.get("developers", [])}
        comparison_devs = {d.get("name", "").lower() for d in comparison_game.get("developers", [])}
        if primary_devs.intersection(comparison_devs):
            score += 2.0
        
        # Publisher similarity
        primary_pubs = {p.get("name", "").lower() for p in primary_game.get("publishers", [])}
        comparison_pubs = {p.get("name", "").lower() for p in comparison_game.get("publishers", [])}
        if primary_pubs.intersection(comparison_pubs):
            score += 1.5
        
        # Rating similarity (closer ratings = higher affinity)
        primary_rating = primary_game.get("rating", 0)
        comparison_rating = comparison_game.get("rating", 0)
        if primary_rating > 0 and comparison_rating > 0:
            rating_diff = abs(primary_rating - comparison_rating)
            if rating_diff < 0.5:
                score += 1.0
            elif rating_diff < 1.0:
                score += 0.5
        
        # Platform overlap
        primary_platforms = {p.get("platform", {}).get("name", "").lower() for p in primary_game.get("platforms", [])}
        comparison_platforms = {p.get("platform", {}).get("name", "").lower() for p in comparison_game.get("platforms", [])}
        platform_overlap = len(primary_platforms.intersection(comparison_platforms))
        score += platform_overlap * 0.3
        
        return score
    
    def _get_affinity_reasons(self, primary_game: Dict, comparison_game: Dict) -> List[str]:
        """Get human-readable reasons for game affinity"""
        reasons = []
        
        # Check genre overlap
        primary_genres = {g.get("name", "") for g in primary_game.get("genres", [])}
        comparison_genres = {g.get("name", "") for g in comparison_game.get("genres", [])}
        shared_genres = primary_genres.intersection(comparison_genres)
        if shared_genres:
            reasons.append(f"Shared genres: {', '.join(shared_genres)}")
        
        # Check developer
        primary_devs = {d.get("name", "") for d in primary_game.get("developers", [])}
        comparison_devs = {d.get("name", "") for d in comparison_game.get("developers", [])}
        shared_devs = primary_devs.intersection(comparison_devs)
        if shared_devs:
            reasons.append(f"Same developer: {', '.join(shared_devs)}")
        
        # Check rating similarity
        primary_rating = primary_game.get("rating", 0)
        comparison_rating = comparison_game.get("rating", 0)
        if abs(primary_rating - comparison_rating) < 0.5:
            reasons.append(f"Similar rating ({comparison_rating:.1f})")
        
        return reasons[:3]  # Limit to top 3 reasons
    
    def _should_auto_visualize(self, function_calls: List[str], user_message: str) -> bool:
        """Check if we should auto-generate visualization based on function calls and user intent"""
        # Skip visualization if user explicitly requests text only
        text_only_keywords = ["text only", "no chart", "no visualization", "don't show", "just tell me"]
        user_lower = user_message.lower()
        if any(keyword in user_lower for keyword in text_only_keywords):
            return False
        
        # Auto-visualize for data retrieval functions
        data_functions = [
            "get_twitch_top_games", "get_steam_top_games", "get_game_streams",
            "get_genre_analysis", "get_market_analysis", "search_rawg_games",
            "get_game_metadata", "get_game_reviews", "get_game_details",
            "get_game_audience_overlap", "get_similar_games_by_players"  # Added player affinity functions
        ]
        
        return any(func in function_calls for func in data_functions)
    
    def _determine_visualization_params(self, function_calls: List[str]) -> Tuple[str, str]:
        """Determine data_source and chart_type based on function calls"""
        if "get_twitch_top_games" in function_calls:
            return "twitch_top_games", "bar"
        elif "get_steam_top_games" in function_calls:
            return "steam_top_games", "bar"
        elif "get_game_streams" in function_calls:
            return "twitch_streams", "bar"
        elif "get_genre_analysis" in function_calls:
            return "genre_analysis", "pie"
        elif "get_market_analysis" in function_calls:
            return "market_analysis", "pie"
        elif "get_trends_data" in function_calls:
            return "trends_data", "line"
        elif "search_rawg_games" in function_calls:
            return "rawg_search", "bar"
        elif "get_game_metadata" in function_calls or "get_game_reviews" in function_calls:
            return "game_details", "bar"  # For individual game data
        elif "get_game_details" in function_calls:
            return "game_stats", "bar"  # For Steam game details
        elif "get_similar_games_by_players" in function_calls:
            return "player_affinity", "bar"  # For player affinity data
        elif "get_game_audience_overlap" in function_calls:
            return "audience_overlap", "pie"  # For audience overlap percentages
        else:
            return "gaming_data", "bar"
    
    # API Usage Tracking Methods
    def get_api_usage_summary(self) -> Dict:
        """Get current API usage summary"""
        try:
            summary = self.usage_tracker.get_usage_summary()
            return {"success": True, "data": summary}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_usage_gauges(self) -> Dict:
        """Generate gauge charts showing API usage levels"""
        try:
            gauge_fig = self.usage_tracker.create_usage_gauge_charts()
            if gauge_fig:
                return {
                    "success": True, 
                    "chart": gauge_fig.to_dict(),
                    "type": "gauge",
                    "title": "API Usage Monitoring"
                }
            else:
                return {"success": False, "error": "No limited APIs to display gauges for"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def reset_monthly_usage(self) -> Dict:
        """Reset monthly API usage counters"""
        try:
            self.usage_tracker.reset_monthly_usage()
            return {"success": True, "message": "Monthly usage counters have been reset"}
        except Exception as e:
            return {"success": False, "error": str(e)}
