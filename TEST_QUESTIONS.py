"""
🎮 Gaming AI Chatbot - Comprehensive Test Questions

This file contains sample questions to test all APIs, functions, and features
of the enhanced Gaming AI system with DataFrame processing and export capabilities.

EXPORT INSTRUCTIONS:
- Users can now export data by:
  1. Asking "export to Excel" in their chat messages
  2. Clicking the "📁 Export" button next to charts
  3. Requesting "table format" with export options
"""

# =============================================================================
# 🎯 BASIC API TESTING - Individual API Functions
# =============================================================================

STEAM_API_TESTS = [
    "Show me the top 10 Steam games by player count",
    "What are the most popular games on Steam right now?",
    "Give me Steam's top games in a bar chart",
    "Show me current Steam player statistics",
    "What games have the highest concurrent players on Steam?",
    "Display Steam top games data in a table I can export to Excel"
]

TWITCH_API_TESTS = [
    "What are the top games being streamed on Twitch?",
    "Show me Twitch viewer counts for top games",
    "Give me a chart of most watched games on Twitch",
    "What games have the highest Twitch viewership?",
    "Display Twitch streaming data in a table format",
    "Show me Twitch top games and export the data"
]

RAWG_API_TESTS = [
    "Find information about Cyberpunk 2077",
    "Get game details for The Witcher 3",
    "Show me metadata for Call of Duty",
    "What's the rating for Elden Ring?",
    "Give me detailed info about Counter-Strike 2",
    "Search for indie games with high ratings"
]

GAMALYTIC_API_TESTS = [
    "Show me gaming market analysis",
    "What are the latest gaming industry trends?",
    "Give me market segments breakdown",
    "Show gaming revenue by platform",
    "Display market analysis in a pie chart",
    "Show me gaming industry insights with export options"
]

STEAMSPY_API_TESTS = [
    "Get ownership statistics for popular games",
    "Show me player demographics data",
    "What are the sales estimates for top games?",
    "Give me ownership data for Steam games",
    "Display player statistics in a chart"
]

# =============================================================================
# 🔍 ENHANCED AI FEATURES - DataFrame & Multi-API
# =============================================================================

MULTI_API_COMPARISON_TESTS = [
    "Compare Steam player counts with Twitch viewership",
    "Show me data from both Steam and Twitch in one chart",
    "Compare gaming platforms - Steam vs Twitch data",
    "Give me a comprehensive analysis using Steam, Twitch, and RAWG",
    "Show me multi-platform gaming data with export to Excel",
    "Create a table comparing Steam players and Twitch viewers"
]

DATAFRAME_PROCESSING_TESTS = [
    "Give me gaming data in a table format",
    "Show me detailed analytics with all available metrics",
    "Create a comprehensive data analysis with multiple APIs",
    "Process data from Steam, Twitch, and market analysis",
    "Generate a detailed report with all gaming metrics",
    "Show me structured data that I can export"
]

CHART_TYPE_INTELLIGENCE_TESTS = [
    "Show me trending games data (should auto-select line chart)",
    "Give me genre distribution (should suggest pie chart)",
    "Compare player counts across games (should use bar chart)",
    "Show me correlation between ratings and prices (should use scatter)",
    "Display detailed game metrics (should suggest table)",
    "Show me gaming data trends over time"
]

# =============================================================================
# 📊 EXPORT FUNCTIONALITY TESTING
# =============================================================================

EXPORT_SPECIFIC_TESTS = [
    "Show me Steam data and export it to Excel",
    "Give me a table of gaming data that I can download",
    "Create a comprehensive report I can export",
    "Show me Twitch data in Excel format",
    "Generate gaming analytics with export capabilities",
    "I want downloadable data from multiple gaming APIs",
    "Create a table with gaming metrics and export options",
    "Show me detailed analytics that I can save as Excel"
]

TABLE_VISUALIZATION_TESTS = [
    "Display gaming data in a table",
    "Show me tabular format of Steam games",
    "Create a data table with Twitch viewer counts",
    "Give me a formatted table of game information",
    "Display comprehensive gaming data in table format",
    "Show me all available metrics in a table view"
]

# =============================================================================
# 🤖 AI INTELLIGENCE & UNDERSTANDING TESTS
# =============================================================================

COMPLEX_ANALYSIS_TESTS = [
    "Analyze the gaming market and show me key insights",
    "What metrics should I track for game performance?",
    "Give me a complete picture of gaming trends with data",
    "Show me the relationship between different gaming metrics",
    "Provide comprehensive gaming industry analysis",
    "What are the most important gaming KPIs to monitor?"
]

