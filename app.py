"""
Gaming AI Chatbot - Main Dash Application

A modern web interface for the gaming industry chatbot that can answer questions,
analyze data, and generate visualizations using gaming APIs.
"""

import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from datetime import datetime
import json
import numpy as np
import pandas as pd
from io import BytesIO
import base64
import re
import traceback
import os

from agent import GamingChatbotAgent
from utils.simple_gaming_agent import SimpleGamingAgent
from utils.intelligent_gaming_agent import IntelligentGamingAgent
from apis.steam_api import SteamAPI
from apis.steamspy_api import SteamSpyAPI  
from apis.rawg_api import RAWGAPI
from apis.twitch_api import TwitchAPI
from apis.gamalytic_api import GamalyticAPI

# Test flag to use intelligent agent
USE_INTELLIGENT_AGENT = True

# Global variable to store current chart data for export
current_chart_data = {"data": None, "title": "Default Chart"}

def _clean_for_json(obj):
    """Clean object for JSON serialization by converting numpy arrays to lists"""
    if obj is None:
        return None
    
    if isinstance(obj, dict):
        return {key: _clean_for_json(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_clean_for_json(item) for item in obj]
    elif hasattr(obj, 'tolist'):  # numpy array
        return obj.tolist()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def _clean_ai_response(response_text):
    """Clean up AI response text by removing markdown artifacts"""
    if not response_text:
        return response_text
    
    import re
    
    # Remove code block markers and language identifiers
    response_text = re.sub(r'```\w*\n?', '', response_text)
    response_text = response_text.replace("```", "")
    
    # Remove markdown headers that don't make sense in chat
    response_text = re.sub(r'^#+\s*', '', response_text, flags=re.MULTILINE)
    
    # Clean up numbered lists to be more readable
    response_text = re.sub(r'^\s*(\d+)\.\s*\*\*([^*]+)\*\*\s*-\s*', r'\1. \2: ', response_text, flags=re.MULTILINE)
    
    # Convert bold markdown to just emphasis (remove **)
    response_text = response_text.replace("**", "")
    
    # Convert bullet points to simple dashes
    response_text = re.sub(r'^\s*[-*]\s*', '• ', response_text, flags=re.MULTILINE)
    
    # Clean up excessive whitespace but preserve intentional line breaks
    response_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', response_text)
    response_text = re.sub(r'^\s+|\s+$', '', response_text, flags=re.MULTILINE)
    response_text = response_text.strip()
    
    # Remove any remaining artifacts
    response_text = response_text.replace("plaintext", "")
    
    return response_text

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.icons.BOOTSTRAP])
app.title = "Gaming AI Chatbot"

# Expose the Flask server for deployment platforms like Render
server = app.server

# Initialize the chatbot agent
chatbot = GamingChatbotAgent()

# Initialize simple and intelligent agents for testing
if USE_INTELLIGENT_AGENT:
    # Initialize APIs for intelligent agent
    class APIs:
        def __init__(self):
            self.steam_api = SteamAPI()
            self.steamspy_api = SteamSpyAPI()
            self.rawg_api = RAWGAPI()
            self.twitch_api = TwitchAPI()
            self.gamalytic_api = GamalyticAPI()
    
    apis = APIs()
    intelligent_agent = IntelligentGamingAgent(apis)

def _create_welcome_chart():
    """Create a welcome chart with instructions"""
    fig = go.Figure()
    
    fig.add_annotation(
        text="Welcome to Gaming AI Chatbot!<br><br>Ask questions about gaming data to see visualizations here.<br><br>Try the example questions below to get started.",
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=16, color='#ffffff'),
        align="center"
    )
    
    fig.update_layout(
        title="🎮 Gaming AI Chatbot - Ready for Your Questions",
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#2d2d2d',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=False, showticklabels=False, showline=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, showline=False, zeroline=False),
        title_font_size=16,
        height=500
    )
    
    return fig

def _create_contextual_chart(user_message):
    """Create a contextual chart based on user message"""
    # No more fake data - return welcome chart for all cases
    return _create_welcome_chart()

def _create_no_data_chart(message="No visualization data available"):
    """Create a chart indicating no data is available"""
    fig = go.Figure()
    
    fig.add_annotation(
        text=message,
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=16, color='#ffffff'),
        align="center"
    )
    
    fig.update_layout(
        title="No Data Available",
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#2d2d2d',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=False, showticklabels=False, showline=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, showline=False, zeroline=False),
        height=500
    )
    
    return fig

