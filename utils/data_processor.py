"""
Data Processor

Standardizes API outputs into DataFrames and provides structured data transformation
for visualizations and exports.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
import json

class DataProcessor:
    """Processes API data into standardized DataFrames for visualization and export"""
    
    def __init__(self):
        self.data_cache = {}
        
    def process_api_data(self, data: Any, api_source: str) -> pd.DataFrame:
        """
        Convert API response to standardized DataFrame
        
        Args:
            data: Raw API response data
            api_source: Source API identifier (steam, twitch, rawg, etc.)
            
        Returns:
            Standardized pandas DataFrame
        """
        try:
            if api_source.lower() == 'steam':
                return self._process_steam_data(data)
            elif api_source.lower() == 'twitch':
                return self._process_twitch_data(data)
            elif api_source.lower() == 'rawg':
                return self._process_rawg_data(data)
            elif api_source.lower() == 'gamalytic':
                return self._process_gamalytic_data(data)
            elif api_source.lower() == 'steamspy':
                return self._process_steamspy_data(data)
            else:
                return self._process_generic_data(data)
                
        except Exception as e:
            print(f"❌ Error processing {api_source} data: {e}")
            return pd.DataFrame()
    
    def _process_steam_data(self, data: Any) -> pd.DataFrame:
        """Process Steam API data into DataFrame"""
        if isinstance(data, list) and data:
            # Top games data
            if "players" in data[0]:
                df = pd.DataFrame(data)
                df['api_source'] = 'steam'
                df['data_type'] = 'player_count'
                df['timestamp'] = datetime.now()
                
                # Standardize columns
                standardized = {
                    'name': df['name'],
                    'value': df['players'], 
                    'metric': 'concurrent_players',
                    'category': df.get('category', 'game'),
                    'api_source': 'steam',
                    'data_type': 'ranking',
                    'timestamp': datetime.now()
                }
                return pd.DataFrame(standardized)
                
        elif isinstance(data, dict):
            # Single game data
            if "players" in data:
                standardized = {
                    'name': [data.get('name', 'Unknown')],
                    'value': [data['players']],
                    'metric': ['concurrent_players'],
                    'category': ['game'],
                    'api_source': ['steam'],
                    'data_type': ['single_game'],
                    'timestamp': [datetime.now()]
                }
                return pd.DataFrame(standardized)
        
        return pd.DataFrame()
    
    def _process_twitch_data(self, data: Any) -> pd.DataFrame:
        """Process Twitch API data into DataFrame"""
        if isinstance(data, list) and data:
            # Top games data
            if "viewer_count" in data[0]:
                df = pd.DataFrame(data)
                
                standardized = {
                    'name': df['name'],
                    'value': df['viewer_count'],
                    'metric': 'viewer_count',
                    'category': df.get('category', 'game'),
                    'api_source': 'twitch',
                    'data_type': 'ranking',
                    'timestamp': datetime.now()
                }
                return pd.DataFrame(standardized)
                
        return pd.DataFrame()
    
    def _process_rawg_data(self, data: Any) -> pd.DataFrame:
        """Process RAWG API data into DataFrame"""
        if isinstance(data, dict):
            # Single game metadata
            if "name" in data:
                metrics_data = []
                
                # Extract various metrics
                if data.get('metacritic'):
                    metrics_data.append({
                        'name': data['name'],
                        'metric': 'metacritic_score',
                        'value': data['metacritic'],
                        'category': 'rating'
                    })
                
                if data.get('rating'):
                    metrics_data.append({
                        'name': data['name'], 
                        'metric': 'user_rating',
                        'value': data['rating'] * 20,  # Convert to 100-scale
                        'category': 'rating'
                    })
                
                if data.get('ratings_count'):
                    metrics_data.append({
                        'name': data['name'],
                        'metric': 'review_count',
                        'value': data['ratings_count'],
                        'category': 'engagement'
                    })
                
                if metrics_data:
                    df = pd.DataFrame(metrics_data)
                    df['api_source'] = 'rawg'
                    df['data_type'] = 'game_details'
                    df['timestamp'] = datetime.now()
                    return df
                    
        elif isinstance(data, list):
            # Game search results or reviews
            if data and "name" in data[0]:
                df = pd.DataFrame(data)
                df['api_source'] = 'rawg'
                df['data_type'] = 'search_results'
                df['timestamp'] = datetime.now()
                return df
        
        return pd.DataFrame()
    
    def _process_gamalytic_data(self, data: Any) -> pd.DataFrame:
        """Process Gamalytic API data into DataFrame"""
        if isinstance(data, dict):
            metrics_data = []
            
            # Market segments data
            if "segments" in data:
                for segment, info in data["segments"].items():
                    metrics_data.append({
                        'name': segment,
                        'metric': 'revenue_billions',
                        'value': info["revenue"] / 1e9,
                        'category': 'market_segment'
                    })
            
            # Top markets data
            elif "top_markets" in data:
                for market in data["top_markets"]:
                    metrics_data.append({
                        'name': market["country"],
                        'metric': 'revenue_billions', 
                        'value': market["revenue"] / 1e9,
                        'category': 'country_market'
                    })
            
            # Genre data
            elif "genres" in data:
                for genre, info in data["genres"].items():
                    metrics_data.append({
                        'name': genre,
                        'metric': 'revenue_billions',
                        'value': info["total_revenue"] / 1e9,
                        'category': 'genre'
                    })
            
            if metrics_data:
                df = pd.DataFrame(metrics_data)
                df['api_source'] = 'gamalytic'
                df['data_type'] = 'market_analysis'
                df['timestamp'] = datetime.now()
                return df
        
        return pd.DataFrame()
    
    def _process_steamspy_data(self, data: Any) -> pd.DataFrame:
        """Process SteamSpy API data into DataFrame"""
        if isinstance(data, list) and data:
            df = pd.DataFrame(data)
            df['api_source'] = 'steamspy'
            df['data_type'] = 'ownership_stats'
            df['timestamp'] = datetime.now()
            return df
        
        return pd.DataFrame()
    
    def _process_generic_data(self, data: Any) -> pd.DataFrame:
        """Process generic data formats"""
        if isinstance(data, list) and data:
            # List of name/value pairs
            if isinstance(data[0], dict) and "name" in data[0] and "value" in data[0]:
                df = pd.DataFrame(data)
                df['api_source'] = 'generic'
                df['data_type'] = 'key_value'
                df['timestamp'] = datetime.now()
                return df
        
        return pd.DataFrame()
    
    def get_visualization_mapping(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Determine optimal visualization type and axis mapping for DataFrame
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Dictionary with visualization recommendations
        """
        if df.empty:
            return {"chart_type": "default", "x_axis": None, "y_axis": None}
        
        data_type = df['data_type'].iloc[0] if 'data_type' in df.columns else 'unknown'
        api_source = df['api_source'].iloc[0] if 'api_source' in df.columns else 'unknown'
        
        # Determine best chart type based on data characteristics
        num_records = len(df)
        has_numeric_values = 'value' in df.columns and pd.api.types.is_numeric_dtype(df['value'])
        
        mapping = {
            "chart_type": "bar",  # Default
            "x_axis": "name",
            "y_axis": "value", 
            "title": f"Data from {api_source.upper()}",
            "x_label": "Items",
            "y_label": "Values",
            "data_source": api_source,
            "recommended_charts": ["bar", "table"]
        }
        
        # Customize based on data type and content
        if data_type == 'ranking':
            mapping.update({
                "chart_type": "bar",
                "title": f"Top {api_source.title()} Rankings",
                "x_label": "Games",
                "recommended_charts": ["bar", "horizontal_bar", "table"]
            })
            
            if api_source == 'steam':
                mapping["y_label"] = "Current Players"
            elif api_source == 'twitch':
                mapping["y_label"] = "Current Viewers"
                
        elif data_type == 'game_details':
            mapping.update({
                "chart_type": "bar",
                "title": f"Game Metrics - {df['name'].iloc[0] if 'name' in df.columns else 'Unknown'}",
                "x_label": "Metrics",
                "y_label": "Score/Count",
                "recommended_charts": ["bar", "radar", "table"]
            })
            
        elif data_type == 'market_analysis':
            mapping.update({
                "chart_type": "pie",
                "title": "Market Analysis",
                "recommended_charts": ["pie", "bar", "treemap", "table"]
            })
            
        elif num_records <= 5:
            mapping["recommended_charts"] = ["pie", "bar", "table"]
        elif num_records > 20:
            mapping["recommended_charts"] = ["bar", "line", "heatmap", "table"]
        
        # Always include table option
        if "table" not in mapping["recommended_charts"]:
            mapping["recommended_charts"].append("table")
            
        return mapping
    
    def prepare_for_export(self, df: pd.DataFrame, format_type: str = "excel") -> Dict[str, Any]:
        """
        Prepare DataFrame for export in various formats
        
        Args:
            df: DataFrame to export
            format_type: Export format (excel, csv, json)
            
        Returns:
            Dictionary with export data and metadata
        """
        if df.empty:
            return {"success": False, "error": "No data to export"}
        
        export_data = {
            "success": True,
            "format": format_type,
            "filename": f"gaming_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "row_count": len(df),
            "column_count": len(df.columns),
            "generated_at": datetime.now().isoformat()
        }
        
        if format_type.lower() == "excel":
            # Clean data for Excel export
            clean_df = df.copy()
            
            # Convert datetime columns to strings for Excel compatibility
            for col in clean_df.columns:
                if pd.api.types.is_datetime64_any_dtype(clean_df[col]):
                    clean_df[col] = clean_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            export_data.update({
                "filename": export_data["filename"] + ".xlsx",
                "data": clean_df,
                "sheets": ["Data", "Summary"]  # Could add summary sheet
            })
            
        elif format_type.lower() == "csv":
            export_data.update({
                "filename": export_data["filename"] + ".csv",
                "data": df.to_csv(index=False)
            })
            
        elif format_type.lower() == "json":
            export_data.update({
                "filename": export_data["filename"] + ".json",
                "data": df.to_dict('records')
            })
        
        return export_data
    
    def create_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics for the DataFrame"""
        if df.empty:
            return {}
        
        summary = {
            "total_records": len(df),
            "columns": list(df.columns),
            "data_types": df.dtypes.to_dict(),
            "generated_at": datetime.now().isoformat()
        }
        
        # Numeric column statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            summary["numeric_stats"] = df[numeric_cols].describe().to_dict()
        
        # Categorical column value counts
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            summary["categorical_stats"] = {}
            for col in categorical_cols:
                value_counts = df[col].value_counts().head(10).to_dict()
                summary["categorical_stats"][col] = value_counts
        
        return summary

    def combine_multiple_sources(self, api_results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Combine DataFrames from multiple API sources into a unified dataset
        
        Args:
            api_results: Dictionary mapping API names to their processed DataFrames
            
        Returns:
            Combined DataFrame with consistent structure
        """
        try:
            if not api_results:
                return pd.DataFrame()
            
            combined_dfs = []
            
            for api_name, df in api_results.items():
                if df is not None and not df.empty:
                    # Ensure api_source column exists and is set correctly
                    df_copy = df.copy()
                    df_copy['api_source'] = api_name
                    combined_dfs.append(df_copy)
            
            if not combined_dfs:
                return pd.DataFrame()
            
            # Combine all DataFrames
            combined_df = pd.concat(combined_dfs, ignore_index=True, sort=False)
            
            # Standardize common columns
            if 'name' not in combined_df.columns:
                # Try to find a name-like column
                name_candidates = ['game_name', 'title', 'app_name']
                for candidate in name_candidates:
                    if candidate in combined_df.columns:
                        combined_df['name'] = combined_df[candidate]
                        break
                else:
                    combined_df['name'] = 'Unknown'
            
            # Ensure consistent data types
            if 'value' in combined_df.columns:
                combined_df['value'] = pd.to_numeric(combined_df['value'], errors='coerce')
            
            if 'timestamp' not in combined_df.columns:
                combined_df['timestamp'] = datetime.now().isoformat()
            
            # Sort by value if available, otherwise by name
            if 'value' in combined_df.columns:
                combined_df = combined_df.sort_values('value', ascending=False)
            else:
                combined_df = combined_df.sort_values('name')
            
            combined_df = combined_df.reset_index(drop=True)
            
            print(f"✅ Combined {len(api_results)} API sources into DataFrame with {len(combined_df)} rows")
            return combined_df
            
        except Exception as e:
            print(f"❌ Error combining API sources: {e}")
            return pd.DataFrame()
