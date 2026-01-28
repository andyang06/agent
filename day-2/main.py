"""
Personal Agent Twin with Memory and Tools - Day 2
==================================================

This extends Day 1 by adding:
- Memory (Short-Term, Long-Term, Entity, Contextual)
- Tools from CrewAI collection
- Custom tool creation

Students: Follow the steps to add memory and tools to your agent!
"""

from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool, WebsiteSearchTool, YoutubeVideoSearchTool
from pydantic import BaseModel, Field
from typing import Type
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# ==============================================================================
# STEP 1: Configure your LLM (same as Day 1)
# ==============================================================================

llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.7,
)

# ==============================================================================
# STEP 2: Define Tools
# ==============================================================================

# Tool 1: Directory Reading
# Allows agent to browse directories
docs_tool = DirectoryReadTool(directory='./blog-posts')

# Tool 2: File Reading
# Allows agent to read specific files
file_tool = FileReadTool()

# Tool 3: Website Search (RAG-based)
# Searches and extracts content from websites
web_rag_tool = WebsiteSearchTool()

# Tool 4: YouTube Video Search (RAG-based)
# Searches within video transcripts
youtube_tool = YoutubeVideoSearchTool()

# Tool 5: Web Search (requires SERPER_API_KEY in .env)
# Get free key at: https://serper.dev
search_tool = None
if os.getenv('SERPER_API_KEY'):
    search_tool = SerperDevTool()

# ==============================================================================
# STEP 3: Create Custom Tool
# ==============================================================================

class CalculatorInput(BaseModel):
    """Input schema for Calculator tool."""
    expression: str = Field(..., description="Mathematical expression to evaluate")

class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Performs mathematical calculations. Use for any math operations."
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        """Execute the calculation."""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"

calculator_tool = CalculatorTool()

# ==============================================================================
# CUSTOM TOOL: Image Generation
# ==============================================================================

class ImageGenerationInput(BaseModel):
    """Input schema for Image Generation tool."""
    prompt: str = Field(..., description="Detailed description of the image to generate")

class ImageGenerationTool(BaseTool):
    name: str = "image_generator"
    description: str = "Generates an image based on a text description using DALL-E 3. Use this when asked to create, generate, or draw an image."
    args_schema: Type[BaseModel] = ImageGenerationInput

    def _run(self, prompt: str) -> str:
        """Generate an image using DALL-E."""
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            revised_prompt = response.data[0].revised_prompt

            return f"✅ Image generated successfully!\n\nImage URL: {image_url}\n\nRevised prompt used: {revised_prompt}\n\nYou can view the image by opening the URL in your browser."
        except Exception as e:
            return f"❌ Error generating image: {str(e)}\n\nMake sure your OPENAI_API_KEY is set and has available credits."

image_tool = ImageGenerationTool()

# ==============================================================================
# MULTIMODAL TOOLS: Vision, Audio, Documents
# ==============================================================================

# VISION: Image Analysis Tool (GPT-4 Vision)
class ImageAnalysisInput(BaseModel):
    """Input schema for Image Analysis tool."""
    image_url: str = Field(..., description="URL of the image to analyze")
    question: str = Field(default="What's in this image?", description="Specific question about the image")

