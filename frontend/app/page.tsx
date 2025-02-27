"use client";
import { useEffect, useState } from "react";
import io from "socket.io-client";

const Index = () => {
  const [text, setText] = useState("");
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");
  const [result, setResult] = useState<any | null>(null);
  const [socket, setSocket] = useState<any>(null);

  useEffect(() => {
    // Conectando ao WebSocket
    const socketConnection = io("http://localhost:5000", {
      transports: ["websocket"],
    });
    setSocket(socketConnection);

    // Ouvindo o evento de status
    socketConnection.on(
      "status",
      (data: { job_id: string; status: string }) => {
        if (data.job_id === jobId) {
          setStatus(data.status);
        }
      }
    );

    // Ouvindo o evento de resultado
    socketConnection.on("result", (data: { job_id: string; result: any }) => {
      if (data.job_id === jobId) {
        setResult(data.result);
        setStatus("Resultado: Processado!");
      }
    });

    // Cleanup (fechando a conexão WebSocket quando o componente for desmontado)
    return () => {
      socketConnection.disconnect();
    };
  }, [jobId]); // Dependência no jobId para reconectar com o job correto

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setJobId(data.job_id);
    setStatus("Job enviado. Aguardando resultado...");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="max-w-xl w-full bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-3xl font-bold text-center mb-4">
          Demo de Mensageria
        </h1>
        <form onSubmit={handleSubmit}>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Digite seu texto aqui"
            rows={5}
            className="w-full p-2 border border-gray-300 rounded-md mb-4"
          />
          <br />
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600"
          >
            Enviar
          </button>
        </form>
        <div className="mt-4">
          {jobId && <p className="text-gray-700">Job ID: {jobId}</p>}
          <p className="text-gray-700">{status}</p>
          {result && (
            <pre className="bg-gray-200 p-4 rounded-md mt-2">
              {JSON.stringify(result, null, 2)}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
};

export default Index;

