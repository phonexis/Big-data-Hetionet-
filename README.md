# Big-data-Hetionet

Dorjee Gyaltsen
CSCI 49376
Professor Xie


USED:
Pycharm 2020.2.3
Python 3.9
MongoDB 4+
MongoDB Compass
PyMongo 
Py2neo 
Neo4j 4.1.3

Files:
Neo4j.py
Mongodb.py
Main.py
Edges.tsv
Nodes.tsv

To run the file on terminal:
python main.py

Questions asked for this project:
1) Given a disease id, what is its name, what are drug names that can treat or palliate this disease, what are gene names that cause this disease, and where this disease occurs? Obtain and output this information in a single query. 
We used mongoDB for this part of the question as this document based DB is really good for storing information about each disease. We used mongoDB compass as our GUI alongside Pycharm as our IDE.

2) We assume that a compound can treat a disease if the compound or its resembled compound up-regulates/down- regulates a gene, but the location down-regulates/up-regulates the gene in an opposite direction where the disease occurs. Find all compounds that can treat a new disease name (i.e. the missing edges between compound and disease excluding existing drugs). Obtain and output all drugs in a single query. 

For this part of the question, we used neo4j which imitates a hetionet graph and using cypher query language inside of python(Pycharm). Py2neo package was also used.
