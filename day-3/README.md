# Day 3: Deploy Your Agent to Railway

**Goal:** Deploy your Day 2 agent (with memory and tools) to the cloud using Railway, making it accessible via REST API from anywhere!

---

## ⚡ Quick Start (5 Steps)

```bash
# 1. Deploy
cd day-3
railway link
railway up

# 2. Add OPENAI_API_KEY
# Go to railway.app → Your Service → Variables → Add OPENAI_API_KEY

# 3. Add Volume for Memory
# Settings → Volumes → Mount path: /root/.local/share/crewai → Size: 1 GB

# 4. Get URL
railway domain

# 5. Test
curl https://your-url.up.railway.app/health
```

**See detailed instructions below!**

---

## 🎯 What You'll Learn

- **What is FastAPI?** How to turn Python code into a web service
- **What is REST API?** How to make your agent accessible via HTTP
- **Cloud Deployment:** How to deploy to Railway using CLI
- **Memory Persistence:** How to keep ChromaDB working in production
- **Microservices:** How to connect multiple services (agent + database)

---

## 📚 Understanding FastAPI

### What is FastAPI?

**FastAPI** is a Python web framework that creates REST APIs. Think of it as a translator:

```
Before (Day 1-2):
You → Terminal → Python script → Agent → Response
(Only works on your computer)

After (Day 3):
Anyone → Internet → HTTP Request → FastAPI → Agent → Response
(Works from anywhere in the world!)
```

### Why Do We Need It?

Without FastAPI, your agent only runs locally. With FastAPI:
- ✅ Anyone can use your agent via HTTP requests
- ✅ Works from terminal, browser, or other apps
- ✅ Can be integrated into websites or mobile apps
- ✅ Industry-standard way to expose AI services

### How Does It Work?

```python
# This is an API endpoint
@app.post("/query")
async def query_agent(request: QueryRequest):
    # Your agent code here
    result = crew.kickoff(inputs={"question": request.question})
    return {"answer": result}

# Now accessible via:
curl -X POST https://your-app.com/query -d '{"question": "Hello"}'
```

---

## 🏗️ Architecture Overview

We'll deploy **one service** with persistent storage:

```
┌─────────────────────────────────┐
│  Your Agent Service             │
│  (FastAPI + CrewAI)             │
│                                 │
│  ┌─────────────────────┐        │
│  │  Your Agent Code    │        │
│  │  - FastAPI wrapper  │        │
│  │  - Memory + Tools   │        │
│  └─────────────────────┘        │
│           ↓                     │
│  ┌─────────────────────┐        │
│  │  ChromaDB (Local)   │        │
│  │  - Stored in Volume │        │
│  │  - Persistent       │        │
│  └─────────────────────┘        │
└─────────────────────────────────┘
         ▲
         │
    HTTP Requests
    (from anywhere!)
```

**Why this approach?**
- **Simple:** One service to manage
- **Persistent:** Railway Volume keeps memory across restarts
- **Cost-effective:** Single service = lower costs
- **Perfect for learning:** Focus on deployment basics

---

## 🚀 Deployment Steps

### Prerequisites

