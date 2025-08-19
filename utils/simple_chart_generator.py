"""
Simple Chart Generator - Creates charts directly from DataFrames

This module takes clean DataFrames and creates Plotly charts with
consistent styling and proper data handling.
"""

import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, Optional

class SimpleChartGenerator:
    """Creates charts from clean DataFrames"""
    
    def __init__(self):
        self.theme = {
            'background_color': '#1e1e1e',
            'paper_color': '#2d2d2d',
            'text_color': '#ffffff',
            'grid_color': '#404040'
        }
        
        self.colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
    
    def create_chart(self, df: pd.DataFrame, chart_type: str, data_format: Dict[str, str]) -> go.Figure:
        """
        Create a chart from a DataFrame
        
        Args:
            df: Clean DataFrame with data
            chart_type: Type of chart ('bar', 'line', 'pie', 'scatter')
            data_format: Format configuration from metric registry
            
        Returns:
            Plotly Figure object
        """
        print(f"📊 SIMPLE CHART GENERATOR:")
        print(f"   → Chart Type: {chart_type}")
        print(f"   → DataFrame Shape: {df.shape}")
        print(f"   → DataFrame Columns: {list(df.columns)}")
        print(f"   → Data Format: {data_format}")
        
        if chart_type == "bar":
            return self._create_bar_chart(df, data_format)
        elif chart_type == "line":
            return self._create_line_chart(df, data_format)
        elif chart_type == "pie":
            return self._create_pie_chart(df, data_format)
        elif chart_type == "scatter":
            return self._create_scatter_chart(df, data_format)
        else:
            # Default to bar chart
            return self._create_bar_chart(df, data_format)
    
    def _create_bar_chart(self, df: pd.DataFrame, data_format: Dict[str, str]) -> go.Figure:
        """Create a bar chart from DataFrame"""
        print(f"🔧 Creating bar chart...")
        
        # Get column names
        x_col = data_format["x_column"]
        y_col = data_format["y_column"]
        
        # Extract data
        x_data = df[x_col].tolist()
        y_data = df[y_col].tolist()
        
        print(f"   → X Data: {x_data[:5]}...")
        print(f"   → Y Data: {y_data[:5]}...")
        
        # Create figure
        fig = go.Figure()
        
        # Add bar trace
        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            marker_color=self.colors[:len(x_data)],
            text=[f"{y:,}" if isinstance(y, (int, float)) else str(y) for y in y_data],
            textposition='auto'
        ))
        
        # Update layout
        fig.update_layout(
            title=data_format.get("title_template", "Chart"),
            xaxis_title=data_format.get("x_title", "X Axis"),
            yaxis_title=data_format.get("y_title", "Y Axis"),
            plot_bgcolor=self.theme['background_color'],
            paper_bgcolor=self.theme['paper_color'],
            font=dict(color=self.theme['text_color']),
            xaxis=dict(
                gridcolor=self.theme['grid_color'],
                color=self.theme['text_color'],
                tickangle=-45
            ),
            yaxis=dict(
                gridcolor=self.theme['grid_color'],
                color=self.theme['text_color']
            )
        )
        
        print(f"✅ Bar chart created with {len(x_data)} bars")
        print(f"📊 Figure data length: {len(fig.data)}")
        
        return fig
    
    def _create_line_chart(self, df: pd.DataFrame, data_format: Dict[str, str]) -> go.Figure:
        """Create a line chart from DataFrame"""
        x_col = data_format["x_column"]
        y_col = data_format["y_column"]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            line=dict(color=self.colors[0]),
            marker=dict(color=self.colors[0])
        ))
        
        fig.update_layout(
            title=data_format.get("title_template", "Chart"),
            xaxis_title=data_format.get("x_title", "X Axis"),
            yaxis_title=data_format.get("y_title", "Y Axis"),
            plot_bgcolor=self.theme['background_color'],
            paper_bgcolor=self.theme['paper_color'],
            font=dict(color=self.theme['text_color']),
            xaxis=dict(
                gridcolor=self.theme['grid_color'],
                color=self.theme['text_color']
            ),
            yaxis=dict(
                gridcolor=self.theme['grid_color'],
                color=self.theme['text_color']
            )
        )
        
        return fig
    
    def _create_pie_chart(self, df: pd.DataFrame, data_format: Dict[str, str]) -> go.Figure:
        """Create a pie chart from DataFrame"""
        x_col = data_format["x_column"]
        y_col = data_format["y_column"]
        
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=df[x_col],
            values=df[y_col],
            marker_colors=self.colors[:len(df)]
        ))
        
        fig.update_layout(
            title=data_format.get("title_template", "Chart"),
            plot_bgcolor=self.theme['background_color'],
            paper_bgcolor=self.theme['paper_color'],
            font=dict(color=self.theme['text_color'])
        )
        
        return fig
    
    def _create_scatter_chart(self, df: pd.DataFrame, data_format: Dict[str, str]) -> go.Figure:
        """Create a scatter chart from DataFrame"""
        x_col = data_format["x_column"]
        y_col = data_format["y_column"]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(
                color=self.colors[0],
                size=8
            )
        ))
        
        fig.update_layout(
            title=data_format.get("title_template", "Chart"),
            xaxis_title=data_format.get("x_title", "X Axis"),
            yaxis_title=data_format.get("y_title", "Y Axis"),
            plot_bgcolor=self.theme['background_color'],
            paper_bgcolor=self.theme['paper_color'],
            font=dict(color=self.theme['text_color']),
            xaxis=dict(
                gridcolor=self.theme['grid_color'],
                color=self.theme['text_color']
            ),
            yaxis=dict(
                gridcolor=self.theme['grid_color'],
                color=self.theme['text_color']
            )
        )
        
        return fig
