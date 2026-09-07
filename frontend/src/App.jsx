import { useState } from "react";
import "./App.css";

function App() {
  const [scene, setScene] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!scene.trim() || loading) {
      return;
    }

    const userScene = scene;

    // Show user's message immediately
    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: userScene,
      },
    ]);

    // Clear input
    setScene("");

    // Show loading state
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            scene: userScene,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Something went wrong."
        );
      }

      // Add AI response
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: data.final_plan,
        },
      ]);

    } catch (error) {

      // Show error in chat
      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: `Error: ${error.message}`,
        },
      ]);

    } finally {
      setLoading(false);
    }
  };


  // Allow Enter to send
  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      handleSend();
    }
  };


  return (
    <div className="app">

      {/* =================================
          HEADER
      ================================= */}

      <header className="header">

        <div className="logo">
          🎬
        </div>

        <div>
          <h1>Camera Shot Planner</h1>

          <p>
            AI-powered cinematography assistant
          </p>
        </div>

      </header>


      {/* =================================
          CHAT AREA
      ================================= */}

      <main className="chat-container">

        {/* Welcome Screen */}

        {messages.length === 0 && (

          <div className="welcome">

            <div className="welcome-icon">
              🎥
            </div>

            <h2>
              Camera Shot Planner
            </h2>

            <p>
              Describe your scene and I'll create
              a cinematographic shot plan for you.
            </p>

          </div>

        )}


        {/* Messages */}

        <div className="messages">

          {messages.map((message, index) => (

            <div
              key={index}
              className={`message ${
                message.role === "user"
                  ? "user-message"
                  : "assistant-message"
              }`}
            >

              <div className="message-avatar">

                {message.role === "user"
                  ? "👤"
                  : "🎬"}

              </div>


              <div className="message-content">

                <div className="message-name">

                  {message.role === "user"
                    ? "You"
                    : "Camera Agent"}

                </div>


                <div className="message-text">

                  {message.content}

                </div>

              </div>

            </div>

          ))}


          {/* Loading message */}

          {loading && (

            <div className="message assistant-message">

              <div className="message-avatar">
                🎬
              </div>

              <div className="message-content">

                <div className="message-name">
                  Camera Agent
                </div>

                <div className="message-text">
                  Creating your camera shot plan...
                </div>

              </div>

            </div>

          )}

        </div>

      </main>


      {/* =================================
          INPUT
      ================================= */}

      <div className="input-container">

        <div className="input-box">

          <textarea
            value={scene}
            onChange={(event) =>
              setScene(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Describe your scene..."
            rows="1"
            disabled={loading}
          />


          <button
            onClick={handleSend}
            disabled={loading || !scene.trim()}
          >
            {loading ? "..." : "Send"}
          </button>

        </div>


        <p className="input-note">
          Camera Shot Planner can make cinematography
          recommendations.
        </p>

      </div>

    </div>
  );
}

export default App;