# Define the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🎮 Gaming AI Chatbot", className="text-center mb-4"),
            html.P(
                "Ask me anything about gaming industry trends, player statistics, game performance, and more!",
                className="text-center text-muted mb-4"
            )
        ], width=10),
        dbc.Col([
            dbc.ButtonGroup([
                dbc.Button("ℹ️", id="info-btn", size="sm", color="info", outline=True, title="Data Sources Info")
            ], className="mb-2"),
        ], width=2)
    ]),
    
    # Main content area
    dbc.Row([
        # Chat interface
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("💬 Chat Interface", className="mb-0")
                ]),
                dbc.CardBody([
                    # Chat history
                    html.Div(
                        id="chat-history",
                        style={
                            "height": "400px",
                            "overflow-y": "auto",
                            "border": "1px solid #444",
                            "border-radius": "5px",
                            "padding": "10px",
                            "background-color": "#1e1e1e"
                        }
                    ),
                    
                    # Input area
                    html.Br(),
                    dbc.InputGroup([
                        dbc.Input(
                            id="user-input",
                            placeholder="Ask me about gaming trends, player stats, game analysis...",
                            type="text",
                            style={
                                "background-color": "#3d3d3d", 
                                "border-color": "#555", 
                                "color": "#ffffff",
                                "font-size": "14px"
                            }
                        ),
                        dbc.Button(
                            "Send",
                            id="send-button",
                            color="primary",
                            n_clicks=0
                        )
                    ]),
                    
                    # Example questions
                    html.Br(),
                    html.H6("💡 Try asking:"),
                    dbc.ListGroup([
                        dbc.ListGroupItem(
                            "What are the top games on Steam right now?",
                            action=True,
                            id="example-1"
                        ),
                        dbc.ListGroupItem(
                            "What games are most popular on Twitch?",
                            action=True,
                            id="example-2"
                        ),
                        dbc.ListGroupItem(
                            "What other games do Elden Ring players also play?",
                            action=True,
                            id="example-3"
                        )
                    ], flush=True)
                ])
            ])
        ], width=6),
        
        # Visualization area
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            html.H4("📊 Visualizations", className="mb-0")
                        ], width=4),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.Small("🎨 Theme:", className="text-muted me-2"),
                                    dcc.Dropdown(
                                        id="color-theme-selector",
                                        options=[
                                            {"label": "🌈 Vibrant", "value": "vibrant"},
                                            {"label": "🌊 Ocean", "value": "ocean"},
                                            {"label": "🌅 Sunset", "value": "sunset"},
                                            {"label": "🌸 Pastel", "value": "pastel"},
                                            {"label": "🔥 Fire", "value": "fire"},
                                            {"label": "🌿 Nature", "value": "nature"}
                                        ],
                                        value="vibrant",
                                        clearable=False,
                                        style={"fontSize": "12px"},
                                        className="mb-1"
                                    )
                                ], width=12)
                            ])
                        ], width=4),
                        dbc.Col([
                            dbc.ButtonGroup([
                                dbc.Button("⬅️", id="prev-chart", size="sm", disabled=True),
                                html.Span("1/1", id="chart-counter", className="mx-2 text-muted small"),
                                dbc.Button("➡️", id="next-chart", size="sm", disabled=True),
                                dbc.Button(
                                    "📁 Export",
                                    id="export-chart-btn",
                                    size="sm",
                                    color="success",
                                    outline=True,
                                    className="ms-2",
                                    disabled=True  # Initially disabled
                                )
                            ])
                        ], width=4, className="text-end")
                    ])
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id="main-chart",
                        figure=_create_welcome_chart(),
                        style={"height": "500px"}
                    ),
                    html.Div(id="chart-title", className="text-center text-muted small mt-2")
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # API Usage Tracking Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            html.H5("🔧 API Usage Monitoring", className="mb-0 text-white")
                        ], width=8),
                        dbc.Col([
                            dbc.Button(
                                "🔄 Refresh",
                                id="refresh-usage-btn",
                                size="sm",
                                color="secondary",
                                outline=True
                            )
                        ], width=4, className="text-end")
                    ])
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id="usage-gauges",
                        style={"height": "270px"}
                    ),
                    html.Div(id="usage-summary", className="text-center text-muted small mt-2")
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # Information cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🔥 Hot Topics", className="card-title"),
                    html.P("Battle Royale games continue to dominate", className="card-text"),
                    html.P("VR gaming market growing 25% YoY", className="card-text"),
                    html.P("Mobile gaming reaches $95B revenue", className="card-text")
                ])
            ])
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("📈 Market Stats", className="card-title"),
                    html.P("Global Gaming Market: $180B", className="card-text"),
                    html.P("Active Gamers: 3.2B worldwide", className="card-text"),
                    html.P("Growth Rate: 9.7% annually", className="card-text")
                ])
            ])
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🎯 Data Sources", className="card-title"),
                    html.P("Steam Web API - Complete platform data", className="card-text"),
                    html.P("SteamSpy - Ownership & engagement analytics", className="card-text"),
                    html.P("RAWG - Game database", className="card-text"),
                    html.P("Twitch Analytics - Streaming & monetization analytics", className="card-text"),
                    html.P("Gamalytic - Market insights", className="card-text")
                ])
            ])
        ], width=4)
    ]),
    
    # Hidden div to store conversation state
    html.Div(id="conversation-state", style={"display": "none"}),
    
    # Hidden div to store chart history
    html.Div(id="chart-history", style={"display": "none"}),
    html.Div(id="chart-index", style={"display": "none"}, children="0"),
    
    # Info Modal
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("📊 Available Data Sources & Capabilities")),
        dbc.ModalBody([
            dbc.Accordion([
                dbc.AccordionItem([
                    html.H6("🎮 What you can ask:", className="text-primary"),
                    html.Ul([
                        html.Li("Current player counts for any Steam game"),
                        html.Li("Top games by concurrent players, revenue, or new releases"),
                        html.Li("Game details: release date, developer, publisher, tags"),
                        html.Li("Player statistics: peak players, average players, reviews"),
                        html.Li("Game comparisons and trend analysis"),
                        html.Li("Individual player profiles and game libraries"),
                        html.Li("Recently played games for any Steam user"),
                        html.Li("Game ownership verification and statistics"),
                        html.Li("Steam news and updates for specific games"),
                        html.Li("Achievement data and player progress"),
                        html.Li("Steam Workshop content and statistics")
                    ]),
                    html.H6("📈 Core Gaming Metrics:", className="text-primary"),
                    html.Ul([
                        html.Li("Real-time concurrent players (ISteamUserStats)"),
                        html.Li("All-time peak players and historical data"),
                        html.Li("User reviews (positive/negative ratios)"),
                        html.Li("Game prices and discount history"),
                        html.Li("Release dates and developer information")
                    ]),
                    html.H6("👤 Player Services (IPlayerService):", className="text-success"),
                    html.Ul([
                        html.Li("GetRecentlyPlayedGames - Games played in last 2 weeks"),
                        html.Li("GetOwnedGames - Complete player game library"),
                        html.Li("GetSteamLevel - Player's Steam account level"),
                        html.Li("GetBadges - Badge collection and progress"),
                        html.Li("GetCommunityBadgeProgress - Community achievements"),
                        html.Li("IsPlayingSharedGame - Family sharing detection")
                    ]),
                    html.H6("🎯 User & App Data (ISteamUser/ISteamApps):", className="text-info"),
                    html.Ul([
                        html.Li("GetPlayerSummaries - Player profiles and status"),
                        html.Li("GetFriendList - Social connections and friends"),
                        html.Li("GetPlayerBans - VAC and community ban status"),
                        html.Li("GetAppList - Complete Steam game catalog"),
                        html.Li("GetServersAtAddress - Server information"),
                        html.Li("CheckAppOwnership - Verify game ownership")
                    ]),
                    html.H6("📰 Content & Community (ISteamNews):", className="text-warning"),
                    html.Ul([
                        html.Li("GetNewsForApp - Game news and updates"),
                        html.Li("Steam community announcements"),
                        html.Li("Developer posts and patch notes"),
                        html.Li("Community event information")
                    ])
                ], title="🎮 Steam Web API - Comprehensive Gaming Platform Data"),
                
                dbc.AccordionItem([
                    html.H6("📊 SteamSpy Overview:", className="text-primary"),
                    html.P([
                        "Comprehensive Steam game ownership, playtime, and engagement analytics. Data updated daily with 1-second rate limits (60-second limit for bulk requests)."
                    ], className="mb-3"),
                    
                    html.H6("🎯 Core API Endpoints:", className="text-success"),
                    html.Ul([
                        html.Li("appdetails - Detailed statistics for specific games (requires appid)"),
                        html.Li("top100in2weeks - Top 100 games by players in last 2 weeks"),
                        html.Li("top100forever - Top 100 games by players since March 2009"), 
                        html.Li("top100owned - Top 100 games by total ownership"),
                        html.Li("genre - Games filtered by specific genre (e.g., 'Early Access')"),
                        html.Li("tag - Games filtered by specific tag (e.g., 'Multiplayer')"),
                        html.Li("all - Complete Steam catalog with ownership data (paginated, 1,000 per page)")
                    ]),
                    
                    html.H6("📈 Available Game Metrics:", className="text-info"),
                    html.Ul([
                        html.Li("owners - Estimated ownership ranges (e.g., '1,000,000 - 2,000,000')"),
                        html.Li("average_forever - Average playtime since March 2009 (minutes)"),
                        html.Li("average_2weeks - Average playtime in last 2 weeks (minutes)"),
                        html.Li("median_forever - Median playtime since March 2009 (minutes)"),
                        html.Li("median_2weeks - Median playtime in last 2 weeks (minutes)"),
                        html.Li("ccu - Peak concurrent users yesterday"),
                        html.Li("score_rank - User review score ranking"),
                        html.Li("price - Current US price in cents"),
                        html.Li("initialprice - Original US price in cents"),
                        html.Li("discount - Current discount percentage")
                    ]),
                    
                    html.H6("🎮 Game Information Fields:", className="text-warning"),
                    html.Ul([
                        html.Li("appid - Steam Application ID"),
                        html.Li("name - Game title"),
                        html.Li("developer - Comma-separated developer list"),
                        html.Li("publisher - Comma-separated publisher list"),
                        html.Li("tags - Game tags with vote counts (JSON array)"),
                        html.Li("languages - Supported language list"),
                        html.Li("genre - Game genre classifications")
                    ]),
                    
                    html.H6("� What you can ask:", className="text-primary"),
                    html.Ul([
                        html.Li("\"Show me ownership statistics for Counter-Strike 2\""),
                        html.Li("\"What are the top 100 most played games in the last 2 weeks?\""),
                        html.Li("\"Find games in the 'Early Access' genre\""),
                        html.Li("\"Show me all 'Multiplayer' tagged games\""), 
                        html.Li("\"What are the most owned games of all time?\""),
                        html.Li("\"Compare average playtime between different games\""),
                        html.Li("\"Show me games with the highest concurrent player counts\""),
                        html.Li("\"Find games by specific developers or publishers\""),
                        html.Li("\"Analyze pricing and discount trends\""),
                        html.Li("\"Show me median vs average playtime statistics\"")
                    ]),
                    
                    html.H6("📋 Data Accuracy & Limitations:", className="text-secondary"),
                    html.Ul([
                        html.Li("Ownership data: Statistical estimates, not exact counts"),
                        html.Li("Playtime: Aggregated from public Steam profiles only"),
                        html.Li("Updates: Data refreshed once daily"),
                        html.Li("Rate limits: 1 request/second (60 seconds for 'all' endpoint)"),
                        html.Li("Privacy: Some apps hidden on developer request (appid 999999)")
                    ])
                ], title="📊 SteamSpy API - Ownership & Engagement Analytics"),
                
                dbc.AccordionItem([
                    html.H6("🎮 What you can ask:", className="text-primary"),
                    html.Ul([
                        html.Li("Game metadata: genres, platforms, ratings"),
                        html.Li("Game screenshots, videos, and media"),
                        html.Li("Developer and publisher information"),
                        html.Li("Game series and franchise data"),
                        html.Li("Release dates across different platforms"),
                        html.Li("User and critic review scores")
                    ]),
                    html.H6("🔍 Search capabilities:", className="text-primary"),
                    html.Ul([
                        html.Li("Search games by name, genre, or platform"),
                        html.Li("Find games by specific criteria (year, rating, etc.)"),
                        html.Li("Get comprehensive game databases"),
                        html.Li("Access to 500,000+ games across all platforms")
                    ])
                ], title="🎯 RAWG API - Game Database & Metadata"),
                
                dbc.AccordionItem([
                    html.H6("� Twitch Analytics Overview:", className="text-primary"),
                    html.P([
                        "Comprehensive streaming analytics and developer insights for extensions and games through Twitch's official Analytics & Insights API."
                    ], className="mb-3"),
                    
                    html.H6("🎮 Game Analytics (CSV Reports):", className="text-success"),
                    html.Ul([
                        html.Li("View counts and concurrent viewer analytics"),
                        html.Li("Total hours watched and broadcaster statistics"),
                        html.Li("Chat participation rates and engagement metrics"),
                        html.Li("Clip generation data and viral content tracking"),
                        html.Li("Peak viewership analytics and trend identification"),
                        html.Li("Channel growth metrics and audience retention")
                    ]),
                    
                    html.H6("🔧 Extension Analytics (CSV Reports):", className="text-info"),
                    html.Ul([
                        html.Li("Viewer engagement rates and interaction metrics"),
                        html.Li("Extension installation and usage counts"),
                        html.Li("Revenue analytics for Bits products and monetization"),
                        html.Li("User interaction patterns and session duration"),
                        html.Li("Device ID tracking and platform distribution"),
                        html.Li("Daily active users and retention analytics")
                    ]),
                    
                    html.H6("� Monetization Analytics:", className="text-warning"),
                    html.Ul([
                        html.Li("Bits Leaderboard - Top contributors with channel points"),
                        html.Li("Extension Transactions - Monetization tracking for Bits products"),
                        html.Li("Custom Reward Redemptions - Channel points engagement analytics"),
                        html.Li("Subscription analytics and revenue insights")
                    ]),
                    
                    html.H6("📈 What you can ask:", className="text-primary"),
                    html.Ul([
                        html.Li("\"Generate extension analytics report for the last 30 days\""),
                        html.Li("\"Show me game analytics for [Game Name] viewership trends\""),
                        html.Li("\"What are the top revenue-generating Twitch extensions?\""),
                        html.Li("\"Analyze viewer engagement metrics for my extension\""),
                        html.Li("\"Get Bits leaderboard for channel monetization analysis\""),
                        html.Li("\"Compare game viewership analytics across different time periods\"")
                    ]),
                    
                    html.H6("📋 Data Format & Access:", className="text-secondary"),
                    html.Ul([
                        html.Li("CSV download URLs with daily granularity (overview_v2 format)"),
                        html.Li("Extension Analytics: From January 31, 2018 onwards"),
                        html.Li("Game Analytics: Last 365 days maximum, 5+ hour minimum broadcast"),
                        html.Li("Requires analytics:read:extensions or analytics:read:games scopes"),
                        html.Li("Real-time access to Bits transactions and custom reward data")
                    ])
                ], title="📺 Twitch Analytics & Insights API"),
                
                dbc.AccordionItem([
                    html.H6("💼 What you can ask:", className="text-primary"),
                    html.Ul([
                        html.Li("Gaming industry market analysis and trends"),
                        html.Li("Revenue data and financial performance metrics"),
                        html.Li("Market share analysis by platform and region"),
                        html.Li("Industry growth projections and forecasts"),
                        html.Li("Competitive landscape and company performance"),
                        html.Li("Gaming sector investment and funding data")
                    ]),
                    html.H6("📈 Business insights:", className="text-primary"),
                    html.Ul([
                        html.Li("Market size and revenue breakdowns"),
                        html.Li("Platform performance comparisons"),
                        html.Li("Regional gaming market analysis"),
                        html.Li("Industry trend identification"),
                        html.Li("Competitive intelligence and benchmarking")
                    ]),
                    html.H6("🎯 Player Behavior Analysis:", className="text-success"),
                    html.Ul([
                        html.Li("'Also Played' Games - What other games do players of [Game X] actually play?"),
                        html.Li("Audience Overlap - Which games share similar player demographics?"),
                        html.Li("Geographic player distribution by country"),
                        html.Li("Playtime patterns and engagement metrics"),
                        html.Li("Historical player trends and growth analysis")
                    ]),
                    html.H6("🔍 Example 'Also Played' Questions:", className="text-info"),
                    html.Ul([
                        html.Li("\"What other games do Counter-Strike 2 players also play?\""),
                        html.Li("\"Show me games that Dota 2 fans also enjoy\""),
                        html.Li("\"What do people who play Cyberpunk 2077 also play?\""),
                        html.Li("\"Find games that Elden Ring players also own\""),
                        html.Li("\"What are the most popular secondary games for Valorant players?\"")
                    ]),
                    html.H6("👥 Example 'Audience Overlap' Questions:", className="text-warning"),
                    html.Ul([
                        html.Li("\"Which games have similar audiences to League of Legends?\""),
                        html.Li("\"Show me games with overlapping player demographics to Fortnite\""),
                        html.Li("\"What games compete for the same audience as Call of Duty?\""),
                        html.Li("\"Find games that share players with World of Warcraft\""),
                        html.Li("\"Which games have the most audience crossover with Minecraft?\"")
                    ])
                ], title="💼 Gamalytic API - Industry Analytics & Player Behavior"),
                
                dbc.AccordionItem([
                    html.H6("💡 Example Questions:", className="text-success"),
                    html.Ul([
                        html.Li("\"What are the top 10 games on Steam right now?\""),
                        html.Li("\"Show me player statistics for Counter-Strike 2\""),
                        html.Li("\"What games has [SteamID] played recently?\""),
                        html.Li("\"Check if user owns Cyberpunk 2077\""),
                        html.Li("\"What's the Steam level of this player?\""),
                        html.Li("\"Show me recent news for Elden Ring\""),
                        html.Li("\"Compare the popularity of RPG vs Action games\""),
                        html.Li("\"Generate extension analytics report for the last 30 days\""),
                        html.Li("\"What other games do Elden Ring players also play?\""),
                        html.Li("\"Show me the most owned indie games\""),
                        html.Li("\"Which games have similar audiences to Fortnite?\""),
                        html.Li("\"Generate a chart of gaming market trends\""),
                        html.Li("\"What are the highest-rated games released in 2024?\""),
                        html.Li("\"Show me playtime distribution for popular games\""),
                        html.Li("\"Find games that compete for the same audience as Valorant\""),
                        html.Li("\"Get player profile and badge collection for [SteamID]\""),
                        html.Li("\"Show me the complete Steam app catalog\"")
                    ])
                ], title="💬 Example Queries"),
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Close", id="close-info", className="ms-auto", n_clicks=0)
        ])
    ], id="info-modal", size="lg"),
    
    # Loading overlay
    dcc.Loading(
        id="loading-overlay",
        type="default",
        children=html.Div(id="loading-output")
    ),
    
    # Download component for exporting files
    dcc.Download(id="download-component")
    
], fluid=True, className="p-4")

