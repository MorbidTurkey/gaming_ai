# 🎮 Gaming AI Chatbot - Setup Guide

## Overview

This is a comprehensive gaming industry chatbot built with Dash that can:
- Answer questions about gaming trends and statistics
- Call multiple gaming APIs (Steam, SteamSpy, Gamalytic)
- Generate interactive visualizations with Plotly
- Maintain conversation memory
- Use OpenAI for natural language understanding

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
```
OPENAI_API_KEY=your_openai_key_here
STEAM_API_KEY=your_steam_key_here
```

### 3. Test the Setup

```bash
python test_setup.py
```

### 4. Run the Application

**Option A: Direct run**
```bash
python app.py
```

**Option B: Using startup script**
```bash
python start.py
```

The app will be available at: http://localhost:8050

## 📁 Project Structure

```
gaming_ai/
├── app.py                 # Main Dash application
├── start.py              # Startup script with setup checks
├── test_setup.py         # System test script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # Project documentation
├── agent/
│   ├── __init__.py
│   └── chatbot_agent.py # Main AI agent with OpenAI integration
├── apis/
│   ├── __init__.py
│   ├── steam_api.py     # Steam Web API client
│   ├── steamspy_api.py  # SteamSpy API client
│   └── gamalytic_api.py # Gamalytic API client
└── utils/
    ├── __init__.py
    └── visualization.py  # Plotly chart generator
```

## 🔑 Required API Keys

### OpenAI API Key (Required)
- Sign up at: https://platform.openai.com/
- Create an API key in your dashboard
- Add to `.env` as `OPENAI_API_KEY`

### Steam API Key (Optional)
- Sign up at: https://steamcommunity.com/dev/apikey
- Add to `.env` as `STEAM_API_KEY`
- Note: Without this, Steam API will use mock data

## 💬 Example Questions

Try asking the chatbot:

- **Game Statistics:**
  - "What are the top games on Steam right now?"
  - "Show me player count data for Counter-Strike 2"
  - "Get details about Baldur's Gate 3"

- **Market Analysis:**
  - "Compare RPG vs Action game performance"
  - "Show me gaming market trends by platform"
  - "Analyze the indie game market"

- **Visualizations:**
  - "Generate a chart of top games by player count"
  - "Create a pie chart of gaming revenue by genre"
  - "Show player trends over time for popular games"

## 🛠️ Features

### AI Agent Capabilities
- **Natural Language Processing:** Uses OpenAI GPT-4o for understanding queries
- **Function Calling:** Automatically calls appropriate APIs based on user questions
- **Memory:** Maintains conversation history for context
- **Error Handling:** Graceful fallbacks when APIs are unavailable

### Data Sources
- **Steam API:** Live game data, player counts, store information
- **SteamSpy:** Game statistics, ownership data, historical trends
- **Gamalytic:** Industry insights, market analysis (mock data for demo)

### Visualizations
- **Interactive Charts:** Line charts, bar charts, pie charts, scatter plots
- **Real-time Updates:** Charts update based on chatbot responses
- **Dark Theme:** Gaming-focused dark theme for better UX

### Web Interface
- **Modern UI:** Built with Dash and Bootstrap components
- **Responsive Design:** Works on desktop and mobile
- **Chat Interface:** Real-time conversation with the AI
- **Example Prompts:** Quick-start buttons for common questions

## 🔧 Development

### Adding New APIs
1. Create a new API client in `apis/` directory
2. Add the client to `agent/chatbot_agent.py`
3. Define new functions and tools for OpenAI

### Adding New Chart Types
1. Add new chart methods to `utils/visualization.py`
2. Update the `generate_visualization` function in the agent
3. Add new chart types to the OpenAI tools definition

### Customizing the UI
- Edit `app.py` for layout changes
- Modify styles in the Dash components
- Add new cards or sections as needed

## 🐛 Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install -r requirements.txt
```

**OpenAI API Errors:**
- Check your API key in `.env`
- Ensure you have credits in your OpenAI account
- Verify the API key has the correct permissions

**Port Already in Use:**
- Change the port in `app.py`: `app.run_server(port=8051)`
- Or kill the process using port 8050

**API Rate Limits:**
- The code includes rate limiting for external APIs
- For heavy usage, consider caching responses

### Getting Help

1. Run the test script: `python test_setup.py`
2. Check the console output for specific error messages
3. Ensure all dependencies are installed correctly
4. Verify your `.env` file has the correct API keys

## 🚀 Deployment

### Local Development
The current setup is perfect for local development and testing.

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (e.g., Gunicorn)
- Setting up environment variables securely
- Adding authentication if needed
- Implementing proper logging
- Using a reverse proxy (nginx)

### Docker (Optional)
You can containerize the application:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8050
CMD ["python", "app.py"]
```

## 📈 Future Enhancements

Potential improvements:
- [ ] Add more gaming APIs (IGDB, Epic Games, etc.)
- [ ] Implement user authentication
- [ ] Add data persistence/database
- [ ] Create scheduled reports
- [ ] Add export functionality for charts
- [ ] Implement WebSocket for real-time updates
- [ ] Add voice input/output
- [ ] Create mobile app version

## 📄 License

This project is for educational and demonstration purposes. Make sure to respect the terms of service of all integrated APIs.
