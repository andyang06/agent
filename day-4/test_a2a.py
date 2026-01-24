"""
Simple test script for A2A (Agent-to-Agent) communication

This script demonstrates how to:
1. Send direct messages to your agent
2. Register other agents
3. Route messages to other agents using @agent-id syntax
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"  # Change to your Railway URL when deployed

def test_health():
    """Test if the agent is running"""
    print("\n" + "="*70)
    print("Test 1: Health Check")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_agent_info():
    """Get agent information"""
    print("\n" + "="*70)
    print("Test 2: Agent Information")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Agent ID: {data.get('agent_id')}")
    print(f"Agent Name: {data.get('agent_name')}")
    print(f"A2A Enabled: {data.get('a2a_enabled')}")
    print(f"Known Agents: {data.get('known_agents')}")
    return response.status_code == 200

def test_direct_message():
    """Send a direct message (no routing)"""
    print("\n" + "="*70)
    print("Test 3: Direct Message (No Routing)")
    print("="*70)
    
    message = {
        "content": {
            "text": "What is 2+2?",
            "type": "text"
        },
        "role": "user",
        "conversation_id": "test-direct-001"
    }
    
    print(f"Sending: {message['content']['text']}")
    response = requests.post(f"{BASE_URL}/a2a", json=message)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\nAgent Response:")
        print(data['content']['text'])
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_register_agent():
    """Register a test agent"""
    print("\n" + "="*70)
    print("Test 4: Register Another Agent")
    print("="*70)
    
    # Register a mock agent (replace with real agent URL)
    agent_id = "test-agent"
    agent_url = "http://example.com/a2a"  # Replace with real URL
    
    response = requests.post(
        f"{BASE_URL}/agents/register",
        params={"agent_id": agent_id, "agent_url": agent_url}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Message: {data['message']}")
        print(f"Total Known Agents: {data['total_known_agents']}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_list_agents():
    """List all known agents"""
    print("\n" + "="*70)
    print("Test 5: List Known Agents")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/agents")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nMy Agent ID: {data['my_agent_id']}")
        print(f"My Agent Name: {data['my_agent_name']}")
        print(f"My Agent Username: {data.get('my_agent_username', 'N/A')}")
        print("\nKnown Agents:")
        for agent_id, agent_url in data['known_agents'].items():
            print(f"  - {agent_id}: {agent_url}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_agent_facts():
    """Get AgentFacts (NANDA schema)"""
    print("\n" + "="*70)
    print("Test 6: AgentFacts (NANDA Discovery)")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/agentfacts")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n📋 AgentFacts:")
        print(f"  ID: {data.get('id')}")
        print(f"  Agent Name (URN): {data.get('agent_name')}")
        print(f"  Label: {data.get('label')}")
        print(f"  Description: {data.get('description')}")
        print(f"  Version: {data.get('version')}")
        print(f"  Provider: {data.get('provider', {}).get('name')}")
        print(f"  Jurisdiction: {data.get('jurisdiction')}")
        print("\n🔗 Endpoints:")
        for endpoint in data.get('endpoints', {}).get('static', []):
            print(f"    - {endpoint}")
        print(f"\n🎯 Skills ({len(data.get('skills', []))}):")
        for skill in data.get('skills', []):
            print(f"    - {skill['id']}: {skill['description']}")
        print("\n⚡ Performance:")
        metrics = data.get('telemetry', {}).get('metrics', {})
        print(f"    - Latency P95: {metrics.get('latency_p95_ms')}ms")
        print(f"    - Throughput: {metrics.get('throughput_rps')} req/s")
        print(f"    - Availability: {metrics.get('availability')}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_routed_message():
    """Send a message to be routed to another agent"""
    print("\n" + "="*70)
    print("Test 6: Routed Message (with @agent-id)")
    print("="*70)
    
    # First, make sure we have at least one agent registered
    test_register_agent()
    
    message = {
        "content": {
            "text": "@test-agent Can you help me with this task?",
            "type": "text"
        },
        "role": "user",
        "conversation_id": "test-routed-001"
    }
    
    print(f"\nSending to YOUR agent: {message['content']['text']}")
    print("(Your agent will route this to test-agent)")
    print("\nWhat happens:")
    print("  1. You → YOUR agent")
    print("  2. YOUR agent sees @test-agent")
    print("  3. YOUR agent → test-agent's /a2a endpoint")
    print("  4. test-agent responds")
    print("  5. YOUR agent returns the response")
    
    response = requests.post(f"{BASE_URL}/a2a", json=message)
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\nResponse:")
        print(data['content']['text'])
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_standard_query():
    """Test the standard /query endpoint (from Day 3)"""
    print("\n" + "="*70)
    print("Test 7: Standard Query Endpoint (Day 3)")
    print("="*70)
    
    query = {
        "question": "What is 10 * 10?",
        "user_id": "test-user"
    }
    
    print(f"Sending: {query['question']}")
    response = requests.post(f"{BASE_URL}/query", json=query)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nAnswer: {data['answer']}")
        print(f"Processing Time: {data['processing_time']:.2f}s")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def main():
    """Run all tests"""
    print("\n🤖 A2A Testing Suite")
    print("="*70)
    print(f"Testing agent at: {BASE_URL}")
    print("="*70)
    
    tests = [
        ("Health Check", test_health),
        ("Agent Info", test_agent_info),
        ("AgentFacts", test_agent_facts),
        ("Direct Message", test_direct_message),
        ("List Agents", test_list_agents),
        ("Register Agent", test_register_agent),
        ("Standard Query", test_standard_query),
        # ("Routed Message", test_routed_message),  # Uncomment when you have real agents
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*70)

if __name__ == "__main__":
    # Note: Make sure your agent is running first!
    # Run: uvicorn main:app --reload
    main()

