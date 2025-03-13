export default function ChatHeader() {
  return (
    <div className="text-center mb-4"> {/* 🔹 Csökkentett bottom margin */}
      <h1 className="text-2xl font-bold font-serif">KOLOS TAKÁCS, CEMS MIM, MSC</h1>
      <p className="text-base text-gray-600 font-medium">
        Generative AI Product Manager | Data Scientist | Financial Analyst
      </p>
      <p className="text-xs text-gray-500 mt-1">
        📧 kolos.takacs75@gmail.com • 🌍{" "}
        <a
          href="https://www.linkedin.com/in/kolos-takacs-214257257"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 underline"
        >
          LinkedIn Profile
        </a>
      </p>
    </div>
  );
}



