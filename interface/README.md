# 🚀 CrewAI Agent Interface

**All-in-one package:** Frontend + Backend combined for easy deployment!

Students can share and chat with each other's CrewAI agents through a beautiful web interface.

## 🎯 What This Is

A combined Next.js frontend and Express backend in one deployable package:
- **Backend:** REST API that stores agent URLs in `agents.json`
- **Frontend:** Beautiful chat UI to interact with agents
- **Deployed together:** One Railway deployment for everything!

---

## ⚡ Quick Start (Local Development)

### Option 1: Run Both Together

```bash
cd interface
npm install
npm run dev
```

This runs:
- Backend on http://localhost:3001
- Frontend on http://localhost:3000

### Option 2: Run Separately

**Terminal 1 - Backend:**
```bash
npm run dev:backend
```

**Terminal 2 - Frontend:**
```bash
npm run dev:frontend
```

---

## 🚀 Deploy to Railway (One Command!)

```bash
cd interface
railway init
railway up
railway domain
```

That's it! Railway will:
1. Install dependencies
2. Build Next.js frontend
3. Start Express backend
4. Serve everything on one URL! ✨

Your URL will look like:
```
https://crewai-interface.up.railway.app
```

---

## 📋 How Students Use It

1. **Open the deployed URL**
   ```
   https://your-interface.up.railway.app
   ```

2. **Add their agent**
   - Click "Add Your Agent"
   - Enter name and Railway URL
   - Submit!

3. **Chat with agents**
   - Click any agent from the list
   - Start chatting!
   - Switch between different agents

---

## 🏗️ Project Structure

```
interface/
├── server.js              # Express backend (API)
├── agents.json            # Stores agent URLs
├── app/                   # Next.js frontend
│   ├── page.tsx          # Main UI
│   ├── layout.tsx
│   └── globals.css
├── package.json           # Combined dependencies
├── railway.json           # Railway config
├── next.config.js         # Next.js config
├── tailwind.config.js     # Tailwind CSS
└── tsconfig.json          # TypeScript config
```

---

## 🔌 API Endpoints

All API routes are under `/api` prefix:

- **GET /api/agents** - List all agents
- **POST /api/agents** - Add new agent
- **DELETE /api/agents/:id** - Remove agent
- **GET /api/health** - Health check

Example:
```bash
curl https://your-app.up.railway.app/api/agents
```

---

## 🛠️ Development Commands

```bash
# Install dependencies
npm install

# Run both frontend and backend
npm run dev

# Run backend only
npm run dev:backend

# Run frontend only
npm run dev:frontend

# Build for production
npm run build

# Start production server
npm start
```

---

## 🌐 Environment Variables

No environment variables needed! Everything works out of the box.

The frontend automatically detects:
- **Development:** Uses `http://localhost:3001/api`
- **Production:** Uses same domain with `/api` prefix

---

## 📊 How It Works

### Development Mode
```
Frontend (localhost:3000)
    ↓
API calls to localhost:3001/api
    ↓
Backend (localhost:3001)
```

### Production Mode (Railway)
```
Browser → https://your-app.railway.app
    ↓
    ├─ /api/* → Backend API
    └─ /* → Frontend UI
```

Everything served from one domain! No CORS issues. ✨

---

## 🎓 For Teachers

### One-Time Setup:

1. **Deploy to Railway:**
   ```bash
   cd interface
   railway up
   railway domain
   ```

2. **Share URL with students:**
   ```
   https://crewai-interface.up.railway.app
   ```

3. **That's it!** Students can now:
   - Add their agents
   - See all classmates' agents
   - Chat with any agent

---

## 🎮 For Students

### Add Your Agent:

1. Deploy your Day 3 agent to Railway
2. Get your URL: `railway domain`
3. Open the interface URL (shared by teacher)
4. Click "Add Your Agent"
5. Fill in:
   - **Name:** "Alice's Agent"
   - **URL:** `https://alice-agent.up.railway.app`
   - **Description:** "Specializes in math"
6. Submit!

### Chat with Agents:

