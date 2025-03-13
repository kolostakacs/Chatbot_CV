import { Loader, MessageSquare } from "lucide-react";

export default function ChatMessages({ messages, loading, messagesEndRef, followUpQuestions, sendMessage }) {
  return (
    <div className="flex-grow overflow-y-auto p-6 border rounded-2xl bg-gray-50 flex flex-col">
      {messages.map((msg, index) => (
        <div key={index} className={`mb-2 p-3 rounded-2xl max-w-3xl ${
          msg.sender === "user"
            ? "bg-blue-500 text-white self-end ml-auto"
            : "bg-gray-200 text-black"
        }`}>
          {msg.text}

          {/* 🔹 Ha ez az utolsó chatbot válasz, akkor itt jelenjen meg a Suggested Questions */}
          {msg.sender === "bot" && index === messages.length - 1 && followUpQuestions.length > 0 && (
            <div className="mt-2 text-sm italic text-gray-600">
              Suggested questions:
              <div className="flex flex-wrap mt-2 gap-2">
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
        </div>
      ))}

      {loading && (
        <div className="mb-2 p-3 rounded-2xl bg-gray-200 text-black max-w-3xl self-start flex items-center">
          <Loader className="animate-spin mr-2" size={18} /> Typing...
        </div>
      )}

      {/* 🔹 Görgetés az utolsó üzenetre */}
      <div ref={messagesEndRef} />
    </div>
  );
}


