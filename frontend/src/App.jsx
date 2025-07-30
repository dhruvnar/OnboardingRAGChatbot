import { useState, useRef, useEffect } from "react";
import "./App.css";
import logo from "./sagesure-logo.png";
import botLogo from "./botLogo.png"; // Make sure logo is present in src

const SendIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M7 11L12 6L17 11M12 18V7" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"></path>
    </svg>
);

const PlusIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 5V19M5 12H19" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"></path>
    </svg>
);

const UserAvatar = () => <span>You</span>
const BotAvatar = ({logo}) => <img src={logo} alt="bot avatar" style={{height: '24px', width: '24px'}}/>

const EXAMPLE_PROMPTS = [
    { title: "Vacation Policy", question: "What is the policy on vacation days?" },
    { title: "Office Locations", question: "What are the different office locations?" },
    { title: "Code of Conduct", question: "Summarize the company's code of conduct." },
    { title: "WFH Policy", question: "What is the work from home policy?" },
];


function App() {
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatContainerRef = useRef(null);

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, loading]);

  const handleSend = async (message) => {
    if (!message.trim()) return;

    const newChatHistory = [
      ...chatHistory,
      {
        id: Date.now(),
        type: "user",
        message: message,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      },
    ];
    setChatHistory(newChatHistory);
    setQuestion("");
    setLoading(true);

    try {
      const res = await fetch(`http://localhost:8000/ask?q=${encodeURIComponent(message)}`);
      const data = await res.json();
      setChatHistory(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          type: "bot",
          message: data.answer,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
      ]);
    } catch (error) {
      setChatHistory(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          type: "bot",
          message: "Sorry, something went wrong. Please try again.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        },
      ]);
    } finally {
      setLoading(false);
    }
  };
  
  const handlePromptClick = (prompt) => {
    handleSend(prompt);
  };
  
  const handleNewChat = () => {
      setChatHistory([]);
  }

  return (
    <div className="App">
      <aside className="sidebar">
          <div className="sidebar-header">
            <img src={logo} alt="SageSure Logo" className="logo" />
            <h1>HR Assistant</h1>
          </div>
          <button className="new-chat-button" onClick={handleNewChat}>
              <PlusIcon />
              New Chat
          </button>
          <ul className="chat-history-list">
              {chatHistory.length > 0 && <li className="chat-history-item">Current Conversation</li>}
          </ul>
      </aside>

      <main className="chat-area">
        {chatHistory.length === 0 ? (
          <div className="welcome-container">
              <img src={logo} alt="SageSure Logo" className="welcome-logo" />
              <h2>How can I help you today?</h2>
              <p>Ask me anything about our company policies and procedures.</p>
              <div className="example-prompts-grid">
                  {EXAMPLE_PROMPTS.map(prompt => (
                      <div key={prompt.title} className="prompt-card" onClick={() => handlePromptClick(prompt.question)}>
                          <h3>{prompt.title}</h3>
                          <p>{prompt.question}</p>
                      </div>
                  ))}
              </div>
          </div>
        ) : (
          <div className="chat-container" ref={chatContainerRef}>
            {chatHistory.map((chat) => (
              <div key={chat.id} className={`chat-message ${chat.type}-message`}>
                  <div className="avatar">
                      {chat.type === 'bot' ? <BotAvatar logo={botLogo} /> : <UserAvatar />}
                  </div>
                  <div className="message-details">
                    <div className="message-bubble">{chat.message}</div>
                    <div className="message-timestamp">{chat.timestamp}</div>
                  </div>
              </div>
            ))}
            {loading && (
                <div className="chat-message bot-message">
                    <div className="avatar"><BotAvatar logo={botLogo}/></div>
                    <div className="message-details">
                        <div className="message-bubble">
                            <div className="typing-indicator"><span></span><span></span><span></span></div>
                        </div>
                    </div>
                </div>
            )}
          </div>
        )}
        
        <div className="input-area">
          <div className="input-wrapper">
            <input
              type="text"
              placeholder="Ask a follow-up, or start a new conversation..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSend(question)}
            />
            <button className="send-button" onClick={() => handleSend(question)}>
                <SendIcon />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
