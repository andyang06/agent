'use client'

import { useState, useEffect, useRef } from 'react'
import EdithInterface from './edith-page'

interface Message {
  id: string
  type: 'user' | 'agent'
  content: string
  timestamp: string
  processingTime?: number
}

interface Agent {
  id: string
  username: string
  name: string
  url: string
  description: string
  createdAt: string
}

// In development: use localhost:3001, in production: use same domain
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 
  (typeof window !== 'undefined' && window.location.hostname === 'localhost' 
    ? 'http://localhost:3001' 
    : (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3001'))

const API_BASE = `${BACKEND_URL}/api`

export default function Home() {
  // Use the JARVIS-style EDITH interface
  return <EdithInterface />
}

function ClassicInterface() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [currentAgent, setCurrentAgent] = useState<Agent | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showAddAgent, setShowAddAgent] = useState(false)
  const [showAgentList, setShowAgentList] = useState(true)

  const [newAgentUsername, setNewAgentUsername] = useState('')
  const [newAgentName, setNewAgentName] = useState('')
  const [newAgentUrl, setNewAgentUrl] = useState('')
  const [newAgentDescription, setNewAgentDescription] = useState('')

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const loadAgents = async () => {
    try {
      const response = await fetch(`${API_BASE}/agents`)
      const data = await response.json()
      setAgents(data.agents || [])
    } catch (error) {
      console.error('Failed to load agents:', error)
    }
  }

  useEffect(() => {
    loadAgents()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const addAgent = async () => {
    if (!newAgentUsername || !newAgentName || !newAgentUrl) return

    let url = newAgentUrl.trim()
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = 'https://' + url
    }

    try {
      const response = await fetch(`${API_BASE}/agents`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: newAgentUsername.trim().toLowerCase(),
          name: newAgentName.trim(),
          url: url,
          description: newAgentDescription.trim()
        })
      })

      if (response.ok) {
        setNewAgentUsername('')
        setNewAgentName('')
        setNewAgentUrl('')
        setNewAgentDescription('')
        setShowAddAgent(false)
        await loadAgents()
      } else {
        const data = await response.json()
        alert(data.error)
      }
    } catch (error) {
      alert('Failed to add agent. Please check the backend connection.')
    }
  }

  const removeAgent = async (id: string) => {
    if (!confirm('Remove this agent from the registry?')) return

    try {
      const response = await fetch(`${API_BASE}/agents/${id}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        await loadAgents()
        if (currentAgent?.id === id) {
          setCurrentAgent(null)
          setMessages([])
        }
      }
    } catch (error) {
      alert('Failed to remove agent')
    }
  }

  const selectAgent = (agent: Agent) => {
    setCurrentAgent(agent)
    setShowAgentList(false)
    setMessages([{
      id: Date.now().toString(),
      type: 'agent',
      content: `Hello, I'm ${agent.name}. How can I help you today?`,
      timestamp: new Date().toISOString()
    }])
  }

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading || !currentAgent) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch(`${currentAgent.url}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: inputMessage,
          user_id: 'student'
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: data.answer,
        timestamp: data.timestamp,
        processingTime: data.processing_time
      }

      setMessages(prev => [...prev, agentMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: `Connection failed. The agent may be offline or unreachable.`,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  if (showAgentList || !currentAgent) {
    return (
      <div className="min-h-screen bg-[#FAFBFC]">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="mb-12">
            <div className="flex items-center justify-between mb-2">
              <div>
                <h1 className="text-4xl font-bold text-[#1e3a8a] tracking-tight">E.D.I.T.H</h1>
                <p className="text-sm text-[#3b82f6] font-medium mt-1">Enhanced Digital Intelligence & Tactical Helper</p>
              </div>
              <div className="flex gap-3">
                <button
                  onClick={loadAgents}
                  className="px-4 py-2 text-sm font-medium text-[#6B7280] hover:text-[#2D3142] bg-white border border-[#E5E7EB] rounded-lg hover:border-[#9CA3AF] transition-all"
                >
                  Refresh
                </button>
                <button
                  onClick={() => setShowAddAgent(!showAddAgent)}
                  className="px-4 py-2 text-sm font-medium text-white bg-[#3b82f6] rounded-lg hover:bg-[#2563eb] transition-all shadow-sm"
                >
                  {showAddAgent ? 'Cancel' : 'Add Agent'}
                </button>
              </div>
            </div>
            <p className="text-[#6B7280]">Select an agent to start a conversation</p>
          </div>

          {showAddAgent && (
            <div className="bg-white rounded-2xl border border-[#E5E7EB] p-8 mb-8 shadow-sm">
              <h2 className="text-xl font-semibold text-[#2D3142] mb-6">Register New Agent</h2>
              <div className="space-y-5">
                <div>
                  <label className="block text-sm font-medium text-[#4F5D75] mb-2">
                    Username <span className="text-[#EF4444]">*</span>
                  </label>
                  <input
                    type="text"
                    value={newAgentUsername}
                    onChange={(e) => setNewAgentUsername(e.target.value)}
                    placeholder="agent_1 or maria-agent"
                    className="w-full px-4 py-3 bg-white border border-[#E5E7EB] rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent outline-none text-[#2D3142] placeholder-[#9CA3AF]"
                  />
                  <p className="text-sm text-[#9CA3AF] mt-2">
                    Unique identifier for @mentions (letters, numbers, hyphens, underscores)
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#4F5D75] mb-2">
                    Agent Name <span className="text-[#EF4444]">*</span>
                  </label>
                  <input
                    type="text"
                    value={newAgentName}
                    onChange={(e) => setNewAgentName(e.target.value)}
                    placeholder="Weather Predictor Agent"
                    className="w-full px-4 py-3 bg-white border border-[#E5E7EB] rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent outline-none text-[#2D3142] placeholder-[#9CA3AF]"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#4F5D75] mb-2">
                    Deployment URL
                  </label>
                  <input
                    type="text"
                    value={newAgentUrl}
                    onChange={(e) => setNewAgentUrl(e.target.value)}
                    placeholder="agent-name.up.railway.app"
                    className="w-full px-4 py-3 bg-white border border-[#E5E7EB] rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent outline-none text-[#2D3142] placeholder-[#9CA3AF]"
                  />
                  <p className="text-sm text-[#9CA3AF] mt-2">
                    Your Railway deployment URL
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-[#4F5D75] mb-2">
                    Description
                  </label>
                  <input
                    type="text"
                    value={newAgentDescription}
                    onChange={(e) => setNewAgentDescription(e.target.value)}
                    placeholder="What this agent specializes in"
                    className="w-full px-4 py-3 bg-white border border-[#E5E7EB] rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent outline-none text-[#2D3142] placeholder-[#9CA3AF]"
                  />
                </div>
                <button
                  onClick={addAgent}
                  disabled={!newAgentUsername || !newAgentName || !newAgentUrl}
                  className="w-full bg-[#6366F1] text-white py-3 rounded-lg font-medium hover:bg-[#4F46E5] disabled:bg-[#E5E7EB] disabled:text-[#9CA3AF] disabled:cursor-not-allowed transition-all shadow-sm"
                >
                  Register Agent
                </button>
              </div>
            </div>
          )}

          {agents.length === 0 ? (
            <div className="bg-white rounded-2xl border border-[#E5E7EB] p-16 text-center shadow-sm">
              <div className="max-w-sm mx-auto">
                <h3 className="text-xl font-semibold text-[#2D3142] mb-3">No Agents Registered</h3>
                <p className="text-[#6B7280] mb-6">Add your first agent to get started</p>
                <button
                  onClick={() => setShowAddAgent(true)}
                  className="px-6 py-3 bg-[#6366F1] text-white rounded-lg hover:bg-[#4F46E5] transition-all font-medium shadow-sm"
                >
                  Register First Agent
                </button>
              </div>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {agents.map((agent) => (
                <div
                  key={agent.id}
                  onClick={() => selectAgent(agent)}
                  className="bg-white rounded-xl border border-[#E5E7EB] p-6 hover:border-[#6366F1] hover:shadow-md transition-all cursor-pointer group"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-semibold text-[#2D3142] mb-1 truncate group-hover:text-[#6366F1] transition-colors">
                        {agent.name}
                      </h3>
                      <p className="text-sm text-[#6366F1] font-mono mb-2">@{agent.username}</p>
                      {agent.description && (
                        <p className="text-sm text-[#6B7280] line-clamp-2">{agent.description}</p>
                      )}
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        removeAgent(agent.id)
                      }}
                      className="ml-3 text-[#9CA3AF] hover:text-[#EF4444] transition-colors text-lg leading-none"
                    >
                      ×
                    </button>
                  </div>
                  <div className="flex items-center justify-between pt-4 border-t border-[#F3F4F6]">
                    <span className="text-xs text-[#9CA3AF]">
                      {new Date(agent.createdAt).toLocaleDateString()}
                    </span>
                    <span className="text-sm font-medium text-[#6366F1] opacity-0 group-hover:opacity-100 transition-opacity">
                      Open →
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen bg-[#FAFBFC]">
      <div className="bg-white border-b border-[#E5E7EB]">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setShowAgentList(true)}
              className="text-[#3b82f6] hover:text-[#2563eb] font-medium text-sm transition-colors"
            >
              ← Back to E.D.I.T.H
            </button>
            <div className="h-6 w-px bg-[#E5E7EB]"></div>
            <div>
              <h1 className="text-lg font-semibold text-[#2D3142]">{currentAgent.name}</h1>
              <p className="text-xs text-[#9CA3AF] truncate max-w-md">{currentAgent.url}</p>
            </div>
          </div>
          <div className="text-xs text-[#9CA3AF]">
            {messages.length - 1} {messages.length === 2 ? 'message' : 'messages'}
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto px-6 py-8 space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[75%] rounded-2xl px-5 py-3 ${
                  message.type === 'user'
                    ? 'bg-[#6366F1] text-white'
                    : 'bg-white text-[#2D3142] border border-[#E5E7EB] shadow-sm'
                }`}
              >
                <p className="whitespace-pre-wrap break-words leading-relaxed">{message.content}</p>
                <div className={`flex items-center gap-3 mt-2 text-xs ${
                  message.type === 'user' ? 'text-indigo-200' : 'text-[#9CA3AF]'
                }`}>
                  <span>{new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                  {message.processingTime && (
                    <span>{message.processingTime.toFixed(2)}s</span>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-2xl px-5 py-4 border border-[#E5E7EB] shadow-sm">
                <div className="flex items-center gap-1.5">
                  <div className="w-2 h-2 bg-[#9CA3AF] rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-[#9CA3AF] rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-[#9CA3AF] rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="bg-white border-t border-[#E5E7EB]">
        <div className="max-w-5xl mx-auto px-6 py-5">
          <div className="flex gap-3">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1 px-4 py-3 border border-[#E5E7EB] rounded-lg focus:ring-2 focus:ring-[#6366F1] focus:border-transparent outline-none transition-all disabled:bg-[#F9FAFB] disabled:text-[#9CA3AF] text-[#2D3142] placeholder-[#9CA3AF]"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="bg-[#6366F1] text-white px-8 py-3 rounded-lg font-medium hover:bg-[#4F46E5] disabled:bg-[#E5E7EB] disabled:text-[#9CA3AF] disabled:cursor-not-allowed transition-all shadow-sm"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
