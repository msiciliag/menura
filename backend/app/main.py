import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Menura Backend",
    description="Motor Inteligente para el Asistente Personal Menura 2.0 (GraphRAG Híbrido)",
    version="2.0.0"
)

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
    Recibe un stream continuo de PCM del cliente, aplica VAD (Voice Activity Detection),
    transcribe con Faster-Whisper, y devuelve texto parcial/final.
    """
    await websocket.accept()
    print("Nuevo cliente conectado al canal de ingesta de audio.")
    try:
        while True:
            # En la Fase 2, aquí recibiremos los bytes de audio:
            data = await websocket.receive_bytes()
            
            # TODO: Pasar por VAD y Faster-Whisper
            # Simulamos que le devolvemos una transcripción al cliente en tiempo real
            await websocket.send_json({
                "type": "transcription_update",
                "content": f"[Simulación] Recibido fragmento de {len(data)} bytes.",
                "is_final": False
            })

    except WebSocketDisconnect:
        print("Cliente desconectado del canal de audio.")
    except Exception as e:
        print(f"Error en WebSocket: {e}")
