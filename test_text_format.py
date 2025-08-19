"""
Simple text formatting test - just test the response generation
"""

def test_text_response():
    # Simulate the response generation without APIs
    response = "Here are the most popular games on twitch by viewer count:\n\n"
    
    for i in range(1, 6):
        game = f"Game {i}"
        viewers = 100000 - (i * 10000)
        if viewers >= 1_000_000:
            formatted_viewers = f"{viewers/1_000_000:.1f}M"
        elif viewers >= 1_000:
            formatted_viewers = f"{viewers:,.0f}"
        else:
            formatted_viewers = f"{viewers:.1f}"
        
        response += f"{i}. {game}: {formatted_viewers}\n"
    
    response += "\n📊 Data from Twitch API"
    
    print("🧪 TESTING TEXT FORMATTING:")
    print("RAW RESPONSE:")
    print(repr(response))
    print("\nFORMATTED RESPONSE:")
    print(response)
    print("\n" + "="*50)
    
    # Test game name extraction
    queries = [
        "What other games do players of Total War Attila play the most?",
        "What are similar games to Counter-Strike?",
        "Tell me about Dota 2 statistics"
    ]
    
    print("🧪 TESTING GAME NAME EXTRACTION:")
    for query in queries:
        print(f"Query: {query}")
        
        # Simulate extraction logic
        query_lower = query.lower()
        extracted_game = None
        
        if "players of" in query_lower:
            parts = query_lower.split("players of")
            if len(parts) > 1:
                game_part = parts[1].strip()
                game_part = game_part.replace(" play", "").replace(" also play", "").replace("?", "").replace(" the most", "").strip()
                if game_part:
                    extracted_game = game_part.title()
        
        elif "similar" in query_lower and "to" in query_lower:
            parts = query_lower.split(" to ")
            if len(parts) > 1:
                game_part = parts[1].strip()
                game_part = game_part.replace("?", "").strip()
                if game_part:
                    extracted_game = game_part.title()
        
        elif "tell me about" in query_lower:
            parts = query_lower.split("tell me about")
            if len(parts) > 1:
                game_name = parts[1].strip()
                game_name = game_name.replace("statistics", "").replace("?", "").strip()
                if game_name:
                    extracted_game = game_name.title()
        
        print(f"Extracted game: {extracted_game}")
        print("-" * 30)

if __name__ == "__main__":
    test_text_response()
