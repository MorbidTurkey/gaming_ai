# Comprehensive Gaming API Reference

This document contains the complete reference for all gaming APIs used in the Gaming AI Chatbot system.

## Table of Contents
1. [Gamalytic API](#gamalytic-api)
2. [Steam Web API](#steam-web-api)
3. [SteamSpy API](#steamspy-api)
4. [RAWG API](#rawg-api)
5. [Twitch API](#twitch-api)

---

## Gamalytic API

**Base URL**: `https://api.gamalytic.com/v1/`
**Authentication**: Bearer token in Authorization header
**Rate Limits**: 
- Free: 500 requests/day
- Starter: 2,500 requests/day  
- Pro: Unlimited

### Endpoints

#### 1. Get Game Details
- **Endpoint**: `GET /game/{id}`
- **Description**: Returns comprehensive game details including audience overlap data
- **Parameters**:
  - `id` (path, required): Steam game ID

#### 2. Steam Games List
- **Endpoint**: `GET /steam-games/list`
- **Description**: Returns a list of up to 1000 games with basic information
- **Parameters**:
  - `search` (query, optional): Search term to filter games
  - `limit` (query, optional): Number of results to return (max 1000)

#### 3. Game Regional History
- **Endpoint**: `GET /game/{id}/regional-history`
- **Description**: Returns regional sales/revenue history

#### 4. Game Regional Price History
- **Endpoint**: `GET /game/{id}/regional-price-history`
- **Description**: Returns regional price history

#### 5. Game Change History
- **Endpoint**: `GET /game/{id}/change-history`
- **Description**: Returns game change history

#### 6. Wishlist Insights
- **Endpoint**: `GET /game/{id}/wishlist-insights`
- **Description**: Returns detailed game wishlist data

#### 7. Active Users History
- **Endpoint**: `GET /game/{id}/active-users-history`
- **Description**: Returns DAU/MAU history

#### 8. Review Sentiment
- **Endpoint**: `GET /game/{id}/review-sentiment`
- **Description**: Returns LLM based review sentiment summaries

#### 9. Active Users by Region
- **Endpoint**: `GET /game/{id}/active-users-regions`
- **Description**: Returns MAU percentage by country

#### 10. Global Game Stats
- **Endpoint**: `GET /steam-games/stats`
- **Description**: Returns global games stats

#### 11. Genre Stats
- **Endpoint**: `GET /steam-games/genres/stats`
- **Description**: Returns global game stats grouped by criteria

### Complete Game Object Schema

```json
{
  "steamId": "730",
  "name": "Counter-Strike 2",
  "description": "string",
  "price": 59.99,
  "reviews": 1234,
  "reviewsSteam": 1234,
  "followers": 1000,
  "avgPlaytime": 14.9,
  "reviewScore": 87,
  "tags": [
    "Open World",
    "Story Rich",
    "Western",
    "Adventure",
    "Multiplayer"
  ],
  "genres": [
    "Action",
    "Adventure"
  ],
  "features": [
    "Single-player",
    "Online PvP",
    "Online Co-op",
    "Steam Achievements",
    "In-App Purchases",
    "Remote Play on Phone",
    "Remote Play on Tablet"
  ],
  "languages": [
    "English",
    "French",
    "Italian"
  ],
  "developers": [
    "Valve"
  ],
  "publishers": [
    "Valve"
  ],
  "copiesSold": 1000,
  "players": 2000,
  "owners": 4000,
  "revenue": 5000,
  "totalRevenue": 6000,
  "estimateDetails": {
    "rankBased": 15322140,
    "playtimeBased": 13324589,
    "reviewBased": 20427660
  },
  "wishlists": 2000,
  "firstReleaseDate": 1575522000000,
  "earlyAccessExitDate": 1675522000000,
  "releaseDate": 1675522000000,
  "EAReleaseDate": 1575522000000,
  "unreleased": false,
  "earlyAccess": false,
  "countryData": {
    "cn": 34.8,
    "us": 15.8,
    "tr": 3.6
  },
  "itemType": "game",
  "itemCode": 0,
  "DLC": [
    "string"
  ],
  "history": [
    {
      "timeStamp": 1420070400000,
      "reviews": 292666,
      "price": 7.49,
      "score": 93,
      "players": 183683.687,
      "avgPlaytime": 1.0237,
      "sales": 10129448,
      "revenue": 750738,
      "followers": 1000,
      "wishlists": 5000
    }
  ],
  "playtimeData": {
    "median": 34.93333333333333,
    "distribution": {
      "0-1h": 4.885496183206107,
      "1-5h": 14.525627044711015,
      "5-10h": 11.232279171210468,
      "10-20h": 11.930207197382769,
      "20-50h": 18.21882951653944,
      "50-100h": 19.680116321337696,
      "100-500h": 18.25517993456925,
      "500-1000h": 1.2722646310432568
    }
  },
  "alsoPlayed": [
    {
      "steamId": 0,
      "link": 0,
      "name": "string",
      "releaseDate": 0,
      "price": 0,
      "genres": [
        "string"
      ],
      "copiesSold": 0,
      "revenue": 0
    }
  ],
  "audienceOverlap": [
    {
      "steamId": 0,
      "link": 0,
      "name": "string",
      "releaseDate": 0,
      "price": 0,
      "genres": [
        "string"
      ],
      "copiesSold": 0,
      "revenue": 0
    }
  ]
}
```

### Key Data Points for "Also Played" Analysis
- **`alsoPlayed`**: Games that players of this game also play
- **`audienceOverlap`**: Games with overlapping player demographics
- **`countryData`**: Geographic distribution of players
- **`playtimeData`**: Player engagement patterns

---

## Steam Web API

**Base URL**: `https://api.steampowered.com/`
**Authentication**: API key parameter `?key=YOUR_API_KEY`
**Rate Limits**: 100,000 calls per day

### Core Endpoints

#### Player Services (IPlayerService)
1. **GetRecentlyPlayedGames** - Games played in last 2 weeks
2. **GetOwnedGames** - Complete player game library
3. **GetSteamLevel** - Player's Steam account level
4. **GetBadges** - Badge collection and progress
5. **GetCommunityBadgeProgress** - Community achievements
6. **IsPlayingSharedGame** - Family sharing detection

#### User Data (ISteamUser)
1. **GetPlayerSummaries** - Player profiles and status
2. **GetFriendList** - Social connections and friends
3. **GetPlayerBans** - VAC and community ban status

#### App Data (ISteamApps)
1. **GetAppList** - Complete Steam game catalog
2. **GetServersAtAddress** - Server information
3. **CheckAppOwnership** - Verify game ownership

#### News & Content (ISteamNews)
1. **GetNewsForApp** - Game news and updates

---

## SteamSpy API

**Base URL**: `https://steamspy.com/api.php`
**Authentication**: None required
**Rate Limits**: 1 request/second, 60 seconds for bulk requests

### Endpoints

#### Core Data Endpoints
1. **appdetails** - Detailed statistics for specific games (requires appid)
2. **top100in2weeks** - Top 100 games by players in last 2 weeks
3. **top100forever** - Top 100 games by players since March 2009
4. **top100owned** - Top 100 games by total ownership
5. **genre** - Games filtered by specific genre
6. **tag** - Games filtered by specific tag
7. **all** - Complete Steam catalog with ownership data

### Available Metrics
- **owners**: Estimated ownership ranges
- **average_forever**: Average playtime since March 2009 (minutes)
- **average_2weeks**: Average playtime in last 2 weeks (minutes)
- **median_forever**: Median playtime since March 2009 (minutes)
- **median_2weeks**: Median playtime in last 2 weeks (minutes)
- **ccu**: Peak concurrent users yesterday
- **score_rank**: User review score ranking
- **price**: Current US price in cents
- **initialprice**: Original US price in cents
- **discount**: Current discount percentage

---

## RAWG API

**Base URL**: `https://api.rawg.io/api/`
**Authentication**: API key parameter `?key=YOUR_API_KEY`
**Rate Limits**: 20,000 requests/month (free tier)

### Key Endpoints
1. **GET /games** - Search games
2. **GET /games/{id}** - Game details
3. **GET /games/{id}/reviews** - User reviews
4. **GET /genres** - Available genres
5. **GET /platforms** - Gaming platforms
6. **GET /developers** - Game developers
7. **GET /publishers** - Game publishers

---

## Twitch API

**Base URL**: `https://api.twitch.tv/helix/`
**Authentication**: OAuth 2.0 Bearer token
**Rate Limits**: Varies by endpoint

### Analytics Endpoints
1. **GET /analytics/extensions** - Extension analytics reports
2. **GET /analytics/games** - Game analytics reports
3. **GET /bits/leaderboard** - Bits leaderboard data
4. **GET /analytics/extensions/transactions** - Extension transaction data

### Game & Stream Data
1. **GET /games** - Game information
2. **GET /streams** - Live stream data
3. **GET /clips** - Video clips
4. **GET /videos** - VOD data

---

## Implementation Guidelines

### For "What other games do players also play?" queries:

1. **Primary Method (Gamalytic)**: Use `/game/{id}` endpoint and parse `alsoPlayed` array
2. **Fallback Method (SteamSpy)**: Use genre/tag analysis for similar games
3. **Supplementary (Steam)**: Use user library analysis for behavioral patterns

### Error Handling
All APIs should return consistent error messages:
```
"Unable to access {API_NAME} API, please add an API key or check with your system admin."
```

### Data Processing
- Convert all timestamps to ISO format
- Normalize price data to USD
- Standardize game names and IDs across APIs
- Merge data from multiple sources when possible

---

This reference should be used as the source of truth for all API implementations in the Gaming AI Chatbot system.
