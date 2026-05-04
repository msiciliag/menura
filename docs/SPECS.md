# Especificaciones Técnicas (Specs) - Menura 2.0

## 1. Arquitectura General (Cliente-Servidor Local)
El proyecto "Menura" funcionará como un sistema desacoplado, dividido en dos piezas clave para garantizar fluidez extrema, mínimo consumo de recursos y capacidades de IA avanzadas:
*   **Frontend (App Cliente - Tauri):** Interfaz gráfica nativa ultraligera impulsada por Rust y tecnologías web.
*   **Backend (Motor IA - FastAPI):** Servidor local de alto rendimiento para captura de audio, STT, LLM y el motor de conocimiento híbrido.

## 2. Especificaciones del Frontend (El Cliente Tauri)
*   **Framework Core:** **Tauri v2** (Rust para la lógica de sistema, acceso a hardware y puente de alto rendimiento).
*   **Tecnología UI:** **React o SvelteKit** + Tailwind CSS. Garantiza una UI reactiva, moderna y de diseño premium.
*   **Plataformas Soportadas:**
    *   macOS (Intel & Apple Silicon nativo).
    *   Windows (x64 y ARM64 nativo).
    *   Android e iOS (aprovechando Tauri v2 mobile).
*   **Características Principales:**
    *   **Audio Streaming Nativo:** Rust captura el micrófono a muy bajo nivel (sin la sobrecarga del navegador) y envía el stream PCM por WebSockets al backend Python.
    *   **UI "Invisible":** Minimalismo extremo (Notion/Apple Notes). El usuario ve un botón de grabar y un chat/bloc de notas. Cero jerga técnica.
    *   **Consumo Mínimo:** Huella de memoria de la app < 80MB.

## 3. Especificaciones del Backend (El Motor Python)
*   **Framework:** FastAPI (Python 3.12+), 100% asíncrono.
*   **Protocolo:** WebSockets para audio en tiempo real y REST para gestión documental.
*   **Motor STT (El Oído):**
    *   **VAD:** Silero VAD (ignora silencios para ahorrar CPU).
    *   **Transcriptor:** Faster-Whisper (modelo `whisper-large-v3-turbo`). Transcripción SOTA en español, casi en tiempo real.

## 4. El Cerebro (Sistema Multi-Agente)
*   **Motor LLM:** Ollama / llama.cpp (Gemma 4 e2b, Llama 3 8B, Qwen). Ejecución local acelerada por GPU/Metal.
*   **Agentes:**
    *   **Bibliotecario:** Extrae información estructurada de las transcripciones crudas.
    *   **Explorador (Retriever):** Navega el grafo híbrido para recuperar contexto.
    *   **Sintetizador:** Genera la respuesta final al usuario.

## 5. El RAG DEFINITIVO (Hybrid Graph-Vector Knowledge System)
Para lograr una memoria perfecta y un razonamiento complejo (Zettelkasten inteligente), Menura no usará solo vectores ni solo grafos, sino una **fusión ultra-optimizada de ambos (GraphRAG híbrido)**.

*   **El Almacén Base:** Archivos Markdown puros (`.md`) con Frontmatter YAML. Es la fuente de la verdad inmutable y legible por humanos.
*   **Capa Vectorial (Similitud Semántica):**
    *   **Tecnología:** LanceDB (embebida, ultrarrápida).
    *   **Función:** Almacena embeddings de los fragmentos de texto (chunks) y de las descripciones de los nodos del grafo. Permite buscar conceptos abstractos ("ideas sobre marketing que mencioné la semana pasada").
*   **Capa de Grafo (Conocimiento Estructurado):**
    *   **Tecnología:** KùzuDB (grafo embebido ultrarrápido) o un motor SQLite relacional altamente optimizado para nodos/aristas.
    *   **Función:** Mapea relaciones duras. Nodos (Personas, Proyectos, Conceptos, Fechas) y Aristas (Pertenece a, Conoce a, Mencionado en).
*   **El Flujo Híbrido (La Magia):**
    1.  **Ingesta:** Cuando hablas, el Agente Bibliotecario transcribe el Markdown, pero además *extrae un sub-grafo* (ej. `[Juan] -> (trabaja_en) -> [Proyecto X]`) y *vectoriza* el contenido.
    2.  **Recuperación:** Cuando preguntas algo, el sistema primero hace una **búsqueda vectorial** rápida para encontrar los "nodos semilla" más relevantes.
    3.  **Expansión:** Desde esos nodos semilla, el sistema **atraviesa el grafo** (1 o 2 saltos) para entender el contexto relacional que los vectores no ven (ej. "Ah, Juan trabaja en el Proyecto X, y el Proyecto X tiene la fecha límite mañana").
    4.  **Respuesta:** Todo este contexto hiper-enriquecido se le pasa al modelo Gemma para que responda como una secretaria omnisciente.
*   **Transparencia:** Todo este sistema Graph-Vector ocurre en milisegundos en segundo plano. El usuario solo ve una respuesta perfecta.
