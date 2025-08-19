"""
API Usage Tracker

Tracks API calls and limits for each service to monitor usage and prevent exceeding quotas.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class APIUsageTracker:
    """Track API usage across all gaming APIs"""
    
    def __init__(self):
        self.usage_file = "api_usage.json"
        
        # API limits (monthly)
        self.api_limits = {
            "rawg": 20000,          # RAWG: 20k requests/month (free tier)
            "gamalytic": 1000,      # Gamalytic: 1k requests/month (estimated premium)
            "twitch": 800000,       # Twitch: ~800k requests/month (rate limit based)
            "steam": float('inf'),   # Steam: No official monthly limit (rate limited only)
            "steamspy": float('inf'), # SteamSpy: No official monthly limit
            "openai": 500           # OpenAI: Track completion calls (varies by plan)
        }
        
        # Load existing usage data
        self.usage_data = self._load_usage_data()
        
    def _load_usage_data(self) -> Dict:
        """Load usage data from file"""
        if os.path.exists(self.usage_file):
            try:
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                    
                print(f"🔍 DEBUG: Loaded data from {self.usage_file}: {data}")
                    
                # Check if we need to reset monthly counters
                current_month = datetime.now().strftime("%Y-%m")
                print(f"🔍 DEBUG: Current month: {current_month}, Data month: {data.get('month')}")
                
                if data.get("month") != current_month:
                    # Reset for new month
                    print("🔄 DEBUG: Resetting for new month")
                    data = {
                        "month": current_month,
                        "usage": {api: 0 for api in self.api_limits.keys()},
                        "last_reset": datetime.now().isoformat()
                    }
                    self._save_usage_data(data)
                else:
                    print("✅ DEBUG: Using existing month data")
                    
                return data
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ DEBUG: Error loading data: {e}")
                pass
        
        # Create new usage data structure
        current_month = datetime.now().strftime("%Y-%m")
        return {
            "month": current_month,
            "usage": {api: 0 for api in self.api_limits.keys()},
            "last_reset": datetime.now().isoformat()
        }
    
    def _save_usage_data(self, data: Dict):
        """Save usage data to file"""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save API usage data: {e}")
    
    def track_api_call(self, api_name: str, calls: int = 1):
        """Track an API call"""
        api_name = api_name.lower()
        if api_name in self.usage_data["usage"]:
            self.usage_data["usage"][api_name] += calls
            self._save_usage_data(self.usage_data)
            
            # Check if approaching limit
            limit = self.api_limits.get(api_name, float('inf'))
            current_usage = self.usage_data["usage"][api_name]
            
            if limit != float('inf'):
                usage_percentage = (current_usage / limit) * 100
                
                if usage_percentage >= 90:
                    print(f"🚨 WARNING: {api_name.upper()} API usage at {usage_percentage:.1f}% ({current_usage}/{limit})")
                elif usage_percentage >= 75:
                    print(f"⚠️  {api_name.upper()} API usage at {usage_percentage:.1f}% ({current_usage}/{limit})")
                elif usage_percentage >= 50:
                    print(f"ℹ️  {api_name.upper()} API usage at {usage_percentage:.1f}% ({current_usage}/{limit})")
    
    def get_usage_summary(self) -> Dict:
        """Get current usage summary"""
        summary = {}
        for api, usage in self.usage_data["usage"].items():
            limit = self.api_limits[api]
            percentage = (usage / limit * 100) if limit != float('inf') else 0
            
            summary[api] = {
                "usage": usage,
                "limit": limit,
                "percentage": round(percentage, 1),
                "remaining": limit - usage if limit != float('inf') else "Unlimited",
                "status": self._get_status(percentage) if limit != float('inf') else "unlimited"
            }
        
        return summary
    
    def _get_status(self, percentage: float) -> str:
        """Get status based on usage percentage"""
        if percentage >= 90:
            return "critical"
        elif percentage >= 75:
            return "warning"
        elif percentage >= 50:
            return "moderate"
        else:
            return "good"
    
    def create_usage_gauge_charts(self) -> go.Figure:
        """Create gauge charts showing API usage"""
        summary = self.get_usage_summary()
        
        # Filter out unlimited APIs for gauge display
        limited_apis = {k: v for k, v in summary.items() 
                       if v["limit"] != float('inf') and v["limit"] > 0}
        
        if not limited_apis:
            return None
        
        # Create subplots for gauge charts
        num_apis = len(limited_apis)
        cols = min(4, num_apis)  # Max 4 columns
        rows = (num_apis + cols - 1) // cols  # Calculate needed rows
        
        subplot_titles = [f"{api.upper()} API" for api in limited_apis.keys()]
        
        fig = make_subplots(
            rows=rows,
            cols=cols,
            specs=[[{"type": "indicator"}] * cols] * rows,
            subplot_titles=subplot_titles,
            vertical_spacing=0.3,
            horizontal_spacing=0.2
        )
        
        # Color scheme based on usage
        def get_gauge_color(percentage):
            if percentage >= 90:
                return "red"
            elif percentage >= 75:
                return "orange"
            elif percentage >= 50:
                return "yellow"
            else:
                return "green"
        
        # Add gauge charts
        for idx, (api, data) in enumerate(limited_apis.items()):
            row = (idx // cols) + 1
            col = (idx % cols) + 1
            
            percentage = data["percentage"]
            
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number",
                    value=percentage,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': get_gauge_color(percentage)},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 75], 'color': "yellow"},
                            {'range': [75, 90], 'color': "orange"},
                            {'range': [90, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    },
                    number={'suffix': "%"}
                ),
                row=row, col=col
            )
            
            # Add ratio text below the gauge
            fig.add_annotation(
                text=f"{data['usage']:,} / {data['limit']:,}",
                x=(col-1) / cols + 1/(2*cols),  # Center horizontally in subplot
                y=(rows-row) / rows + 0.1/rows,  # Position below the gauge
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=12, color="white"),
                xanchor="center",
                yanchor="middle"
            )
        
        fig.update_layout(
            title={
                'text': f"API Usage Tracking - {self.usage_data['month']}",
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.95,
                'yanchor': 'top'
            },
            height=220 * rows + 60,  # Add extra space for ratio text below gauges
            showlegend=False,
            margin=dict(l=20, r=20, t=80, b=40)  # Increase bottom margin for ratio text
        )
        
        return fig
    
    def reset_monthly_usage(self):
        """Reset usage counters for new month"""
        current_month = datetime.now().strftime("%Y-%m")
        self.usage_data = {
            "month": current_month,
            "usage": {api: 0 for api in self.api_limits.keys()},
            "last_reset": datetime.now().isoformat()
        }
        self._save_usage_data(self.usage_data)
        print(f"✅ API usage counters reset for {current_month}")
    
    def get_cost_estimate(self) -> Dict:
        """Estimate costs based on current usage (approximate)"""
        costs = {
            "rawg": 0,  # Free tier
            "gamalytic": self.usage_data["usage"]["gamalytic"] * 0.01,  # Estimated $0.01/call
            "twitch": 0,  # Free
            "steam": 0,   # Free
            "steamspy": 0,  # Free
            "openai": self.usage_data["usage"]["openai"] * 0.03  # Approximate GPT-4o-mini cost
        }
        
        total_estimated_cost = sum(costs.values())
        
        return {
            "individual_costs": costs,
            "total_estimated": round(total_estimated_cost, 2),
            "currency": "USD",
            "note": "Estimates only - actual costs may vary"
        }
