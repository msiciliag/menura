import kuzu

class GraphDBService:
    def __init__(self, db_path="data/kuzudb"):
        self.db = kuzu.Database(db_path)
        self.conn = kuzu.Connection(self.db)
        
        # Initialize schema if it doesn't exist
        self._init_schema()

    def _init_schema(self):
        try:
            # Simple nodes
            self.conn.execute("CREATE NODE TABLE Entity (name STRING, type STRING, PRIMARY KEY (name))")
            self.conn.execute("CREATE NODE TABLE Concept (name STRING, PRIMARY KEY (name))")
            
            # Simple edges
            self.conn.execute("CREATE REL TABLE RelatesTo (FROM Entity TO Entity, type STRING)")
            self.conn.execute("CREATE REL TABLE Mentions (FROM Entity TO Concept, count INT64)")
        except RuntimeError as e:
            # Schema might already exist
            pass
            
    def add_entity(self, name: str, entity_type: str):
        query = f"MERGE (e:Entity {{name: '{name}', type: '{entity_type}'}})"
        self.conn.execute(query)

    def add_relation(self, from_entity: str, to_entity: str, rel_type: str):
        query = f"""
            MATCH (a:Entity {{name: '{from_entity}'}}), (b:Entity {{name: '{to_entity}'}})
            MERGE (a)-[:RelatesTo {{type: '{rel_type}'}}]->(b)
        """
        self.conn.execute(query)

    def query_graph(self, query: str):
        return self.conn.execute(query).get_as_df()
