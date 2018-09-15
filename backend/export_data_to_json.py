import os
from models import ClassifiedCompilation, Article, Paragraph
from py2neo import Graph, NodeMatcher, RelationshipMatcher
import json


DB_URI = os.environ.get("DB_URI", "localhost")
DB_USER = os.environ.get("DB_USER", "user")
DB_PW = os.environ.get("DB_PW", "'pw1")

graph = Graph(DB_URI, auth=(DB_USER, DB_PW))

# We do export the data into json because the query takes to long (BAD WIFI)
data = []
classifiedCompilations = ClassifiedCompilation.match(graph)
for i, classifiedCompilation in enumerate(classifiedCompilations):
    data.append(classifiedCompilation.toDict())

with open("data.json", "w") as file:
    file.write(json.dumps(data, indent=4))
