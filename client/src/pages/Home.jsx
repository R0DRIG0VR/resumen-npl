"use client";

import React, { useState } from "react";
import {
  Copy,
  FileText,
  Upload,
  Loader2,
  Type,
  AlignJustify,
  BarChart2,
  Shuffle,
  TrendingUp,
  CheckCircle,
} from "lucide-react";

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [summaryLevel, setSummaryLevel] = useState(50);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("text");
  const [toast, setToast] = useState(null);

  const showToast = (title, description, variant = "default") => {
    setToast({ title, description, variant });
    setTimeout(() => setToast(null), 3000);
  };

  const handleTextSummarize = async () => {
    if (!inputText.trim()) {
      showToast("Error", "Por favor ingresa texto para resumir", "destructive");
      return;
    }
    setIsLoading(true);
    try {
      const res = await fetch("/api/summarize-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText, level: summaryLevel }),
      });
      if (!res.ok) throw new Error();
      setResult(await res.json());
    } catch {
      showToast("Error", "Error al resumir el texto.", "destructive");
    } finally {
      setIsLoading(false);
    }
  };

  const handlePdfSummarize = async (file) => {
    setIsLoading(true);
    try {
      const form = new FormData();
      form.append("pdf", file);
      form.append("level", summaryLevel.toString());
      const res = await fetch("/api/summarize-pdf", { method: "POST", body: form });
      if (!res.ok) throw new Error();
      setResult(await res.json());
    } catch {
      showToast("Error", "Error al resumir el PDF.", "destructive");
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      showToast("¡Copiado!", "Resumen copiado al portapapeles");
    } catch {
      showToast("Error", "Error al copiar al portapapeles", "destructive");
    }
  };

  const steps = [
    { icon: <Type className="w-5 h-5" />, title: "Tokens Limpios", text: "Se eliminan puntuación y caracteres no alfabéticos, dejando solo palabras en minúscula." },
    { icon: <AlignJustify className="w-5 h-5" />, title: "Oraciones Segmentadas", text: "Se divide el texto en oraciones para analizarlas individualmente." },
    { icon: <BarChart2 className="w-5 h-5" />, title: "TF-IDF por Oración", text: "Cada oración se vectoriza con TF-IDF para identificar términos representativos." },
    { icon: <Shuffle className="w-5 h-5" />, title: "Selección MMR", text: "Se eligen oraciones maximizando relevancia y diversidad (fórmula MMR)." },
    { icon: <TrendingUp className="w-5 h-5" />, title: "Puntuaciones MMR", text: "Se muestran los puntajes que obtuvo cada oración durante MMR." },
    { icon: <CheckCircle className="w-5 h-5" />, title: "Resumen Final", text: "Las oraciones seleccionadas se unen para formar un resumen coherente y conciso." },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4">
      {/* Toast */}
      {toast && (
        <div
          className={`fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg ${
            toast.variant === "destructive" ? "bg-red-500 text-white" : "bg-green-500 text-white"
          }`}
        >
          <div className="font-medium">{toast.title}</div>
          <div className="text-sm opacity-90">{toast.description}</div>
        </div>
      )}

      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-3">
          <h1 className="text-5xl font-light text-gray-800 tracking-tight">Resumidor de Textos</h1>
          <p className="text-xl text-gray-600 font-light">
            Resume textos y PDFs con niveles de compresión personalizables
          </p>
          <div className="w-24 h-1 bg-gradient-to-r from-gray-400 to-gray-600 mx-auto rounded-full" />
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input */}
          <div className="rounded-lg overflow-hidden shadow-xl bg-white/70 backdrop-blur-sm">
            <div className="bg-gradient-to-r from-gray-800 to-gray-700 text-white p-6 flex items-center gap-2">
              <FileText className="w-6 h-6" /> <span className="text-xl font-light">Entrada</span>
            </div>
            <div className="p-8 space-y-8">
              {/* Slider */}
              <div className="space-y-2">
                <label className="block text-gray-700 font-medium">Nivel de Resumen: {summaryLevel}%</label>
                <input
                  type="range"
                  min="10"
                  max="100"
                  step="5"
                  value={summaryLevel}
                  onChange={(e) => setSummaryLevel(+e.target.value)}
                  className="w-full h-2 bg-gray-200 rounded-lg cursor-pointer"
                />
                <div className="flex justify-between text-sm text-gray-500">
                  <span>Más detallado</span>
                  <span>Más conciso</span>
                </div>
              </div>

              {/* Tabs */}
              <div className="space-y-4">
                <div className="flex bg-gray-100 rounded-lg overflow-hidden">
                  {["text", "pdf"].map((tab) => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`flex-1 py-2 text-center font-medium transition-colors ${
                        activeTab === tab
                          ? "bg-white text-gray-800 shadow-inner"
                          : "text-gray-600 hover:text-gray-800"
                      }`}
                    >
                      {tab === "text" ? "Pegar Texto" : <Upload className="inline w-5 h-5 mr-1" /> && "Subir PDF"}
                    </button>
                  ))}
                </div>

                {activeTab === "text" && (
                  <div className="space-y-4">
                    <textarea
                      className="w-full min-h-[200px] p-4 border border-gray-200 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-300"
                      placeholder="Pega tu texto aquí..."
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                    />
                    <button
                      onClick={handleTextSummarize}
                      disabled={isLoading || !inputText.trim()}
                      className="w-full bg-gray-800 hover:bg-gray-700 disabled:bg-gray-400 text-white py-3 rounded-lg font-medium transition-colors flex justify-center items-center gap-2"
                    >
                      {isLoading ? <Loader2 className="animate-spin w-5 h-5" /> : "Resumir Texto"}
                    </button>
                  </div>
                )}

                {activeTab === "pdf" && (
                  <div className="space-y-4">
                    <label className="block border-2 border-dashed border-gray-300 rounded-xl p-12 text-center cursor-pointer hover:bg-gray-50 transition-colors">
                      <input
                        type="file"
                        accept="application/pdf"
                        className="hidden"
                        onChange={(e) => e.target.files?.[0] && handlePdfSummarize(e.target.files[0])}
                        disabled={isLoading}
                      />
                      <Upload className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                      <div className="text-gray-600">Arrastra tu PDF o haz clic</div>
                      {isLoading && <div className="mt-2 text-gray-500">Procesando...</div>}
                    </label>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Results */}
          <div className="rounded-lg overflow-hidden shadow-xl bg-white/70 backdrop-blur-sm">
            <div className="bg-gradient-to-r from-gray-700 to-gray-600 text-white p-6 flex justify-between items-center">
              <span className="text-xl font-light">Resultados</span>
              {result && (
                <button
                  onClick={() => copyToClipboard(result.summary)}
                  className="flex items-center gap-1 bg-white/20 hover:bg-white/30 px-3 py-1 rounded-md text-sm transition"
                >
                  <Copy className="w-4 h-4" /> Copiar
                </button>
              )}
            </div>
            <div className="p-8 space-y-6">
              {result ? (
                <>
                  <div>
                    <label className="block text-gray-700 font-medium">📄 Resumen Final</label>
                    <div className="mt-2 p-4 bg-gray-50 border border-gray-200 rounded-lg whitespace-pre-wrap">
                      {result.summary}
                    </div>
                  </div>
                  <div>
                    <label className="block text-gray-700 font-medium">🔤 Tokens Limpios</label>
                    <div className="mt-1 text-sm text-gray-600">{result.tokens_limpios.join(", ")}</div>
                  </div>
                </>
              ) : (
                <div className="text-center text-gray-500 py-16">No hay resumen aún</div>
              )}
            </div>
          </div>
        </div>

        {/* Explicación Paso a Paso */}
        <div className="rounded-lg overflow-hidden shadow-xl bg-white/70 backdrop-blur-sm">
          <div className="bg-gradient-to-r from-gray-800 to-gray-700 text-white p-6">
            <span className="text-xl font-light flex items-center gap-2">
              <FileText className="w-6 h-6" /> Explicación del Proceso
            </span>
          </div>
          <div className="p-8 space-y-6">
            {steps.map(({ icon, title, text }, idx) => (
              <div key={idx} className="space-y-2">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center text-gray-700">
                    {icon}
                  </div>
                  <h3 className="text-lg font-medium text-gray-800">{title}</h3>
                </div>
                <p className="ml-11 text-gray-700">{text}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