1. Click any agent from the list
2. Type your question
3. Press Enter
4. See the response!
5. Click "← Back" to try another agent

---

## 🔧 Configuration

### Backend Configuration

Edit `server.js`:
- Port: `process.env.PORT || 3001`
- Data file: `agents.json`
- API prefix: `/api`

### Frontend Configuration

Edit `app/page.tsx`:
- API base URL auto-detected
- Uses same domain in production
- Falls back to `localhost:3001` in dev

---

## 💡 Key Features

### ✅ Easy Deployment
- One command to deploy
- No environment variables needed
- Works on Railway, Render, etc.

### ✅ Simple Architecture
- Backend serves API under `/api`
- Frontend handles all other routes
- No CORS issues!

### ✅ Persistent Storage
- `agents.json` stores all data
- Survives restarts with Railway Volume

### ✅ Beautiful UI
- Modern, responsive design
- Mobile-friendly
- Smooth animations

---

## 🐛 Troubleshooting

### Can't Add Agent

**Check URL format:**
- ✅ `https://agent.up.railway.app`
- ❌ `agent.up.railway.app` (missing https://)
- ❌ `https://agent.up.railway.app/` (trailing slash)

### Can't Connect to Agent

**Test the agent directly:**
```bash
curl https://agent.up.railway.app/health
```

Should return:
```json
{"status": "healthy", ...}
```

### Backend Not Working

**Check Railway logs:**
```bash
railway logs
```

Look for errors in startup or API calls.

### Frontend Not Loading

**Check build succeeded:**
- Railway logs should show "Building Next.js"
- Should complete without errors

---

## 📈 Scaling

### Add Railway Volume (For Persistence)

To keep `agents.json` across deployments:

1. Go to Railway dashboard
2. Your service → Settings → Volumes
3. Add Volume:
   - **Mount Path:** `/app/agents.json`
   - **Size:** 1 GB

Now agents persist even after redeployments! ✅

---

## 🎨 Customization

### Change UI Colors

Edit `app/page.tsx`:
```tsx
// Change blue to purple
className="bg-purple-600 text-white"
```

### Add New API Endpoints

Edit `server.js`:
```javascript
app.get('/api/stats', async (req, res) => {
  const agents = await readAgents();
  res.json({ 
    total: agents.length,
    // ... more stats
  });
});
```

### Customize Welcome Message

Edit `app/page.tsx`:
```tsx
content: `👋 Hello! I'm ${agent.name}. Ask me anything!`
```

---

## 💰 Cost

### Railway Deployment
- **Free Tier:** $5 credit/month
- **Usage:** ~$3-5/month
- **Volume:** ~$0.25/GB/month

**Total:** ~$5/month or FREE with Railway credits! ✅

---

## 📚 Tech Stack

- **Frontend:** Next.js 14, React, TypeScript, Tailwind CSS
- **Backend:** Express.js, Node.js
- **Storage:** JSON file (`agents.json`)
- **Deployment:** Railway (or any Node.js host)

---

## ✅ What's Included

- ✅ Complete frontend UI
- ✅ Complete backend API
- ✅ Railway deployment config
- ✅ Development setup
- ✅ TypeScript support
- ✅ Tailwind CSS styling
- ✅ Error handling
- ✅ URL validation
- ✅ CORS handled
- ✅ Responsive design

---

## 🎉 Success!

When working correctly:

1. ✅ Deploy to Railway
2. ✅ Get public URL
3. ✅ Students add their agents
4. ✅ Everyone can chat with all agents
5. ✅ No separate frontend/backend deployments needed!

---

## 🆘 Need Help?

1. **Check Railway logs:** `railway logs`
2. **Test API directly:** `curl https://your-app.railway.app/api/health`
3. **Check browser console:** F12 → Console
4. **Verify agent URLs:** Make sure they start with `https://`

---

## 📖 Additional Resources

- [Railway Docs](https://docs.railway.app/)
- [Next.js Docs](https://nextjs.org/docs)
- [Express Docs](https://expressjs.com/)

---

**Built for MIT IAP NANDA Course 2026** 🚀

**One deployment. Two services. Zero hassle.** ✨
