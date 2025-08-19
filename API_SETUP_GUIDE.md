# 🔑 API Keys Setup Guide

## OpenAI API Setup (Required)

### Step 1: Create a Separate Project
1. Go to https://platform.openai.com/
2. Click **"Projects"** in the left sidebar
3. Click **"Create Project"**
4. Name: "Gaming AI Chatbot" (or similar)
5. This isolates billing for this specific project

### Step 2: Generate API Key
1. Inside your new project, go to **"API Keys"**
2. Click **"Create new secret key"**
3. Name: "Gaming Chatbot Key"
4. **Copy the key immediately** (you can't see it again!)
5. Add it to your `.env` file as `OPENAI_API_KEY`

### Step 3: Set Usage Limits (Recommended)
1. Go to **"Settings" → "Limits"**
2. Set monthly spending limit: $10-20 for testing
3. This prevents unexpected charges

### Step 4: Model Access
- Your key automatically has access to `gpt-4o`
- No special setup or "agents" needed
- The chatbot uses standard Chat Completions API

### Expected Costs
- **GPT-4o**: ~$2.50 per 1M input tokens, ~$10 per 1M output tokens
- **Typical usage**: $0.01-0.05 per conversation
- **Monthly estimate**: $5-15 for moderate testing

---

## Other APIs (Optional/Mock Data)

### Gamalytic API - ❌ Not Required
- **Status**: Uses comprehensive mock data
- **Why**: Gamalytic requires paid subscription despite advertising "free" tier
- **Impact**: Zero - realistic gaming industry data provided via mock responses
- **Data includes**: Genre analysis, market trends, revenue data, predictions

### IGDB (Internet Game Database) - ❌ Not Currently Used
- **What it is**: Game metadata database
- **Status**: Not integrated in current version
- **Future**: Could be added for additional game information

---

## Quick Setup Checklist

1. **✅ You already have your OpenAI API key ready**
2. **✅ Your Steam API key is already configured**
3. **✅ `.env` file is created with your keys**
4. **🧪 Run `python test_setup.py` to verify everything works**
5. **🚀 Run `python start.py` to launch the chatbot**

**No additional API keys needed!** The system will work perfectly with just OpenAI + Steam.

---

## Cost Management Tips

### For OpenAI API
- Start with usage limits ($10/month)
- Monitor usage in OpenAI dashboard
- The chatbot uses efficient prompts to minimize costs
- Each conversation typically costs $0.01-0.05

### Free Alternatives (if budget is a concern)
- Could modify to use local models (Ollama, etc.)
- Use OpenAI free tier credits if available
- Mock responses for development/testing

Let me know if you need help with any of these steps!
