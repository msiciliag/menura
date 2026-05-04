import asyncio
from app.services.llm_service import LLMService
from app.services.zettelkasten_service import ZettelkastenService
from app.services.vector_db_service import VectorDBService
from app.services.graph_db_service import GraphDBService

class LibrarianAgent:
    def __init__(self, 
                 llm_service: LLMService, 
                 zk_service: ZettelkastenService,
                 vector_db: VectorDBService,
                 graph_db: GraphDBService):
        self.llm = llm_service
        self.zk = zk_service
        self.vector_db = vector_db
        self.graph_db = graph_db

    async def process_transcription(self, raw_text: str):
        """
        El flujo principal del Bibliotecario:
        Convierte un volcado de audio crudo en conocimiento estructurado híbrido.
        """
        if len(raw_text.strip()) < 10:
            return None # Ignorar audios muy cortos o ruidos
            
        print(f"[Librarian] Procesando nueva transcripción de {len(raw_text)} caracteres...")

        system_prompt = """
        Eres un Bibliotecario experto en metodologías Zettelkasten y extracción de conocimiento.
        Tu tarea es analizar la transcripción de voz del usuario y extraer información estructurada.
        Debes devolver un JSON con la siguiente estructura exacta:
        {
            "title": "Un título corto y descriptivo (max 5 palabras)",
            "summary": "Un resumen limpio y bien redactado en Markdown de lo que dijo el usuario, corrigiendo errores típicos del habla.",
            "tags": ["tag1", "tag2", "tag3"],
            "entities": ["Persona A", "Proyecto B", "Concepto C"],
            "graph_relations": [
                {"from": "Entidad A", "to": "Entidad B", "type": "relacion_logica"}
            ]
        }
        Las relaciones del grafo ('graph_relations') deben ser conexiones lógicas entre las entidades (ej. "trabaja_en", "pertenece_a", "es_un", "menciona").
        """

        try:
            # 1. Extracción con LLM
            extracted_data = await self.llm.extract_json(
                prompt=f"Transcripción cruda:\n{raw_text}",
                system_prompt=system_prompt
            )

            title = extracted_data.get("title", "Nota sin título")
            summary = extracted_data.get("summary", raw_text)
            tags = extracted_data.get("tags", [])
            entities = extracted_data.get("entities", [])
            relations = extracted_data.get("graph_relations", [])

            # 2. Guardar en el Zettelkasten (El archivo físico Markdown)
            filepath = self.zk.save_note(
                title=title,
                content=summary,
                tags=tags,
                entities=entities
            )

            # 3. Indexar en VectorDB (LanceDB)
            # En un entorno real, generaríamos el embedding aquí, o LanceDB lo hace automáticamente si le pasamos el modelo configurado
            self.vector_db.add_document(
                text=summary,
                metadata={"title": title, "filepath": filepath, "tags": tags}
            )

            # 4. Actualizar el Grafo de Conocimiento (KùzuDB)
            for entity in entities:
                # Asumimos tipo genérico "Concept" para simplificar, el prompt podría inferir tipos
                self.graph_db.add_entity(name=entity, entity_type="Concept")

            for rel in relations:
                source = rel.get("from")
                target = rel.get("to")
                rel_type = rel.get("type", "relates_to").replace(" ", "_").upper()
                if source and target:
                    self.graph_db.add_entity(source, "Concept")
                    self.graph_db.add_entity(target, "Concept")
                    self.graph_db.add_relation(source, target, rel_type)

            print(f"[Librarian] Procesamiento exitoso. Nota '{title}' guardada e indexada en Grafo y VectorDB.")
            
            return {
                "status": "success",
                "title": title,
                "filepath": filepath
            }

        except Exception as e:
            print(f"[Librarian] Error procesando transcripción: {e}")
            # Fallback de emergencia: guardar en crudo si el LLM falla
            self.zk.save_note("Dump de Emergencia", raw_text, tags=["error-procesamiento"])
            return {"status": "error", "message": str(e)}
