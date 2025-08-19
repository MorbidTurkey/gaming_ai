"""
Visualization Generator

Creates Plotly charts and visualizations for gaming data analysis.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime, timedelta

class VisualizationGenerator:
    """Generates various types of charts for gaming data"""
    
    def __init__(self):
        # Vibrant color palette for better visibility
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
            '#AED6F1',  # Powder Blue
            '#F39C12',  # Orange
            '#E74C3C',  # Strong Red
            '#3498DB',  # Strong Blue
            '#2ECC71'   # Strong Green
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
        
        self.theme = {
            'background_color': '#1e1e1e',
            'paper_color': '#2d2d2d',
            'text_color': '#ffffff',
            'grid_color': '#404040'
        }
    
    def set_color_theme(self, theme_name: str):
        """Set the color theme for charts"""
        if theme_name in self.color_themes:
            self.current_theme = theme_name
            self.color_palette = self.color_themes[theme_name]
            print(f"🎨 Visualization color theme changed to: {theme_name}")
        else:
            print(f"❌ Unknown color theme: {theme_name}")
    
    def create_chart(self, chart_type: str, data_source: str, title: str, 
                     data: Optional[Any] = None) -> go.Figure:
        """
        Create a chart based on type and data
        
        Args:
            chart_type: Type of chart ('line', 'bar', 'pie', 'scatter', 'heatmap', 'box')
            data_source: Description of data source
            title: Chart title
            data: Optional data to use for chart
            
        Returns:
            Plotly Figure object
        """
        print(f"🎨 VISUALIZATION GENERATOR CALLED:")
        print(f"   → Chart Type: {chart_type}")
        print(f"   → Data Source: {data_source}")
        print(f"   → Title: {title}")
        print(f"   → Data Type: {type(data)}")
        print(f"   → Data Content: {data}")
        
        if chart_type == "line":
            return self.create_line_chart(title, data)
        elif chart_type == "bar":
            return self.create_bar_chart(title, data)
        elif chart_type == "pie":
            return self.create_pie_chart(title, data)
        elif chart_type == "scatter":
            return self.create_scatter_chart(title, data)
        elif chart_type == "heatmap":
            return self.create_heatmap(title, data)
        elif chart_type == "box":
            return self.create_box_plot(title, data)
        elif chart_type == "gauge":
            return self.create_gauge_chart(title, data)
        elif chart_type == "table":
            return self.create_table_chart(title, data)
        else:
            return self.create_default_chart(title, data_source)
    
    def create_line_chart(self, title: str, data: Optional[Any] = None) -> go.Figure:
        """Create a line chart for time series data"""
        if data is None:
            # Generate sample player count data
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
            games = ['Counter-Strike 2', 'Dota 2', 'PUBG', 'Apex Legends']
            
            fig = go.Figure()
            
            for i, game in enumerate(games):
                # Generate realistic player count data
                base_count = 500000 + i * 200000
                noise = np.random.normal(0, 0.1, len(dates))
                trend = np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 0.2
                
                player_counts = base_count * (1 + trend + noise)
                player_counts = np.maximum(player_counts, 0)  # Ensure non-negative
                
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=player_counts,
                    mode='lines',
                    name=game,
                    line=dict(color=self.color_palette[i % len(self.color_palette)])
                ))
        else:
            fig = self._create_line_from_data(data)
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Player Count",
            **self._get_layout_theme(),
            hovermode='x unified'
        )
        
        return fig
    
    def create_bar_chart(self, title: str, data: Optional[Any] = None) -> go.Figure:
        """Create a bar chart for categorical data"""
        if data is None:
            # Generate sample top games data
            games = ['Counter-Strike 2', 'Dota 2', 'PUBG', 'Apex Legends', 
                    'Valorant', 'Rust', 'GTA V', 'Destiny 2']
            player_counts = [1200000, 800000, 600000, 500000, 400000, 300000, 250000, 200000]
            
            fig = go.Figure([go.Bar(
                x=games,
                y=player_counts,
                marker_color=self.color_palette[:len(games)]
            )])
        else:
            fig = self._create_bar_from_data(data)
        
        # Debug: Check figure data after _create_bar_from_data
        print(f"🔍 FIGURE DEBUG AFTER _create_bar_from_data:")
        print(f"   → Figure type: {type(fig)}")
        print(f"   → Figure data length: {len(fig.data)}")
        
        fig.update_layout(
            title=title,
            xaxis_title="Games",
            yaxis_title="Current Players",
            **self._get_layout_theme(),
            xaxis_tickangle=-45
        )
        
        # Debug: Check figure data after update_layout
        print(f"🔍 FIGURE DEBUG AFTER UPDATE_LAYOUT:")
        print(f"   → Figure type: {type(fig)}")
        print(f"   → Figure data length: {len(fig.data)}")
        if fig.data:
            print(f"   → First trace type: {type(fig.data[0])}")
        
        return fig
    
    def create_pie_chart(self, title: str, data: Optional[Any] = None) -> go.Figure:
        """Create a pie chart for distribution data"""
        if data is None:
            # Generate sample genre distribution
            genres = ['Action', 'RPG', 'Strategy', 'Indie', 'Sports', 'Racing', 'Simulation']
            market_share = [25, 20, 15, 18, 8, 6, 8]
            
            fig = go.Figure([go.Pie(
                labels=genres,
                values=market_share,
                marker_colors=self.color_palette[:len(genres)]
            )])
        else:
            fig = self._create_pie_from_data(data)
        
        fig.update_layout(
            title=title,
            **self._get_layout_theme()
        )
        
        return fig
    
    def create_scatter_chart(self, title: str, data: Optional[Any] = None) -> go.Figure:
        """Create a scatter plot for correlation analysis"""
        if data is None:
            # Generate sample price vs rating data
            np.random.seed(42)
            prices = np.random.uniform(0, 60, 50)
            ratings = 70 + 20 * (1 - prices/60) + np.random.normal(0, 5, 50)
            ratings = np.clip(ratings, 0, 100)
            
            game_names = [f"Game {i+1}" for i in range(50)]
            
            fig = go.Figure([go.Scatter(
                x=prices,
                y=ratings,
                mode='markers',
                text=game_names,
                marker=dict(
                    size=8,
                    color=ratings,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Rating")
                )
            )])
        else:
            fig = self._create_scatter_from_data(data)
        
        fig.update_layout(
            title=title,
            xaxis_title="Price ($)",
            yaxis_title="User Rating",
            **self._get_layout_theme()
        )
        
        return fig
    
    def create_gauge_chart(self, title: str, data: Optional[Any] = None) -> go.Figure:
        """Create gauge charts for API usage monitoring"""
        from plotly.subplots import make_subplots
        
        if data is None:
            # Default gauge data
            data = [
                {"name": "Sample API", "value": 25, "limit": 1000, "calls": 250}
            ]
        
        print(f"🔧 CREATE_GAUGE_CHART CALLED:")
        print(f"   → Data type: {type(data)}")
        print(f"   → Data content: {data}")
        
        # Filter to only show APIs with limits (not unlimited ones)
        limited_apis = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get('limit') != float('inf'):
                    limited_apis.append(item)
        
        if not limited_apis:
            # Fallback if no limited APIs
            limited_apis = [
                {"name": "RAWG API", "value": 0.14, "limit": 20000, "calls": 28},
                {"name": "GAMALYTIC API", "value": 3.4, "limit": 1000, "calls": 34},
                {"name": "OPENAI API", "value": 4.0, "limit": 500, "calls": 20}
            ]
        
        # Create subplots for multiple gauges
        num_gauges = len(limited_apis)
        if num_gauges == 1:
            fig = go.Figure()
            rows, cols = 1, 1
        elif num_gauges <= 4:
            rows, cols = 1, num_gauges
            
            # Create subplot titles with API names and empty subtitles for spacing
            subplot_titles = []
            for api in limited_apis:
                subplot_titles.append(f"<b>{api['name']}</b><br>   ")
            
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=subplot_titles,
                specs=[[{"type": "indicator"}] * cols]
            )
        else:
            rows = 2
            cols = (num_gauges + 1) // 2
            
            # Create subplot titles with API names and empty subtitles for spacing
            subplot_titles = []
            for api in limited_apis:
                subplot_titles.append(f"<b>{api['name']}</b><br>   ")
            
            fig = make_subplots(
                rows=rows, cols=cols,
                subplot_titles=subplot_titles,
                specs=[[{"type": "indicator"}] * cols for _ in range(rows)]
            )
        
        for i, api in enumerate(limited_apis):
            # Calculate position for subplot
            if num_gauges == 1:
                row, col = 1, 1
            else:
                row = (i // cols) + 1
                col = (i % cols) + 1
            
            # Get actual usage numbers
            calls = api.get('calls', 0)
            limit = api.get('limit', 1000)
            
            # Create usage text with proper formatting
            if limit == float('inf'):
                usage_text = f"{calls:,} calls"
            else:
                usage_text = f"{calls:,}/{limit:,}"
            
            # Determine gauge color based on usage percentage with better visibility
            value = float(api.get('value', 0))
            if value >= 80:
                color = "#ff4444"      # Bright red for high usage
            elif value >= 60:
                color = "#ff8800"      # Bright orange for moderate-high
            elif value >= 40:
                color = "#ffcc00"      # Bright yellow for moderate
            elif value >= 20:
                color = "#66ff66"      # Bright green for low-moderate
            else:
                color = "#00ff88"      # Bright green for very low
            
            gauge = go.Indicator(
                mode="gauge+number",  # Keep it simple 
                value=value,
                domain={'x': [0, 1], 'y': [0.2, 0.8]} if num_gauges == 1 else None,  # Better centering for single gauge
                title={'text': f"{api['name']}" if num_gauges == 1 else "", 'font': {'size': 12}},  # Just the name for single gauge
                number={'suffix': "%", 'font': {'size': 16, 'color': 'white'}},  # Add percentage symbol and white text
                gauge={
                    'axis': {
                        'range': [None, 100], 
                        'tickwidth': 2, 
                        'tickcolor': "lightblue",
                        'tickfont': {'size': 10, 'color': 'white'}
                    },
                    'bar': {
                        'color': color, 
                        'thickness': 0.8,  # Even thicker fill bar (was 0.6)
                        'line': {'color': 'darkblue', 'width': 1}  # Add border to the fill
                    },
                    'bgcolor': "#2a2a2a",  # Dark background for contrast
                    'borderwidth': 3,  # Thicker outer border
                    'bordercolor': "#555555",
                    'steps': [
                        {'range': [0, 20], 'color': '#404040'},      # Grey for very low usage
                        {'range': [20, 40], 'color': '#505050'},    # Slightly lighter grey
                        {'range': [40, 60], 'color': '#606060'},    # Medium grey
                        {'range': [60, 80], 'color': '#707070'},    # Lighter grey until 80%
                        {'range': [80, 90], 'color': '#cc7a00'},    # Orange for high usage
                        {'range': [90, 100], 'color': '#cc0000'}    # Red for critical usage
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 3},  # White threshold line
                        'thickness': 0.8,  # Bigger threshold indicator
                        'value': 80  # Show threshold at 80% instead of 90%
                    }
                }
            )
            
            if num_gauges == 1:
                fig.add_trace(gauge)
            else:
                fig.add_trace(gauge, row=row, col=col)
        
        # Add ratio text annotations in the center of each gauge
        for i, api in enumerate(limited_apis):
            # Get usage text
            calls = api.get('calls', 0)
            limit = api.get('limit', 1000)
            if limit == float('inf'):
                usage_text = f"{calls:,} calls"
            else:
                usage_text = f"{calls:,}/{limit:,}"
            
            # Calculate position for ratio text in center of gauge
            if num_gauges == 1:
                x_pos = 0.5
                y_pos = 0.52  # Slightly higher for better centering in gauge arch
            elif num_gauges <= 4:
                # Single row layout with individual positioning adjustments for each API
                api_name = api['name'].upper()
                if 'RAWG' in api_name:  # RAWG API
                    x_pos = (i + 0.45) / num_gauges  
                elif 'GAMALYTIC' in api_name:  # Gamalytic API
                    x_pos = (i + 0.48) / num_gauges
                elif 'TWITCH' in api_name:  # Twitch API
                    x_pos = (i + 0.55) / num_gauges
                elif 'OPENAI' in api_name:  # OpenAI API
                    x_pos = (i + 0.58) / num_gauges
                else:  # Any other APIs - standard centering
                    x_pos = (i + 0.5) / num_gauges
                y_pos = 0.52  # Slightly higher for better centering in gauge arch
            else:
                # Two row layout
                row = (i // cols) + 1
                col = (i % cols) + 1
                x_pos = ((col - 1) + 0.5) / cols  # Center horizontally for each gauge in its column
                y_pos = 0.77 if row == 1 else 0.27  # Slightly higher for better centering in gauge arches
            
            # Add ratio annotation in center of gauge
            fig.add_annotation(
                text=usage_text,
                x=x_pos,
                y=y_pos,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=12, color="lightgray", weight="bold"),
                align="center",
                xanchor="center",
                yanchor="middle"
            )
        
        # Update layout
        fig.update_layout(
            title=None,  # Remove the redundant "API Usage Levels" title
            **self._get_layout_theme(),
            height=220 if num_gauges <= 4 else 320,  # Increased height to accommodate custom text
            margin=dict(l=15, r=15, t=50, b=15),  # Moderate top margin for custom text positioning
            showlegend=False
        )
        
        print(f"✅ Successfully created gauge chart with {len(limited_apis)} gauges")
        return fig
    
    def create_table_chart(self, title: str, data: Optional[Any] = None) -> go.Figure:
        """Create a table visualization for data display"""
        from utils.data_processor import DataProcessor
        
        if data is None:
            # Generate sample table data
            data = [
                {"name": "Counter-Strike 2", "players": 1200000, "peak": 1400000},
                {"name": "Dota 2", "players": 800000, "peak": 900000}, 
                {"name": "PUBG", "players": 600000, "peak": 700000},
                {"name": "Apex Legends", "players": 500000, "peak": 550000}
            ]
        
        print(f"🔧 CREATE_TABLE_CHART CALLED:")
        print(f"   → Data type: {type(data)}")
        print(f"   → Data content: {data}")
        
        # Process data into DataFrame
        processor = DataProcessor()
        if isinstance(data, list) and data:
            # Detect data format and create appropriate table
            first_item = data[0]
            
            if isinstance(first_item, dict):
                # Convert to DataFrame for table display
                import pandas as pd
                df = pd.DataFrame(data)
                
                # Prepare table data
                headers = list(df.columns)
                values = []
                
                for col in headers:
                    # Format values for display
                    col_values = []
                    for val in df[col]:
                        if isinstance(val, (int, float)) and val > 1000:
                            col_values.append(f"{val:,}")  # Add commas for large numbers
                        else:
                            col_values.append(str(val))
                    values.append(col_values)
                
                # Create table figure
                fig = go.Figure(data=[go.Table(
                    header=dict(
                        values=[f"<b>{header.title().replace('_', ' ')}</b>" for header in headers],
                        fill_color='#2d2d2d',
                        font=dict(color='white', size=14),
                        align="center",
                        height=40
                    ),
                    cells=dict(
                        values=values,
                        fill_color=['#1e1e1e', '#252525'] * (len(headers) // 2 + 1),  # Alternating colors
                        font=dict(color='white', size=12),
                        align="center",
                        height=35
                    )
                )])
                
                fig.update_layout(
                    title=title,
                    **self._get_layout_theme(),
                    height=min(600, 100 + len(df) * 35),  # Dynamic height based on row count
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                
                print(f"✅ Successfully created table chart with {len(df)} rows and {len(headers)} columns")
                return fig
        
        # Fallback to default chart if table creation fails
        return self.create_default_chart(title, "table_data")
    
    def create_heatmap(self, title: str, data: Optional[Any] = None) -> go.Figure:
        """Create a heatmap for matrix data"""
        if data is None:
            # Generate sample genre popularity by region
            genres = ['Action', 'RPG', 'Strategy', 'Sports', 'Racing']
            regions = ['North America', 'Europe', 'Asia', 'South America', 'Oceania']
            
            np.random.seed(42)
            popularity_matrix = np.random.randint(20, 100, (len(regions), len(genres)))
            
            fig = go.Figure([go.Heatmap(
                z=popularity_matrix,
                x=genres,
                y=regions,
                colorscale='Viridis',
                colorbar=dict(title="Popularity Score")
            )])
        else:
            fig = self._create_heatmap_from_data(data)
        
        fig.update_layout(
            title=title,
            xaxis_title="Game Genres",
            yaxis_title="Regions",
            **self._get_layout_theme()
        )
        
        return fig
    
    def create_box_plot(self, title: str, data: Optional[Any] = None) -> go.Figure:
        """Create a box plot for distribution analysis"""
        if data is None:
            # Generate sample playtime distributions by genre
            np.random.seed(42)
            genres = ['Action', 'RPG', 'Strategy', 'Indie']
            
            fig = go.Figure()
            
            for i, genre in enumerate(genres):
                # Different distributions for different genres
                if genre == 'RPG':
                    playtimes = np.random.lognormal(4, 1, 1000)  # Higher playtime
                elif genre == 'Action':
                    playtimes = np.random.lognormal(3, 0.8, 1000)
                elif genre == 'Strategy':
                    playtimes = np.random.lognormal(3.5, 0.9, 1000)
                else:  # Indie
                    playtimes = np.random.lognormal(2.5, 1.2, 1000)
                
                fig.add_trace(go.Box(
                    y=playtimes,
                    name=genre,
                    marker_color=self.color_palette[i % len(self.color_palette)]
                ))
        else:
            fig = self._create_box_from_data(data)
        
        fig.update_layout(
            title=title,
            xaxis_title="Game Genre",
            yaxis_title="Playtime (hours)",
            **self._get_layout_theme()
        )
        
        return fig
    
    def create_default_chart(self, title: str, data_source: str) -> go.Figure:
        """Create a default chart when type is unknown"""
        fig = go.Figure()
        
        fig.add_annotation(
            text=f"Chart for: {data_source}<br>No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=16, color=self.theme['text_color'])
        )
        
        fig.update_layout(
            title=title,
            **self._get_layout_theme(),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        
        return fig
    
    def _get_layout_theme(self) -> Dict:
        """Get common layout theme for all charts"""
        return {
            'plot_bgcolor': self.theme['background_color'],
            'paper_bgcolor': self.theme['paper_color'],
            'font': dict(color=self.theme['text_color']),
            'xaxis': dict(
                gridcolor=self.theme['grid_color'],
                color=self.theme['text_color']
            ),
            'yaxis': dict(
                gridcolor=self.theme['grid_color'],
                color=self.theme['text_color']
            )
        }
    
    def _create_line_from_data(self, data: Any) -> go.Figure:
        """Create line chart from provided data"""
        # Implementation would depend on data structure
        fig = go.Figure()
        # Add logic to parse data and create appropriate traces
        return fig
    
    def _create_bar_from_data(self, data: Any) -> go.Figure:
        """Create bar chart from provided data"""
        fig = go.Figure()
        
        print(f"🔧 _CREATE_BAR_FROM_DATA CALLED:")
        print(f"   → Data type: {type(data)}")
        print(f"   → Data content: {data}")
        print(f"   → Is list: {isinstance(data, list)}")
        if isinstance(data, list) and data:
            print(f"   → First item: {data[0]}")
            print(f"   → First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
        
        # Handle Twitch data format
        if isinstance(data, list) and data:
            if "viewer_count" in data[0]:
                # Twitch top games data
                games = [game.get("name", "Unknown") for game in data]
                viewers = [game.get("viewer_count", 0) for game in data]
                
                # Debug logging for Twitch chart axes
                print(f"📊 TWITCH CHART AXES DEBUG:")
                print(f"   X-AXIS (Games): {games}")
                print(f"   Y-AXIS (Viewer Count): {viewers}")
                print(f"   X-AXIS TITLE: 'Games'")
                print(f"   Y-AXIS TITLE: 'Current Viewers'")
                print(f"   CHART TYPE: Bar Chart")
                print(f"   DATA POINTS: {len(games)} bars")
                
                fig.add_trace(go.Bar(
                    x=games,
                    y=viewers,
                    marker_color=self.color_palette[:len(games)],
                    text=[f"{v:,}" for v in viewers],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    xaxis_title="Games",
                    yaxis_title="Current Viewers"
                )
                
                print(f"✅ Twitch bar chart created with {len(games)} bars: {list(zip(games, viewers))}")
            
            elif "players" in data[0]:
                # Steam data format
                games = [game.get("name", "Unknown") for game in data]
                players = [game.get("players", 0) for game in data]
                
                # Debug logging for Steam chart axes
                print(f"📊 STEAM CHART AXES DEBUG:")
                print(f"   X-AXIS (Games): {games}")
                print(f"   Y-AXIS (Player Count): {players}")
                print(f"   X-AXIS TITLE: 'Games'")
                print(f"   Y-AXIS TITLE: 'Current Players'")
                print(f"   CHART TYPE: Bar Chart")
                print(f"   DATA POINTS: {len(games)} bars")
                
                fig.add_trace(go.Bar(
                    x=games,
                    y=players,
                    marker_color=self.color_palette[:len(games)],
                    text=[f"{p:,}" for p in players],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    xaxis_title="Games",
                    yaxis_title="Current Players"
                )
                
                print(f"✅ Steam bar chart created with {len(games)} bars: {list(zip(games, players))}")
        
        # Handle dict format with success/data structure
        elif isinstance(data, dict) and "data" in data:
            return self._create_bar_from_data(data["data"])
        
        # Handle Gamalytic market data format
        elif isinstance(data, dict) and "segments" in data:
            # Market segments data (PC, Mobile, Console)
            segments = data["segments"]
            names = list(segments.keys())
            revenues = [segments[name]["revenue"] / 1e9 for name in names]  # Convert to billions
            
            fig.add_trace(go.Bar(
                x=names,
                y=revenues,
                marker_color=self.color_palette[:len(names)],
                text=[f"${r:.1f}B" for r in revenues],
                textposition='auto'
            ))
            
            fig.update_layout(
                xaxis_title="Market Segments",
                yaxis_title="Revenue (Billions USD)"
            )
        
        # Handle Gamalytic top markets data
        elif isinstance(data, dict) and "top_markets" in data:
            markets = data["top_markets"]
            countries = [market["country"] for market in markets]
            revenues = [market["revenue"] / 1e9 for market in markets]  # Convert to billions
            
            fig.add_trace(go.Bar(
                x=countries,
                y=revenues,
                marker_color=self.color_palette[:len(countries)],
                text=[f"${r:.1f}B" for r in revenues],
                textposition='auto'
            ))
            
            fig.update_layout(
                xaxis_title="Countries",
                yaxis_title="Revenue (Billions USD)"
            )
        
        # Handle game details format (list of name/value pairs)
        elif isinstance(data, list) and data and "name" in data[0] and "value" in data[0]:
            # Game details data (Metacritic Score, User Rating, etc.)
            names = [item["name"] for item in data]
            values = [item["value"] for item in data]
            
            # Debug logging for chart axes
            print(f"📊 CHART AXES DEBUG:")
            print(f"   X-AXIS (Categories): {names}")
            print(f"   Y-AXIS (Values): {values}")
            print(f"   X-AXIS TITLE: 'Metrics'")
            print(f"   Y-AXIS TITLE: 'Score/Count'")
            print(f"   CHART TYPE: Bar Chart")
            print(f"   DATA POINTS: {len(names)} bars")
            
            fig.add_trace(go.Bar(
                x=names,
                y=values,
                marker_color=self.color_palette[:len(names)],
                text=[f"{v}" for v in values],
                textposition='auto'
            ))
            
            fig.update_layout(
                xaxis_title="Metrics",
                yaxis_title="Score/Count",
                xaxis_tickangle=-45
            )
            
            print(f"✅ Bar chart created with {len(names)} bars: {list(zip(names, values))}")
        
        # Debug: Check figure data before returning
        print(f"🔍 FIGURE DEBUG BEFORE RETURN:")
        print(f"   → Figure type: {type(fig)}")
        print(f"   → Figure data length: {len(fig.data)}")
        if fig.data:
            print(f"   → First trace type: {type(fig.data[0])}")
            print(f"   → First trace x: {fig.data[0].x[:5] if hasattr(fig.data[0], 'x') and fig.data[0].x is not None else 'None'}")
            print(f"   → First trace y: {fig.data[0].y[:5] if hasattr(fig.data[0], 'y') and fig.data[0].y is not None else 'None'}")
        
        return fig
    
    def _create_pie_from_data(self, data: Any) -> go.Figure:
        """Create pie chart from provided data"""
        fig = go.Figure()
        
        # Handle Gamalytic market segments data
        if isinstance(data, dict) and "segments" in data:
            segments = data["segments"]
            labels = list(segments.keys())
            values = [segments[name]["revenue"] / 1e9 for name in labels]  # Convert to billions
            
            fig.add_trace(go.Pie(
                labels=labels,
                values=values,
                marker_colors=self.color_palette[:len(labels)],
                textinfo='label+percent+value',
                texttemplate='%{label}<br>$%{value:.1f}B<br>%{percent}'
            ))
        
        # Handle Gamalytic genre data
        elif isinstance(data, dict) and "genres" in data:  # Genre analysis data
            genres_data = data["genres"]
            labels = list(genres_data.keys())
            values = [genres_data[genre]["total_revenue"] / 1e9 for genre in labels]  # Convert to billions
            
            fig.add_trace(go.Pie(
                labels=labels,
                values=values,
                marker_colors=self.color_palette[:len(labels)],
                textinfo='label+percent+value',
                texttemplate='%{label}<br>$%{value:.1f}B<br>%{percent}'
            ))
        
        return fig
    
    def _create_scatter_from_data(self, data: Any) -> go.Figure:
        """Create scatter plot from provided data"""
        fig = go.Figure()
        # Add logic to parse data and create appropriate traces
        return fig
    
    def _create_heatmap_from_data(self, data: Any) -> go.Figure:
        """Create heatmap from provided data"""
        fig = go.Figure()
        # Add logic to parse data and create appropriate traces
        return fig
    
    def _create_box_from_data(self, data: Any) -> go.Figure:
        """Create box plot from provided data"""
        fig = go.Figure()
        # Add logic to parse data and create appropriate traces
        return fig
    
    def create_comparison_chart(self, games: List[str], metrics: Dict[str, List]) -> go.Figure:
        """Create a multi-metric comparison chart"""
        fig = go.Figure()
        
        for metric, values in metrics.items():
            fig.add_trace(go.Bar(
                name=metric,
                x=games,
                y=values,
                yaxis=f'y{len(metrics)}' if len(metrics) > 1 else 'y'
            ))
        
        fig.update_layout(
            title="Game Comparison",
            **self._get_layout_theme(),
            barmode='group'
        )
        
        return fig
    
    def create_trend_analysis(self, trend_data: Dict) -> go.Figure:
        """Create a trend analysis visualization"""
        fig = go.Figure()
        
        # Implementation would create various trend visualizations
        # based on the trend_data structure
        
        return fig
    
    def export_data_to_excel(self, data: Any, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Export visualization data to Excel file
        
        Args:
            data: Data to export (list, dict, or DataFrame)
            filename: Optional custom filename
            
        Returns:
            Dictionary with export results
        """
        try:
            from utils.data_processor import DataProcessor
            import pandas as pd
            from datetime import datetime
            import os
            
            processor = DataProcessor()
            
            # Convert data to DataFrame if needed
            if isinstance(data, pd.DataFrame):
                df = data
            elif isinstance(data, list) and data:
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to extract meaningful data from dict
                if "data" in data:
                    df = pd.DataFrame(data["data"]) if isinstance(data["data"], list) else pd.DataFrame([data["data"]])
                else:
                    df = pd.DataFrame([data])
            else:
                return {"success": False, "error": "No exportable data found"}
            
            if df.empty:
                return {"success": False, "error": "DataFrame is empty"}
            
            # Generate filename if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"gaming_data_export_{timestamp}.xlsx"
            elif not filename.endswith('.xlsx'):
                filename += '.xlsx'
            
            # Prepare export data
            export_result = processor.prepare_for_export(df, "excel")
            
            if not export_result["success"]:
                return export_result
            
            # Save to file
            export_df = export_result["data"]
            export_path = os.path.join(os.getcwd(), filename)
            
            with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
                # Main data sheet
                export_df.to_excel(writer, sheet_name='Data', index=False)
                
                # Summary sheet
                summary = processor.create_summary_stats(df)
                summary_df = pd.DataFrame([summary])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            return {
                "success": True,
                "filename": filename,
                "filepath": export_path,
                "row_count": len(df),
                "column_count": len(df.columns),
                "exported_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": f"Export failed: {str(e)}"}
    
    def get_chart_recommendations(self, data: Any) -> List[str]:
        """
        Get recommended chart types for given data
        
        Args:
            data: Data to analyze
            
        Returns:
            List of recommended chart types
        """
        try:
            from utils.data_processor import DataProcessor
            import pandas as pd
            
            processor = DataProcessor()
            
            # Convert to DataFrame for analysis
            if isinstance(data, pd.DataFrame):
                df = data
            elif isinstance(data, list) and data:
                df = pd.DataFrame(data)
            else:
                return ["bar", "table"]  # Default recommendations
            
            if df.empty:
                return ["table"]
            
            # Get visualization mapping
            mapping = processor.get_visualization_mapping(df)
            return mapping.get("recommended_charts", ["bar", "table"])
            
        except Exception as e:
            print(f"❌ Error getting chart recommendations: {e}")
            return ["bar", "table"]