# Callback for API usage gauge charts
@app.callback(
    [Output("usage-gauges", "figure"),
     Output("usage-summary", "children")],
    [Input("refresh-usage-btn", "n_clicks")]
)
def update_usage_gauges(refresh_clicks):
    """Update API usage gauge charts"""
    try:
        # Get usage summary from the appropriate agent
        if USE_INTELLIGENT_AGENT:
            usage_result = intelligent_agent.get_api_usage_summary()
        else:
            usage_result = chatbot.get_api_usage_summary()
        
        if usage_result.get("success"):
            usage_data = usage_result["data"]
            
            # Create gauge charts
            if USE_INTELLIGENT_AGENT:
                # For intelligent agent, create gauges using the tracker directly
                gauge_fig = intelligent_agent.usage_tracker.create_usage_gauge_charts()
                if gauge_fig:
                    gauge_result = {
                        "success": True, 
                        "chart": gauge_fig.to_dict(),
                        "type": "gauge",
                        "title": "API Usage Monitoring"
                    }
                else:
                    gauge_result = {"success": False, "error": "No limited APIs to display gauges for"}
            else:
                gauge_result = chatbot.get_usage_gauges()
            
            if gauge_result.get("success"):
                fig = go.Figure(gauge_result["chart"])
                
                # Update styling for dark theme
                fig.update_layout(
                    plot_bgcolor='#1e1e1e',
                    paper_bgcolor='#2d2d2d',
                    font=dict(color='#ffffff'),
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                # Create summary text
                limited_apis = {k: v for k, v in usage_data.items() 
                              if v["limit"] != float('inf') and v["limit"] > 0}
                
                if limited_apis:
                    summary_parts = []
                    for api, data in limited_apis.items():
                        status_emoji = {
                            "good": "🟢",
                            "moderate": "🟡", 
                            "warning": "🟠",
                            "critical": "🔴"
                        }.get(data["status"], "⚪")
                        
                        summary_parts.append(
                            f"{status_emoji} {api.upper()}: {data['usage']:,}/{data['limit']:,} ({data['percentage']}%)"
                        )
                    
                    summary_text = " | ".join(summary_parts)
                else:
                    summary_text = "✅ All APIs are unlimited or have no usage tracking"
                
                return fig, summary_text
            else:
                # Fallback chart
                fig = go.Figure()
                fig.add_annotation(
                    text="No limited APIs to monitor",
                    x=0.5, y=0.5,
                    font=dict(size=16, color="#ffffff"),
                    showarrow=False
                )
                fig.update_layout(
                    plot_bgcolor='#1e1e1e',
                    paper_bgcolor='#2d2d2d',
                    font=dict(color='#ffffff')
                )
                return fig, "No API limits to track"
        else:
            # Error creating usage charts
            fig = go.Figure()
            fig.add_annotation(
                text="Error loading usage data",
                x=0.5, y=0.5,
                font=dict(size=16, color="#ff6b6b"),
                showarrow=False
            )
            fig.update_layout(
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#2d2d2d',
                font=dict(color='#ffffff')
            )
            return fig, "⚠️ Failed to load usage data"
            
    except Exception as e:
        # Error handling
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error: {str(e)}",
            x=0.5, y=0.5,
            font=dict(size=14, color="#ff6b6b"),
            showarrow=False
        )
        fig.update_layout(
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#2d2d2d',
            font=dict(color='#ffffff')
        )
        return fig, f"❌ Error: {str(e)}"

