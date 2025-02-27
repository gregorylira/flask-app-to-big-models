// app/page.tsx
import { useState } from "react";

const Index = () => {
  const [text, setText] = useState("");
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");
  const [result, setResult] = useState<any | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    setJobId(data.job_id);
    setStatus("Job enviado. Aguardando resultado...");
    startPolling(data.job_id);
  };

  const startPolling = (jobId: string) => {
    const interval = setInterval(async () => {
      const res = await fetch(`http://localhost:5000/api/result/${jobId}`);
      const data = await res.json();
      if (data.result) {
        setResult(data.result);
        setStatus("Resultado: Processado!");
        clearInterval(interval);
      } else if (data.status) {
        setStatus(`Status: ${data.status}`);
      }
    }, 2000);
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
