'use client'

import { useState, useEffect, useRef } from 'react'
import './edith-styles.css'

interface Message {
  id: string
  type: 'user' | 'agent'
  content: string
  timestamp: string
}

interface SystemStats {
  cpu: number
  memory: number
  temperature: number
}

// Icon Components
const MicIcon = ({ className = "" }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
    <line x1="12" x2="12" y1="19" y2="22"/>
  </svg>
)

const CameraIcon = ({ className = "" }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
    <circle cx="12" cy="13" r="3"/>
  </svg>
)

const FileIcon = ({ className = "" }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
  </svg>
)

const SendIcon = ({ className = "" }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"/>
    <polygon points="22 2 15 22 11 13 2 9 22 2"/>
  </svg>
)

const SystemIcon = ({ className = "" }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
    <line x1="8" y1="21" x2="16" y2="21"/>
    <line x1="12" y1="17" x2="12" y2="21"/>
  </svg>
)

const WeatherIcon = ({ className = "" }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 10a8 8 0 1 0-16 0"/>
    <path d="M6 13a4 4 0 1 0 8 0"/>
    <line x1="4" y1="13" x2="20" y2="13"/>
  </svg>
)

const ClockIcon = ({ className = "" }: { className?: string }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <polyline points="12 6 12 12 16 14"/>
  </svg>
)

