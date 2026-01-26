"""
Robot Expert Agent with A2A Communication
==========================================

AI agent specialized in robotics, automation systems, and robotic engineering.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os
import re
import httpx
import logging
from typing import Optional, Dict, Any

from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from crewai_tools import FileReadTool, SerperDevTool, WebsiteSearchTool, YoutubeVideoSearchTool
from pydantic import Field
from typing import Type

load_dotenv()

# ==============================================================================
# Logging Setup
# ==============================================================================

os.makedirs("logs", exist_ok=True)

# A2A Communication Logger
a2a_logger = logging.getLogger("a2a")
a2a_logger.setLevel(logging.INFO)

a2a_file_handler = logging.FileHandler("logs/a2a_messages.log")
a2a_file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
a2a_file_handler.setFormatter(formatter)

a2a_logger.addHandler(a2a_file_handler)

# Detailed Flow Logger (tracks everything)
flow_logger = logging.getLogger("flow")
flow_logger.setLevel(logging.INFO)

flow_file_handler = logging.FileHandler("logs/detailed_flow.log")
flow_file_handler.setLevel(logging.INFO)

detailed_formatter = logging.Formatter('%(asctime)s | [%(name)s] | %(levelname)s | %(message)s')
flow_file_handler.setFormatter(detailed_formatter)

flow_logger.addHandler(flow_file_handler)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(detailed_formatter)
flow_logger.addHandler(console_handler)

# ==============================================================================
# FastAPI Application Setup
# ==============================================================================

app = FastAPI(
    title="Robot Expert Agent API",
    description="AI agent specialized in robotics, automation, and robotic engineering with A2A communication",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# Request/Response Models
# ==============================================================================

class QueryRequest(BaseModel):
    question: str
    user_id: str = "anonymous"

class QueryResponse(BaseModel):
    answer: str
    timestamp: str
    processing_time: float

class A2AMessage(BaseModel):
    content: Dict[str, Any]
    role: str = "user"
    conversation_id: str
    agent_id: Optional[str] = None  # Which agent sent this message

class A2AResponse(BaseModel):
    content: Dict[str, Any]
    role: str = "assistant"
    conversation_id: str
    timestamp: str
    agent_id: str

class HealthResponse(BaseModel):
    status: str
    memory_enabled: bool
    tools_count: int
    a2a_enabled: bool

# ==============================================================================
# Agent Registry
# ==============================================================================

# Central registry URL
REGISTRY_URL = "https://nest.projectnanda.org/api/agents"

# Store known agents - fetched from central registry
KNOWN_AGENTS: Dict[str, str] = {
    # Format: "username": "http://agent-url/a2a"
    # Auto-populated from registry on startup
}

# ==============================================================================
# Agent Identity Configuration
# ==============================================================================

MY_AGENT_USERNAME = "agent_2"
MY_AGENT_NAME = "Robot Expert Agent"
MY_AGENT_DESCRIPTION = "Specialized AI agent for robotics, automation systems, robotic engineering, and intelligent machine design with expertise in industrial and service robots"
MY_AGENT_PROVIDER = "NANDA Student"
MY_AGENT_PROVIDER_URL = "https://nanda.mit.edu"

MY_AGENT_ID = MY_AGENT_USERNAME
MY_AGENT_VERSION = "1.0.0"
MY_AGENT_JURISDICTION = "USA"

PUBLIC_URL = os.getenv("PUBLIC_URL") or os.getenv("RAILWAY_PUBLIC_DOMAIN")
if PUBLIC_URL and not PUBLIC_URL.startswith("http"):
    PUBLIC_URL = f"https://{PUBLIC_URL}"

# ==============================================================================
# Tools Setup
# ==============================================================================

class CalculatorInput(BaseModel):
    expression: str = Field(..., description="Mathematical expression to evaluate")

class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Performs mathematical calculations"
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

calculator_tool = CalculatorTool()
file_tool = FileReadTool()
web_rag_tool = WebsiteSearchTool()
youtube_tool = YoutubeVideoSearchTool()

search_tool = None
if os.getenv('SERPER_API_KEY'):
    search_tool = SerperDevTool()

available_tools = [
    calculator_tool,
    file_tool,
    web_rag_tool,
    youtube_tool
]

if search_tool:
    available_tools.append(search_tool)

# ==============================================================================
# Agent Setup
# ==============================================================================

llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.6,
)

my_agent_twin = Agent(
    role="Robotics and Automation Systems Expert",
    
    goal="Provide expert knowledge on robotics, automation, robot design, and intelligent machine systems",
    
    backstory=f"""
    You are an advanced AI robotics expert specialized in all aspects of robotics and automation.
    Your agent ID is: {MY_AGENT_ID}
    
    EXPERTISE:
    - Industrial robotics and manufacturing automation
    - Service robots and assistive robotics
    - Robot kinematics and dynamics
    - Robotic control systems and algorithms
    - Autonomous navigation and path planning
    - Computer vision and perception for robotics
    - Human-robot interaction
    - Robot operating systems (ROS)
    - Actuators, sensors, and robot hardware
    - Robotic arm design and manipulation
    - Mobile robotics and drones
    - AI and machine learning for robotics
    
    CAPABILITIES:
    - Explain robotic concepts and technologies
    - Design recommendations for robot systems
    - Troubleshoot robotic systems
    - Analyze robot specifications and performance
    - Programming guidance for robot control
    - Sensor selection and integration advice
    - Safety protocols for robotic systems
    - Latest trends in robotics research
    
    MEMORY CAPABILITIES:
    1. Short-Term Memory: Recent robotics discussions
    2. Long-Term Memory: Technical specifications and design patterns
    3. Entity Memory: Robot types, manufacturers, technologies
    4. Contextual Memory: User projects and preferences
    
    TOOL CAPABILITIES:
    - FileReadTool: Read robot specifications and code files
    - WebsiteSearchTool: Search robotics resources and documentation
    - YoutubeVideoSearchTool: Find robotics tutorials and demos
    - SerperDevTool: Real-time robotics news and research
    - Calculator: Engineering calculations (torque, speed, payload, etc.)
    
    A2A COMMUNICATION:
    You can collaborate with other specialized agents! When you receive messages with
    @agent-id syntax, route them to the appropriate agent. For example, if someone asks
    about weather conditions for outdoor robot operation, you might collaborate with
    weather prediction agents.
    
    Use your tools to access latest robotics research. Use memory to track ongoing
    projects. Use A2A to collaborate with other domain experts when needed!
    """,
    
    tools=available_tools,
    llm=llm,
    verbose=False,
)

# ==============================================================================
# Registry Helper Functions
# ==============================================================================

async def fetch_agents_from_registry():
    """
    Fetch all registered agents from the central registry
    Updates the KNOWN_AGENTS dictionary with username -> A2A endpoint mappings
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(REGISTRY_URL)
            response.raise_for_status()
            data = response.json()
            
            # Handle both old and new API formats
            agents = data.get("agents", [])
            if not agents and isinstance(data, list):
                # New API might return list directly
                agents = data
            
            print(f"📥 Fetched {len(agents)} agents from registry")
            
            # Update KNOWN_AGENTS with username -> A2A endpoint mapping
            for agent in agents:
                # Support both old (username/url) and new (agent_id/endpoint) formats
                username = agent.get("agent_id") or agent.get("username")
                url = agent.get("endpoint") or agent.get("url", "")
                
                # Skip if no username or if it's this agent
                if not username or username == MY_AGENT_USERNAME:
                    continue
                
                # Ensure URL ends with /a2a
                if not url.endswith("/a2a"):
                    url = url.rstrip("/") + "/a2a"
                
                KNOWN_AGENTS[username] = url
                print(f"   ✅ Registered: @{username} -> {url}")
            
            return True
    except Exception as e:
        print(f"⚠️ Failed to fetch agents from registry: {str(e)}")
        return False

