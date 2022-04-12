import os

from mongodb import MongoDB
from neo4j import Neo4jDB

if __name__ == "__main__":

    mongod = MongoDB()
    mongod.create_db()
    neo4j_d = Neo4jDB()
    neo4j_d.create_db()
    print("Welcome to HetioNet")
    query = input("Enter a disease ID: ")

    cont_mongo = mongod
    cont_mongo.query_db(query)
    cont_neo4j = neo4j_d
    neo4j_query = input("Enter a compound name: ")
    cont_neo4j.query_db(query)