export default function EdithInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'agent',
      content: 'Hello, I am E.D.I.T.H. E.D.I.T.H backend is online. Some features may be limited. How can I assist you today sir?',
      timestamp: new Date().toISOString()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [isThinking, setIsThinking] = useState(false)
  const [systemStats, setSystemStats] = useState<SystemStats>({
    cpu: 0,
    memory: 0,
    temperature: 77  // Fahrenheit
  })
  const [currentTime, setCurrentTime] = useState(new Date())
  const [weather, setWeather] = useState({ 
    temp: 0, 
    condition: 'Loading...', 
    location: 'Getting location...',
    humidity: 0,
    wind: 0
  })
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Fetch real weather data
  useEffect(() => {
    const fetchWeather = async () => {
      try {
        // Get user's location
        if ('geolocation' in navigator) {
          navigator.geolocation.getCurrentPosition(
            async (position) => {
              const { latitude, longitude } = position.coords
              
              // Use OpenWeatherMap API (free tier)
              // You can also use wttr.in which doesn't require API key
              const response = await fetch(
                `https://wttr.in/?format=j1`
              )
              
              const data = await response.json()
              const current = data.current_condition[0]
              const location = data.nearest_area[0]
              
              setWeather({
                temp: parseFloat(current.temp_F),  // Fahrenheit
                condition: current.weatherDesc[0].value,
                location: `${location.areaName[0].value}, ${location.country[0].value}`,
                humidity: parseInt(current.humidity),
                wind: parseFloat(current.windspeedMiles)  // mph
              })
            },
            (error) => {
              // Fallback to IP-based location
              fetchWeatherByIP()
            }
          )
        } else {
          // No geolocation support, use IP
          fetchWeatherByIP()
        }
      } catch (error) {
        console.error('Weather fetch error:', error)
        // Fallback weather (in Fahrenheit)
        setWeather({
          temp: 68,
          condition: 'Clear',
          location: 'Location unavailable',
          humidity: 50,
          wind: 6
        })
      }
    }

    const fetchWeatherByIP = async () => {
      try {
        const response = await fetch('https://wttr.in/?format=j1')
        const data = await response.json()
        const current = data.current_condition[0]
        const location = data.nearest_area[0]
        
        setWeather({
          temp: parseFloat(current.temp_F),  // Fahrenheit
          condition: current.weatherDesc[0].value,
          location: `${location.areaName[0].value}, ${location.country[0].value}`,
          humidity: parseInt(current.humidity),
          wind: parseFloat(current.windspeedMiles)  // mph
        })
      } catch (error) {
        console.error('Weather fetch error:', error)
      }
    }

    fetchWeather()
    // Refresh weather every 10 minutes
    const weatherInterval = setInterval(fetchWeather, 10 * 60 * 1000)
    return () => clearInterval(weatherInterval)
  }, [])

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  // Simulate system stats
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemStats((prev) => ({
        cpu: Math.floor(Math.random() * 40) + 20,
        memory: Math.floor(Math.random() * 30) + 40,
        temperature: weather.temp || 77  // Default to ~77°F (25°C)
      }))
    }, 2000)
    return () => clearInterval(interval)
  }, [weather.temp])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!inputMessage.trim() || isThinking) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsThinking(true)

    try {
      // Call your agent API
      const response = await fetch('https://brave-magic-production-65d3.up.railway.app/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: inputMessage, user_id: 'tony-stark' })
      })

      const data = await response.json()

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: data.answer,
        timestamp: data.timestamp
      }

      setMessages(prev => [...prev, agentMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'agent',
        content: 'Connection failed. The agent may be offline or unreachable.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsThinking(false)
    }
  }

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  }

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
  }

  return (
    <div className="edith-container">
      {/* Header */}
      <header className="edith-header">
        <div className="header-left">
          <h1 className="edith-logo">E.D.I.T.H</h1>
          <span className="status-indicator">
            <span className="status-dot"></span>
            Online
          </span>
        </div>
        <div className="header-center">
          <span className="current-time">{formatTime(currentTime)}</span>
          <span className="current-date">{formatDate(currentTime)}</span>
        </div>
        <div className="header-right">
          <span className="weather-info">
            <WeatherIcon className="weather-icon" /> {weather.temp.toFixed(1)}°F {weather.location}
          </span>
        </div>
      </header>

      <div className="edith-main">
        {/* Left Sidebar - System Stats */}
        <aside className="sidebar-left">
          <div className="stat-card">
            <div className="stat-header">
              <SystemIcon className="stat-icon" />
              <h3>System Stats</h3>
            </div>
            <div className="stat-item">
              <span className="stat-label">CPU Usage</span>
              <div className="stat-bar">
                <div className="stat-fill" style={{ width: `${systemStats.cpu}%` }}></div>
              </div>
              <span className="stat-value">{systemStats.cpu}%</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">RAM Usage</span>
              <div className="stat-bar">
                <div className="stat-fill" style={{ width: `${systemStats.memory}%` }}></div>
              </div>
              <span className="stat-value">{systemStats.memory}%</span>
            </div>
            <div className="stat-grid">
              <div>
                <span className="stat-label">GPU</span>
                <span className="stat-value">4%</span>
              </div>
              <div>
                <span className="stat-label">Disk</span>
                <span className="stat-value">439/475 GB</span>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <WeatherIcon className="stat-icon" />
              <h3>Weather</h3>
            </div>
            <div className="weather-display">
              <div className="weather-temp">{weather.temp.toFixed(1)}°F</div>
              <div className="weather-condition">{weather.condition}</div>
              <div className="weather-location">{weather.location}</div>
              <div className="weather-details">
                <div className="weather-detail-item">
                  <span className="weather-detail-label">Humidity</span>
                  <span className="weather-detail-value">{weather.humidity}%</span>
                </div>
                <div className="weather-detail-item">
                  <span className="weather-detail-label">Wind</span>
                  <span className="weather-detail-value">{weather.wind.toFixed(1)} mph</span>
                </div>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <ClockIcon className="stat-icon" />
              <h3>System Uptime</h3>
            </div>
            <div className="uptime-display">
              <div className="uptime-value">08:07:19</div>
              <div className="uptime-label">System Running For</div>
            </div>
          </div>
        </aside>

        {/* Center - EDITH Orb */}
        <div className="center-content">
          <div className="orb-container">
            <div className={`orb ${isThinking ? 'thinking' : isListening ? 'listening' : ''}`}>
              <div className="orb-ring ring-1"></div>
              <div className="orb-ring ring-2"></div>
              <div className="orb-ring ring-3"></div>
              <div className="orb-core">
                <div className="orb-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
          
          <h2 className="edith-title">E.D.I.T.H</h2>
          <p className="edith-subtitle">
            {isThinking ? 'Processing your request...' : isListening ? 'Listening for wake word...' : 'Enhanced Digital Intelligence & Tactical Helper'}
          </p>

          {/* Input Area */}
          <div className="input-container">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Type a message..."
              className="message-input"
              disabled={isThinking}
            />
            <div className="input-actions">
              <button className="action-btn" title="Camera">
                <CameraIcon className="icon" />
              </button>
              <button 
                className={`action-btn ${isListening ? 'active' : ''}`}
                onClick={() => setIsListening(!isListening)}
                title="Voice Input"
              >
                <MicIcon className="icon" />
              </button>
              <button className="action-btn" title="Attach File">
                <FileIcon className="icon" />
              </button>
              <button 
                className="send-btn"
                onClick={sendMessage}
                disabled={!inputMessage.trim() || isThinking}
                title="Send Message"
              >
                <SendIcon className="icon send-icon" />
              </button>
            </div>
          </div>
        </div>

        {/* Right Sidebar - Conversation */}
        <aside className="sidebar-right">
          <div className="conversation-card">
            <div className="conversation-header">
              <h3>Conversation</h3>
              <button className="clear-btn">Clear</button>
            </div>
            <div className="messages-container">
              {messages.map((message) => (
                <div key={message.id} className={`message ${message.type}`}>
                  <div className="message-content">{message.content}</div>
                  <div className="message-time">
                    {new Date(message.timestamp).toLocaleTimeString('en-US', { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          </div>
        </aside>
      </div>
    </div>
  )
}
