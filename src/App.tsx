import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [isRecording, setIsRecording] = useState(false)
  const [transcription, setTranscription] = useState("")
  const ws = useRef<WebSocket | null>(null)
  
  useEffect(() => {
    // Connect to WebSocket backend
    ws.current = new WebSocket("ws://localhost:8000/ws/audio")
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === "transcription_update") {
        setTranscription(prev => prev + " " + data.content)
      }
    }
    
    return () => {
      ws.current?.close()
    }
  }, [])

  const handleRecordClick = () => {
    // In Tauri, this will be handled by Rust layer for real low-level access.
    // For now, we mock the UI state
    setIsRecording(!isRecording)
    
    if (!isRecording && ws.current && ws.current.readyState === WebSocket.OPEN) {
       // Mock sending some data to trigger the backend simulation
       ws.current.send(new Uint8Array([1, 2, 3, 4]))
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-neutral-100 dark:bg-neutral-900 text-neutral-900 dark:text-neutral-100 p-4">
      <h1 className="text-3xl font-bold mb-8 opacity-80">Menura</h1>
      
      <div className="w-full max-w-2xl bg-white dark:bg-neutral-800 rounded-2xl shadow-sm p-6 min-h-[400px] mb-8 relative">
        <p className="text-lg leading-relaxed whitespace-pre-wrap">
          {transcription || <span className="opacity-40 italic">Pulsa el botón para hablar con tu secretaria...</span>}
        </p>
        
        {isRecording && (
          <div className="absolute top-4 right-4 flex items-center gap-2">
            <span className="animate-pulse h-3 w-3 rounded-full bg-red-500"></span>
            <span className="text-sm opacity-60">Escuchando</span>
          </div>
        )}
      </div>
      
      <button 
        onClick={handleRecordClick}
        className={`w-16 h-16 rounded-full flex items-center justify-center transition-all ${
          isRecording 
            ? 'bg-red-500 hover:bg-red-600 scale-110 shadow-lg shadow-red-500/30' 
            : 'bg-neutral-800 dark:bg-white text-white dark:text-neutral-900 hover:scale-105 shadow-md'
        }`}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinelinejoin="round">
          {isRecording ? (
            <rect x="6" y="6" width="12" height="12" rx="2" ry="2" />
          ) : (
            <>
              <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
              <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
              <line x1="12" x2="12" y1="19" y2="22" />
            </>
          )}
        </svg>
      </button>
    </div>
  )
}

export default App
