# Plan de Ejecución Detallado (Menura 2.0 - Arquitectura Híbrida Tauri)

Este documento detalla las fases operativas para construir el nuevo sistema Menura desde cero. Pasaremos de un script aislado a un sistema de escritorio premium basado en Tauri (Rust+React/SvelteKit) y un backend de inteligencia artificial super-optimizado con un sistema de conocimiento híbrido (Vector + Grafo).

---

## Fase 1: Limpieza, Cimentación y Nuevo Backend Core (Semanas 1-2)
**Objetivo:** Establecer la arquitectura base de comunicación en tiempo real y eliminar la deuda técnica.

1.  **Limpieza del repositorio actual:**
    *   Eliminar dependencias de `flet` y código UI antiguo (`menura/main.py`).
    *   Purgar scripts bloqueantes (`menura/src/record.py`, `menura/src/transcript.py`).
2.  **Inicialización de FastAPI:**
    *   Crear una estructura limpia (ej. `backend/app`).
    *   Configurar Uvicorn + FastAPI con soporte para WebSockets (`/ws/audio`).
    *   Configurar endpoints REST básicos (`/api/status`, `/api/config`).
3.  **Implementar VAD y STT (El Oído):**
    *   Integrar **Silero VAD** en el endpoint de WebSocket para descartar silencios (filtro vital de batería/CPU).
    *   Sustituir la librería `transformers` pura por **Faster-Whisper** (`whisper-large-v3-turbo` o `distil-whisper`).
    *   Crear un pipeline asíncrono que reciba chunks de audio PCM por WebSocket, detecte voz y devuelva transcripciones parciales y finales al instante.

## Fase 2: El Cerebro (Sistema Híbrido Graph-Vector RAG) (Semanas 3-5)
**Objetivo:** Dotar al sistema de "inteligencia" local y persistencia de memoria (Zettelkasten "Definitivo").

1.  **Motor LLM Local:**
    *   Integrar **Ollama** o **llama.cpp-python** como motor de inferencia principal (Soporte para Gemma 4 e2b / Llama 3 8B cuantizados a 4-bit para velocidad vertiginosa).
2.  **Sistema de Archivos y Metadatos (Zettelkasten):**
    *   Crear el gestor base que guarda archivos Markdown (`.md`) con Frontmatter YAML (para fechas, tags, entidades). La fuente de la verdad intocable e inmutable para el usuario.
3.  **Implementación del Grafo de Conocimiento Híbrido (GraphRAG Definitivo):**
    *   **Extracción de Grafos:** Desarrollar prompts optimizados para que el LLM tome la transcripción cruda y extraiga entidades (nodos) y relaciones (aristas) de manera estructurada (JSON).
    *   **Almacén Dual:** Configurar **KùzuDB** (o un esquema SQLite relacional optimizado para grafos embebidos) para guardar estas relaciones lógicas exactas. Paralelamente, inicializar **LanceDB** para generar y almacenar embeddings semánticos densos (texto -> vector) usando un modelo de embedding ligero (`nomic-embed-text`).
    *   **Motor de Recuperación Híbrida (Retriever):** Crear el flujo central de consulta:
        *   **Paso 1:** Búsqueda Vectorial Rápida en LanceDB (encuentra los fragmentos semánticamente más similares a la pregunta del usuario).
        *   **Paso 2:** Extraer los nodos/entidades de esos fragmentos.
        *   **Paso 3:** Expansión del Grafo: Hacer un query de 1 o 2 saltos en KùzuDB a partir de esos nodos semilla para descubrir conexiones ocultas (ej. "A se relaciona con B, y B se relaciona con C").
        *   **Paso 4:** Unir contexto vectorial y grafo-relacional.
4.  **Sistema Multi-Agente (Bibliotecario y Sintetizador):**
    *   Orquestar el flujo automatizado: Audio Ingestado -> Transcrito -> Extraído Grafo/Vector (Bibliotecario).
    *   Flujo de Consulta: Usuario Pregunta -> Recuperación Híbrida -> LLM Genera Respuesta Perfecta (Sintetizador).

## Fase 3: Frontend Tauri (App Premium Multiplataforma) (Semanas 6-7)
**Objetivo:** Crear la interfaz ligera, invisible y multiplataforma usando Rust y tecnologías web modernas.

1.  **Inicializar Proyecto Tauri v2:**
    *   Generar un nuevo workspace de Tauri con soporte mobile.
    *   Elegir **SvelteKit** (o React) como framework UI. Instalar Tailwind CSS y configurarlo para un diseño ultralimpio (Apple Notes / Notion vibe).
2.  **Comunicación Backend-Frontend de Bajo Nivel (Rust):**
    *   Implementar captura de audio continua a través de Rust (evitando la capa del navegador para reducir consumo de RAM y CPU).
    *   Crear el puente (IPC) entre la UI web y el backend en Rust para enviar audio PCM por WebSockets hacia la instancia de FastAPI.
3.  **Desarrollo de la UI ("La Secretaria"):**
    *   Botón/atajo global del sistema operativo para "Empezar a hablar" desde cualquier ventana.
    *   Vista de chat/bloc de notas super minimalista.
    *   Renderizado en tiempo real de las transcripciones parciales (efecto "tecleo").
    *   Renderizado Markdown nativo para las respuestas del Agente Sintetizador (con soporte para bloques de código y enlaces internos Zettelkasten).

## Fase 4: Optimización Extrema y Empaquetado (Semanas 8)
**Objetivo:** Pulir la experiencia de usuario, reducir el footprint de memoria y compilar binarios.

1.  **Optimización Edge Computing:**
    *   Configurar carga diferida (lazy loading) de los modelos en memoria (Ollama/Faster-Whisper solo se cargan si es necesario y se descargan tras inactividad).
    *   Asegurar que el cliente Tauri use < 80MB de RAM.
2.  **Pruebas Multiplataforma:**
    *   macOS (M-Series / Intel).
    *   Windows (con GPU y CPU).
    *   Android (APK/AAB).
3.  **Empaquetado y Release:**
    *   Generar instaladores (.dmg, .exe, .apk) optimizados.
    *   Redactar la documentación final orientada a usuario ("Cómo hablar con tu segunda memoria").
