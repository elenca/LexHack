#! /usr/bin/env python

import os
import json
from flask import Flask, request, jsonify
from py2neo import Graph
from models import Person
from ml import predict_tags

DB_URI = os.environ.get("DB_URI", "localhost")
DB_USER = os.environ.get("DB_USER", "user")
DB_PW = os.environ.get("DB_PW", "'pw1")

app = Flask(__name__, static_url_path='/static/')
graph = Graph("bolt://the-admins.ch:7687", auth=(DB_USER, DB_PW))
classifiedCompilations = json.load(open("db/data.json"))
tags = json.load(open("db/tags.json"))

def find_persons(from_person):
    person = Person.match(graph, from_person).first()
    if not person:
        return None
    return person.toDict()
    
def find_mails(from_person):
    person = Person.match(graph, from_person).first()
    if not person:
        print("PERSON NOT FOUND")
        return None
    mails = [m.toDict() for m in person.Mails_sent]
    return mails

def find_cases(from_person):
    person = Person.match(graph, from_person).first()
    if not person:
        print("PERSON NOT FOUND")
        return None
    cases = [c.toDict() for c in person.Accuser]
    return cases

@app.route("/")
def get_index():
    return app.send_static_file('index.html')

@app.route("/messages", methods=['POST'])
def new_message():
    data = request.get_json()
    message = data.get("message", "")
    from_person = data.get("from", "")
    (result, tag_list) = predict_tags(classifiedCompilations, tags, message)
    involved_persons = find_persons(from_person)
    mails = find_mails(from_person)
    cases = find_cases(from_person)
    return jsonify(build_response(result, involved_persons, mails, tag_list, cases))

def build_response(classifiedCompilation, persons, mails, tag_list, cases):
    return {
        "classifiedCompilation": classifiedCompilation,
        "persons": persons,
        "mails": mails,
        "tags": tag_list,
        "cases": cases
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
