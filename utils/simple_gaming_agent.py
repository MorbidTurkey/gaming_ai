"""
Simple Gaming Agent - Uses structured metric-based approach

This agent uses the metric registry to match user queries to specific
data retrievals and chart generation.
"""

from typing import Tuple, Optional, Dict, Any
import pandas as pd

from utils.metric_registry import MetricRegistry
from utils.data_retriever import DataRetriever
from utils.simple_chart_generator import SimpleChartGenerator

class SimpleGamingAgent:
    """Simple structured gaming agent"""
    
    def __init__(self, apis):
        """
        Initialize with API instances
        
        Args:
            apis: Object containing API instances (steam_api, twitch_api, etc.)
        """
        self.apis = apis
        self.metric_registry = MetricRegistry()
        self.data_retriever = DataRetriever(apis)
        self.chart_generator = SimpleChartGenerator()
    
    def respond(self, user_query: str) -> Tuple[str, Optional[Dict]]:
        """
        Process user query and return response with visualization
        
        Args:
            user_query: User's natural language query
            
        Returns:
            Tuple of (text_response, visualization_dict)
        """
        print(f"🎯 SIMPLE AGENT PROCESSING: {user_query}")
        
        # Step 1: Find matching metric
        metric_key = self.metric_registry.find_metric(user_query)
        
        if not metric_key:
            return self._handle_unknown_query(user_query)
        
        print(f"✅ Found metric: {metric_key}")
        
        # Step 2: Get metric information
        metric_info = self.metric_registry.get_metric_info(metric_key)
        
        # Step 3: Extract game name if needed
        game_name = None
        if metric_info["api"] in ["multi", "gamalytic", "gamalytic_simple"]:
            game_name = self.metric_registry.extract_game_name(user_query)
            print(f"🎮 Extracted game name: '{game_name}' for API: {metric_info['api']}")
            if not game_name:
                return "I couldn't identify which game you're asking about. Please specify a game name.", None
        
        # Step 4: Retrieve data
        df, error = self.data_retriever.get_metric_data(metric_info, game_name)
        
        if df is None:
            return f"Sorry, I couldn't retrieve the data: {error}", None
        
        # Step 5: Generate text response
        text_response = self._generate_text_response(df, metric_info, game_name)
        
        # Step 6: Create chart (skip for simple lists)
        chart_type = metric_info.get("chart_type", "bar")
        if chart_type == "list":
            # No visualization for simple lists
            print(f"✅ Simple agent response complete (no visualization for list type)")
            return text_response, None
        
        try:
            chart_fig = self.chart_generator.create_chart(
                df, 
                metric_info["chart_type"], 
                metric_info["data_format"]
            )
            
            visualization = {
                "success": True,
                "chart": chart_fig.to_dict(),
                "title": metric_info["data_format"]["title_template"],
                "chart_type": metric_info["chart_type"]
            }
            
            print(f"✅ Simple agent response complete with visualization")
            return text_response, visualization
            
        except Exception as e:
            print(f"❌ Chart generation error: {e}")
            return text_response, None
    
    def _generate_text_response(self, df: pd.DataFrame, metric_info: Dict, game_name: Optional[str] = None) -> str:
        """Generate natural language response from DataFrame"""
        
        # Handle simple game names list (from gamalytic_simple)
        if metric_info.get("data_format", {}).get("response_type") == "game_names_list":
            if "game_name" in df.columns:
                game_names = df["game_name"].tolist()
                response = f"Other games that {game_name} players also play:\n\n"
                for i, name in enumerate(game_names[:10], 1):
                    response += f"{i}. {name}\n"
                return response
        
        # Handle regular DataFrame format
        if game_name:
            response = f"Here are the statistics for {game_name}:\n\n"
            for _, row in df.head(10).iterrows():
                response += f"• {row[metric_info['data_format']['x_column']]}: {row[metric_info['data_format']['y_column']]}\n"
        else:
            response = f"Here are the {metric_info['description'].lower()}:\n\n"
            
            x_col = metric_info["data_format"]["x_column"]
            y_col = metric_info["data_format"]["y_column"]
            
            for i, (_, row) in enumerate(df.head(10).iterrows(), 1):
                x_val = row[x_col]
                y_val = row[y_col]
                
                # Format numbers nicely
                if isinstance(y_val, (int, float)):
                    if y_val >= 1_000_000:
                        y_formatted = f"{y_val/1_000_000:.1f}M"
                    elif y_val >= 1_000:
                        y_formatted = f"{y_val:,.0f}"
                    else:
                        y_formatted = f"{y_val:.1f}"
                else:
                    y_formatted = str(y_val)
                
                response += f"{i}. {x_val}: {y_formatted}\n"
        
        # Add data source
        api_name = metric_info["api"].title()
        if api_name == "Multi":
            response += "\n📊 Data compiled from multiple sources"
        else:
            response += f"\n📊 Data from {api_name} API"
        
        return response
    
    def _handle_unknown_query(self, user_query: str) -> Tuple[str, None]:
        """Handle queries that don't match any metrics"""
        
        # List available metrics
        available_metrics = self.metric_registry.list_all_metrics()
        
        response = "I'm not sure what data you're looking for. Here's what I can help you with:\\n\\n"
        
        for metric_key, description in available_metrics.items():
            response += f"• {description}\\n"
        
        response += "\\nTry asking something like:\\n"
        response += "• 'What are the top games on Twitch?'\\n"
        response += "• 'Show me Steam's most popular games'\\n"
        response += "• 'Tell me about Counter-Strike 2 statistics'\\n"
        
        return response, None
