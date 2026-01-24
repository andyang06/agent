# 🏗️ Architecture Overview

## How Everything Connects

```
┌─────────────────────────────────────────────────────────┐
│                       STUDENT'S                         │
│                       BROWSER                           │
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │        Chat Frontend (Next.js)                │     │
│  │                                               │     │
│  │  - React UI                                   │     │
│  │  - Message history                            │     │
│  │  - API URL input                              │     │
│  │  - localStorage for config                    │     │
│  └───────────────────────────────────────────────┘     │
│                        │                                │
│                        │ HTTP POST /query               │
│                        │ {"question": "..."}            │
└────────────────────────┼─────────────────────────────────┘
                         │
                         │ Internet
                         ▼
┌─────────────────────────────────────────────────────────┐
│                      RAILWAY                            │
│                                                         │
│  ┌───────────────────────────────────────────────┐     │
│  │      Student's Agent API (FastAPI)            │     │
│  │                                               │     │
│  │  - /query endpoint                            │     │
│  │  - CrewAI agent                               │     │
│  │  - Memory (ChromaDB)                          │     │
│  │  - Tools (calculator, web, etc.)              │     │
│  └───────────────────────────────────────────────┘     │
│                        │                                │
│                        │ Returns                        │
│                        │ {"answer": "...",              │
│                        │  "timestamp": "...",           │
│                        │  "processing_time": 2.5}       │
└────────────────────────┼─────────────────────────────────┘
                         │
                         ▼
                    Back to Browser
                    (displays in chat)
```

## Data Flow

### 1. Configuration Phase
```
Student opens frontend
    ↓
Enters Railway URL
    ↓
URL saved to localStorage
    ↓
Ready to chat!
```

### 2. Chat Phase
```
Student types message
    ↓
Frontend sends POST to {railway_url}/query
    ↓
FastAPI receives request
    ↓
CrewAI agent processes (uses memory + tools)
    ↓
Agent returns answer
    ↓
Frontend displays response with timing
```

## File Structure

### Frontend (This Folder)
```
frontend/
├── app/
│   ├── page.tsx           # Main chat UI component
│   ├── layout.tsx         # Root layout wrapper
│   └── globals.css        # Global styles + Tailwind
├── package.json           # Dependencies (React, Next.js)
├── tailwind.config.js     # Tailwind CSS config
├── tsconfig.json          # TypeScript config
└── README.md              # Documentation
```

### Backend (Day 3)
```
day-3/
├── main.py                # FastAPI + CrewAI agent
├── requirements.txt       # Python dependencies
├── railway.json           # Railway config
└── README.md              # Deployment guide
```

## API Contract

The frontend and backend communicate via this simple API:

### Request (Frontend → Backend)
```typescript
POST {apiUrl}/query
Content-Type: application/json

{
  "question": string,      // User's question
  "user_id": string        // Always "student"
}
```

### Response (Backend → Frontend)
```typescript
200 OK
Content-Type: application/json

{
  "answer": string,           // Agent's response
  "timestamp": string,        // ISO 8601 format
  "processing_time": number   // Seconds (float)
}
```

### Error Response
```typescript
500 Internal Server Error
Content-Type: application/json

{
  "detail": string  // Error message
}
```

## Technologies Used

### Frontend Stack
- **Next.js 14:** React framework with App Router
- **TypeScript:** Type-safe JavaScript
- **Tailwind CSS:** Utility-first styling
- **localStorage:** Persistent config (browser)

### Backend Stack (Day 3)
- **FastAPI:** Python web framework
- **CrewAI:** AI agent framework
- **ChromaDB:** Vector database for memory
- **OpenAI:** LLM provider
- **Railway:** Cloud hosting

## Security & Privacy

- **No Authentication:** Simple demo (add auth for production)
- **CORS:** Enabled on backend (allows browser requests)
- **API Keys:** Backend handles all API keys (never exposed)
- **Data Storage:** 
  - Frontend: Only API URL in localStorage
  - Backend: Agent memory stored in Railway Volume

## Deployment Options

### Frontend Deployment
1. **Vercel** (Recommended - Free)
   ```bash
   vercel
   ```

2. **Netlify** (Alternative)
   ```bash
   npm run build
   # Upload build folder to Netlify
   ```

3. **Railway** (Same as backend)
   ```bash
   railway up
   ```

### Shared vs Individual Frontends

**Option A: Shared Frontend (Recommended for Teachers)**
- Deploy ONE frontend to Vercel
- All students use same URL
- Each student enters their own Railway agent URL
- Benefits: Simple, one deployment

**Option B: Individual Frontends**
- Each student deploys their own frontend
- More customization options
- Good for learning deployment
- Benefits: Portfolio project

## Customization Ideas

### Easy Customizations
1. **Colors:** Change Tailwind classes in `page.tsx`
2. **Logo:** Add image in header
3. **Title:** Update text in configuration screen
4. **Placeholder:** Change input placeholder text

### Medium Customizations
1. **Message Export:** Add button to download chat history
2. **Dark Mode:** Add theme toggle
3. **User Avatar:** Show user initials or image
4. **Typing Indicator:** More realistic agent "typing"

### Advanced Customizations
1. **Authentication:** Add user login
2. **Multi-Agent:** Connect to multiple agents
3. **Streaming:** Real-time token streaming
4. **Voice Input:** Speech-to-text integration
5. **Analytics:** Track usage and popular questions

## Troubleshooting

### Frontend Issues
- **Won't start:** Run `npm install` again
- **Port in use:** Change port in `package.json` dev script
- **TypeScript errors:** Check `tsconfig.json` is correct

### Connection Issues
- **CORS error:** Backend needs CORS enabled (already is!)
- **Network error:** Check Railway URL is correct
- **Timeout:** Agent taking too long (check Railway logs)

### Backend Issues
- **Agent not responding:** Check Railway logs
- **Memory not working:** Check Volume is mounted
- **API key error:** Check environment variables

## Performance

### Frontend Performance
- **Bundle Size:** ~200KB (Next.js + React)
- **Load Time:** <1s on modern connection
- **Responsiveness:** Instant UI updates

### Backend Performance
- **Cold Start:** ~5s (Railway free tier)
- **Warm Request:** 2-5s (depends on agent complexity)
- **Memory:** ~500MB RAM (Railway)

## Cost Breakdown

### Frontend (Vercel Free Tier)
- **Hosting:** FREE (100GB bandwidth/month)
- **Builds:** FREE (100 builds/month)
- **Total:** $0/month ✅

### Backend (Railway)
- **Free Tier:** $5 credit/month
- **Hobby Plan:** $5/month (500 hours)
- **Volume:** ~$0.25/GB/month
- **Total:** ~$5-10/month per student

## Next Steps

### For Students
1. ✅ Deploy Day 3 agent to Railway
2. ✅ Run this frontend locally
3. ✅ Connect and test
4. ⭐ (Optional) Deploy frontend to Vercel
5. ⭐ (Optional) Customize the UI

### For Teachers
1. ✅ Deploy one shared frontend to Vercel
2. ✅ Share URL with all students
3. ✅ Students enter their Railway URLs
4. ✅ Everyone chats with their own agent!

---

**Built for MIT IAP NANDA Course 2026** 🚀