NATURAL_LANGUAGE_TESTS = [
    "I need gaming data for my presentation",
    "Help me understand current gaming trends",
    "What's happening in the gaming industry right now?",
    "Give me insights about popular games",
    "I'm researching gaming market dynamics",
    "Show me what gamers are playing most"
]

AXIS_AND_METRICS_TESTS = [
    "Show me player count as the main metric",
    "Display viewer numbers on the Y-axis",
    "Create a chart with games on X-axis and ratings on Y-axis", 
    "I want to see revenue data across different categories",
    "Show me time-based trends with proper axis labels",
    "Display correlation between game price and user ratings"
]

# =============================================================================
# 🚀 ADVANCED FEATURE TESTING
# =============================================================================

ERROR_HANDLING_TESTS = [
    "Show me data for a non-existent game",
    "Get information about invalid API endpoints",
    "Display charts with missing data",
    "Export empty datasets",
    "Handle API rate limit scenarios"
]

PERFORMANCE_TESTS = [
    "Get data from all APIs simultaneously",
    "Create multiple charts with large datasets",
    "Export large amounts of gaming data",
    "Process complex multi-API queries",
    "Generate comprehensive reports with all features"
]

EDGE_CASE_TESTS = [
    "Show me data and then export it multiple times",
    "Create charts with very small datasets",
    "Handle special characters in game names",
    "Process data with missing values",
    "Export data with different formats"
]

# =============================================================================
# 📋 TESTING CHECKLIST
# =============================================================================

TESTING_CHECKLIST = """
✅ API Integration Tests:
- [ ] Steam API: Player counts, top games
- [ ] Twitch API: Viewer counts, streaming data  
- [ ] RAWG API: Game metadata, ratings
- [ ] Gamalytic API: Market analysis, trends
- [ ] SteamSpy API: Ownership statistics

✅ DataFrame Processing Tests:
- [ ] Data standardization across APIs
- [ ] Multi-API data combination
- [ ] Column mapping and type conversion
- [ ] Summary statistics generation

✅ Visualization Tests:
- [ ] Bar charts for rankings
- [ ] Pie charts for distributions  
- [ ] Table charts for detailed data
- [ ] Auto chart type selection
- [ ] Custom chart recommendations

✅ Export Functionality Tests:
- [ ] Excel export with data sheets
- [ ] CSV export for data portability
- [ ] Export button in UI
- [ ] Chat-based export requests
- [ ] Metadata and summary inclusion

✅ AI Intelligence Tests:
- [ ] Natural language understanding
- [ ] API selection based on context
- [ ] Chart type recommendations
- [ ] Axis and metric identification
- [ ] Export intent recognition

✅ UI/UX Tests:
- [ ] Export button activation
- [ ] Chart navigation
- [ ] Gauge positioning
- [ ] Error message display
- [ ] Loading states
"""

# =============================================================================
# 🎯 RECOMMENDED TEST SEQUENCE
# =============================================================================

RECOMMENDED_TEST_SEQUENCE = [
    # 1. Basic API functionality
    "Show me top Steam games",
    "What are popular Twitch games?", 
    "Get info about Cyberpunk 2077",
    
    # 2. Enhanced DataFrame features
    "Compare Steam and Twitch data",
    "Show me gaming data in a table",
    
    # 3. Export functionality
    "Give me Steam data I can export to Excel",
    # Then click the Export button in UI
    
    # 4. Advanced AI features
    "Create comprehensive gaming analytics with export options",
    "Show me multi-platform data analysis",
    
    # 5. Edge cases
    "Export data for non-existent games",
    "Show me very detailed analytics"
]

if __name__ == "__main__":
    print("🎮 Gaming AI Test Questions Loaded!")
    print(f"📊 Total test categories: 10")
    print(f"🔍 Total test questions: {len(STEAM_API_TESTS + TWITCH_API_TESTS + RAWG_API_TESTS + GAMALYTIC_API_TESTS + STEAMSPY_API_TESTS + MULTI_API_COMPARISON_TESTS + DATAFRAME_PROCESSING_TESTS + EXPORT_SPECIFIC_TESTS + COMPLEX_ANALYSIS_TESTS + NATURAL_LANGUAGE_TESTS)}")
    print("\n🚀 Ready for comprehensive testing!")
