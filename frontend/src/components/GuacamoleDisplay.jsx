// src/components/GuacamoleDisplay.jsx
const GuacamoleDisplay = ({ connectionToken }) => {
  // L'URL pointe vers ton service Guacamole géré par Docker
  const guacUrl = `http://localhost:8088/guacamole/#/client/${connectionToken}`;

  return (
    <div className="w-full h-[80vh] border-2 border-gray-800 rounded-lg overflow-hidden">
      <iframe
        src={guacUrl}
        width="100%"
        height="100%"
        title="VM Display"
        allowFullScreen
      />
    </div>
  );
};

export default GuacamoleDisplay;