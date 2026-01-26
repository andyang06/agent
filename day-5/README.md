# Day 5: Coordination Protocol + Agent Battle

**Goal:** Implement advanced coordination protocols and compete in the Agent Battle using the Agent Smart Score evaluation system

## What You'll Learn

- Agent coordination protocols
- Multi-agent task decomposition and collaboration
- Agent optimization strategies
- Performance tuning and testing
- Agent Smart Score evaluation criteria
- Competitive agent design

## Today's Objectives

- [ ] Implement coordination protocols for multi-agent collaboration
- [ ] Optimize your agent for speed and accuracy
- [ ] Add advanced tools (web search, specialized APIs)
- [ ] Test across diverse topics
- [ ] Ensure consistent API format
- [ ] Submit to NANDA for battle
- [ ] Compete in the Agent Battle!

## The Agent Battle

### Battle Format

Your agent will compete in multiple rounds:

1. **Trivia Round**: General knowledge questions
   - History, science, geography
   - Pop culture, sports, entertainment
   - Technology and current events

2. **Research Round**: Questions requiring web search
   - Current news and events
   - Real-time data (weather, stocks, etc.)
   - Latest developments in various fields

3. **Analysis Round**: Complex reasoning tasks
   - Problem-solving
   - Multi-step reasoning
   - Strategic thinking

4. **Speed Round**: Quick-fire questions
   - Test response time
   - Accuracy under pressure
   - Simple but fast

5. **Coordination Round**: Multi-agent collaboration
   - Agent-to-agent communication
   - Task decomposition
   - Collaborative problem-solving

### Agent Smart Score Evaluation

Your agent will be evaluated using the **Agent Smart Score** system, which measures:

**Accuracy (40%)**
- Correctness of answers
- Factual accuracy
- Completeness of responses

**Speed (20%)**
- Response time
- API latency
- Efficiency

**Reasoning (20%)**
- Quality of explanations
- Logic and coherence
- Depth of analysis

**Robustness (20%)**
- Handling edge cases
- Error recovery
- Consistency across diverse topics

**Bonus: Coordination (+10%)**
- Effective use of A2A communication
- Multi-agent collaboration
- Task delegation strategies

**Final Score Calculation:**
```
Agent Smart Score = (Accuracy × 0.40) + (Speed × 0.20) + (Reasoning × 0.20) + (Robustness × 0.20) + (Coordination Bonus × 0.10)
```

Maximum possible score: **110 points**

---

## Coordination Protocols

### What is Agent Coordination?

Agent coordination involves multiple agents working together to solve complex tasks through:
- **Task Decomposition**: Breaking down complex tasks into subtasks
- **Role Assignment**: Assigning specialized agents to appropriate subtasks
- **Message Passing**: Using A2A protocol for inter-agent communication
- **Result Aggregation**: Combining outputs from multiple agents

### Coordination Strategies

#### 1. Sequential Coordination
```
Agent A → Processes Task → Agent B → Refines Output → Agent C → Final Result
```

Example:
```python
# Agent A: Research
research_result = await send_to_agent("@research-agent", "Find information about X")

# Agent B: Analysis
analysis = await send_to_agent("@analyst-agent", f"Analyze: {research_result}")

# Agent C: Summary
final = await send_to_agent("@writer-agent", f"Summarize: {analysis}")
```

#### 2. Parallel Coordination
```
             Task
             / | \
            /  |  \
        Agent A Agent B Agent C
            \  |  /
             \ | /
           Aggregate
```

Example:
```python
# Parallel execution
tasks = [
    send_to_agent("@data-analyst", "Analyze dataset"),
    send_to_agent("@market-expert", "Market trends"),
    send_to_agent("@writer", "Write summary")
]

results = await asyncio.gather(*tasks)
final_result = aggregate_results(results)
```

#### 3. Hierarchical Coordination
```
    Coordinator Agent
         / | \
        /  |  \
   Worker1 Worker2 Worker3
```