# ==============================================================================
# A2A Helper Functions
# ==============================================================================

async def send_message_to_agent(agent_id: str, message: str, conversation_id: str, from_agent_id: Optional[str] = None) -> str:
    if agent_id not in KNOWN_AGENTS:
        error_msg = f"❌ Agent '{agent_id}' not found. Known agents: {list(KNOWN_AGENTS.keys())}"
        flow_logger.error(f"SEND_FAILED | target={agent_id} | reason=not_found | conversation_id={conversation_id}")
        return error_msg
    
    agent_url = KNOWN_AGENTS[agent_id]
    
    flow_logger.info(f"📤 SENDING | to={agent_id} | url={agent_url} | conversation_id={conversation_id} | message_preview={message[:100]}...")
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:  # 2 minutes for CrewAI processing
            payload = {
                "content": {
                    "text": message,
                    "type": "text"
                },
                "role": "user",
                "conversation_id": conversation_id
            }
            if from_agent_id:
                payload["agent_id"] = from_agent_id
                flow_logger.info(f"   └─ Including agent_id={from_agent_id} in payload")
            
            response = await client.post(agent_url, json=payload)
            response.raise_for_status()
            data = response.json()
            response_text = data.get("content", {}).get("text", str(data))
            
            flow_logger.info(f"✅ RECEIVED | from={agent_id} | conversation_id={conversation_id} | response_length={len(response_text)} chars | preview={response_text[:100]}...")
            
            return response_text
    
    except httpx.TimeoutException:
        error_msg = f"❌ Timeout connecting to agent '{agent_id}'"
        flow_logger.error(f"TIMEOUT | target={agent_id} | conversation_id={conversation_id}")
        return error_msg
    except httpx.HTTPError as e:
        error_msg = f"❌ Error communicating with agent '{agent_id}': {str(e)}"
        flow_logger.error(f"HTTP_ERROR | target={agent_id} | error={str(e)} | conversation_id={conversation_id}")
        return error_msg
    except Exception as e:
        error_msg = f"❌ Unexpected error: {str(e)}"
        flow_logger.error(f"UNEXPECTED_ERROR | target={agent_id} | error={str(e)} | conversation_id={conversation_id}")
        return error_msg

