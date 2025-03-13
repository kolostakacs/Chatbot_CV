import { Send } from "lucide-react";

export default function ChatInput({ input, setInput, sendMessage }) {
  return (
    <div className="flex items-center mt-4 border-t pt-4">
      <input
        type="text"
        className="flex-grow border rounded-2xl p-3 focus:outline-none focus:ring focus:border-blue-300"
        placeholder="Type a message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
      />
      <button
        onClick={() => sendMessage(input)}
        className="ml-2 bg-blue-500 hover:bg-blue-600 text-white p-3 rounded-2xl flex items-center"
        disabled={!input.trim()}
      >
        <Send size={20} />
      </button>
    </div>
  );
}