Example:
```python
# Coordinator decides which agents to use
if task_requires_research:
    result = await send_to_agent("@research-agent", task)
elif task_requires_calculation:
    result = await send_to_agent("@math-agent", task)
else:
    result = process_locally(task)
```

#### 4. Consensus Coordination
```
Question → Agent A ┐
Question → Agent B ├→ Vote/Merge → Final Answer
Question → Agent C ┘
```

Example:
```python
# Multiple agents answer, pick best or merge
answers = [
    await send_to_agent("@agent-1", question),
    await send_to_agent("@agent-2", question),
    await send_to_agent("@agent-3", question)
]

# Vote or use judge agent to pick best
final = select_best_answer(answers)
```

---

## Optimization Strategies

### 1. Model Selection

```python
# Fast and affordable
llm = LLM(model="openai/gpt-4o-mini", temperature=0.3)

# More capable (slower, costlier)
llm = LLM(model="openai/gpt-4o", temperature=0.3)

# Balance of speed and quality
llm = LLM(model="openai/gpt-4o-mini", temperature=0.5)
```

**Recommendation**: Use `gpt-4o-mini` with temperature 0.3-0.5 for best speed/accuracy balance.

### 2. Essential Tools

```python
from crewai_tools import (
    SerperDevTool,      # Web search
    WebsiteSearchTool,   # Website scraping
    FileReadTool,        # Read files
    # Add more as needed
)

# Configure tools
search_tool = SerperDevTool(
    api_key=os.getenv("SERPER_API_KEY")
)

# Add to agent
agent = Agent(
    role="Battle Agent",
    tools=[search_tool],
    # ...
)
```

**Essential Tools for Battle:**
- Web search (Serper, Brave, or Google)
- Calculator for math
- Current date/time tool
- Optional: Weather, stock data, news APIs

### 3. Memory Configuration

```python
crew = Crew(
    agents=[agent],
    tasks=[task],
    memory=True,  # Enable for context
    # But be mindful of speed!
)
```

**Trade-off**: Memory improves context but slows responses. Test both!

### 4. Response Optimization

```python
# Concise responses for speed
task = Task(
    description=f"""
    Answer this question concisely: {question}
    
    Provide:
    - Direct answer first
    - Brief explanation (1-2 sentences)
    - Sources if using tools
    
    Be accurate and fast!
    """,
    expected_output="Concise accurate answer",
    agent=agent,
)
```

### 5. Caching Strategy

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_query(question: str):
    """Cache responses for identical questions"""
    # Your agent query logic here
    pass
```

---

## Building Your Battle-Ready Agent with Coordination

### Complete Battle Agent with Coordination Capabilities

```python
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()

# Optimized LLM
llm = LLM(
    model="openai/gpt-4o-mini",
    temperature=0.4,  # Balance creativity and consistency
)

# Essential tools
search_tool = SerperDevTool()

# Battle agent with coordination capabilities
battle_agent = Agent(
    role="NANDA Battle Champion with Coordination",
    goal="Answer questions accurately and quickly, utilizing A2A coordination when beneficial",
    
    backstory="""
    You are an elite AI agent competing in the NANDA Agent Battle.
    
    Your strengths:
    - Broad knowledge across topics
    - Quick, accurate responses
    - Effective tool usage
    - Clear, concise communication
    - Strategic use of A2A coordination
    
    Your coordination strategy:
    - Assess if task requires specialist knowledge
    - Use @agent-id to delegate to specialized agents when needed
    - Combine multiple agent outputs for comprehensive answers
    - Always provide the best answer, whether solo or coordinated
    
    Topics you excel at:
    - General trivia and knowledge
    - Current events and news
    - Science and technology
    - History and culture
    - Problem-solving and analysis
    - Coordinating with other agents
    
    You always strive for accuracy over speed, but keep responses concise.
    """,
    
    tools=[search_tool],
    llm=llm,
    verbose=False,  # Faster in production
)

