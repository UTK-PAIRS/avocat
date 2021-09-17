#!/usr/bin/env python3

'''
    Author: Gregory Croisdale
'''

from flask import Flask, json, request, jsonify
from flask_restful import Resource, Api, reqparse
from os.path import exists
from helpers import *

"""
    Load API keys and the like
"""
keydir = "API_KEYS"
STACKOVERFLOW = None
if exists(f"{keydir}/stackoverflow.json"):
    STACKOVERFLOW = json.load(open(f"{keydir}/stackoverflow.json", 'r'))

"""
    Initialize flask app
"""
app = Flask(__name__)
api = Api(app)

"""
    First, we must define a parser to understand url options
    Format: url/req?argv=argv[0],argv[1],...;stdout="output";stderr="errput";ret=num
"""
descparse = reqparse.RequestParser()
descparse.add_argument('argv', type=list)
descparse.add_argument('stdout', type=str)
descparse.add_argument('stderr', type=str)
descparse.add_argument('r', type=int)

class Diagnose(Resource):
    def get(self):
        """
            Client has requested diagnosis of error -- send it off to stackoverflow!
        """
        args = descparse.parse_args()
        args['argv'] = ''.join(args['argv']).split(',')

        r = query(**args, apikey=STACKOVERFLOW['key'] if STACKOVERFLOW else None)

        print(f"{r['remaining']} calls remaining\n\n")

        return r

api.add_resource(Diagnose, '/req')

if __name__ == '__main__':
    app.run(debug=True)

