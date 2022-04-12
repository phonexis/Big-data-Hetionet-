import csv

try:
    import pymongo
    from pymongo import MongoClient
    import pandas as pd
    import json
    import os
except Exception as e:
    print("Some Modules are Missing")


class MongoDB():

    def __init__(self):

        self.data_dir = os.path.join(os.getcwd(), 'data')
        self.client = MongoClient("localhost", 27017)

        self.DB = self.client['HetioNet']
        self.collection = self.DB['Data']


    def create_db(self):
        cols = 0
        for _ in self.collection.find().limit(1):
            cols += 1
        if cols != 0:
            print("Mongo database available")
            return
        print("Creating Mongo database")

        diseases = {}
        # helps structure the diseases in a manner where we can have on document

        data = {
            'Anatomy': {},
            'Gene': {},
            'Disease': {},
            'Compound': {}
        }

        with open(os.path.join(self.data_dir, "nodes_test.tsv"), "r") as nodes_file:
            reader = csv.DictReader(nodes_file, delimiter="\t")
            for row in reader:
                data[row['kind']][row['id']] = row['name']

        for x, y in data['Disease'].items():
            diseases[x] = {
                'id': x,
                'name': y,
                "treatment": [],
                "palliate": [],
                "gene": [],
                "location": [],
            }
        # keys for the meta-edges specifically for edges.tsv
        edges_map = {
            "CtD": ['target', 'source', "Compound", "treatment"],
            "CpD": ['target', 'source', "Compound", "palliate"],
            "DaG": ['source', 'target', "Gene", "gene"],
            "DdG": ['source', 'target', "Gene", "gene"],
            "DlA": ['source', 'target', "Anatomy", "location"],
            "DuG": ['source', 'target', "Gene", "gene"]

            }
        # opens the data directory data and opens the edges tsv
        with open(os.path.join(self.data_dir, "edges_test.tsv"), "r") as nodes_file:
            reader = csv.DictReader(nodes_file, delimiter="\t")
            for row in reader:
                edge = row['metaedge']
                if edge in edges_map.keys():
                    diseases[row[edges_map[edge][0]]][edges_map[edge][3]].append(
                        data[edges_map[edge][2]][row[edges_map[edge][1]]]
                    )

            # helps make disease{} to become a single document
            # allowing us to refer to the map much easier
        self.collection.insert([v for _, v in diseases.items()])

    "Function consists of queries used in the databases"
    def query_db(self, query):
        """
        Instance attribute collection of test.
        MongoDB collection: Collection = self.DB['Data']
        """
        tmp_1 = self.collection.find({"id": query})

        cols = 0   # counter
        for _ in tmp_1:
            if cols > 0:
                break
            cols += 1

        if cols == 0:
            tmp_2 = self.collection.find({"name": query})
        else:
            "rewind for resetting the tmp counter"
            tmp_1.rewind()
            tmp_2 = tmp_1

        cols = 0
        id = ""
        name = ""
        treatment = []
        palliate = []
        gene = []
        location = []

        for i in tmp_2:
            "set the name and id when found through the database"
            id = i['id']
            name = i['name']

            # Extend list by appending elements from the iterable.
            treatment.extend(i['treatment'])
            palliate.extend(i['palliate'])
            gene.extend(i['gene'])
            location.extend(i['location'])
        cols += 1

        if cols == 0:
            print(f'The input you entered "{query}" is either incorrect or not a disease.')
            return

        def join_db(sep, items):
            # function that helps clean up the database making it readable
            # by using join to mend the items after split
            return sep.join(items)

        def pretty_db(items):
            "Formats the list by separating into groups of 5 "
            items = [items[i:i + 5] for i in range(0, len(items), 5)]
            if not items:
                return "None"
            # using join to combine the groups
            # join all groups by using newlines and removing the commas
            commas = map(lambda x: join_db(", ", x) + ',', items)
            return join_db("\n\t", commas)[:-1]


        print(
            f'For disease id"{query}" these are the following info:',
            f'ID:\n\t{query}',
            f'Name:\n\t{name}',
            f'Drugs that Palliate "{query}":\n\t{pretty_db(palliate)}',
            f'Drugs that Treat "{query}":\n\t{pretty_db(treatment)}',
            f'Genes that cause "{query}":\n\t{pretty_db(gene)}',
            f'Where "{query}" Occurs:\n\t{pretty_db(location)}',
            sep='\n\n'
        )





