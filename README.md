# Gaming AI Chatbot

A comprehensive gaming analytics platform that combines multiple gaming APIs and intelligent processing to provide insights into gaming trends, player statistics, and game performance.

## Features

- 🤖 **Intelligent Gaming Agent**: Natural language interface for querying gaming data
- 📊 **Multi-API Integration**: Access to Steam, SteamSpy, RAWG, Twitch, and Gamalytic APIs
- 📈 **Interactive Visualizations**: Automatically generated charts and graphs
- 🔄 **API Usage Monitoring**: Track API usage and stay within rate limits
- 🎮 **Game Analytics**: In-depth analysis of player behavior, game popularity, and trends
- 🔍 **Similar Games Analysis**: Find games with overlapping player demographics
- 📱 **Responsive Web Interface**: Easy-to-use dashboard for all gaming analytics

## Getting Started

### Prerequisites

- Python 3.8+
- API keys for:
  - Steam Web API
  - RAWG API
  - Twitch API
  - Gamalytic API (optional)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/gaming_ai.git
   cd gaming_ai
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your API keys:
   ```
   STEAM_API_KEY=your_steam_api_key
   RAWG_API_KEY=your_rawg_api_key
   TWITCH_CLIENT_ID=your_twitch_client_id
   TWITCH_CLIENT_SECRET=your_twitch_client_secret
   GAMALYTIC_API_KEY=your_gamalytic_api_key
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Access the web interface at `http://localhost:8050`

## Usage

### Example Queries

- "What are the top games on Steam right now?"
- "What games are most popular on Twitch?"
- "What other games do Elden Ring players also play?"
- "Tell me about Cyberpunk 2077"
- "Show me player statistics for Counter-Strike 2"
- "Compare the popularity of RPG vs Action games"

### Features

- **Chat Interface**: Natural language interaction with the AI agent
- **Visualizations**: Automatically generated charts based on queries
- **Data Export**: Download visualization data in various formats
- **API Usage Monitoring**: Track your API usage to avoid rate limits
- **Multiple Data Sources**: Access comprehensive gaming data across platforms

## API Sources

- **Steam Web API**: Player statistics, game details, user profiles
- **SteamSpy API**: Game ownership, playtime, engagement analytics
- **RAWG API**: Game metadata, ratings, platforms, screenshots
- **Twitch API**: Streaming data, viewer counts, broadcaster metrics
- **Gamalytic API**: Player behavior analysis, market insights, audience overlap

## Architecture

- **Dash/Flask**: Web application framework
- **Plotly**: Data visualization
- **Python**: Backend processing
- **Intelligent Agent**: Natural language understanding and query processing
- **API Integration**: Multiple gaming data sources with fallback handling
- **Visualization Generator**: Automated chart creation based on data type

## Project Structure

- `app.py` - Main Dash application
- `agent/` - Chatbot agent logic (standard and Pydantic variants)
- `apis/` - API integration modules for gaming data sources
- `utils/` - Utility functions and data processing
- `test_*.py` - Test scripts for different components

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Usage

Ask questions like:
- "What are the top games on Steam this week?"
- "Show me player count trends for Cyberpunk 2077"
- "Compare the performance of indie vs AAA games"
- "Generate a chart of gaming revenue by genre"

## 🔑 API Key Summary

| Service | Cost | Monthly Limit | What You Get |
|---------|------|---------------|--------------|
| **OpenAI** | $5-15/month | Usage-based | AI responses, function calling |
| **Steam** | Free | Rate limited | Game data, player counts (you have this) |
| **RAWG** | Free | 20k requests | Game database, reviews, ratings |
| **Twitch** | Free | Rate limited | Streaming data, popularity trends |
| **Gamalytic** | $99+/month | Varies | Professional industry insights |

**Recommended setup for most users:** OpenAI + Steam + RAWG = Real gaming insights for ~$5-15/month
