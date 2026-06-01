import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";

import "./App.css";

function App() {

  // ==============================
  // STATES
  // ==============================

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedAudio, setSelectedAudio] = useState(null);

  // ==============================
  // AUTO SCROLL
  // ==============================

  const chatEndRef = useRef(null);

  useEffect(() => {

    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages]);

  // ==============================
  // IMAGE UPLOAD
  // ==============================

  const handleImageUpload = (e) => {

    const file = e.target.files[0];

    if (file) {

      setSelectedImage(file);

      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          text: `📷 Image Uploaded: ${file.name}`,
        },
      ]);
    }
  };

  // ==============================
  // AUDIO UPLOAD
  // ==============================

  const handleAudioUpload = (e) => {

    const file = e.target.files[0];

    if (file) {

      setSelectedAudio(file);

      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          text: `🎵 Audio Uploaded: ${file.name}`,
        },
      ]);
    }
  };

  // ==============================
  // SEND MESSAGE
  // ==============================

  const sendMessage = async () => {

    // Prevent empty request
    if (
      !input.trim() &&
      !selectedImage &&
      !selectedAudio
    ) {
      return;
    }

    // =====================================
    // AUTO QUESTION FOR IMAGE / AUDIO
    // =====================================

    let userMessage = input.trim();

    if (!userMessage && selectedImage) {
      userMessage = "Analyze uploaded image";
    }

    if (!userMessage && selectedAudio) {
      userMessage = "Analyze uploaded audio";
    }

    // =====================================
    // SHOW USER MESSAGE
    // =====================================

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    // Clear input
    setInput("");

    // Loader
    setLoading(true);

    try {

      // =====================================
      // FORMDATA
      // =====================================

      const formData = new FormData();

      formData.append(
        "question",
        userMessage
      );

      // Add image
      if (selectedImage) {

        formData.append(
          "image",
          selectedImage
        );
      }

      // Add audio
      if (selectedAudio) {

        formData.append(
          "audio",
          selectedAudio
        );
      }

      // =====================================
      // API CALL
      // =====================================

      const res = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          body: formData,
        }
      );

      // =====================================
      // ERROR CHECK
      // =====================================

      if (!res.ok) {

        throw new Error(
          `HTTP Error: ${res.status}`
        );
      }

      // =====================================
      // JSON RESPONSE
      // =====================================

      const data = await res.json();

      console.log(
        "Backend Response:",
        data
      );

      // =====================================
      // AI RESPONSE
      // =====================================

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            data.answer ||
            "No response from AI",
        },
      ]);

      // =====================================
      // CLEAR FILES
      // =====================================

      setSelectedImage(null);
      setSelectedAudio(null);

    } catch (err) {

      console.error(
        "Frontend Error:",
        err
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            "Backend connection failed",
        },
      ]);
    }

    // Stop loader
    setLoading(false);
  };

  // ==============================
  // UI
  // ==============================

  return (

    <div
      className={`container ${
        darkMode ? "dark" : "light"
      }`}
    >

      {/* HEADER */}

      <h2>AI Tax Assistant</h2>

      {/* THEME BUTTON */}

      <button
        className="theme-btn"
        onClick={() =>
          setDarkMode(!darkMode)
        }
      >
        
      </button>

      {/* CHAT BOX */}

      <div className="chat-box">

        {messages.map((msg, i) => (

          <div
            key={i}
            className={`message-row ${
              msg.role === "user"
                ? "user-row"
                : "ai-row"
            }`}
          >

            <div
              className={`message ${
                msg.role === "user"
                  ? "user-message"
                  : "ai-message"
              }`}
            >

              <ReactMarkdown>
                {msg.text}
              </ReactMarkdown>

            </div>

          </div>
        ))}

        {/* LOADING */}

        {loading && (

          <div className="typing">

            <span>.</span>
            <span>.</span>
            <span>.</span>

          </div>
        )}

        {/* AUTO SCROLL */}

        <div ref={chatEndRef} />

      </div>

      {/* INPUT AREA */}

      <div className="input-box">

        {/* IMAGE */}

        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
        />

        {/* AUDIO */}

        <input
          type="file"
          accept="audio/*"
          onChange={handleAudioUpload}
        />

        {/* IMAGE NAME */}

        {selectedImage && (

          <p className="image-name">
            📷 {selectedImage.name}
          </p>
        )}

        {/* AUDIO NAME */}

        {selectedAudio && (

          <p className="audio-name">
            🎵 {selectedAudio.name}
          </p>
        )}

        {/* TEXT INPUT */}

        <input
          value={input}
          onChange={(e) =>
            setInput(e.target.value)
          }
          placeholder="Ask something..."
          onKeyDown={(e) =>
            e.key === "Enter" &&
            sendMessage()
          }
        />

        {/* SEND */}

        <button onClick={sendMessage}>
          Send
        </button>

      </div>

    </div>
  );
}

export default App;