def extract_agent_mentions(text: str) -> list[str]:
    pattern = r'@([\w-]+)'
    mentions = re.findall(pattern, text)
    return mentions

def parse_a2a_request(message: str) -> tuple[Optional[str], str]:
    mentions = extract_agent_mentions(message)
    
    if not mentions:
        return None, message
    
    target_agent = mentions[0]
    clean_message = re.sub(r'@' + target_agent + r'\s*', '', message, count=1)
    
    return target_agent, clean_message

def generate_agent_facts() -> Dict[str, Any]:
    import uuid
    from datetime import timedelta
    
    agent_uuid = os.getenv("AGENT_UUID", str(uuid.uuid4()))
    base_url = PUBLIC_URL or "http://localhost:8000"
    
    agent_facts = {
        "id": f"nanda:{agent_uuid}",
        "agent_name": f"urn:agent:nanda:{MY_AGENT_USERNAME}",
        "label": MY_AGENT_NAME,
        "description": MY_AGENT_DESCRIPTION,
        "version": MY_AGENT_VERSION,
        "documentationUrl": f"{base_url}/docs",
        "jurisdiction": MY_AGENT_JURISDICTION,
        "provider": {
            "name": MY_AGENT_PROVIDER,
            "url": MY_AGENT_PROVIDER_URL,
            "did": f"did:web:{MY_AGENT_PROVIDER_URL.replace('https://', '').replace('http://', '')}"
        },
        "endpoints": {
            "static": [f"{base_url}/a2a"],
            "adaptive_resolver": {
                "url": f"{base_url}/a2a",
                "policies": ["load"]
            }
        },
        "capabilities": {
            "modalities": ["text"],
            "streaming": False,
            "batch": False,
            "authentication": {
                "methods": ["none"],
                "requiredScopes": []
            }
        },
        "skills": [
            {
                "id": "robot_design_consultation",
                "description": "Provide expert guidance on robot design, component selection, and system architecture",
                "inputModes": ["text"],
                "outputModes": ["text"],
                "supportedLanguages": ["en"],
                "latencyBudgetMs": 5000
            },
            {
                "id": "robotics_programming",
                "description": "Assist with robot programming, control algorithms, and ROS implementation",
                "inputModes": ["text"],
                "outputModes": ["text"],
                "supportedLanguages": ["en"],
                "latencyBudgetMs": 6000
            },
            {
                "id": "automation_systems",
                "description": "Design and optimize industrial automation and manufacturing robotics systems",
                "inputModes": ["text"],
                "outputModes": ["text"],
                "supportedLanguages": ["en"],
                "latencyBudgetMs": 5000
            },
            {
                "id": "robot_troubleshooting",
                "description": "Diagnose and solve robotic system issues including mechanical, electrical, and software problems",
                "inputModes": ["text"],
                "outputModes": ["text"],
                "supportedLanguages": ["en"],
                "latencyBudgetMs": 4000
            },
            {
                "id": "kinematics_calculations",
                "description": "Perform robot kinematics, dynamics, and engineering calculations",
                "inputModes": ["text"],
                "outputModes": ["text"],
                "supportedLanguages": ["en"],
                "latencyBudgetMs": 2000
            }
        ],
        "evaluations": {
            "performanceScore": 4.8,
            "availability90d": "99.0%",
            "lastAudited": datetime.now().isoformat(),
            "auditTrail": None,
            "auditorID": "Self-Reported v1.0"
        },
        "telemetry": {
            "enabled": True,
            "retention": "7d",
            "sampling": 1.0,
            "metrics": {
                "latency_p95_ms": 2000,
                "throughput_rps": 10,
                "error_rate": 0.01,
                "availability": "99.0%"
            }
        },
        "certification": {
            "level": "development",
            "issuer": MY_AGENT_PROVIDER,
            "issuanceDate": datetime.now().isoformat(),
            "expirationDate": (datetime.now() + timedelta(days=365)).isoformat()
        }
    }
    
    return agent_facts

