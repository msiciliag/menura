# La Constitución de Menura

## El Alma del Proyecto

Menura no es solo una aplicación de toma de notas o una grabadora con IA. Menura es tu **segundo cerebro y tu asistente personal (secretaria) local**. Este documento establece los pilares fundamentales que guiarán cada decisión técnica y de diseño en la evolución del proyecto. Ninguna característica o actualización debe violar estos principios.

---

### 1. Privacidad y Soberanía Absoluta (Local-First)
- **Ningún byte sale de la máquina:** Todo el procesamiento de audio, transcripción, generación de embeddings, búsquedas semánticas y razonamiento del LLM ocurre 100% en local.
- **Sin Nubes, Sin Suscripciones:** El usuario no debe depender de APIs externas (como OpenAI o Anthropic) para el funcionamiento principal. El poder de computación proviene exclusivamente del hardware del usuario (Edge Computing).
- **Control Total:** Los datos pertenecen al usuario, y nadie más tiene acceso a ellos.

### 2. El Usuario es el Dueño de sus Datos (Agnóstico e Interoperable)
- **El formato rey es el texto plano:** Toda la base de conocimiento se almacenará en archivos Markdown (`.md`) puros y limpios, utilizando YAML Frontmatter para metadatos.
- **Sin "Vendor Lock-in":** Si el usuario decide desinstalar Menura mañana, su conocimiento permanecerá intacto, legible por humanos y compatible con cualquier otra herramienta (Obsidian, Logseq, VSCode).
- **El Grafo es Transparente:** Las relaciones entre ideas (Zettelkasten) se representan mediante enlaces estándar en el texto (ej. `[[Concepto]]`), no en bases de datos oscuras e inaccesibles.

### 3. Fricción Cero y Rendimiento Premium
- **Velocidad de Vértigo:** La transcripción y las respuestas deben sentirse casi instantáneas. Para ello se exprimen las tecnologías más optimizadas (Rust, WebSockets, Faster-Whisper, Modelos Cuantizados).
- **Eficiencia de Recursos:** Menura no debe devorar la batería ni la RAM cuando no está en uso activo. Se usarán detectores de actividad de voz (VAD) y suspensión de modelos para mantener la ligereza.
- **Interfaz "Invisible":** La tecnología debe apartarse del camino. La UI será minimalista, pulida, sin botones innecesarios ni jerga técnica (nada de "embeddings", "chunks" o "RAG" a la vista del usuario). Es una secretaria, no un panel de control de un cohete.

### 4. La Inteligencia Proactiva (La Secretaria)
- **Contexto Infalible:** La IA debe "recordar" lo que se le dijo hace meses. Antes de responder, consulta el grafo de conocimiento para dar contexto exacto.
- **Auto-Organización:** El usuario solo necesita hablar. Menura se encarga de transcribir, estructurar, etiquetar, conectar con notas antiguas y resumir el conocimiento en segundo plano.
- **Interacción Natural:** La forma principal de ingresar datos es hablar. La forma principal de recuperar datos es preguntar en lenguaje natural.

### 5. Universalidad (Multiplataforma Nativa)
- **Dondequiera que esté el usuario:** El sistema debe sentirse como una aplicación nativa premium de primera clase, ya sea en macOS, Windows o Android.
- **Rendimiento sobre Conveniencia de Desarrollo:** Usaremos Rust (Tauri) para las interfaces y lenguajes compilados/optimizados (C++/Python) para la IA, asegurando que la portabilidad no cueste fluidez.
