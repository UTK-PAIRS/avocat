'''
Maintainer: Timothy Player

Ddescription: This file holds information (for now) about database, 
              requests and posts. Eventually there will be RL or idk NLP stuff.

'''


from flask import Flask, request
from flask_restful import Resource, Api
from requests import put, get
from googlesearch import search
import hashlib
from sentence_transformers import SentenceTransformer

result = hashlib.md5(b'GeeksforGeeks')

app = Flask(__name__)
api = Api(app)

solutions = {}

class Solution:
    def __init__(self):
        #The solution graph 
        self.graph = {}



class Parser(Resource):
    #Take error, post error in database, return link, get coffee
    def __init__(self):
        #Issue stack 
        self.issueStack = []

    def put(self, solution):
        #This lets us know what Daemon we're talking to and how to get her info
        return "Cant put stuff on the db yet."

    def parse(self,error):
        return "npm install error "

    def get(self, error):
        #This is what the API tells the daemon when she asks politely
        if "npm install error" in error:
            return "apt-get install npm"
        results = search(error, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
        model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
        error = tuple(model.encode(sentences))
        print(error)

        #If the error is new 
        if error not in solutions[error]:
            solutions[error] = list()

        for result in results:
            solutions[error].append(result)
            #Need to return dictionary for json conversion
        return {error:solutions[error]}

        

api.add_resource(Parser, '/<string:error>')

if __name__ == '__main__':
    app.run(debug=True)

