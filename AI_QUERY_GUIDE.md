# AI Query to API Mapping Guide

This guide helps the AI understand exactly which API to use for different types of user queries.

## 🎯 TWITCH API - Use for Streaming & Viewership Data

### Functions Available:
- `get_twitch_top_games(limit=10)` - Top games by viewer count
- `get_game_streams(game_name, limit=10)` - Active streams for a game
- `get_streaming_stats(game_name)` - Streaming statistics for a game

### User Query Examples → API Call:
- "What are the top watched games on Twitch?" → `get_twitch_top_games()`
- "What games are most popular on Twitch?" → `get_twitch_top_games()`
- "Top streamed games" → `get_twitch_top_games()`
- "What's trending on Twitch?" → `get_twitch_top_games()`
- "Most viewed games on Twitch" → `get_twitch_top_games()`
- "Twitch viewer counts" → `get_twitch_top_games()`
- "Show me popular Twitch games" → `get_twitch_top_games()`

### Important:
- Results contain "viewer_count" (NOT "players")
- Always use "viewers" in descriptions, not "players"
- Perfect for real-time streaming popularity

---

## 🎮 STEAM API - Use for Player Counts & Steam Rankings

### Functions Available:
- `get_steam_top_games(category="concurrent_players")` - Top by current players
- `get_steam_top_games(category="top_sellers")` - Best selling games
- `get_steam_top_games(category="new_releases")` - New releases

### User Query Examples → API Call:
- "What are the top games on Steam?" → `get_steam_top_games(category="concurrent_players")`
- "Most played Steam games" → `get_steam_top_games(category="concurrent_players")`
- "Top Steam games by players" → `get_steam_top_games(category="concurrent_players")`
- "Steam bestsellers" → `get_steam_top_games(category="top_sellers")`
- "New Steam games" → `get_steam_top_games(category="new_releases")`
- "Popular games on Steam" → `get_steam_top_games(category="concurrent_players")`

### Important:
- Results contain "players" or "concurrent_players"
- Use "players" in descriptions
- Perfect for actual gameplay activity

---

## 📊 STEAMSPY API - Use for Ownership & Engagement

### Functions Available:
- `get_game_details(game_name)` - Detailed stats for specific games

### User Query Examples → API Call:
- "Tell me about [Game Name]" → `get_game_details(game_name)`
- "Statistics for Counter-Strike 2" → `get_game_details("Counter-Strike 2")`
- "How many people own [Game]?" → `get_game_details(game_name)`
- "Player engagement for [Game]" → `get_game_details(game_name)`
- "Show me [Game] statistics" → `get_game_details(game_name)`

### Important:
- Provides ownership estimates, playtime data
- Use for detailed individual game analysis

---

## 🎯 RAWG API - Use for Game Database & Metadata

### Functions Available:
- `search_rawg_games(query, limit=10)` - Search games database
- `get_game_metadata(game_name)` - Detailed game information
- `get_game_reviews(game_name)` - Review scores and ratings

### User Query Examples → API Call:
- "Find games like The Witcher 3" → `search_rawg_games("witcher 3 similar")`
- "Search for RPG games" → `search_rawg_games("RPG")`
- "Games by Valve" → `search_rawg_games("valve")`
- "Show me indie games" → `search_rawg_games("indie")`
- "What games are similar to [Game]?" → `search_rawg_games(game_name + " similar")`

### Important:
- Best for discovery and metadata
- Cross-platform game information
- Ratings and review data

---

## 💼 GAMALYTIC API - Use for Market & Industry Data

### Functions Available:
- `get_market_analysis(region="global")` - Market analysis by region
- `get_genre_analysis(genres)` - Genre performance data
- `get_trends_data(time_period="1y")` - Industry trends over time

### User Query Examples → API Call:
- "Gaming market trends" → `get_trends_data()`
- "Industry analysis" → `get_market_analysis()`
- "Market share by platform" → `get_market_analysis()`
- "How is the RPG genre performing?" → `get_genre_analysis(["RPG"])`
- "Gaming industry growth" → `get_trends_data()`

### Important:
- Use for business intelligence
- Market and revenue data
- Industry-wide trends

---

## 🎨 VISUALIZATION REQUIREMENTS

**CRITICAL RULE:** After EVERY data API call, you MUST call `generate_visualization()`

### Required Parameters:
- `chart_type`: "bar" (rankings), "line" (trends), "pie" (categories)
- `data_source`: The exact API used (e.g., "twitch_top_games", "steam_top_games")
- `title`: Descriptive chart title

### Examples:
```
User: "What are the top games on Twitch?"
Step 1: get_twitch_top_games()
Step 2: generate_visualization(chart_type="bar", data_source="twitch_top_games", title="Top Games on Twitch by Viewers")

User: "Top Steam games?"
Step 1: get_steam_top_games(category="concurrent_players")
Step 2: generate_visualization(chart_type="bar", data_source="steam_top_games", title="Top Steam Games by Players")
```

**ONLY SKIP VISUALIZATION IF:** User says "text only", "no chart", "no visualization"

---

## 🚨 COMMON MISTAKES TO AVOID

1. **Wrong API for Query Type:**
   - ❌ Using Steam API for "Twitch" questions
   - ❌ Using Twitch API for "Steam" questions

2. **Wrong Data Labels:**
   - ❌ Calling Twitch "viewers" as "players"
   - ❌ Calling Steam "players" as "viewers"

3. **Missing Visualizations:**
   - ❌ Getting data but not calling `generate_visualization()`
   - ❌ Promising to create charts but not actually doing it

4. **Wrong Function Parameters:**
   - ❌ Using wrong Steam category (use "concurrent_players" for most queries)
   - ❌ Not specifying proper search terms for RAWG

---

## ✅ SUCCESS WORKFLOW

1. **Parse user query** → Identify intent (Twitch? Steam? Specific game? Market data?)
2. **Call appropriate API** → Use exact function with proper parameters
3. **ALWAYS call visualization** → Unless explicitly told not to
4. **Use correct terminology** → "viewers" for Twitch, "players" for Steam
5. **Provide clear response** → State data source and present clean results
