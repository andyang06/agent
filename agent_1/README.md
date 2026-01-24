# Agent-to-Agent (A2A) Testing Guide

Quick guide for testing two specialized agents communicating with each other!

## 🤖 The Agents

**Agent 1 (Weather Predictor)**
- Username: `agent_1`
- URL: `https://agent1-production-78c0.up.railway.app`
- Specialty: Weather forecasting and climate analysis

**Agent 2 (Robot Expert)**
- Username: `agent_2`
- URL: `https://agent2-production.up.railway.app`
- Specialty: Robotics and automation systems

---

## 🚀 Quick Setup

### 1. Deploy Both Agents
```bash
# Deploy agent_1
cd agent_1
railway up

# Deploy agent_2
cd ../agent_2
railway up
```

### 2. Register in Central Registry
```bash
# Register agent_1
curl -X POST https://nanda-testbed-production.up.railway.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "username": "agent_1",
    "name": "Weather Predictor Agent",
    "url": "https://agent1-production-78c0.up.railway.app",
    "description": "Weather forecasting specialist"
  }'

# Register agent_2
curl -X POST https://nanda-testbed-production.up.railway.app/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "username": "agent_2",
    "name": "Robot Expert Agent",
    "url": "https://agent2-production.up.railway.app",
    "description": "Robotics expert"
  }'
```

### 3. Restart Agents (Important!)
Agents fetch the registry on startup, so restart them after registration:
```bash
cd agent_1 && railway up
cd ../agent_2 && railway up
```

### 4. Verify Registration
```bash
# Check agent_1's known agents
curl https://agent1-production-78c0.up.railway.app/agents

# Check agent_2's known agents
curl https://agent2-production.up.railway.app/agents
```

You should see each agent in the other's list!

---

## 🧪 Demo Tests for Class

### Example 1: Weather Agent Asks About Robots
**Scenario:** Weather agent needs to know about robots used in weather stations

```bash
curl -X POST https://agent1-production-78c0.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "@agent_2 What types of robots are used in weather stations?",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "demo1"
  }'
```

**Expected:** Agent_1 routes the question to Agent_2 (robot expert) and returns the answer

---

### Example 2: Robot Agent Asks About Weather
**Scenario:** Robot expert needs weather info for outdoor robot design

```bash
curl -X POST https://agent2-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "@agent_1 What weather conditions are most challenging for outdoor robots?",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "demo2"
  }'
```

**Expected:** Agent_2 routes the question to Agent_1 (weather expert) and returns the answer

---

### Example 3: Complex Collaboration
**Scenario:** Design a weather-resistant robot

```bash
curl -X POST https://agent1-production-78c0.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "@agent_2 Design a robot that can collect weather data in extreme conditions like hurricanes and blizzards",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "demo3"
  }'
```

**Expected:** Agent_1 forwards to Agent_2, who designs the robot considering extreme weather

---

### Example 4: Temperature Conversion Task
**Scenario:** Robot needs temperature calculations for sensor calibration

```bash
curl -X POST https://agent2-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "@agent_1 What is -40 degrees Celsius in Fahrenheit? Our robot sensors need calibration.",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "demo4"
  }'
```

---

### Example 5: Error Demonstration (No @agent-id)
**Scenario:** Show what happens without routing

```bash
curl -X POST https://agent1-production-78c0.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "text": "What is the weather today?",
      "type": "text"
    },
    "role": "user",
    "conversation_id": "demo5"
  }'
```

**Expected:** Error message explaining that @agent-id is required for A2A routing

---

## 📊 Understanding the Response

**Successful A2A routing looks like:**
```json
{
  "content": {
    "text": "[Forwarded to @agent_2]\n\nWeather stations commonly use the following types of robots:\n\n1. Automated Weather Observation Systems (AWOS)...",
    "type": "text"
  },
  "role": "assistant",
  "conversation_id": "demo1",
  "timestamp": "2026-01-24T17:30:00.000000",
  "agent_id": "agent_1"
}
```

**Failed routing (agent not found):**
```json
{
  "content": {
    "text": "[Forwarded to @agent_2]\n\n❌ Agent 'agent_2' not found. Known agents: ['maria-agent']"
  }
}
```

---

## 🎯 Class Demo Flow

### 1. Show Agent Discovery (30 seconds)
```bash
# Show what agents are registered
curl https://nanda-testbed-production.up.railway.app/api/agents | jq '.agents[] | {username, name}'

# Show what each agent knows about
curl https://agent1-production-78c0.up.railway.app/agents | jq '.known_agents'
```

### 2. Demo Cross-Domain Expertise (2 minutes)
Run Examples 1 and 2 to show:
- Weather expert routing robot questions → Robot expert
- Robot expert routing weather questions → Weather expert

### 3. Show Collaboration (2 minutes)
Run Example 3 to show agents working together on complex task

### 4. Demo Error Handling (1 minute)
Run Example 5 to show strict A2A behavior

---

## 🔍 Checking Logs

In Railway Dashboard, check the logs to see:

**Agent_1 logs:**
```
📥 Fetched 5 agents from registry
   ✅ Registered: @agent_2 -> https://agent2-production.up.railway.app/a2a
🔀 Routing message to agent: agent_2
```

**Agent_2 logs:**
```
📥 Fetched 5 agents from registry
   ✅ Registered: @agent_1 -> https://agent1-production-78c0.up.railway.app/a2a
💬 Processing message locally
```

**A2A message logs** (in `logs/a2a_messages.log`):
```
2026-01-24 17:30:15 | INFO | INCOMING | conversation_id=demo1 | message=@agent_2 What types...
2026-01-24 17:30:15 | INFO | ROUTING | conversation_id=demo1 | target=agent_2 | message=What types...
2026-01-24 17:30:18 | INFO | SUCCESS | conversation_id=demo1 | target=agent_2 | response_length=245
```

---

## 🐛 Troubleshooting

### Agents don't see each other
**Problem:** `❌ Agent 'agent_2' not found`

**Solution:**
1. Check registry: `curl https://nanda-testbed-production.up.railway.app/api/agents`
2. Restart agents: `railway up` (forces them to fetch fresh registry)
3. Verify: `curl https://agent1-production-78c0.up.railway.app/agents`

### Messages timing out
**Problem:** Long wait times or timeout errors

**Solution:**
- Both agents use GPT-4o-mini (fast responses)
- Check Railway logs for errors
- Verify OPENAI_API_KEY is set

---

## 💡 Tips for Class Demo

1. **Pre-register agents** before class to save time
2. **Keep curl commands handy** in a text file for quick copy-paste
3. **Show the logs** in Railway dashboard during demo
4. **Explain the @agent-id syntax** - it's like mentioning someone in Slack
5. **Compare to manual APIs** - without A2A, you'd need to know each agent's specific API

---

## 🎓 Key Concepts to Highlight

1. **Automatic Discovery** - Agents find each other via central registry
2. **Specialization** - Each agent has domain expertise
3. **Routing** - Simple @agent-id syntax for message routing
4. **Strict Mode** - A2A endpoint requires routing (no silent fallbacks)
5. **Logging** - All A2A activity is tracked for debugging

---

## 📚 Additional Resources

- Full documentation: `../day-4/README.md`
- Central registry: `https://nanda-testbed-production.up.railway.app`
- NEST A2A protocol: `https://github.com/projnanda/NEST`

