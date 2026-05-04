import { useState, useEffect } from 'react'
import { invoke } from '@tauri-apps/api/core'
import { listen } from '@tauri-apps/api/event'
import './App.css'

function App() {
  const [isRecording, setIsRecording] = useState(false)
  const [transcription, setTranscription] = useState("")

  useEffect(() => {
    // Inicializar motores IA locales
    invoke('init_ai_engine')
      .then((res) => console.log(res))
      .catch(console.error)

    // Escuchar actualizaciones de transcripción desde Rust
    const unlisten = listen<string>('transcription_update', (event) => {
      setTranscription(prev => prev + " " + event.payload)
    })

    return () => {
      unlisten.then(f => f())
    }
  }, [])

  const handleRecordClick = async () => {
    try {
      const recordingState = await invoke<boolean>('toggle_recording')
      setIsRecording(recordingState)
    } catch (e) {
      console.error("Failed to toggle recording:", e)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-neutral-100 dark:bg-neutral-900 text-neutral-900 dark:text-neutral-100 p-4">
      <h1 className="text-3xl font-bold mb-8 opacity-80 tracking-widest">Menura</h1>
      
      <div className="w-full max-w-2xl bg-white dark:bg-neutral-800 rounded-3xl shadow-sm p-8 min-h-[400px] mb-8 relative border border-neutral-200 dark:border-neutral-700">
        <p className="text-lg leading-relaxed whitespace-pre-wrap font-medium">
          {transcription || <span className="opacity-30 italic">Púlsame para hablar con tu memoria...</span>}
        </p>
        
        {isRecording && (
          <div className="absolute top-6 right-6 flex items-center gap-3">
            <span className="animate-pulse h-3 w-3 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.7)]"></span>
            <span className="text-sm font-semibold opacity-60 tracking-wider uppercase">ESCUCHANDO</span>
          </div>
        )}
      </div>
      
      <button 
        onClick={handleRecordClick}
        className={`w-20 h-20 rounded-full flex items-center justify-center transition-all duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)] ${
          isRecording 
            ? 'bg-red-500 hover:bg-red-600 scale-110 shadow-[0_10px_30px_rgba(239,68,68,0.4)]' 
            : 'bg-neutral-800 dark:bg-white text-white dark:text-neutral-900 hover:scale-105 shadow-xl hover:shadow-2xl'
        }`}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
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
