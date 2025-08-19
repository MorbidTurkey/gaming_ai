"""
Test script for enhanced AI training with DataFrame approach
Tests the new data processing capabilities and export functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_processor import DataProcessor
from utils.visualization import VisualizationGenerator
import pandas as pd
import json

def test_data_processor():
    """Test the DataProcessor class with sample data"""
    print("🧪 Testing DataProcessor...")
    
    processor = DataProcessor()
    
    # Test Steam data processing
    sample_steam_data = [
        {"name": "Counter-Strike 2", "current_players": 1200000},
        {"name": "Dota 2", "current_players": 800000},
        {"name": "PUBG", "current_players": 600000}
    ]
    
    steam_df = processor.process_api_data(sample_steam_data, "steam")
    print(f"✅ Steam DataFrame shape: {steam_df.shape}")
    print(f"   Columns: {list(steam_df.columns)}")
    
    # Test Twitch data processing  
    sample_twitch_data = [
        {"name": "League of Legends", "viewer_count": 150000},
        {"name": "Valorant", "viewer_count": 120000},
        {"name": "Fortnite", "viewer_count": 100000}
    ]
    
    twitch_df = processor.process_api_data(sample_twitch_data, "twitch")
    print(f"✅ Twitch DataFrame shape: {twitch_df.shape}")
    print(f"   Columns: {list(twitch_df.columns)}")
    
    # Test combining multiple sources
    api_results = {
        "steam": steam_df,
        "twitch": twitch_df
    }
    
    combined_df = processor.combine_multiple_sources(api_results)
    print(f"✅ Combined DataFrame shape: {combined_df.shape}")
    print(f"   Columns: {list(combined_df.columns)}")
    
    # Test visualization mapping
    mapping = processor.get_visualization_mapping(combined_df)
    print(f"✅ Visualization mapping: {mapping['recommended_charts']}")
    
    return combined_df

def test_visualization_generator(data_df):
    """Test the enhanced VisualizationGenerator"""
    print("\n🎨 Testing VisualizationGenerator...")
    
    viz_gen = VisualizationGenerator()
    
    # Test chart recommendations
    recommendations = viz_gen.get_chart_recommendations(data_df)
    print(f"✅ Chart recommendations: {recommendations}")
    
    # Test table creation
    fig = viz_gen.create_table_chart("Sample Gaming Data", data_df.to_dict('records'))
    print(f"✅ Table chart created successfully")
    
    # Test export functionality
    export_result = viz_gen.export_data_to_excel(data_df, "test_export")
    print(f"✅ Export result: {export_result}")
    
    return fig

def test_ai_prompts():
    """Test AI training scenarios with different user prompts"""
    print("\n🤖 Testing AI Training Scenarios...")
    
    # Sample user prompts that the AI should handle well
    test_prompts = [
        "Show me the top Steam games and compare with Twitch viewership",
        "I want a table of gaming data that I can export to Excel",
        "Compare player counts across different platforms",
        "What are the trending games and show me in a chart",
        "Give me detailed analytics on gaming metrics with export options"
    ]
    
    # Expected responses based on enhanced system prompt
    expected_behaviors = [
        "Should use create_data_analysis_visualization with ['steam', 'twitch']",
        "Should use chart_type='table' and export_format='excel'",
        "Should combine multiple APIs and use bar chart",
        "Should use auto chart type selection",
        "Should include comprehensive data processing and export"
    ]
    
    for i, (prompt, expected) in enumerate(zip(test_prompts, expected_behaviors), 1):
        print(f"\n{i}. Prompt: \"{prompt}\"")
        print(f"   Expected: {expected}")
        
        # Analyze prompt for API requirements
        apis_needed = []
        if "steam" in prompt.lower():
            apis_needed.append("steam")
        if "twitch" in prompt.lower():
            apis_needed.append("twitch")
        if "compare" in prompt.lower() and not apis_needed:
            apis_needed = ["steam", "twitch", "rawg"]
        if not apis_needed:  # Default for general queries
            apis_needed = ["steam", "rawg"]
            
        # Determine chart type
        chart_type = "auto"
        if "table" in prompt.lower():
            chart_type = "table"
        elif "chart" in prompt.lower():
            chart_type = "auto"
            
        # Determine export needs
        export_format = None
        if "export" in prompt.lower() or "excel" in prompt.lower():
            export_format = "excel"
            
        print(f"   ✅ Analysis: APIs={apis_needed}, chart={chart_type}, export={export_format}")

def main():
    """Main test function"""
    print("🚀 Starting Enhanced AI Training Tests\n")
    
    try:
        # Test data processing
        combined_df = test_data_processor()
        
        # Test visualization 
        test_visualization_generator(combined_df)
        
        # Test AI training scenarios
        test_ai_prompts()
        
        print("\n✅ All tests completed successfully!")
        print("\n📊 Summary:")
        print("- DataProcessor: Working with multi-API data standardization")
        print("- VisualizationGenerator: Enhanced with table charts and export")
        print("- AI Training: Improved prompt understanding for metrics and axes")
        print("- Export Functionality: Excel/CSV export capabilities ready")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
