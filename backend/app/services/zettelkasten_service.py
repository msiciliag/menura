import os
import yaml
from datetime import datetime
import re

class ZettelkastenService:
    def __init__(self, vault_path="data/vault"):
        """
        Gestiona el sistema de archivos Markdown.
        Es la única fuente de la verdad para el usuario.
        """
        self.vault_path = vault_path
        os.makedirs(self.vault_path, exist_ok=True)

    def _sanitize_filename(self, title: str) -> str:
        # Remueve caracteres especiales para un nombre de archivo seguro
        clean = re.sub(r'[^\w\s-]', '', title).strip().lower()
        return re.sub(r'[-\s]+', '-', clean)

    def save_note(self, title: str, content: str, tags: list = None, entities: list = None) -> str:
        """
        Guarda una nueva nota en el sistema de archivos con Frontmatter YAML.
        """
        filename = f"{self._sanitize_filename(title)}.md"
        filepath = os.path.join(self.vault_path, filename)
        
        # Evitar sobreescribir si ya existe, añadimos un timestamp
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{self._sanitize_filename(title)}_{timestamp}.md"
            filepath = os.path.join(self.vault_path, filename)

        frontmatter = {
            "title": title,
            "date": datetime.now().isoformat(),
            "tags": tags or [],
            "entities": entities or []
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("---\n")
            yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
            f.write("---\n\n")
            f.write(content)
            
        print(f"Nota Zettelkasten guardada: {filepath}")
        return filepath

    def get_all_notes(self) -> list:
        # En el futuro: leer notas para reindexar si la DB vectorial se borra
        pass
