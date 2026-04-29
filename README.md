# 🤖 E.D.I.T.H - Enhanced Digital Intelligence & Tactical Helper

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

**A sophisticated multimodal AI agent system with memory, tool usage, and agent-to-agent communication**

[Live Demo](https://brave-magic-production-65d3.up.railway.app) • [Frontend](https://frontend-production-0617.up.railway.app) • [Documentation](#documentation)

</div>

---

## 📖 Overview

E.D.I.T.H is a full-stack AI agent system. It demonstrates advanced AI concepts including multi-agent systems, RAG (Retrieval-Augmented Generation), multimodal processing, and distributed agent communication protocols.

### ✨ Key Achievements

- 🧠 **Intelligent Memory System** - 4-type memory architecture (short-term, long-term, entity, contextual)
- 🎨 **Multimodal Capabilities** - Text, image generation/analysis, audio processing, PDF analysis
- 🌐 **RESTful API** - Production-ready FastAPI backend with 9 specialized tools
- 🤝 **Agent-to-Agent Communication** - Implements A2A protocol for distributed agent networks
- 🎯 **Custom JARVIS-style UI** - Sleek Next.js frontend with real-time weather integration
- ☁️ **Cloud Deployment** - Fully deployed on Railway with CI/CD via GitHub

---

## 🚀 Tech Stack

### Backend
- **CrewAI** - AI agent orchestration framework
- **FastAPI** - High-performance REST API
- **OpenAI GPT-4o-mini** - Primary LLM for reasoning
- **ChromaDB** - Vector database for memory persistence
- **OpenAI Multimodal APIs** - DALL-E 3, GPT-4 Vision, Whisper, TTS

### Frontend
- **Next.js 14** - React framework with server-side rendering
- **Express.js** - API middleware layer
- **Custom SVG Icons** - Tech-inspired UI elements
- **Real-time Weather API** - Live weather integration

### Deployment & DevOps
- **Railway** - Cloud hosting platform
- **GitHub Actions** - CI/CD automation
- **Docker** (via Railway) - Containerized deployments
- **Environment Management** - Secure API key handling

---

## 🎯 Core Features

### 🧰 Advanced Tool Suite (9 Tools)

| Tool | Description | Technology |
|------|-------------|------------|
| **Calculator** | Mathematical computations | Python eval |
| **Web Search** | Real-time web queries | SerperDev API |
| **Website RAG** | Extract & analyze website content | BeautifulSoup + RAG |
| **YouTube RAG** | Search & analyze video transcripts | YouTube Transcript API |
| **File Reader** | Process local files | Python I/O |
| **Image Generation** | Create images from text | DALL-E 3 |
| **Image Analysis** | OCR, object detection, scene understanding | GPT-4 Vision |
| **Speech-to-Text** | Transcribe audio (9 languages) | Whisper |
| **Text-to-Speech** | Generate audio (6 voices) | OpenAI TTS |
| **PDF Analysis** | Extract text from documents | pdfplumber |

### 🧠 Intelligent Memory System

```
┌─────────────────────────────────────────┐
│         Memory Architecture             │
├─────────────────────────────────────────┤
│  Short-Term   │  Recent conversation    │
│  Long-Term    │  Important facts        │
│  Entity       │  People, places, topics │
│  Contextual   │  Combined insights      │
└─────────────────────────────────────────┘
```

### 🤝 Agent-to-Agent (A2A) Communication

- **AgentFacts Protocol** - Standardized capability discovery
- **Message Routing** - `@agent-id` mention system
- **Cross-Agent Collaboration** - Query external agents for specialized tasks
- **Smart Agent Discovery** - LLM-powered agent selection from registry

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     E.D.I.T.H System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐         ┌─────────────────┐          │
│  │   Next.js UI    │────────▶│  Express API    │          │
│  │  (Port 3000)    │         │  (Port 3001)    │          │
│  └─────────────────┘         └─────────────────┘          │
│           │                           │                     │
│           │                           ▼                     │
│           │                  ┌─────────────────┐          │
│           └─────────────────▶│   FastAPI       │          │
│                              │  Backend API    │          │
│                              │  (Port 8000)    │          │
│                              └─────────────────┘          │
│                                      │                     │
│                    ┌─────────────────┼─────────────────┐  │
│                    │                 │                 │  │
│           ┌────────▼────────┐ ┌─────▼──────┐ ┌───────▼──────┐
│           │  CrewAI Agent   │ │ ChromaDB   │ │ OpenAI APIs  │
│           │  (9 Tools)      │ │  (Memory)  │ │ (Multimodal) │
│           └─────────────────┘ └────────────┘ └──────────────┘
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key
- (Optional) SerperDev API key for web search

### 1. Clone Repository

```bash
git clone https://github.com/andyang06/agent.git
cd agent
```

### 2. Backend Setup (Day 4 - A2A Agent)

```bash
cd day-4

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your API keys to .env

# Run locally
uvicorn main:app --reload
```

**Backend runs at:** `http://localhost:8000`

### 3. Frontend Setup (E.D.I.T.H Interface)

```bash
cd interface

# Install dependencies
npm install

# Run development server
npm run dev
```

**Frontend runs at:** `http://localhost:3000`

---

## 📊 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API information & status |
| `GET` | `/health` | Health check |
| `GET` | `/agentfacts` | Agent capabilities (A2A discovery) |
| `POST` | `/query` | Direct agent query |
| `POST` | `/a2a` | Agent-to-agent messaging |
| `POST` | `/search` | Intelligent agent routing |
| `GET` | `/docs` | Interactive API documentation |

### Example: Query Agent

```bash
curl -X POST https://brave-magic-production-65d3.up.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are my interests?",
    "user_id": "demo-user"
  }'
```

### Example: A2A Communication

```bash
curl -X POST https://brave-magic-production-65d3.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "@weather-agent What is the weather in Boston?",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "conv-123"
  }'
```

---

## 📁 Project Structure

```
5-day-course/
├── day-1/          # Basic agent loop + AI twin
├── day-2/          # Memory + tools integration
├── day-3/          # FastAPI + Railway deployment
├── day-4/          # A2A communication (PRIMARY)
│   ├── main.py                 # FastAPI app + CrewAI agent
│   ├── requirements.txt        # Python dependencies
│   ├── railway.json            # Deployment config
│   ├── .env                    # Environment variables
│   └── testing/
│       └── agent_test_gui.html # Testing interface
├── interface/      # E.D.I.T.H frontend (PRIMARY)
│   ├── app/                    # Next.js pages
│   ├── server.js               # Express API middleware
│   ├── agents.json             # Agent registry
│   └── railway.json            # Frontend deployment config
└── README.md       # This file
```

---

## 🎓 Learning Journey (5-Day Course)

### Day 1: Foundation
- Built basic agent loop with CrewAI
- Learned agent, task, and crew concepts
- Set up GitHub repository

### Day 2: Intelligence
- Added 4-type memory system (RAG-based)
- Integrated 9 specialized tools
- Implemented multimodal capabilities

### Day 3: Production
- Wrapped agent in FastAPI
- Deployed to Railway with CI/CD
- Exposed REST API endpoints

### Day 4: Collaboration
- Implemented A2A communication protocol
- Added AgentFacts for capability discovery
- Integrated with central agent registry

### Day 5: Optimization
- Enhanced agent coordination
- Optimized response speed vs. accuracy
- Prepared for agent evaluation

---

## 🌟 Key Highlights

### Technical Skills Demonstrated

✅ **AI/ML Engineering**
- LLM orchestration with CrewAI
- RAG (Retrieval-Augmented Generation)
- Vector databases (ChromaDB)
- Prompt engineering

✅ **Full-Stack Development**
- Python backend (FastAPI)
- JavaScript frontend (Next.js, React)
- REST API design
- Async programming

✅ **Cloud & DevOps**
- Railway deployment
- GitHub Actions CI/CD
- Environment management
- API security

✅ **System Design**
- Microservices architecture
- Agent communication protocols
- Distributed systems
- API versioning

---

## 🔮 Future Enhancements

- [ ] Voice input/output in frontend
- [ ] Streaming responses (SSE)
- [ ] Agent performance analytics dashboard
- [ ] Multi-agent task decomposition
- [ ] Enhanced A2A protocol (pub/sub)
- [ ] Agent marketplace integration

---

## 📚 Documentation

- **Frontend:** See [`interface/README.md`](./interface/README.md)
- **Day 4 Backend:** See [`day-4/README.md`](./day-4/README.md)
- **A2A Setup:** See [`day-4/AGENTFACTS_SETUP.md`](./day-4/AGENTFACTS_SETUP.md)
- **API Docs:** [https://brave-magic-production-65d3.up.railway.app/docs](https://brave-magic-production-65d3.up.railway.app/docs)

---

## 🤝 Connect

**Andy Yang**
- 📧 Email: [your.email@example.com](mailto:your.email@example.com)
- 🔗 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- 🐙 GitHub: [@andyang06](https://github.com/andyang06)
- 🌐 Portfolio: [your-portfolio.com](https://your-portfolio.com)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- **MIT IAP NANDA Course** - Project foundation and guidance
- **CrewAI** - AI agent framework
- **OpenAI** - GPT-4o-mini, DALL-E 3, Whisper, Vision APIs
- **Railway** - Cloud hosting platform

---

<div align="center">

**Built with 🧠 by Andy Yang | MIT Student | CS & Finance**

⭐ Star this repo if you found it helpful!

</div>
