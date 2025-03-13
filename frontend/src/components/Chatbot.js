import { useState, useEffect, useRef } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "" } // 🔥 Üresen indul, hogy streamelni tudjuk az első üzenetet
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [followUpQuestions, setFollowUpQuestions] = useState([
    "Why should I hire Kolos?",
    "What are Kolos's biggest achievements?",
    "What is Kolos's educational background?"
  ]);
  const messagesEndRef = useRef(null);
  const [isStreaming, setIsStreaming] = useState(false); // 🔥 Új állapot a stream figyelésére

  const streamText = async (fullText, callback) => {
    let displayedText = "";
    const words = fullText.split(" ");

    setIsStreaming(true); // 🔥 Streamelés elindul
    for (let i = 0; i < words.length; i++) {
      displayedText += words[i] + " ";
      callback(displayedText);
      await new Promise(resolve => setTimeout(resolve, 30)); // 🔥 Streamelési sebesség (30ms szóként)
    }
    setIsStreaming(false); // 🔥 Streamelés vége
  };

  // 🔹 Az üdvözlő üzenet is streamelve jelenik meg
  useEffect(() => {
    const welcomeMessage =
      "Hi! I'm KAI, Kolos's AI-powered assistant. I specialize in answering questions about Kolos' professional background, achievements, and experience. How can I assist you today?";

    streamText(welcomeMessage, (text) => {
      setMessages([{ sender: "bot", text }]);
    });
  }, []);

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    setMessages(prev => [...prev, { sender: "user", text: messageText }]);
    setInput("");
    setLoading(true);
    setFollowUpQuestions([]); // 🔥 Előző follow-up kérdések törlése

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: messageText }),
      });

      const data = await response.json();
      const fullResponse = data.response; // 🔥 Backend teljes válasz

      // 🔹 Üres bot válasz inicializálása a stream kezdése előtt
      setMessages(prev => [...prev, { sender: "bot", text: "" }]);

      await streamText(fullResponse, (text) => {
        setMessages(prev => {
          const updatedMessages = [...prev];
          updatedMessages[updatedMessages.length - 1] = { sender: "bot", text };
          return updatedMessages;
        });
      });

      // 📌 Suggested Questions csak a stream végén jelenik meg
      setTimeout(() => {
        setFollowUpQuestions(data.follow_up_questions.slice(0, 3));
      }, 500); // Késleltetés a smooth megjelenítés érdekében

    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [...prev, { sender: "bot", text: "Error retrieving response." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-100 p-6">
      <div className="bg-white shadow-xl rounded-lg w-full max-w-[85vw] p-8 h-[90vh] flex flex-col mx-auto">
        <ChatHeader />
        <ChatMessages
          messages={messages}
          loading={loading}
          isStreaming={isStreaming} // 🔥 Ezt továbbadjuk a ChatMessages-nek
          messagesEndRef={messagesEndRef}
          followUpQuestions={followUpQuestions}
          sendMessage={sendMessage}
        />
        <ChatInput input={input} setInput={setInput} sendMessage={sendMessage} />
      </div>
    </div>
  );
}

