import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {

  // =========================
  // STATES
  // =========================

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const [showMenu, setShowMenu] = useState(false);

  // =========================
  // CHAT HISTORY
  // =========================

  const [chatHistory, setChatHistory] = useState([
    {
      id: 1,
      title: "New Chat",
      messages: [],
    },
  ]);

  const [activeChatId, setActiveChatId] = useState(1);

  // =========================
  // AUTO SCROLL
  // =========================

  const chatEndRef = useRef(null);

  useEffect(() => {

    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages]);

  // =========================
  // IMAGE UPLOAD
  // =========================

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

  // =========================
  // FILE UPLOAD
  // =========================

  const handleFileUpload = (e) => {

    const file = e.target.files[0];

    if (file) {

      setSelectedFile(file);

      setMessages((prev) => [
        ...prev,
        {
          role: "user",
          text: `📄 File Uploaded: ${file.name}`,
        },
      ]);
    }
  };

  // =========================
  // NEW CHAT
  // =========================

  const createNewChat = () => {

    const newChat = {
      id: Date.now(),
      title: "New Chat",
      messages: [],
    };

    setChatHistory((prev) => [
      newChat,
      ...prev,
    ]);

    setActiveChatId(newChat.id);

    setMessages([]);
  };

  // =========================
  // SWITCH CHAT
  // =========================

  const switchChat = (chat) => {

    setActiveChatId(chat.id);

    setMessages(chat.messages);
  };

  // =========================
  // SEND MESSAGE
  // =========================

  const sendMessage = async () => {

    if (
      !input.trim() &&
      !selectedImage &&
      !selectedFile
    ) {
      return;
    }

    let userMessage = input.trim();

    if (!userMessage && selectedImage) {
      userMessage = "Analyze uploaded image";
    }

    if (!userMessage && selectedFile) {
      userMessage = "Analyze uploaded file";
    }

    // =========================
    // USER MESSAGE
    // =========================

    const updatedMessages = [
      ...messages,
      {
        role: "user",
        text: userMessage,
      },
    ];

    setMessages(updatedMessages);

    // =========================
    // UPDATE SIDEBAR
    // =========================

    setChatHistory((prev) =>
      prev.map((chat) =>
        chat.id === activeChatId
          ? {
              ...chat,
              title:
                userMessage.slice(0, 20) ||
                "New Chat",
              messages: updatedMessages,
            }
          : chat
      )
    );

    setInput("");
    setLoading(true);

    try {

      // =========================
      // FORMDATA
      // =========================

      const formData = new FormData();

      formData.append(
        "question",
        userMessage
      );

      if (selectedImage) {

        formData.append(
          "image",
          selectedImage
        );
      }

      if (selectedFile) {

        formData.append(
          "audio",
          selectedFile
        );
      }

      // =========================
      // API CALL
      // =========================

      const res = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await res.json();

      // =========================
      // AI MESSAGE
      // =========================

      const aiMessages = [
        ...updatedMessages,
        {
          role: "ai",
          text:
            data.answer ||
            "No response from AI",
        },
      ];

      setMessages(aiMessages);

      // =========================
      // UPDATE CHAT HISTORY
      // =========================

      setChatHistory((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? {
                ...chat,
                messages: aiMessages,
              }
            : chat
        )
      );

      // =========================
      // CLEAR FILES
      // =========================

      setSelectedImage(null);
      setSelectedFile(null);

    } catch (err) {

      console.error(err);

      const errorMessages = [
        ...updatedMessages,
        {
          role: "ai",
          text:
            "Backend connection failed",
        },
      ];

      setMessages(errorMessages);

      setChatHistory((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? {
                ...chat,
                messages: errorMessages,
              }
            : chat
        )
      );
    }

    setLoading(false);
  };

  // =========================
  // UI
  // =========================

  return (

    <div className="app">

      {/* =========================
          SIDEBAR
      ========================= */}

      <div className="sidebar">

        <div className="sidebar-top">

          <h2>AI Tax</h2>

          <button
            className="new-chat-btn"
            onClick={createNewChat}
          >
            + New Chat
          </button>

        </div>

        <div className="history">

          {chatHistory.map((chat) => (

            <div
              key={chat.id}
              className={`history-item ${
                activeChatId === chat.id
                  ? "active-history"
                  : ""
              }`}
              onClick={() =>
                switchChat(chat)
              }
            >
              {chat.title}
            </div>

          ))}

        </div>

      </div>

      {/* =========================
          MAIN AREA
      ========================= */}

      <div className="main">

        {/* TOP BAR */}

        <div className="top-bar">

          AI Tax Assistant

        </div>

        {/* CHAT AREA */}

        <div className="chat-area">

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

          <div ref={chatEndRef} />

        </div>

        {/* =========================
            BOTTOM BAR
        ========================= */}

        <div className="bottom-bar">

          {/* POPUP MENU */}

          {showMenu && (

            <div className="upload-popup">

              {/* CAMERA */}

              <label className="popup-item">

                📷 Camera

                <input
                  type="file"
                  accept="image/*"
                  capture="environment"
                  hidden
                  onChange={handleImageUpload}
                />

              </label>

              {/* PHOTOS */}

              <label className="popup-item">

                🖼 Photos

                <input
                  type="file"
                  accept="image/*"
                  hidden
                  onChange={handleImageUpload}
                />

              </label>

              {/* FILES */}

              <label className="popup-item">

                📄 Files

                <input
                  type="file"
                  hidden
                  onChange={handleFileUpload}
                />

              </label>

            </div>
          )}

          {/* INPUT BAR */}

          <div className="input-wrapper">

            {/* PLUS BUTTON */}

            <button
              className="plus-btn"
              onClick={() =>
                setShowMenu(!showMenu)
              }
            >
              +
            </button>

            {/* INPUT */}

            <input
              className="chat-input"
              value={input}
              onChange={(e) =>
                setInput(e.target.value)
              }
              placeholder="Ask anything"
              onKeyDown={(e) =>
                e.key === "Enter" &&
                sendMessage()
              }
            />

            {/* SEND */}

            <button
              className="send-btn"
              onClick={sendMessage}
            >
              Send
            </button>

          </div>

          {/* FILE PREVIEW */}

          {selectedImage && (

            <div className="file-preview">

              📷 {selectedImage.name}

            </div>
          )}

          {selectedFile && (

            <div className="file-preview">

              📄 {selectedFile.name}

            </div>
          )}

        </div>

      </div>

    </div>
  );
}

export default App;