'''
Maintainer: Timothy Player

Ddescription: This file holds information (for now) about database, 
              requests and posts. Eventually there will be RL or idk NLP stuff.

'''


from flask import Flask, request
from flask_restful import Resource, Api
from requests import put, get
from googlesearch import search


app = Flask(__name__)
api = Api(app)

solutions = {}

class errorParse(Resource):
    #Take error, post error in database, return link, get coffee
    def put(self, error):
        #This is how the daemon interfaces with the restful API
        results = search(error, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
        for result in results:
            solutions[error] = result
            #Need to return dictionary for json conversion
            return {error:solutions[error]}
        

    def get(self, error):
        #This is what the API tells the daemon when she asks politely
        return {error:solutions[error]}
        

api.add_resource(errorParse, '/<string:error>')

if __name__ == '__main__':
    app.run(debug=True)

