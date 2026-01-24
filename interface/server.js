/**
 * Combined Server - Backend API + Frontend
 */

const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
const { createServer } = require('http');

const app = express();
const PORT = process.env.PORT || 3001;
const AGENTS_FILE = path.join(__dirname, 'agents.json');
const IS_PRODUCTION = process.env.NODE_ENV === 'production';

// Middleware
app.use(cors());
app.use(express.json());

// Initialize agents.json
async function initializeAgentsFile() {
  try {
    await fs.access(AGENTS_FILE);
  } catch {
    await fs.writeFile(AGENTS_FILE, JSON.stringify([], null, 2));
    console.log('✅ Created agents.json');
  }
}

// Read agents
async function readAgents() {
  try {
    const data = await fs.readFile(AGENTS_FILE, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error reading agents:', error);
    return [];
  }
}

// Write agents
async function writeAgents(agents) {
  try {
    await fs.writeFile(AGENTS_FILE, JSON.stringify(agents, null, 2));
  } catch (error) {
    console.error('Error writing agents:', error);
    throw error;
  }
}

// ==============================================================================
// API Endpoints
// ==============================================================================

app.get('/api', (req, res) => {
  res.json({
    message: '🚀 CrewAI Agent Registry API',
    version: '2.0.0',
    endpoints: {
      'GET /api/agents': 'List all registered agents',
      'POST /api/agents': 'Add a new agent (requires: username, name, url)',
      'DELETE /api/agents/:id': 'Remove an agent',
      'GET /api/health': 'Health check'
    },
    fields: {
      username: 'Unique identifier for @mentions (e.g., "agent_1", "maria-agent")',
      name: 'Human-readable name (e.g., "Weather Agent")',
      url: 'Agent A2A endpoint URL (e.g., "https://agent.railway.app/a2a")',
      description: 'Optional description of agent capabilities'
    }
  });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.get('/api/agents', async (req, res) => {
  try {
    const agents = await readAgents();
    res.json({ agents, count: agents.length });
  } catch (error) {
    res.status(500).json({ error: 'Failed to read agents' });
  }
});

app.post('/api/agents', async (req, res) => {
  try {
    const { name, username, url, description } = req.body;

    if (!name || !username || !url) {
      return res.status(400).json({ 
        error: 'Missing required fields: name, username, and url' 
      });
    }

    // Validate username format (alphanumeric, hyphens, underscores only)
    if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
      return res.status(400).json({ 
        error: 'Username must contain only letters, numbers, hyphens, and underscores' 
      });
    }

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      return res.status(400).json({ 
        error: 'URL must start with http:// or https://' 
      });
    }

    const agents = await readAgents();

    // Check for duplicate username
    if (agents.some(agent => agent.username === username)) {
      return res.status(409).json({ 
        error: 'This username is already taken' 
      });
    }

    // Check for duplicate URL
    if (agents.some(agent => agent.url === url)) {
      return res.status(409).json({ 
        error: 'This agent URL is already registered' 
      });
    }

    const newAgent = {
      id: Date.now().toString(),
      username: username.trim().toLowerCase(),
      name: name.trim(),
      url: url.trim(),
      description: description?.trim() || '',
      createdAt: new Date().toISOString()
    };

    agents.push(newAgent);
    await writeAgents(agents);

    res.status(201).json({ 
      message: 'Agent added successfully', 
      agent: newAgent 
    });
  } catch (error) {
    console.error('Error adding agent:', error);
    res.status(500).json({ error: 'Failed to add agent' });
  }
});

app.delete('/api/agents/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const agents = await readAgents();
    
    const filteredAgents = agents.filter(agent => agent.id !== id);
    
    if (filteredAgents.length === agents.length) {
      return res.status(404).json({ error: 'Agent not found' });
    }

    await writeAgents(filteredAgents);
    
    res.json({ 
      message: 'Agent removed successfully',
      id 
    });
  } catch (error) {
    console.error('Error removing agent:', error);
    res.status(500).json({ error: 'Failed to remove agent' });
  }
});

// ==============================================================================
// Start Server
// ==============================================================================

async function startServer() {
  await initializeAgentsFile();
  
  // In production, prepare Next.js first
  if (IS_PRODUCTION) {
    const next = require('next');
    const nextApp = next({ dev: false, dir: __dirname });
    const nextHandler = nextApp.getRequestHandler();
    
    try {
      await nextApp.prepare();
      console.log('✅ Next.js prepared successfully');
      
      // Let Next.js handle all non-API routes
      app.all('*', (req, res) => {
        // Skip API routes - let Express handle them
        if (req.path.startsWith('/api')) {
          return;
        }
        return nextHandler(req, res);
      });
    } catch (err) {
      console.error('❌ Error preparing Next.js:', err);
      process.exit(1);
    }
  }
  
  const server = createServer(app);
  
  server.listen(PORT, '0.0.0.0', () => {
    console.log('\n' + '='.repeat(70));
    console.log('🚀 CrewAI Agent Interface');
    console.log('='.repeat(70));
    console.log(`\n✅ Server running on port ${PORT}`);
    console.log(`✅ Mode: ${IS_PRODUCTION ? 'PRODUCTION' : 'DEVELOPMENT'}`);
    console.log(`✅ Agents file: ${AGENTS_FILE}`);
    
    if (IS_PRODUCTION) {
      console.log('\n📱 Frontend + Backend served on same port');
    } else {
      console.log('\n📱 Frontend: Run "npm run dev:frontend" (port 3000)');
    }
    
    console.log('\n📚 API Endpoints:');
    console.log(`   GET    /api/agents`);
    console.log(`   POST   /api/agents`);
    console.log(`   DELETE /api/agents/:id`);
    console.log('\n' + '='.repeat(70) + '\n');
  });
}

startServer();