# Callback for sending messages
@app.callback(
    [Output("chat-history", "children"),
     Output("main-chart", "figure"),
     Output("user-input", "value"),
     Output("conversation-state", "children"),
     Output("chart-history", "children"),
     Output("chart-index", "children"),
     Output("chart-counter", "children", allow_duplicate=True),
     Output("prev-chart", "disabled", allow_duplicate=True),
     Output("next-chart", "disabled", allow_duplicate=True)],
    [Input("send-button", "n_clicks"),
     Input("user-input", "n_submit"),
     Input("example-1", "n_clicks"),
     Input("example-2", "n_clicks"),
     Input("example-3", "n_clicks")],
    [State("user-input", "value"),
     State("conversation-state", "children"),
     State("chart-history", "children")],
    prevent_initial_call=True
)
def handle_user_input(send_clicks, enter_submit, ex1_clicks, ex2_clicks, ex3_clicks, 
                     user_message, conversation_state, chart_history_json):
    """Handle user input and generate chatbot response"""
    
    # Determine which input triggered the callback
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], _create_welcome_chart(), "", "", "[]", "0", "1/1", True, True
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Set message based on trigger
    if trigger_id == "example-1":
        user_message = "What are the top games on Steam right now?"
    elif trigger_id == "example-2":
        user_message = "What games are most popular on Twitch?"
    elif trigger_id == "example-3":
        user_message = "What other games do Elden Ring players also play?"
    elif not user_message:
        return [], _create_welcome_chart(), "", "", "[]", "0", "1/1", True, True
    
    # Load existing conversation and chart history
    conversation_history = []
    chart_history = []
    
    if conversation_state:
        try:
            conversation_history = json.loads(conversation_state)
        except:
            conversation_history = []
    
    if chart_history_json:
        try:
            chart_history = json.loads(chart_history_json)
        except:
            chart_history = []
    
    # Get response from chatbot
    try:
        if USE_INTELLIGENT_AGENT:
            print(f"🧠 USING INTELLIGENT AGENT for: {user_message}")
            response_text, visualization = intelligent_agent.respond(user_message)
        else:
            response_text, visualization = chatbot.respond(user_message)
        
        # Clean up the AI response text
        response_text = _clean_ai_response(response_text)
        
        # Clean visualization data for JSON serialization
        clean_visualization = None
        if visualization:
            clean_visualization = _clean_for_json(visualization)
        
        # Add to conversation history
        conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "bot": response_text,
            "visualization": clean_visualization
        })
        
        # Create chat history display
        chat_display = []
        for turn in conversation_history:
            # User message
            chat_display.append(
                dbc.Alert([
                    html.Strong("You: "),
                    turn["user"]
                ], color="primary", className="mb-2")
            )
            
            # Bot response - cleaned and formatted
            cleaned_response = _clean_ai_response(turn["bot"])
            
            # Try to use markdown for better formatting, fallback to plain text
            try:
                bot_content = [
                    html.Strong("🤖 Gaming AI: "),
                    dcc.Markdown(
                        cleaned_response,
                        style={
                            "color": "inherit",
                            "margin": "0",
                            "padding": "0"
                        }
                    )
                ]
            except:
                # Fallback to plain text if markdown fails
                bot_content = [
                    html.Strong("🤖 Gaming AI: "),
                    cleaned_response
                ]
            
            chat_display.append(
                dbc.Alert(
                    bot_content,
                    color="secondary", 
                    className="mb-3"
                )
            )
        
        # Update visualization if provided by the AI
        print(f"🖥️  WEB APP VISUALIZATION DEBUG:")
        print(f"   → visualization type: {type(visualization)}")
        print(f"   → visualization content: {visualization}")
        
        # Handle different visualization formats
        has_visualization = False
        if visualization:
            if isinstance(visualization, dict):
                # Check if it's the old format with "success" key
                if "success" in visualization and visualization.get("success"):
                    has_visualization = True
                    print(f"✅ Processing old format successful visualization")
                # Check if it's the new intelligent agent format with chart data directly
                elif "data" in visualization and "layout" in visualization:
                    has_visualization = True
                    print(f"✅ Processing new format intelligent agent visualization")
                    # Extract title properly - it might be a dict with 'text' key
                    title_obj = visualization.get("layout", {}).get("title", f"Chart for: {user_message[:50]}...")
                    if isinstance(title_obj, dict):
                        title_text = title_obj.get("text", f"Chart for: {user_message[:50]}...")
                    else:
                        title_text = title_obj
                    # Convert to old format for compatibility
                    visualization = {
                        "success": True,
                        "chart": visualization,
                        "title": title_text
                    }
        
        if has_visualization:
            print(f"✅ Processing successful visualization for web display")
            current_chart = go.Figure(visualization["chart"])
            chart_title = visualization.get("title", f"Chart for: {user_message[:50]}...")
            print(f"📊 Chart title: {chart_title}")
            print(f"📈 Chart created: {type(current_chart)}")
            
            # Add to chart history (convert figure to dict for JSON serialization)
            chart_dict = current_chart.to_dict()
            clean_chart_dict = _clean_for_json(chart_dict)
            chart_history.append({
                "chart": clean_chart_dict,
                "title": chart_title,
                "timestamp": datetime.now().isoformat()
            })
            print(f"✅ Chart added to history. Total charts: {len(chart_history)}")
        else:
            print(f"❌ No successful visualization received, using fallback chart")
            # If no visualization from AI, use the welcome chart (don't create contextual charts)
            current_chart = _create_welcome_chart()
            # Only add to history if there's actual new content, not the default chart
            if not chart_history:  # Only for first interaction
                welcome_chart_dict = current_chart.to_dict()
                clean_welcome_chart = _clean_for_json(welcome_chart_dict)
                chart_history.append({
                    "chart": clean_welcome_chart,
                    "title": "Welcome Chart",
                    "timestamp": datetime.now().isoformat()
                })
            else:
                # For subsequent interactions without visualization, use the latest chart
                current_chart = go.Figure(chart_history[-1]["chart"])
        
        # Chart navigation info
        chart_index = len(chart_history) - 1  # Latest chart
        chart_counter = f"{chart_index + 1}/{len(chart_history)}"
        prev_disabled = len(chart_history) <= 1
        next_disabled = True  # Always disabled for latest chart
        
        return (chat_display, 
                current_chart, 
                "", 
                json.dumps(_clean_for_json(conversation_history)),
                json.dumps(_clean_for_json(chart_history)),
                str(chart_index),
                chart_counter,
                prev_disabled,
                next_disabled)
        
    except Exception as e:
        error_message = f"Sorry, I encountered an error: {str(e)}"
        
        conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "bot": error_message,
            "visualization": None
        })
        
        # Create chat history display
        chat_display = []
        for turn in conversation_history:
            chat_display.append(
                dbc.Alert([
                    html.Strong("You: "),
                    turn["user"]
                ], color="primary", className="mb-2")
            )
            
            # Bot response - cleaned and formatted
            cleaned_response = _clean_ai_response(turn["bot"])
            
            # Try to use markdown for better formatting, fallback to plain text
            try:
                bot_content = [
                    html.Strong("🤖 Gaming AI: "),
                    dcc.Markdown(
                        cleaned_response,
                        style={
                            "color": "inherit",
                            "margin": "0",
                            "padding": "0"
                        }
                    )
                ]
            except:
                # Fallback to plain text if markdown fails
                bot_content = [
                    html.Strong("🤖 Gaming AI: "),
                    cleaned_response
                ]
            
            chat_display.append(
                dbc.Alert(
                    bot_content,
                    color="danger" if "error" in turn["bot"] else "secondary", 
                    className="mb-3"
                )
            )
        
        return (chat_display, 
                _create_welcome_chart(), 
                "", 
                json.dumps(_clean_for_json(conversation_history)),
                json.dumps(_clean_for_json(chart_history)),
                "0",
                f"1/{max(1, len(chart_history))}",
                True,
                True)