class ImageAnalysisTool(BaseTool):
    name: str = "analyze_image"
    description: str = "Analyzes images using GPT-4 Vision. Can describe images, identify objects, read text in images (OCR), and answer questions about visual content. Provide an image URL."
    args_schema: Type[BaseModel] = ImageAnalysisInput

    def _run(self, image_url: str, question: str = "What's in this image? Describe it in detail.") -> str:
        """Analyze an image using GPT-4 Vision."""
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            response = client.chat.completions.create(
                model="gpt-4o",  # GPT-4 with vision capabilities
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": question
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            analysis = response.choices[0].message.content
            return f"🔍 Image Analysis:\n\n{analysis}"
        except Exception as e:
            return f"❌ Error analyzing image: {str(e)}"

vision_tool = ImageAnalysisTool()

# AUDIO: Speech-to-Text Tool (Whisper)
class SpeechToTextInput(BaseModel):
    """Input schema for Speech-to-Text tool."""
    audio_file_path: str = Field(..., description="Path to audio file (mp3, wav, m4a, etc.)")

class SpeechToTextTool(BaseTool):
    name: str = "transcribe_audio"
    description: str = "Converts speech/audio to text using Whisper. Supports mp3, wav, m4a, and other audio formats."
    args_schema: Type[BaseModel] = SpeechToTextInput

    def _run(self, audio_file_path: str) -> str:
        """Transcribe audio to text using Whisper."""
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            with open(audio_file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            return f"🎤 Transcription:\n\n{transcript.text}"
        except Exception as e:
            return f"❌ Error transcribing audio: {str(e)}\n\nMake sure the audio file exists at: {audio_file_path}"

speech_to_text_tool = SpeechToTextTool()

# AUDIO: Text-to-Speech Tool (OpenAI TTS)
class TextToSpeechInput(BaseModel):
    """Input schema for Text-to-Speech tool."""
    text: str = Field(..., description="Text to convert to speech")
    voice: str = Field(default="nova", description="Voice to use: alloy, echo, fable, onyx, nova, shimmer")
    output_file: str = Field(default="speech_output.mp3", description="Output filename for the audio")

class TextToSpeechTool(BaseTool):
    name: str = "text_to_speech"
    description: str = "Converts text to natural-sounding speech audio. Choose from voices: alloy, echo, fable, onyx, nova (default), shimmer."
    args_schema: Type[BaseModel] = TextToSpeechInput

    def _run(self, text: str, voice: str = "nova", output_file: str = "speech_output.mp3") -> str:
        """Convert text to speech using OpenAI TTS."""
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            response.stream_to_file(output_file)
            return f"🔊 Audio generated successfully!\n\nSaved to: {output_file}\nVoice: {voice}\nText: {text[:100]}..."
        except Exception as e:
            return f"❌ Error generating speech: {str(e)}"

text_to_speech_tool = TextToSpeechTool()

# DOCUMENTS: PDF Analysis Tool
class PDFAnalysisInput(BaseModel):
    """Input schema for PDF Analysis tool."""
    pdf_path: str = Field(..., description="Path to PDF file to analyze")

class PDFAnalysisTool(BaseTool):
    name: str = "analyze_pdf"
    description: str = "Reads and extracts text from PDF documents. Can analyze PDFs, extract content, and answer questions about PDF files."
    args_schema: Type[BaseModel] = PDFAnalysisInput

    def _run(self, pdf_path: str) -> str:
        """Analyze a PDF document."""
        try:
            import pdfplumber
            
            text_content = ""
            page_count = 0
            
            with pdfplumber.open(pdf_path) as pdf:
                page_count = len(pdf.pages)
                for page in pdf.pages:
                    text_content += page.extract_text() + "\n\n"
            
            # Limit output size
            if len(text_content) > 3000:
                text_content = text_content[:3000] + "\n\n[Content truncated - PDF is longer]"
            
            return f"📄 PDF Analysis:\n\nPages: {page_count}\n\nContent:\n{text_content}"
        except FileNotFoundError:
            return f"❌ Error: PDF file not found at {pdf_path}"
        except Exception as e:
            return f"❌ Error analyzing PDF: {str(e)}"

pdf_tool = PDFAnalysisTool()

# ==============================================================================
# STEP 4: Create Agent with Memory and Tools
# ==============================================================================

# Collect available tools
available_tools = [
    docs_tool,
    file_tool,
    web_rag_tool,
    youtube_tool,
    calculator_tool,
    image_tool,          # Image generation with DALL-E 3
    vision_tool,         # Image analysis with GPT-4 Vision
    speech_to_text_tool, # Audio transcription with Whisper
    text_to_speech_tool, # Text-to-speech with OpenAI TTS
    pdf_tool            # PDF document analysis
]

if search_tool:
    available_tools.append(search_tool)

my_agent_twin = Agent(
    role="Personal Digital Twin with Memory and Tools",

    goal="Answer questions about me, remember our conversations, and use tools when needed",

    # Edit this backstory to make it your own!
    backstory="""
    You are the digital twin of a student learning AI and CrewAI.
    
    Here's what you know about me:
    - I'm a student learning about AI agents and automation
    - I grew up in Irmo, South Carolina
    - second year student at MIT studying CS and Finance
    - I love playing soccer, watching movies, going on walks, cooking meals, rowing
    - I also like pickup basketball and every nature similar.
    - I'm interested in technology, coding, and building cool projects
    - I love experimenting with new tools like CrewAI
    - My favorite programming language is Python
    - I enjoy problem-solving and creative thinking
    - I'm taking a class where we're building AI agents
    
    When someone asks about me, you provide friendly, accurate information
    based on what I've told you about myself. You're helpful, enthusiastic,
    and represent me well in conversations.
    
    MEMORY CAPABILITIES:
    You have four types of memory:
    
    1. Short-Term Memory (RAG-based): Stores recent conversation context
       - Remembers what we discussed in this session
       - Uses vector embeddings for retrieval
    
    2. Long-Term Memory: Persists important information across sessions
       - Remembers facts that should survive restarts
       - Stores learnings and preferences
    
    3. Entity Memory (RAG-based): Tracks people, places, concepts
       - Remembers entities mentioned in conversations
       - Stores relationships and attributes
    
    4. Contextual Memory: Combines all memory types
       - Fuses short-term, long-term, and entity memory
       - Provides coherent, context-aware responses
    
    TOOL CAPABILITIES:
    
    📁 File & Web Tools:
    - DirectoryReadTool: Browse and list files in directories
    - FileReadTool: Read specific files
    - WebsiteSearchTool: Search and extract content from websites (RAG)
    - YoutubeVideoSearchTool: Search within video transcripts (RAG)
    - SerperDevTool: Web search (if API key configured)
    
    🧮 Utility Tools:
    - Calculator: Perform mathematical calculations
    
    🎨 MULTIMODAL CAPABILITIES (Vision & Image):
    - ImageGenerator: Generate images from text descriptions using DALL-E 3
    - ImageAnalyzer: Analyze images, identify objects, read text (OCR), describe visual content using GPT-4 Vision
    
    🎤 MULTIMODAL CAPABILITIES (Audio):
    - SpeechToText: Transcribe audio/speech to text using Whisper (supports mp3, wav, m4a)
    - TextToSpeech: Convert text to natural-sounding speech audio (6 voice options)
    
    📄 MULTIMODAL CAPABILITIES (Documents):
    - PDFAnalyzer: Extract and analyze text from PDF documents
    
    You are a MULTIMODAL AI agent - you can understand and work with text, images, 
    audio, and documents. Use these tools to provide rich, comprehensive responses.
    Use memory to provide personalized, context-aware answers.
    """,

    tools=available_tools,  # Add tools to agent
    llm=llm,
    verbose=True,
)

# ==============================================================================
# STEP 5: Create Task (same pattern as Day 1)
# ==============================================================================

answer_question_task = Task(
    description="""
    Answer the following question: {question}
    
    Use your memory to recall relevant context from our conversation.
    Use your tools when you need external information or calculations.
    Provide accurate, helpful responses based on your backstory and tools.
    """,

    expected_output="A clear, context-aware answer using memory and tools as needed",

    agent=my_agent_twin,
)

# ==============================================================================
# STEP 6: Create Crew with Memory Enabled
# ==============================================================================

my_crew = Crew(
    agents=[my_agent_twin],
    tasks=[answer_question_task],
    memory=True,  # This enables all 4 memory types!
    verbose=True,
)

# ==============================================================================
# STEP 7: Run Your Agent Twin with Memory!
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Personal Agent Twin - Day 2: Memory + Tools")
    print("="*70 + "\n")

    # Interactive mode
    print("Ask me questions! I'll remember our conversation and use tools when needed.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye! I'll remember this conversation.\n")
            break

        if not question:
            continue

        result = my_crew.kickoff(inputs={"question": question})
        print(f"\nAgent: {result.raw}\n")