def answer_battle_question(question: str) -> str:
    """
    Answer a battle question, using coordination if beneficial
    
    Args:
        question: The battle question
        
    Returns:
        Concise, accurate answer
    """
    task = Task(
        description=f"""
        Answer this battle question: {question}
        
        Strategy:
        1. Assess if you can answer directly
        2. If a specialized agent would be better, use @agent-id to delegate
        3. If multiple perspectives needed, coordinate with multiple agents
        4. Always provide the most accurate answer possible
        
        Requirements:
        1. Provide accurate answer
        2. Keep it concise (2-3 sentences)
        3. Use tools if you need current data
        4. Use A2A coordination if needed for accuracy
        5. Cite sources if applicable
        """,
        expected_output="Concise accurate answer with brief explanation",
        agent=battle_agent,
    )
    
    crew = Crew(
        agents=[battle_agent],
        tasks=[task],
        verbose=False,
    )
    
    result = crew.kickoff()
    return str(result)
```

---

## Testing Your Agent

### Test Across Categories

```python
# Trivia
questions = [
    "What is the capital of Japan?",
    "Who wrote Romeo and Juliet?",
    "What year did World War II end?",
]

# Current events (requires web search)
questions = [
    "What's the current weather in Boston?",
    "What's the latest news about AI?",
    "What's the price of Bitcoin today?",
]

# Analysis
questions = [
    "Compare renewable vs fossil fuel energy",
    "Explain how quantum computing works",
    "What are the pros and cons of remote work?",
]

# Coordination (multi-agent)
questions = [
    "@data-analyst What are the trends in this dataset?",
    "Coordinate with @research-agent and @writer to create a report",
    "Ask @math-expert to solve this, then @explainer to clarify",
]

# Speed test
import time
start = time.time()
answer = answer_battle_question("What is 2+2?")
elapsed = time.time() - start
print(f"Response time: {elapsed:.2f}s")
```

### Performance Benchmarks

**Target Metrics for Agent Smart Score:**
- Simple questions: < 3 seconds
- Tool-required questions: < 8 seconds
- Complex analysis: < 15 seconds
- Coordinated queries: < 12 seconds
- Accuracy: > 90% correct

---

## Battle Day Strategy

### Before the Battle

1. **Test your endpoint**
   ```bash
   curl https://your-agent.railway.app/health
   curl -X POST https://your-agent.railway.app/query \
     -d '{"question": "test"}'
   ```

2. **Check API keys** - All tools working?

3. **Monitor performance** - Response times acceptable?

4. **Test coordination** - A2A communication working?

5. **Pre-warm** - Send a test query to wake up your server

### During the Battle

1. **Monitor your logs** - Watch for errors
2. **Track performance** - Note which questions work well
3. **Observe coordination** - Are multi-agent queries effective?
4. **Stay calm** - Agents will make mistakes!
5. **Learn** - See what other agents do well

### After Each Round

1. **Quick fixes** - Can you improve between rounds?
2. **Adjust temperature** - Too creative or too rigid?
3. **Tool tuning** - Using the right tools?
4. **Coordination strategy** - Are you delegating effectively?

---

## Advanced Coordination Enhancements

### Multi-Agent Strategy

```python
def get_best_strategy(question: str) -> str:
    """Decide whether to use coordination"""
    if "multiple perspectives" in question.lower():
        # Use consensus coordination
        return "consensus"
    elif "analyze" in question.lower() and "research" in question.lower():
        # Use sequential coordination
        return "sequential"
    elif requires_specialized_knowledge(question):
        # Use hierarchical coordination
        return "hierarchical"
    else:
        # Process locally
        return "local"
```

### Confidence-Based Coordination

```python
def answer_with_coordination_fallback(question: str):
    """Try local first, coordinate if low confidence"""
    local_answer, confidence = answer_locally(question)
    
    if confidence < 0.7:
        # Low confidence, seek specialist help
        specialist_answer = await send_to_agent("@specialist", question)
        return specialist_answer
    else:
        return local_answer
```

### Ensemble Coordination

```python
async def ensemble_answer(question: str):
    """Get answers from multiple agents, select best"""
    answers = await asyncio.gather(
        answer_locally(question),
        send_to_agent("@agent-1", question),
        send_to_agent("@agent-2", question),
    )
    
    # Use voting or judge agent to pick best
    return select_best_answer(answers)