1. **Railway Account:** Sign up at [railway.app](https://railway.app)
2. **Railway CLI:** Install Railway CLI
   ```bash
   # macOS/Linux
   curl -fsSL https://railway.app/install.sh | sh
   
   # Or via npm
   npm install -g @railway/cli
   ```
3. **OpenAI API Key:** From Day 1-2

---

## 📋 Deployment Steps (Simple!)

**What you'll do:**
1. Deploy your agent → Creates one service on Railway
2. Add environment variables → OPENAI_API_KEY
3. Add a volume → Makes memory persistent
4. Done! → Agent works with memory

**That's it!** Simple, one service, everything works.

### Step 1: Deploy Your Agent

```bash
# Make sure you're in the day-3 directory
cd day-3

# Login to Railway (first time only)
railway login

# Create/link project
railway link

# First deployment (creates the service)
railway up
```

**⚠️ This will fail** because OPENAI_API_KEY is missing - that's expected! This step creates the service.

### Step 2: Add Environment Variables

Now add your OpenAI API key so the agent can work.

**Option A: Via Railway Dashboard (Easier)**
1. Go to [railway.app](https://railway.app)
2. Click your project → Click your service
3. Go to **Variables** tab
4. Click **+ New Variable**
5. Add `OPENAI_API_KEY` with your key value
6. (Optional) Add `SERPER_API_KEY` for web search tool
7. Railway automatically redeploys!

**Option B: Via CLI**
```bash
# Set environment variables AFTER first deploy
railway variables --set "OPENAI_API_KEY=your-key-here"

# Optional: Add SERPER_API_KEY for web search
railway variables --set "SERPER_API_KEY=your-serper-key"

# Deploy again with variables
railway up
```



**What Railway does:**
1. Reads `railway.json` for config
2. Installs packages from `requirements.txt`
3. Starts your FastAPI server
4. Gives you a public URL

### Step 3: Add Volume (For Memory!)

**⚠️ Without this, your agent forgets everything when it restarts!**

**Where to do it:**
1. Go to Railway dashboard → Your service
2. Click **Settings** tab (top)
3. Scroll to **Volumes** section
4. Click **New Volume**

**What to enter:**
- **Mount Path:** `/root/.local/share/crewai`
- **Size:** 1 GB

**Done!** Railway redeploys automatically and memory now persists. ✅

### Step 4: Get Your Public URL

After deployment completes (takes 2-3 minutes):

**Option A: CLI**
```bash
railway domain
```

**Option B: Dashboard**
- Go to railway.app → Your service → "Settings" tab
- Look for "Public URL" or click "Generate Domain"

**Example output:**
```
https://day-3-agent-production.up.railway.app
```

Save this URL - you'll use it to interact with your agent!

---

## 🧪 Testing Your Deployed Agent

### Test 1: Health Check

```bash
curl https://your-app.up.railway.app/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "memory_enabled": true,
  "tools_count": 5
}
```

### Test 2: Query Your Agent

```bash
curl -X POST https://your-app.up.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is 123 * 456?"}'
```

**Expected response:**
```json
{
  "answer": "The result of 123 * 456 is 56,088.",
  "timestamp": "2026-01-24T10:30:00Z",
  "processing_time": 2.5
}
```

### Test 3: Test Memory

```bash
# First request - tell the agent something
curl -X POST https://your-app.up.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{"question": "My name is Alex and I love Python"}'

# Second request - see if it remembers
curl -X POST https://your-app.up.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is my name?"}'
```

**Expected:** Agent should remember your name from the first request!

### Test 4: Interactive Documentation

Visit in your browser:
```
https://your-app.up.railway.app/docs
```

This shows **Swagger UI** - an interactive API documentation where you can:
- See all endpoints
- Test queries directly in the browser
- View request/response schemas

---

## 🔍 Understanding the Code

### Key Components

#### 1. FastAPI Setup (`main.py` lines 38-48)
```python
app = FastAPI(
    title="Personal Agent Twin API",
    description="Your agent with memory and tools",
    version="1.0.0"
)
```
Creates the web application that handles HTTP requests.

#### 2. Request/Response Models (lines 50-68)
```python
class QueryRequest(BaseModel):
    question: str
    user_id: str = "anonymous"
```
Defines what data the API expects and returns. Pydantic validates this automatically.

#### 3. Agent Setup (lines 120-170)
```python
my_agent_twin = Agent(
    role="Personal Digital Twin",
    tools=available_tools,
    llm=llm,
)
```
Same agent from Day 2, with memory and tools!

#### 4. API Endpoints (lines 180-260)
```python
@app.post("/query")
async def query_agent(request: QueryRequest):
    crew = Crew(
        agents=[my_agent_twin],
        tasks=[task],
        memory=True  # Memory enabled!
    )
    result = crew.kickoff()
    return {"answer": result}
```
Handles incoming HTTP requests and runs your agent.

---

## 🛠️ Troubleshooting

### Problem: Deployment fails during build

**Symptom:** Build fails with `ERROR: Could not find a version that satisfies the requirement...`

**How to diagnose:**
1. Click **"View logs"** in Railway dashboard
2. Look for the **"Build"** section (red X)
3. Read the error message carefully

**Common build errors:**

#### 1. **Package not found** (Most common for students!)
```
ERROR: Could not find a version that satisfies the requirement serper>=0.1.0
ERROR: No matching distribution found for serper>=0.1.0
```

**Cause:** Package name is wrong or doesn't exist on PyPI  
**Fix:** Remove or fix the package in `requirements.txt`

**Example - SerperDevTool:**
- ❌ `serper>=0.1.0` (doesn't exist!)
- ✅ Already included in `crewai-tools` - no separate package needed

#### 2. **Python version mismatch**
```
ERROR: Ignored the following versions that require a different python version
```

**Fix:** Check package compatibility with Python 3.10+

#### 3. **Missing OPENAI_API_KEY** (After successful build)
```
Application error: Missing API key
```

**Fix:** Add OPENAI_API_KEY in Variables tab (see Step 2)

**Check logs:**
```bash
railway logs
```

**Still stuck?**
- Copy the exact error message
- Check Railway's build logs (click "View logs")
- Verify all files are committed and pushed

### Problem: Memory not working

**Symptoms:** Agent doesn't remember previous conversations

**Solutions:**
1. Check ChromaDB is running: `railway status`
2. Verify connection variables are set
3. Check logs for ChromaDB connection errors

**Test ChromaDB directly:**
```bash
# Get ChromaDB service URL
railway variables

# Should show CHROMA_HOST and CHROMA_PORT
```

### Problem: Agent times out

**Cause:** Query takes too long (>30 seconds)

**Solutions:**
- Simplify agent backstory
- Reduce tool usage
- Increase Railway timeout in settings

### Problem: "Port already in use" locally

**Solution:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001
```

---

## 💰 Cost Considerations

### Railway Pricing

- **Free Tier:** $5 credit/month
- **Hobby Plan:** $5/month (500 hours)
- **Pro Plan:** $20/month (unlimited)

### What Uses Credits?

- **Compute time:** Running your services
- **Storage:** ChromaDB persistent volume (~$0.25/GB/month)
- **Network:** Outbound data transfer

### Optimization Tips

1. **Use GPT-4o-mini** (cheaper than GPT-4)
2. **Stop services** when not in use: `railway down`
3. **Monitor usage:** Check Railway dashboard regularly
4. **Limit memory size:** ChromaDB grows over time

---

## 📊 Monitoring Your Agent

### View Logs

```bash
# Real-time logs
railway logs --follow

# Last 100 lines
railway logs --tail 100
```

### Check Status

```bash
# Service status
railway status

# List all services
railway service list
```

### View Variables

```bash
# List all variables for your service
railway variables

# View in key=value format
railway variables --kv
```

### View Metrics

Visit Railway dashboard:
- CPU usage
- Memory usage
- Request counts
- Error rates

---

## 🎓 What You Learned

✅ **FastAPI Basics:** How to create REST APIs with Python  
✅ **HTTP/REST:** How web services communicate  
✅ **Cloud Deployment:** Using Railway CLI  
✅ **Microservices:** Separating database from application  
✅ **Environment Variables:** Managing secrets in production  
✅ **API Testing:** Using curl and Swagger UI  
✅ **Memory Persistence:** Keeping data across deployments  

---

## 🚀 Next Steps

### Day 4: Multi-Agent Coordination

Now that your agent is deployed, you can:
- Connect multiple agents together
- Build agent-to-agent communication
- Create complex workflows

### Bonus Challenges

1. **Add authentication:** Protect your API with API keys
2. **Add rate limiting:** Prevent abuse
3. **Add caching:** Speed up common queries
4. **Custom domain:** Use your own domain name
5. **Monitoring:** Add logging and error tracking

---

## 📚 Resources

- [Railway Documentation](https://docs.railway.app/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CrewAI Memory Docs](https://docs.crewai.com/concepts/memory)
- [ChromaDB Documentation](https://docs.trychroma.com/)

---

## ✅ Day 3 Checklist

Before moving to Day 4:

- [ ] Agent deployed on Railway
- [ ] Railway Volume added (`/root/.local/share/crewai`)
- [ ] Environment variables configured (OPENAI_API_KEY)
- [ ] Health check endpoint works
- [ ] Query endpoint works
- [ ] Memory persistence tested
- [ ] Public URL accessible from terminal

---

## 📚 Appendix: Advanced Approach - Two-Service Architecture

**For advanced students** who want to learn microservices architecture, you can deploy ChromaDB as a separate service:

### Why Use Two Services?

- **Scalability:** Scale database and application independently
- **Isolation:** Database issues don't affect application
- **Professional:** Industry-standard microservices pattern
- **Flexibility:** Can connect multiple agents to one ChromaDB

### How to Deploy Two Services

1. **Deploy ChromaDB First:**
   - Go to https://railway.app/template/kbvIRV
   - Click "Deploy Now" - creates ChromaDB with persistent volume
   - Note the service name (usually "Chroma")

2. **Deploy Your Agent:**
   - Follow Steps 1-2 from main guide
   - Add connection variables:
   ```bash
   railway variables --set "CHROMA_HOST=${{Chroma.RAILWAY_PRIVATE_DOMAIN}}"
   railway variables --set "CHROMA_PORT=8000"
   ```

3. **Connect via Private Network:**
   - Railway automatically handles private networking
   - No authentication needed between services
   - Services communicate securely within project

**Note:** This is more complex but teaches valuable microservices concepts!

---

**🎉 Congratulations!** Your agent is now live on the internet and anyone can interact with it via HTTP!
