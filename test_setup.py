"""
Test script to verify the gaming AI chatbot setup
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import dash
        print("✅ Dash imported successfully")
    except ImportError as e:
        print(f"❌ Dash import failed: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import numpy
        print("✅ Numpy imported successfully")
    except ImportError as e:
        print(f"❌ Numpy import failed: {e}")
        return False
    
    return True

def test_agent_init():
    """Test that the agent can be initialized"""
    print("\n🤖 Testing agent initialization...")
    
    try:
        from agent import GamingChatbotAgent
        agent = GamingChatbotAgent()
        print("✅ Gaming chatbot agent initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def test_visualization():
    """Test that visualization generator works"""
    print("\n📊 Testing visualization generator...")
    
    try:
        from utils.visualization import VisualizationGenerator
        viz_gen = VisualizationGenerator()
        
        # Create a simple chart
        fig = viz_gen.create_chart("bar", "test_data", "Test Chart")
        print("✅ Visualization generator working")
        return True
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def test_apis():
    """Test that API clients can be initialized"""
    print("\n🔌 Testing API clients...")
    
    try:
        from apis import SteamAPI, SteamSpyAPI, GamalyticAPI
        
        steam_api = SteamAPI()
        print("✅ Steam API client initialized")
        
        steamspy_api = SteamSpyAPI()
        print("✅ SteamSpy API client initialized")
        
        gamalytic_api = GamalyticAPI()
        print("✅ Gamalytic API client initialized")
        
        return True
    except Exception as e:
        print(f"❌ API clients test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎮 Gaming AI Chatbot - System Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_apis,
        test_visualization,
        test_agent_init
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Gaming AI Chatbot is ready to run.")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("   OR")
        print("   python start.py")
    else:
        print("⚠️  Some tests failed. Please install missing dependencies:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
