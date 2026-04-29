import { useEffect, useRef, useState } from "react";
import "./ChatWidget.css";

const API_URL =
  import.meta.env.VITE_CHATBOT_API_URL || "http://127.0.0.1:8000/chat";

const quickActions = [
  "Hijama suction gun under 300",
  "Best derma pen",
  "Massage tools suggest karo",
  "Clinic gloves chahiye",
  "Contact support",
];

function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Hi 👋 Welcome to ShopeIndia!\nI can help you find Hijama, Derma, Massage, Therapy, and Beauty products.",
      products: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 200);
    }
  }, [isOpen]);

  function scrollToBottom() {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  async function sendMessage(customMessage) {
    const userMessage = customMessage || input.trim();

    if (!userMessage || isTyping) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
        products: [],
      },
    ]);

    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.detail || "Something went wrong");
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text:
            data.reply ||
            "Sorry, mujhe proper answer nahi mila. Please try again.",
          products: data.products || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text:
            "Backend se connect nahi ho pa raha.\nPlease check karo ki server running hai ya nahi.",
          products: [],
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  }

  function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  function renderMessageText(text) {
    return text.split("\n").map((line, index) => (
      <p key={index} className="message-line">
        {line}
      </p>
    ));
  }

  return (
    <>
      {!isOpen && (
        <button
          className="chat-toggle"
          onClick={() => setIsOpen(true)}
          aria-label="Open ShopeIndia chat"
        >
          <span className="chat-toggle-icon">💬</span>
        </button>
      )}

      {isOpen && (
        <section className="chat-widget">
          <header className="chat-header">
            <div className="brand-block">
              <div className="brand-avatar">S</div>

              <div>
                <strong>ShopeIndia Assistant</strong>
                <span>Wellness & Beauty Product Guide</span>
              </div>
            </div>

            <button
              className="chat-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ×
            </button>
          </header>

          <main className="chat-messages">
            {messages.map((message, index) => (
              <div
                key={index}
                className={
                  message.role === "user"
                    ? "message-row user-row"
                    : "message-row bot-row"
                }
              >
                {message.role === "bot" && (
                  <div className="small-avatar">S</div>
                )}

                <div className="message-content">
                  <div
                    className={
                      message.role === "user" ? "user-message" : "bot-message"
                    }
                  >
                    {renderMessageText(message.text)}
                  </div>

                  {message.products?.length > 0 && (
                    <div className="product-list">
                      {message.products.map((product) => (
                        <article className="product-card" key={product.id}>
                          <div className="product-top">
                            <div>
                              <h4>{product.name}</h4>
                              <p>{product.category}</p>
                            </div>

                            {product.discount && (
                              <span className="discount-badge">
                                {product.discount}
                              </span>
                            )}
                          </div>

                          <div className="product-price">
                            <strong>₹{product.price}</strong>

                            {product.old_price && (
                              <span>₹{product.old_price}</span>
                            )}

                            {product.rating && (
                              <small>⭐ {product.rating}</small>
                            )}
                          </div>

                          {product.product_url && (
                            <a
                              href={product.product_url}
                              target="_blank"
                              rel="noreferrer"
                              className="product-link"
                            >
                              View Product →
                            </a>
                          )}
                        </article>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {messages.length === 1 && (
              <div className="quick-actions">
                {quickActions.map((action) => (
                  <button key={action} onClick={() => sendMessage(action)}>
                    {action}
                  </button>
                ))}
              </div>
            )}

            {isTyping && (
              <div className="message-row bot-row">
                <div className="small-avatar">S</div>

                <div className="typing-bubble">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </main>

          <footer className="chat-footer">
            <div className="chat-input-area">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(event) => setInput(event.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about products..."
                rows={1}
              />

              <button
                onClick={() => sendMessage()}
                disabled={isTyping || !input.trim()}
              >
                Send
              </button>
            </div>

            <div className="built-by">Built by Sanu Sharma</div>
          </footer>
        </section>
      )}
    </>
  );
}

export default ChatWidget;