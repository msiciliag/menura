import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.services.audio_service import AudioProcessor

app = FastAPI(
    title="Menura Backend",
    description="Motor Inteligente para el Asistente Personal Menura 2.0 (GraphRAG Híbrido)",
    version="2.0.0"
)

# Initialize Audio Processor (this is blocking, in production we might lazy-load or use Lifespan events)
audio_processor = AudioProcessor(model_size="tiny", device="cpu", compute_type="int8") # using tiny for faster prototyping without full setup

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
    try:
        while True:
            # Recibimos los bytes de audio crudo (PCM)
            data = await websocket.receive_bytes()
            
            # Procesamos con el motor STT y VAD
            # En un entorno real, esto se haría en un threadpool o worker asíncrono para no bloquear el bucle del WebSocket
            transcription = await asyncio.to_thread(audio_processor.process_audio_chunk, data)
            
            if transcription:
                await websocket.send_json({
                    "type": "transcription_update",
                    "content": transcription,
                    "is_final": True
                })

    except WebSocketDisconnect:
        print("Cliente desconectado del canal de audio.")
    except Exception as e:
        print(f"Error en WebSocket: {e}")
