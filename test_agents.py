"""
Test script to compare the original OpenAI-based agent vs Pydantic AI agent
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_original_agent():
    """Test the original OpenAI-based agent"""
    print("=" * 60)
    print("🔧 TESTING ORIGINAL OPENAI AGENT")
    print("=" * 60)
    
    try:
        # Import original agent
        from agent.chatbot_agent import GamingChatbotAgent as OriginalAgent
        
        agent = OriginalAgent()
        print("✅ Original agent initialized successfully")
        
        # Test simple query
        response, viz = agent.respond("What are the top games on Steam?")
        print(f"\n📝 Query: What are the top games on Steam?")
        print(f"🤖 Response: {response[:200]}...")
        print(f"📊 Visualization: {'✅ Present' if viz else '❌ None'}")
        
    except ImportError as e:
        print(f"❌ Failed to import original agent: {e}")
    except Exception as e:
        print(f"❌ Error testing original agent: {e}")

def test_pydantic_agent():
    """Test the new Pydantic AI agent"""
    print("\n" + "=" * 60)
    print("🚀 TESTING PYDANTIC AI AGENT")
    print("=" * 60)
    
    try:
        # Import Pydantic agent
        from agent.chatbot_agent_pydantic import GamingChatbotAgent as PydanticAgent
        
        agent = PydanticAgent()
        print("✅ Pydantic agent initialized successfully")
        
        # Test simple query
        response, viz = agent.respond("What are the top games on Steam?")
        print(f"\n📝 Query: What are the top games on Steam?")
        print(f"🤖 Response: {response[:200]}...")
        print(f"📊 Visualization: {'✅ Present' if viz else '❌ None'}")
        
        # Test game info query
        response2, viz2 = agent.respond("Tell me about Cyberpunk 2077")
        print(f"\n📝 Query: Tell me about Cyberpunk 2077")
        print(f"🤖 Response: {response2[:200]}...")
        print(f"📊 Visualization: {'✅ Present' if viz2 else '❌ None'}")
        
    except ImportError as e:
        print(f"❌ Failed to import Pydantic agent: {e}")
    except Exception as e:
        print(f"❌ Error testing Pydantic agent: {e}")

def compare_agents():
    """Compare both agents side by side"""
    print("\n" + "=" * 60)
    print("⚖️  AGENT COMPARISON")
    print("=" * 60)
    
    print("\n📊 Feature Comparison:")
    print("┌─────────────────────────────┬─────────────┬─────────────┐")
    print("│ Feature                     │ Original    │ Pydantic AI │")
    print("├─────────────────────────────┼─────────────┼─────────────┤")
    print("│ LLM Framework               │ OpenAI SDK  │ Pydantic AI │")
    print("│ Function Calling            │ Manual      │ Decorators  │")
    print("│ Type Safety                 │ Basic       │ Advanced    │")
    print("│ Structured Outputs          │ Manual      │ Built-in    │")
    print("│ Dependency Injection        │ None        │ Built-in    │")
    print("│ Model Support               │ OpenAI Only │ Multi-model │")
    print("│ Tool Definition             │ JSON Schema │ Annotations │")
    print("│ Error Handling              │ Manual      │ Automatic   │")
    print("│ Fallback Mode               │ Basic       │ Advanced    │")
    print("└─────────────────────────────┴─────────────┴─────────────┘")
    
    print("\n🎯 Key Improvements in Pydantic AI Version:")
    print("• ✅ Type-safe tool definitions with Pydantic models")
    print("• ✅ Dependency injection for clean separation of concerns")
    print("• ✅ Structured response models for consistent outputs")
    print("• ✅ Automatic validation and error handling")
    print("• ✅ Support for multiple LLM providers (OpenAI, Anthropic, etc.)")
    print("• ✅ Decorator-based tool registration")
    print("• ✅ Dynamic system prompts with context")
    print("• ✅ Graceful fallback when Pydantic AI is not available")

def main():
    """Main test function"""
    print("🎮 Gaming AI Agent Comparison Test")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test original agent
    test_original_agent()
    
    # Test Pydantic agent
    test_pydantic_agent()
    
    # Compare features
    compare_agents()
    
    print(f"\n✅ Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
