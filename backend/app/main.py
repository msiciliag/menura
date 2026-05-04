import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.services.audio_service import AudioProcessor
from app.services.llm_service import LLMService
from app.services.zettelkasten_service import ZettelkastenService
from app.services.vector_db_service import VectorDBService
from app.services.graph_db_service import GraphDBService
from app.core.agents.librarian import LibrarianAgent

app = FastAPI(
    title="Menura Backend",
    description="Motor Inteligente para el Asistente Personal Menura 2.0 (GraphRAG Híbrido)",
    version="2.0.0"
)

# Servicios Base
llm_service = LLMService(model="gemma2") # or "gemma:2b" depending on local ollama tags
zk_service = ZettelkastenService()
vector_db = VectorDBService()
graph_db = GraphDBService()

# Agentes
librarian_agent = LibrarianAgent(llm_service, zk_service, vector_db, graph_db)

# Audio Processor
audio_processor = AudioProcessor(model_size="tiny", device="cpu", compute_type="int8")

# Permitir conexiones desde Tauri y otros orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Menura 2.0 Backend en funcionamiento. El cerebro está activo."}

@app.get("/api/status")
async def status():
    # En el futuro, comprobaremos el estado de la conexión a LanceDB, KuzuDB, y el motor STT/LLM
    return {
        "status": "ok",
        "services": {
            "vad_silero": "pending_init",
            "stt_whisper": "pending_init",
            "llm_gemma": "pending_init",
            "vector_db_lance": "pending_init",
            "graph_db_kuzu": "pending_init"
        }
    }

@app.websocket("/ws/audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    """
    Endpoint principal de ingesta de audio.
    Recibe un stream continuo de PCM 16-bit 16kHz mono del cliente, aplica VAD (Voice Activity Detection),
    transcribe con Faster-Whisper, y devuelve texto parcial/final.
    """
    await websocket.accept()
    print("Nuevo cliente conectado al canal de ingesta de audio.")
    
    # Acumulador de transcripciones de una sesión para el Bibliotecario
    session_transcription = ""
    
    try:
        while True:
            # Recibimos los bytes de audio crudo (PCM)
            data = await websocket.receive_bytes()
            
            # En un protocolo real, el cliente enviará una señal de finalización de grabación
            # Para este MVP, si nos envían un byte específico (ej. b"END"), cerramos sesión
            if data == b"END":
                if session_transcription:
                    # Tarea en background para no bloquear: El Bibliotecario procesa todo lo que se habló
                    print("[WebSocket] Fin de grabación detectado. Invocando al Bibliotecario...")
                    asyncio.create_task(librarian_agent.process_transcription(session_transcription))
                    session_transcription = ""
                continue
            
            # Procesamos con el motor STT y VAD
            transcription = await asyncio.to_thread(audio_processor.process_audio_chunk, data)
            
            if transcription:
                session_transcription += transcription + " "
                await websocket.send_json({
                    "type": "transcription_update",
                    "content": transcription,
                    "is_final": True
                })

    except WebSocketDisconnect:
        print("Cliente desconectado del canal de audio.")
        if session_transcription:
            print("[WebSocket] Desconexión. Invocando al Bibliotecario para el texto remanente...")
            asyncio.create_task(librarian_agent.process_transcription(session_transcription))
            
    except Exception as e:
        print(f"Error en WebSocket: {e}")
