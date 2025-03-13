import { useEffect } from "react";
import { Loader, MessageSquare } from "lucide-react";
import ReactMarkdown from "react-markdown"; // 🔥 Markdown támogatás

export default function ChatMessages({ messages, loading, isStreaming, messagesEndRef, followUpQuestions, sendMessage }) {

  useEffect(() => {
    const scrollToBottom = () => {
      if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
      }
    };

    // 🔹 Késleltetés a teljes render után (üzenetek + follow-up kérdések)
    const timeout = setTimeout(scrollToBottom, 200);
    return () => clearTimeout(timeout);
  }, [messages, followUpQuestions, messagesEndRef]);

  return (
    <div className="flex-grow overflow-y-auto p-6 border rounded-2xl bg-gray-50 flex flex-col">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`flex items-start gap-3 mb-4 ${
            msg.sender === "user" ? "justify-end" : "justify-start"
          }`}
        >
          {/* 🔹 Chatbot ikon csak a bot válaszaihoz */}
          {msg.sender === "bot" && (
            <img
              src="/logo.jpg"
              alt="Chatbot Icon"
              className="w-10 h-10 rounded-full self-start"
            />
          )}

          {/* 🔹 Üzenet buborék */}
          <div className={`p-3 rounded-2xl max-w-[70%] ${
            msg.sender === "user"
              ? "bg-blue-500 text-white self-end ml-auto max-w-[60%]"
              : "bg-gray-200 text-black"
          }`}>
            <ReactMarkdown>{msg.text}</ReactMarkdown>
          </div>
        </div>
      ))}

      {/* 🔥 Most már nem "Typing...", hanem "Relevant Document Extraction in Progress..." */}
      {loading && !isStreaming && (
        <div className="mb-2 p-3 rounded-2xl bg-gray-200 text-black max-w-[70%] self-start flex items-center">
          <Loader className="animate-spin mr-2" size={18} /> Relevant Document Extraction in Progress...
        </div>
      )}

      {/* 🔹 Suggested Questions középre igazítva és késleltetve jelenik meg */}
      {followUpQuestions.length > 0 && !loading && !isStreaming && (
        <div className="mt-4 text-sm italic text-gray-600 text-center">
          Suggested questions:
          <div className="flex flex-wrap justify-center mt-2 gap-2">
            {followUpQuestions.map((question, i) => (
              <button
                key={i}
                className="flex items-center gap-2 bg-gray-100 border border-gray-300 hover:bg-gray-200 text-gray-700 font-semibold px-4 py-2 rounded-xl transition text-sm"
                onClick={() => sendMessage(question)}
              >
                <MessageSquare size={16} /> {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* 🔹 Görgetés az utolsó üzenetre */}
      <div ref={messagesEndRef} />
    </div>
  );
}