# Callback for info modal
@app.callback(
    Output("info-modal", "is_open"),
    [Input("info-btn", "n_clicks"), Input("close-info", "n_clicks")],
    [State("info-modal", "is_open")]
)
def toggle_info_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Callback for chart navigation
@app.callback(
    [Output("main-chart", "figure", allow_duplicate=True),
     Output("chart-counter", "children"),
     Output("prev-chart", "disabled"),
     Output("next-chart", "disabled"),
     Output("chart-title", "children"),
     Output("chart-index", "children", allow_duplicate=True)],
    [Input("prev-chart", "n_clicks"),
     Input("next-chart", "n_clicks")],
    [State("chart-history", "children"),
     State("chart-index", "children")],
    prevent_initial_call=True
)
def navigate_charts(prev_clicks, next_clicks, chart_history_json, current_index):
    if not chart_history_json:
        return _create_welcome_chart(), "1/1", True, True, "", "0"
    
    try:
        chart_history = json.loads(chart_history_json)
        current_idx = int(current_index) if current_index else 0
        
        ctx = dash.callback_context
        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if trigger_id == "prev-chart" and current_idx > 0:
                current_idx -= 1
            elif trigger_id == "next-chart" and current_idx < len(chart_history) - 1:
                current_idx += 1
        
        if chart_history:
            chart_data = chart_history[current_idx]
            # Convert dict back to Figure object
            fig = go.Figure(chart_data["chart"])
            counter = f"{current_idx + 1}/{len(chart_history)}"
            prev_disabled = current_idx == 0
            next_disabled = current_idx == len(chart_history) - 1
            title = chart_data.get("title", "")
            # Ensure title is a string for React
            if isinstance(title, dict):
                title = title.get("text", "")
            
            return fig, counter, prev_disabled, next_disabled, title, str(current_idx)
        
    except Exception as e:
        print(f"Chart navigation error: {e}")
        pass
    
    return _create_welcome_chart(), "1/1", True, True, "", "0"

