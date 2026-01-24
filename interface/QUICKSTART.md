# ⚡ Quick Start - 3 Steps

## For Students

### Step 1: Install
```bash
cd frontend
npm install
```

### Step 2: Run
```bash
npm run dev
```

### Step 3: Connect
1. Open http://localhost:3000
2. Paste your Railway URL (from Day 3)
3. Start chatting with your agent! 🤖

---

## Get Your Railway URL

From your Day 3 folder:
```bash
cd ../day-3
railway domain
```

Copy the URL that looks like:
```
https://your-agent.up.railway.app
```

Paste it into the chat frontend (without `/query` at the end).

---

## What You'll See

1. **Configuration Screen**
   - Enter your Railway URL
   - Click "Connect to Agent"

2. **Chat Interface**
   - Type your question
   - Press Enter (or click Send)
   - See your agent's response with timing!

---

## Example Questions

Try asking:
- "What is 50 * 50?" (tests calculator)
- "What do you know about me?" (tests memory)
- "Tell me about Python" (general knowledge)

---

## Deploy Your Own (Optional)

Want your own deployed version?

### Deploy to Vercel (Free)
```bash
npm install -g vercel
vercel
```

Follow the prompts and you'll get a URL like:
```
https://your-chat.vercel.app
```

Share this with others and they can connect to their agents too!

---

## Troubleshooting

**Can't connect?**
- ✅ Check your agent is deployed on Railway
- ✅ Test with: `curl https://your-url.up.railway.app/health`
- ✅ Make sure URL doesn't end with `/`

**CORS error?**
- ✅ Already fixed in Day 3 code!

**Need help?**
- Check the console (F12 → Console)
- Read the full README.md
- Ask your instructor!

---

**That's it! Happy chatting! 🎉**

