try:
    import csv
    import py2neo
    from py2neo import Graph
    import pandas as pd
    import json
    import os
except Exception as e:
    print("Some Modules are Missing")

DATA_DIR = os.path.join(os.getcwd(), "data")

node_types = ["Compound", "Disease", "Gene", "Anatomy"]
abbreviations = {"C": "Compound", "D": "Disease", "G": "Gene", "A": "Anatomy",
        "r": "resembles", "t": "treats", "p": "palliates",
        "u": "upregulates", "d": "downregulates", "b": "binds",
        "a": "associates", "l": "localizes", "e": "expresses",
        "r>": "regulates", "c": "covaries", "i": "interacts"}
edge_types = ["CrC", "CtD", "CpD", "CuG", "CbG", "CdG", "DrD", "DuG", "DaG",
        "DdG", "DlA", "AuG", "AeG", "AdG", "Gr>G", "GcG", "GiG"]


class Neo4jDB():
    def __init__(self):
        self.graph = Graph(uri="bolt://localhost:7687", auth=("neo4j", "csci"))

    def create_db(self):
        query = "MATCH (n) RETURN COUNT(n);"
        result = self.graph.run(query).data()
        if result[0]['COUNT(n)'] != 0:
            print("Neo4j Database is available")
            return

    def query_db(self, compound):
        if compound == "":
            query = """
                    MATCH (c:Compound)-[:upregulates]->(:Gene)<-[:downregulates]-(d:Disease)
                    WHERE NOT (c)-[:treats]->(d)
                    MATCH (c:Compound)-[:downregulates]->(:Gene)<-[:upregulates]-(d:Disease)
                    WHERE NOT (c)-[:treats]->(d)
                    RETURN DISTINCT c.name, d.name
                    """
        else:
            query = f"""
            MATCH (c:Compound {{name: "{compound}"}})-[:upregulates]->(:Gene)<-[:downregulates]-(d:Disease)
            WHERE NOT (c)-[:treats]->(d)
            MATCH (c:Compound {{name: "{compound}"}})-[:downregulates]->(:Gene)<-[:upregulates]-(d:Disease)
            WHERE NOT (c)-[:treats]->(d)
            RETURN DISTINCT c.name, d.name
            """
        results = self.graph.run(query).data()
        if not results:
            print("Pairs not found")
        else:
            print("Disease and Compound pairs:")
            for result in results:
                print(f"\t{result['c.name']}-{result['d.name']}")







