import { useState, useEffect } from 'react';
import './App.css';
import api from './api';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { text: 'Hello! I am your free Manus AI assistant. How can I help you today?', sender: 'ai' }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isBackendConnected, setIsBackendConnected] = useState(false);

  // Check backend connection on component mount
  useEffect(() => {
    const checkBackendConnection = async () => {
      try {
        await api.healthCheck();
        setIsBackendConnected(true);
      } catch (error) {
        console.error('Backend connection failed:', error);
        setIsBackendConnected(false);
      }
    };

    checkBackendConnection();
  }, []);

  const handleSendMessage = async () => {
    if (input.trim() === '') return;
    
    // Add user message
    setMessages([...messages, { text: input, sender: 'user' }]);
    setIsProcessing(true);
    
    try {
      if (isBackendConnected) {
        // Send message to backend if connected
        const response = await api.sendMessage(input);
        setMessages(prev => [...prev, { 
          text: response.message || 'I processed your request successfully.', 
          sender: 'ai' 
        }]);
      } else {
        // Simulate AI response if backend is not connected
        setTimeout(() => {
          setMessages(prev => [...prev, { 
            text: 'I am processing your request. As a free, open-source alternative to Manus AI, I can help with various tasks including research, content creation, and data analysis. (Note: This is a simulated response as the backend is not currently connected)', 
            sender: 'ai' 
          }]);
          setIsProcessing(false);
        }, 1000);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        text: 'Sorry, I encountered an error processing your request. Please try again later.', 
        sender: 'ai' 
      }]);
    } finally {
      setIsProcessing(false);
      setInput('');
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <div className="logo">
          <span>Free Manus AI</span>
        </div>
        <nav className="nav-links">
          <a href="#features" className="nav-link">Features</a>
          <a href="#documentation" className="nav-link">Documentation</a>
          <a href="#github" className="nav-link">GitHub</a>
          <a href="#community" className="nav-link">Community</a>
        </nav>
      </header>

      <main className="main-content">
        <section className="hero-section">
          <h1 className="hero-title">Free Manus AI</h1>
          <p className="hero-subtitle">
            A completely free, open-source alternative to Manus.im with no limitations.
            Experience the power of autonomous AI agents without subscription costs or login requirements.
          </p>
          <button className="cta-button">Start Using Now</button>
          {!isBackendConnected && (
            <div className="backend-status">
              <p>⚠️ Backend connection not detected. Running in demo mode with simulated responses.</p>
            </div>
          )}
        </section>

        <section id="features" className="features-section">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3 className="feature-title">Autonomous Task Execution</h3>
            <p className="feature-description">
              Execute complex tasks independently, from report writing to data analysis and content generation.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔄</div>
            <h3 className="feature-title">Multi-Modal Capabilities</h3>
            <p className="feature-description">
              Process and generate multiple types of data including text, images, and code.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔧</div>
            <h3 className="feature-title">Advanced Tool Integration</h3>
            <p className="feature-description">
              Integrate with external tools including web browsers, code editors, and database systems.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🧠</div>
            <h3 className="feature-title">Adaptive Learning</h3>
            <p className="feature-description">
              Learn from interactions to provide personalized and efficient responses over time.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🌐</div>
            <h3 className="feature-title">Web-Based Interface</h3>
            <p className="feature-description">
              Access your AI assistant through an intuitive web interface from any device.
            </p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">💯</div>
            <h3 className="feature-title">No Limitations</h3>
            <p className="feature-description">
              All features available with no artificial restrictions, paid tiers, or login requirements. Completely free and open-source.
            </p>
          </div>
        </section>

        <section className="chat-demo">
          <h2>Try It Now - No Login Required</h2>
          <div className="chat-container">
            <div className="chat-messages">
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.sender}-message`}>
                  {message.text}
                </div>
              ))}
              {isProcessing && (
                <div className="message ai-message">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}
            </div>
            <div className="chat-input-container">
              <input
                type="text"
                className="chat-input"
                placeholder="Ask anything..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              />
              <button className="send-button" onClick={handleSendMessage}>
                Send
              </button>
            </div>
          </div>
        </section>
      </main>

      <footer className="footer">
        <p className="footer-text">
          Free Manus AI - A completely free, open-source alternative to Manus.im with no limitations or login requirements.
        </p>
      </footer>
    </div>
  );
}

export default App;