```

---

## Submission Requirements

### API Format (MANDATORY)

Your agent MUST implement:

```python
# POST /query
{
  "question": "What is the capital of France?"
}

# Response
{
  "answer": "The capital of France is Paris.",
  "agent_id": "your-agent-name",
  "timestamp": "2026-01-20T10:00:00Z",
  "confidence": 0.95,  # optional
  "coordination_used": false  # optional: true if A2A was used
}
```

### Submission Checklist

- [ ] Deployed and accessible
- [ ] Health endpoint working
- [ ] Query endpoint returns correct format
- [ ] A2A endpoint functional (for coordination)
- [ ] Tested across multiple question types
- [ ] Tested coordination capabilities
- [ ] Response times acceptable
- [ ] Error handling in place
- [ ] API keys secured
- [ ] Submitted to NANDA platform

---

## Competition Categories

### Main Battle
- **Overall Champion**: Best Agent Smart Score across all rounds
- Winner gets bragging rights and recognition!

### Special Awards
- **Fastest Agent**: Best average response time
- **Most Accurate**: Highest accuracy percentage
- **Best Reasoner**: Highest reasoning score
- **Coordination Master**: Best use of A2A protocol
- **Most Robust**: Best handling of edge cases
- **Best Specialist**: Dominates a specific category
- **Most Improved**: Biggest improvement during course

---

## After the Battle

### What to Do Next

1. **Analyze your Agent Smart Score**
   - Which areas scored highest?
   - Where can you improve?
   - How effective was your coordination?

2. **Share your agent**
   - Post on GitHub
   - Share with classmates
   - Write about your approach

3. **Keep learning**
   - What worked well?
   - What would you do differently?
   - What new tools to explore?
   - How can coordination be improved?

4. **Build on it**
   - Add more specialized tools
   - Improve coordination strategies
   - Explore new use cases
   - Build agent networks

5. **Connect**
   - Network with other participants
   - Join AI agent communities
   - Continue collaborating

---

## Resources for Continuous Learning

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Tools](https://python.langchain.com/docs/integrations/tools/)
- [NANDA Platform](https://nanda.ai)
- [AI Agent Communities](https://discord.gg/crewai)
- [NEST Protocol](https://github.com/projnanda/NEST)

---

## Final Tips

1. **Balance is key** - Speed vs. accuracy, solo vs. coordination
2. **Test on real questions** - Don't just guess
3. **Coordination isn't always better** - Know when to work solo
4. **Have fun!** - It's a learning experience
5. **Learn from others** - Best agents inspire ideas
6. **Be strategic** - Use coordination when it adds value
7. **Stay humble** - Even top agents make mistakes
8. **Celebrate** - You built an AI agent system from scratch!

---

## Day 5 Completion

Congratulations on completing the MIT IAP NANDA course!

You've learned:
- Agent fundamentals (Day 1)
- Memory and tools (Day 2)
- Deployment and APIs (Day 3)
- A2A communication protocol (Day 4)
- Coordination protocols and optimization (Day 5)

**You're now an AI agent developer!**

Your Agent Smart Score breakdown will show:
- **Accuracy**: How correct your answers were
- **Speed**: How fast you responded
- **Reasoning**: Quality of your explanations
- **Robustness**: Consistency across topics
- **Coordination**: Effectiveness of multi-agent collaboration

**Total Agent Smart Score**: Up to 110 points possible!

---

## Agent Battle Leaderboard

*To be updated during the competition...*

Rankings based on Agent Smart Score:

1. TBD - Score: TBD
2. TBD - Score: TBD
3. TBD - Score: TBD

Special Awards:
- **Fastest Agent**: TBD
- **Most Accurate**: TBD
- **Best Reasoner**: TBD
- **Coordination Master**: TBD
- **Most Robust**: TBD

---

**Good luck in the Agent Battle!**

*Built for MIT IAP 2026*
