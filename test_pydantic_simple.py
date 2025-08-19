"""
Simple test of the Pydantic AI agent in fallback mode
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_pydantic_fallback():
    """Test the Pydantic AI agent in fallback mode"""
    print("🚀 Testing Pydantic AI Agent (Fallback Mode)")
    print("=" * 50)
    
    try:
        from agent.chatbot_agent_pydantic import GamingChatbotAgent
        
        # Initialize agent
        agent = GamingChatbotAgent()
        
        # Test basic queries
        queries = [
            "What are the top games on Steam?",
            "Tell me about Elden Ring", 
            "Show me API usage statistics",
            "What are the most popular games on Twitch?"
        ]
        
        for query in queries:
            print(f"\n📝 Query: {query}")
            try:
                response, viz = agent.respond(query)
                print(f"🤖 Response: {response[:100]}...")
                print(f"📊 Visualization: {'✅ Present' if viz else '❌ None'}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        print(f"\n✅ Test completed successfully!")
        print(f"💾 Conversation history: {len(agent.get_conversation_history())} items")
        
    except Exception as e:
        print(f"❌ Failed to test agent: {e}")

if __name__ == "__main__":
    test_pydantic_fallback()
