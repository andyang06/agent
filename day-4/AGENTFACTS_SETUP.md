# AgentFacts Configuration Guide

## ⚠️ Important: AgentFacts is AUTO-GENERATED

Your agent **automatically generates** the AgentFacts at `/agentfacts` endpoint based on constants in your code.

You **DO NOT** need to manually edit `agentfacts_example.json` - it's just a reference!

## 🔧 What You Need to Configure

Edit `main.py` (lines 108-116) with your info:

```python
# ==============================================================================
# Agent Identity Configuration
# ==============================================================================
# 👇 EDIT THESE VALUES - This is your agent's public information

MY_AGENT_USERNAME = "edith"  # 👈 CHANGE THIS: Your unique username
MY_AGENT_NAME = "E.D.I.T.H"      # 👈 CHANGE THIS: Human-readable name
MY_AGENT_DESCRIPTION = "AI agent with memory and tools for research, assistance, daily tasks, questions, help with everything"  # 👈 CHANGE THIS
MY_AGENT_PROVIDER = "Andy Yang"        # 👈 CHANGE THIS: Your name
MY_AGENT_PROVIDER_URL = " https://frontend-production-0617.up.railway.app"  # 👈 CHANGE THIS: Your website

# Optional - usually don't need to change these
MY_AGENT_ID = MY_AGENT_USERNAME  # Uses username as ID
MY_AGENT_VERSION = "1.0.0"
MY_AGENT_JURISDICTION = "USA"
```

**Why in code and not environment variables?**
- These are **public information** (shown in AgentFacts)
- NOT secrets like API keys
- Easier to edit and version control
- Students can see exactly what to change

## 🚀 After Configuration

1. **Locally:** Run `uvicorn main:app --reload`
2. **Visit:** `http://localhost:8000/agentfacts`
3. **See your auto-generated AgentFacts!**

## 📋 On Railway

After deployment:
- Visit: `https://YOUR_RAILWAY_URL.up.railway.app/agentfacts`
- Railway automatically sets `PUBLIC_URL` (used in endpoints)
- Your AgentFacts will show the correct Railway URL

## 🎯 What Changes Automatically

Based on your code:
- `agent_name` → Uses `MY_AGENT_USERNAME`
- `label` → Uses `MY_AGENT_NAME`
- `description` → Uses `MY_AGENT_DESCRIPTION`
- `provider.name` → Uses `MY_AGENT_PROVIDER`
- `provider.url` → Uses `MY_AGENT_PROVIDER_URL`
- `endpoints.static` → Uses `PUBLIC_URL` (Railway sets this)
- `skills` → Auto-detected from your agent's tools

## ✅ Quick Check

Test your configuration:
```bash
curl http://localhost:8000/agentfacts
```

You should see your custom values (not "personal-agent-twin" placeholders)!

## 🔐 What About Secrets?

**Secrets (like API keys)** still go in `.env` or Railway environment variables:
```bash
OPENAI_API_KEY=your-secret-key     # ← Secret! Use env var
SERPER_API_KEY=your-secret-key     # ← Secret! Use env var
```

**Public info (like your name)** goes directly in `main.py`:
```python
MY_AGENT_NAME = "Maria's Agent"    # ← Public! In code
MY_AGENT_PROVIDER = "Maria"        # ← Public! In code
```