# ==============================================================================
# API Endpoints
# ==============================================================================

@app.get("/")
async def root():
    return {
        "message": "🤖 Robot Expert Agent API with A2A",
        "version": "1.0.0",
        "agent_id": MY_AGENT_ID,
        "agent_name": MY_AGENT_NAME,
        "agent_username": MY_AGENT_USERNAME,
        "specialization": "Robotics & Automation Systems",
        "memory_enabled": True,
        "tools_enabled": len(available_tools),
        "a2a_enabled": True,
        "known_agents": list(KNOWN_AGENTS.keys()),
        "endpoints": {
            "health": "GET /health",
            "query": "POST /query",
            "a2a": "POST /a2a",
            "agentfacts": "GET /agentfacts",
            "agents": "GET /agents",
            "docs": "GET /docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        memory_enabled=True,
        tools_count=len(available_tools),
        a2a_enabled=True
    )

@app.get("/agents")
async def list_agents():
    return {
        "my_agent_id": MY_AGENT_ID,
        "my_agent_name": MY_AGENT_NAME,
        "my_agent_username": MY_AGENT_USERNAME,
        "known_agents": KNOWN_AGENTS,
        "usage": "Send messages using @agent-id syntax in the /a2a endpoint"
    }

@app.get("/agentfacts")
async def get_agent_facts():
    return generate_agent_facts()

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    start_time = datetime.now()
    
    try:
        task = Task(
            description=f"""
            As a robotics expert, answer this question: {request.question}
            
            Use your robotics knowledge and tools to provide detailed technical information.
            Include relevant details like specifications, design considerations, or implementation guidance.
            Use your memory to recall previous robotics discussions and user projects.
            """,
            expected_output="Expert robotics guidance with technical details and practical recommendations",
            agent=my_agent_twin,
        )
        
        crew = Crew(
            agents=[my_agent_twin],
            tasks=[task],
            memory=True,
            verbose=False,
        )
        
        result = crew.kickoff()
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        return QueryResponse(
            answer=str(result.raw),
            timestamp=end_time.isoformat(),
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.post("/a2a", response_model=A2AResponse)
async def a2a_endpoint(message: A2AMessage):
    try:
        text_content = message.content.get("text", "")
        conversation_id = message.conversation_id
        from_agent = message.agent_id
        
        flow_logger.info(f"{'='*80}")
        flow_logger.info(f"📨 INCOMING MESSAGE | conversation_id={conversation_id}")
        flow_logger.info(f"   └─ from_agent: {from_agent or 'external'}")
        flow_logger.info(f"   └─ message: {text_content[:200]}...")
        
        a2a_logger.info(f"INCOMING | conversation_id={conversation_id} | from={from_agent} | message={text_content}")
        
        target_agent, clean_message = parse_a2a_request(text_content)
        
        if target_agent:
            flow_logger.info(f"🎯 ROUTING DETECTED | target=@{target_agent} | clean_message={clean_message[:100]}...")
        
        if not target_agent:
            # No @agent-id - this message is FOR THIS AGENT to process
            if not from_agent:
                # No agent_id either - reject (must come from another agent)
                error_msg = (
                    "❌ ERROR: /a2a endpoint requires @agent-id for routing OR agent_id for processing.\n\n"
                    f"Your message: '{text_content}'\n\n"
                    "This endpoint is ONLY for agent-to-agent communication.\n"
                    "You must include @agent-id to route to another agent.\n\n"
                    "For direct robotics queries to THIS agent, use POST /query instead."
                )
                a2a_logger.error(f"NO_TARGET_NO_AGENT | conversation_id={conversation_id} | message={text_content}")
                raise HTTPException(status_code=400, detail=error_msg)
            
            # Process locally and send response back to sender
            print(f"💬 Processing message from @{from_agent}")
            flow_logger.info(f"🤖 LOCAL PROCESSING | from=@{from_agent} | conversation_id={conversation_id}")
            flow_logger.info(f"   └─ Task: Answer robotics question")
            a2a_logger.info(f"LOCAL_PROCESSING | conversation_id={conversation_id} | from={from_agent} | message={text_content}")
            
            task = Task(
                description=f"""
                As a robotics expert, answer this question: {text_content}
                
                Use your robotics knowledge and tools to provide detailed technical information.
                Include relevant details like specifications, design considerations, or implementation guidance.
                Use your memory to recall previous robotics discussions and user projects.
                """,
                expected_output="Expert robotics guidance with technical details and practical recommendations",
                agent=my_agent_twin,
            )
            
            crew = Crew(
                agents=[my_agent_twin],
                tasks=[task],
                memory=True,
                verbose=True,  # Enable verbose to see tool usage
            )
            
            flow_logger.info(f"   └─ Starting CrewAI execution...")
            result = crew.kickoff()
            my_response = str(result.raw)
            
            # Response is sent back via HTTP return (not separate A2A message)
            print(f"✅ Processed request from @{from_agent}")
            flow_logger.info(f"✅ PROCESSING COMPLETE | response_length={len(my_response)} chars")
            flow_logger.info(f"   └─ Response preview: {my_response[:200]}...")
            a2a_logger.info(f"LOCAL_SUCCESS | conversation_id={conversation_id} | from={from_agent} | response_length={len(my_response)}")
            
            end_time = datetime.now()
            
            return A2AResponse(
                content={
                    "text": my_response,
                    "type": "text"
                },
                role="assistant",
                conversation_id=conversation_id,
                timestamp=end_time.isoformat(),
                agent_id=MY_AGENT_ID
            )
        
        # Has @agent-id - route to another agent
        print(f"🔀 Routing message to agent: {target_agent}")
        a2a_logger.info(f"ROUTING | conversation_id={conversation_id} | target={target_agent} | message={clean_message}")
        
        agent_response = await send_message_to_agent(target_agent, clean_message, conversation_id, from_agent_id=MY_AGENT_ID)
        
        response_text = f"[Forwarded to @{target_agent}]\n\n{agent_response}"
        
        a2a_logger.info(f"SUCCESS | conversation_id={conversation_id} | target={target_agent} | response_length={len(agent_response)}")
        
        end_time = datetime.now()
        
        return A2AResponse(
            content={
                "text": response_text,
                "type": "text"
            },
            role="assistant",
            conversation_id=conversation_id,
            timestamp=end_time.isoformat(),
            agent_id=MY_AGENT_ID
        )
        
    except HTTPException:
        raise
    except Exception as e:
        a2a_logger.error(f"ERROR | conversation_id={message.conversation_id} | error={str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing A2A message: {str(e)}"
        )

@app.post("/agents/register")
async def register_agent(agent_id: str, agent_url: str):
    KNOWN_AGENTS[agent_id] = agent_url
    return {
        "message": f"✅ Agent '{agent_id}' registered successfully",
        "agent_id": agent_id,
        "agent_url": agent_url,
        "total_known_agents": len(KNOWN_AGENTS)
    }

# ==============================================================================
# Startup Event
# ==============================================================================

@app.on_event("startup")
async def startup_event():
    print("\n" + "="*70)
    print("🤖 Robot Expert Agent Starting...")
    print("="*70)
    print(f"\n✅ Agent ID: {MY_AGENT_ID}")
    print(f"✅ Agent Name: {MY_AGENT_NAME}")
    print(f"✅ Specialization: Robotics & Automation Systems")
    print(f"✅ Model: {llm.model}")
    print("✅ Memory: Enabled (4 types)")
    print(f"✅ Tools: {len(available_tools)} tools loaded")
    print("✅ A2A: Enabled (NANDA-style)")
    
    # Fetch agents from central registry
    print(f"\n🔍 Fetching agents from registry: {REGISTRY_URL}")
    await fetch_agents_from_registry()
    print(f"✅ Known Agents: {len(KNOWN_AGENTS)}")
    
    print("\n📚 Documentation: http://localhost:8000/docs")
    print("🤖 A2A Endpoint: http://localhost:8000/a2a")
    print("📋 AgentFacts: http://localhost:8000/agentfacts")
    if PUBLIC_URL:
        print(f"🌐 Public URL: {PUBLIC_URL}")
    print("="*70 + "\n")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

