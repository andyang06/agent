"""
Day 3: Deploy Your Agent with Memory to Railway
================================================

This wraps your Day 2 agent (with memory and tools) in a FastAPI REST API
so anyone can interact with it via HTTP from anywhere in the world!

What's FastAPI?
- A Python web framework that creates REST APIs
- Turns your local Python code into a web service
- Allows HTTP requests (like from curl, browsers, or other apps)

Architecture:
- Service 1: ChromaDB (persistent memory storage)
- Service 2: This FastAPI app (your agent)
- They communicate via Railway's private network
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os

from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, WebsiteSearchTool, YoutubeVideoSearchTool
from pydantic import Field
from typing import Type
from openai import OpenAI

# Load environment variables
load_dotenv()

# ==============================================================================
# FastAPI Application Setup
# ==============================================================================

app = FastAPI(
    title="Personal Agent Twin API",
    description="Your Day 2 agent with memory and tools, now accessible via REST API!",
    version="1.0.0"
)

# Enable CORS (allows browser requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# Request/Response Models (API Input/Output)
# ==============================================================================

class QueryRequest(BaseModel):
    """What the API expects when you send a question"""
    question: str
    user_id: str = "anonymous"

class QueryResponse(BaseModel):
    """What the API returns after processing"""
    answer: str
    timestamp: str
    processing_time: float

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    memory_enabled: bool
    tools_count: int

# ==============================================================================
# Tools Setup (from Day 2)
# ==============================================================================

# Tool 1: Calculator (custom tool from Day 2)
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

# Tool 2: File Reading
file_tool = FileReadTool()

# Tool 3: Website Search (RAG)
web_rag_tool = WebsiteSearchTool()

# Tool 4: YouTube Search (RAG)
youtube_tool = YoutubeVideoSearchTool()

# Tool 5: Web Search (optional - requires SERPER_API_KEY)
search_tool = None
if os.getenv('SERPER_API_KEY'):
    search_tool = SerperDevTool()

# ==============================================================================
# Multimodal Tools: Vision, Audio, Documents
# ==============================================================================

# Image Generation
class ImageGenerationInput(BaseModel):
    prompt: str = Field(..., description="Description of image to generate")

class ImageGenerationTool(BaseTool):
    name: str = "image_generator"
    description: str = "Generates images using DALL-E 3"
    args_schema: Type[BaseModel] = ImageGenerationInput
    
    def _run(self, prompt: str) -> str:
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard", n=1)
            return f"✅ Image URL: {response.data[0].url}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Image Analysis (Vision)
class ImageAnalysisInput(BaseModel):
    image_url: str = Field(..., description="URL of image to analyze")
    question: str = Field(default="What's in this image?", description="Question about the image")

class ImageAnalysisTool(BaseTool):
    name: str = "analyze_image"
    description: str = "Analyzes images using GPT-4 Vision. Can describe images, identify objects, read text (OCR)."
    args_schema: Type[BaseModel] = ImageAnalysisInput
    
    def _run(self, image_url: str, question: str = "What's in this image?") -> str:
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": [{"type": "text", "text": question}, {"type": "image_url", "image_url": {"url": image_url}}]}],
                max_tokens=500
            )
            return f"🔍 {response.choices[0].message.content}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Speech-to-Text
class SpeechToTextInput(BaseModel):
    audio_file_path: str = Field(..., description="Path to audio file")

class SpeechToTextTool(BaseTool):
    name: str = "transcribe_audio"
    description: str = "Converts speech to text using Whisper"
    args_schema: Type[BaseModel] = SpeechToTextInput
    
    def _run(self, audio_file_path: str) -> str:
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            with open(audio_file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            return f"🎤 {transcript.text}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Text-to-Speech
class TextToSpeechInput(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    voice: str = Field(default="nova", description="Voice: alloy, echo, fable, onyx, nova, shimmer")

class TextToSpeechTool(BaseTool):
    name: str = "text_to_speech"
    description: str = "Converts text to speech audio"
    args_schema: Type[BaseModel] = TextToSpeechInput
    
    def _run(self, text: str, voice: str = "nova") -> str:
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
            filename = "speech_output.mp3"
            response.stream_to_file(filename)
            return f"🔊 Audio saved to {filename}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

# PDF Analysis
class PDFAnalysisInput(BaseModel):
    pdf_path: str = Field(..., description="Path to PDF file")

class PDFAnalysisTool(BaseTool):
    name: str = "analyze_pdf"
    description: str = "Extracts text from PDF documents"
    args_schema: Type[BaseModel] = PDFAnalysisInput
    
    def _run(self, pdf_path: str) -> str:
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n\n"
                return f"📄 Pages: {len(pdf.pages)}\n\n{text[:3000]}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

# Instantiate tools
image_gen_tool = ImageGenerationTool()
vision_tool = ImageAnalysisTool()
speech_to_text_tool = SpeechToTextTool()
text_to_speech_tool = TextToSpeechTool()
pdf_tool = PDFAnalysisTool()

# Collect all tools
available_tools = [
    calculator_tool,
    file_tool,
    web_rag_tool,
    youtube_tool,
    image_gen_tool,
    vision_tool,
    speech_to_text_tool,
    text_to_speech_tool,
    pdf_tool
]

if search_tool:
    available_tools.append(search_tool)

# ==============================================================================
# Agent Setup (from Day 2, with memory!)
# ==============================================================================

# Initialize LLM
llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.7,
)

# Create agent with memory and tools
my_agent_twin = Agent(
    role="Personal Digital Twin with Memory and Tools",

    goal="Answer questions about me, remember conversations, and use tools when needed",

    backstory="""
    You are the digital twin of a student learning AI and CrewAI.
    
    Here's what you know about me:
    - I'm a student learning about AI agents and automation
    - I grew up in Irmo, South Carolina
    - second year student at MIT studying CS and Finance
    - I love playing soccer, watching movies, going on walks, cooking meals, rowing
    - I also like pickup basketball and every nature similar.
    - I'm in the fraternity delta tau delta.
    - I'm interested in technology, coding, and building cool projects
    - I love experimenting with new tools like CrewAI
    - My favorite programming language is Python
    - I enjoy problem-solving and creative thinking
    - I'm taking a class where we're building AI agents
    
    MEMORY CAPABILITIES:
    You have four types of memory:
    1. Short-Term Memory (RAG): Recent conversation context
    2. Long-Term Memory: Important facts across sessions
    3. Entity Memory (RAG): People, places, concepts
    4. Contextual Memory: Combines all memory types
    
    TOOL CAPABILITIES:
    📁 File & Web: FileReadTool, WebsiteSearchTool, YoutubeVideoSearchTool, SerperDevTool
    🧮 Utility: Calculator
    🎨 Vision: Image Generation (DALL-E 3), Image Analysis (GPT-4 Vision, OCR)
    🎤 Audio: Speech-to-Text (Whisper), Text-to-Speech (6 voices)
    📄 Documents: PDF Analysis
    
    You are a MULTIMODAL AI - you can understand and work with text, images, audio, and documents.
    Use tools for external info. Use memory for personalized, context-aware responses.
    """,

    tools=available_tools,
    llm=llm,
    verbose=False,  # Set to True for debugging
)

# ==============================================================================
# API Endpoints
# ==============================================================================

@app.get("/")
async def root():
    """Root endpoint - shows API information"""
    return {
        "message": "🤖 Personal Agent Twin API - Day 3",
        "version": "1.0.0",
        "memory_enabled": True,
        "tools_enabled": len(available_tools),
        "endpoints": {
            "health": "GET /health",
            "query": "POST /query",
            "docs": "GET /docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns the current status of the API and agent.
    """
    return HealthResponse(
        status="healthy",
        memory_enabled=True,
        tools_count=len(available_tools)
    )

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Query the agent with memory and tools
    
    This is the main endpoint! Send a question and get an answer.
    The agent will:
    - Remember previous conversations (if memory is working)
    - Use tools when needed (calculator, web search, etc.)
    - Provide personalized responses
    
    Example:
        curl -X POST https://your-app.up.railway.app/query \\
          -H "Content-Type: application/json" \\
          -d '{"question": "What is 123 * 456?"}'
    """
    start_time = datetime.now()

    try:
        # Create task for this query
        task = Task(
            description=f"""
            Answer the following question: {request.question}
            
            Use your memory to recall relevant context.
            Use your tools when you need external information or calculations.
            Provide accurate, helpful responses.
            """,
            expected_output="A clear, context-aware answer using memory and tools as needed",
            agent=my_agent_twin,
        )

        # Create crew with memory enabled
        crew = Crew(
            agents=[my_agent_twin],
            tasks=[task],
            memory=True,  # This enables all 4 memory types!
            verbose=False,
        )

        # Execute the crew
        result = crew.kickoff()

        # Calculate processing time
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

# ==============================================================================
# Startup Event
# ==============================================================================

@app.on_event("startup")
async def startup_event():
    """Run when the API starts"""
    print("\n" + "="*70)
    print("🚀 Personal Agent Twin API Starting...")
    print("="*70)
    print(f"\n✅ Model: {llm.model}")
    print(f"✅ Memory: Enabled (4 types)")
    print(f"✅ Tools: {len(available_tools)} tools loaded")
    print("✅ Agent: Initialized")
    print("\n📚 Documentation: http://localhost:8000/docs")
    print("="*70 + "\n")

# ==============================================================================
# Run Instructions
# ==============================================================================
"""
LOCAL TESTING:
    uvicorn main:app --reload
    
    Then test:
    curl -X POST http://localhost:8000/query \\
      -H "Content-Type: application/json" \\
      -d '{"question": "What is 50 * 50?"}'

RAILWAY DEPLOYMENT:
    Railway automatically detects and runs this with:
    uvicorn main:app --host 0.0.0.0 --port $PORT
"""

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
