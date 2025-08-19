# API Documentation Summary

## RAWG API (https://api.rawg.io/docs/)

### Authentication
- Requires API key: `?key=YOUR_API_KEY`
- Rate limit: 20,000 requests/month (free tier)

### Key Endpoints

#### 1. Games Search
- **Endpoint**: `GET /games`
- **Parameters**:
  - `search` (string): Search query
  - `page_size` (int): Results per page (1-40, default 20)
  - `page` (int): Page number
  - `ordering` (string): Sort by (-released, -rating, -added, etc.)
  - `genres` (string): Genre slug
  - `platforms` (string): Platform ID
  - `developers` (string): Developer ID
- **Returns**: List of games with basic info

#### 2. Game Details
- **Endpoint**: `GET /games/{id}`
- **Parameters**: Game ID (integer)
- **Returns**: Full game details including description, ratings, platforms, etc.

#### 3. Game Reviews
- **Endpoint**: `GET /games/{id}/reviews`
- **Parameters**: 
  - Game ID (integer)
  - `page_size` (int): Results per page
- **Returns**: User reviews for the game

#### 4. Genres
- **Endpoint**: `GET /genres`
- **Returns**: List of all available genres

### Data Structure
```json
{
  "id": 41561,
  "name": "Total War: Rome II",
  "released": "2013-09-03",
  "rating": 4.18,
  "ratings_count": 61,
  "metacritic": 76,
  "platforms": [{"platform": {"name": "PC"}}],
  "genres": [{"name": "Strategy"}],
  "developers": [{"name": "Creative Assembly"}]
}
```

## Steam Web API (https://partner.steamgames.com/doc/webapi_overview)

### Authentication
- Requires Web API key
- Rate limit: 100,000 requests/day

### Key Endpoints

#### 1. App List
- **Endpoint**: `ISteamApps/GetAppList/v2/`
- **Returns**: List of all Steam apps with appid and name

#### 2. App Details
- **Endpoint**: `ISteamUserStats/GetSchemaForGame/v2/`
- **Parameters**: `appid` (integer)

#### 3. Player Count
- **Endpoint**: `ISteamUserStats/GetNumberOfCurrentPlayers/v1/`
- **Parameters**: `appid` (integer)

### Data Structure
- Uses `appid` (integer) as primary identifier
- Game names are NOT direct API parameters - need appid lookup

## SteamSpy API (https://steamspy.com/api.php)

### Rate Limits
- 1 request/second for most requests
- 1 request/60 seconds for bulk requests

### Key Endpoints

#### 1. App Details
- **Endpoint**: `?request=appdetails&appid={appid}`
- **Parameters**: `appid` (integer)
- **Returns**: Ownership, playtime, price data

#### 2. Top Games
- **Endpoint**: `?request=top100in2weeks`
- **Returns**: Top 100 games by recent players

#### 3. Genre Data
- **Endpoint**: `?request=genre&genre={genre_name}`
- **Parameters**: `genre` (string, URL encoded)

### Data Structure
```json
{
  "appid": 730,
  "name": "Counter-Strike: Global Offensive",
  "owners": "50,000,000 .. 100,000,000",
  "average_forever": 334,
  "average_2weeks": 89,
  "price": "0"
}
```

## Twitch API (https://dev.twitch.tv/docs/)

### Authentication
- Requires Client ID + Client Secret for OAuth
- Rate limit: 800 requests/minute

### Key Endpoints

#### 1. Top Games
- **Endpoint**: `GET /games/top`
- **Parameters**: `first` (int, max 100)
- **Returns**: Most viewed games by viewer count

#### 2. Game Search
- **Endpoint**: `GET /games`
- **Parameters**: 
  - `name` (string): Exact game name
  - `id` (string): Game ID
- **Returns**: Game info with Twitch game ID

#### 3. Streams
- **Endpoint**: `GET /streams`
- **Parameters**:
  - `game_id` (string): Twitch game ID
  - `first` (int): Number of streams

### Data Structure
- Uses Twitch `game_id` (string) as identifier
- Game names can be used directly for search

## Key Integration Patterns

### Game Name → API ID Resolution
1. **RAWG**: Use game name directly in search, get integer ID
2. **Steam**: Need to lookup appid from name via app list
3. **SteamSpy**: Uses same appid as Steam
4. **Twitch**: Use game name directly, get string game_id

### Cross-API Data Flow
```
User: "rome total war 2"
↓
1. RAWG search → get game details (name, rating, release date)
2. Steam lookup → find appid → get player count
3. SteamSpy → use appid → get ownership data  
4. Twitch search → get game_id → get streaming data
```

### Real Data Requirements
- **NO MOCK DATA** - all responses must come from actual API calls
- **Fallback chains**: RAWG → Steam → SteamSpy for game info
- **ID translation**: Always resolve names to proper IDs for each API
- **Error handling**: If one API fails, try alternatives