# Export chart data callback
@app.callback(
    [Output("export-chart-btn", "children"),
     Output("download-component", "data")],
    Input("export-chart-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_chart_data(n_clicks):
    """Export current chart data to Excel and trigger download"""
    if n_clicks is None:
        return "📁 Export", None
    
    try:
        global current_chart_data
        
        if current_chart_data["data"] is None:
            print("❌ No chart data available")
            return "❌ No Data", None
        
        # Extract data from Plotly figure format
        chart_data = current_chart_data["data"]
        print(f"🔍 Chart data type: {type(chart_data)}")
        print(f"🔍 Chart data: {chart_data}")
        
        # Convert Plotly data to DataFrame format
        export_data = []
        
        if isinstance(chart_data, list) and len(chart_data) > 0:
            trace = chart_data[0]  # Get first trace
            print(f"🔍 Trace type: {type(trace)}")
            print(f"🔍 Trace keys: {trace.keys() if isinstance(trace, dict) else 'Not a dict'}")
            
            # Handle both dict and object formats
            x_data = []
            y_data = []
            
            if isinstance(trace, dict):
                x_data = trace.get('x', [])
                y_raw = trace.get('y', [])
                
                # Handle different y data formats
                if isinstance(y_raw, dict):
                    # Check if it's a complex Plotly data structure
                    if '_inputArray' in y_raw and isinstance(y_raw['_inputArray'], dict):
                        # Extract values from _inputArray
                        input_array = y_raw['_inputArray']
                        y_data = []
                        i = 0
                        while str(i) in input_array:
                            y_data.append(input_array[str(i)])
                            i += 1
                    elif isinstance(y_raw, dict) and all(str(i) in y_raw for i in range(len(x_data))):
                        # Direct dict with numeric string keys
                        y_data = [y_raw[str(i)] for i in range(len(x_data))]
                    else:
                        y_data = list(y_raw.values()) if y_raw else []
                elif isinstance(y_raw, list):
                    y_data = y_raw
                else:
                    y_data = [y_raw] if y_raw is not None else []
                    
            elif hasattr(trace, 'x') and hasattr(trace, 'y'):
                x_data = getattr(trace, 'x', [])
                y_raw = getattr(trace, 'y', [])
                
                # Handle object format
                if hasattr(y_raw, '_inputArray'):
                    input_array = y_raw._inputArray
                    if isinstance(input_array, dict):
                        y_data = []
                        i = 0
                        while str(i) in input_array:
                            y_data.append(input_array[str(i)])
                            i += 1
                    else:
                        y_data = list(input_array) if input_array else []
                else:
                    y_data = list(y_raw) if hasattr(y_raw, '__iter__') else [y_raw]
            
            print(f"🔍 X data length: {len(x_data) if x_data else 0}")
            print(f"🔍 X data sample: {x_data[:3] if x_data else 'None'}")
            print(f"🔍 Y data length: {len(y_data) if y_data else 0}")
            print(f"🔍 Y data sample: {y_data[:3] if y_data else 'None'}")
            print(f"🔍 Y data type: {type(y_data)}")
            
            if x_data and y_data:
                # Ensure both are lists and have the same length
                if not isinstance(x_data, list):
                    x_data = list(x_data) if hasattr(x_data, '__iter__') else [x_data]
                if not isinstance(y_data, list):
                    y_data = list(y_data) if hasattr(y_data, '__iter__') else [y_data]
                
                print(f"🔍 Final X data: {x_data}")
                print(f"🔍 Final Y data: {y_data}")
                
                # Create records for DataFrame
                for i in range(min(len(x_data), len(y_data))):
                    export_data.append({
                        'Name': str(x_data[i]),
                        'Value': str(y_data[i])
                    })
                    
                print(f"🔍 Export data created: {len(export_data)} records")
            else:
                print("❌ No x/y data found in trace")
                return "❌ No Data", None
        else:
            print("❌ Chart data is not a list or is empty")
            return "❌ No Data", None
        
        if not export_data:
            print("❌ No export data created")
            return "❌ No Data", None
        
        # Create DataFrame
        import pandas as pd
        from io import BytesIO
        df = pd.DataFrame(export_data)
        print(f"✅ DataFrame created with {len(df)} rows")
        
        # Create Excel file in memory
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Chart Data', index=False)
            
            # Add metadata sheet
            metadata = pd.DataFrame([{
                'Chart Title': current_chart_data.get("title", "Chart"),
                'Export Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Rows': len(df),
                'Columns': len(df.columns)
            }])
            metadata.to_excel(writer, sheet_name='Metadata', index=False)
        
        buffer.seek(0)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"chart_export_{timestamp}.xlsx"
        
        print(f"✅ Chart data prepared for download: {filename}")
        
        # Encode content as base64 for Dash download
        content_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Return download data with proper format for dcc.Download
        download_data = dict(
            content=content_base64,
            filename=filename,
            base64=True
        )
        
        return "✅ Downloaded!", download_data
            
    except Exception as e:
        print(f"❌ Export error: {e}")
        import traceback
        traceback.print_exc()
        return "❌ Error", None

# Update chart data storage and enable export button
@app.callback(
    Output("export-chart-btn", "disabled"),
    Input("main-chart", "figure"),
    prevent_initial_call=True
)
def update_export_button(figure):
    """Enable export button when chart has data"""
    global current_chart_data
    
    try:
        if figure and "data" in figure and len(figure["data"]) > 0:
            # Store chart data for export
            current_chart_data["data"] = figure["data"]
            # Extract title properly whether it's a string or dict
            title_obj = figure.get("layout", {}).get("title", "Chart")
            if isinstance(title_obj, dict):
                current_chart_data["title"] = title_obj.get("text", "Chart")
            else:
                current_chart_data["title"] = title_obj
            return False  # Enable button
        else:
            return True  # Keep button disabled
    except:
        return True  # Keep button disabled on error

# Callback for color theme selection
@app.callback(
    Output("main-chart", "figure", allow_duplicate=True),
    Input("color-theme-selector", "value"),
    [State("chart-history", "children"),
     State("chart-index", "children")],
    prevent_initial_call=True
)
def update_color_theme(selected_theme, chart_history_json, current_index):
    """Update chart colors when theme is changed"""
    if selected_theme:
        if USE_INTELLIGENT_AGENT:
            intelligent_agent.set_color_theme(selected_theme)
        else:
            chatbot.set_color_theme(selected_theme)
        print(f"🎨 Theme updated to: {selected_theme}")
        
        # Update the current chart with new colors if there's chart history
        if chart_history_json:
            try:
                chart_history = json.loads(chart_history_json)
                current_idx = int(current_index) if current_index else 0
                
                if chart_history and current_idx < len(chart_history):
                    # Get current chart and apply new theme colors
                    chart_data = chart_history[current_idx]
                    fig = go.Figure(chart_data["chart"])
                    
                    # Apply new theme colors to the chart
                    if USE_INTELLIGENT_AGENT:
                        current_palette = intelligent_agent.color_themes.get(selected_theme, intelligent_agent.color_palette)
                    else:
                        current_palette = chatbot.visualization_generator.color_themes.get(selected_theme, chatbot.visualization_generator.color_palette)
                    
                    # Update colors for bar charts
                    for i, trace in enumerate(fig.data):
                        if hasattr(trace, 'marker') and hasattr(trace.marker, 'color'):
                            if hasattr(trace.marker.color, '__len__') and not isinstance(trace.marker.color, str):
                                # Multiple colors (bar chart)
                                new_colors = []
                                for j in range(len(trace.marker.color)):
                                    new_colors.append(current_palette[j % len(current_palette)])
                                trace.marker.color = new_colors
                            else:
                                # Single color
                                trace.marker.color = current_palette[i % len(current_palette)]
                    
                    return fig
            except Exception as e:
                print(f"❌ Error updating chart theme: {e}")
    
    # Return current chart if no theme change or error
    return dash.no_update

if __name__ == "__main__":
    print("🎮 Starting Gaming AI Chatbot...")
    print("📊 Features available:")
    print("   - Steam API integration")
    print("   - SteamSpy statistics")
    print("   - AI-powered responses")
    print("   - Interactive visualizations")
    
    # Get port from environment variable for Render deployment
    # Default to 8050 for local development
    port = int(os.environ.get("PORT", 8050))
    
    # Determine if we're in development or production
    debug_mode = os.environ.get("ENVIRONMENT", "development") == "development"
    
    print(f"\n🌐 Access the app at: http://localhost:{port}")
    
    app.run_server(debug=debug_mode, host="0.0.0.0", port=port)
