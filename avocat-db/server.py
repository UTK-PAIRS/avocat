'''


'''
from flask import Flask, json, request, jsonify
from flask_restful import Resource, Api, reqparse
from googlesearch import search
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

# First, we must define a parser to understand url options
# Format: url/req?argv=argv[0],argv[1],...;stdout="output";stderr="errput";ret=num
descparse = reqparse.RequestParser()
descparse.add_argument('argv', type=list)

class Parser(Resource):
    def parse_result(self, link):
        #For now remove all user information and all information not directly relevant to the error
        answertxt = ""
        codetxt = ""
        raw = requests.get(link).text
        soup = BeautifulSoup(raw, 'html.parser')
        answer = soup.find_all('div',class_="answer accepted-answer")

        #If the answer has not been accepted
        if len(answer) == 0:
            answers = soup.find_all('div',class_="answer")
            for response in answers:
                if "data-highest-scored=\"1\"" in str(response):
                    answertxt += str(response.p.string)
                    codetxt += str(response.code.string)
                    return (answertxt,codetxt)

        for paragraph in answer:
            answertxt += str(paragraph.p.string)
            codetxt += str(paragraph.code.string)
        return (answertxt,codetxt)


class Server(Resource):
    #Take error, post error in database, return link, get coffee
    def __init__(self):
        #Issue stack 
        self.parser = Parser()
        #self.database = Database()

    def put(self, solution):
        #This lets us know what Daemon we're talking to and how to get her info aswell as what the final solution cmd is.
        return "Cant put stuff on the db yet."

    def get(self, *arg):
        #This is what the API tells the daemon when she asks politely
        #if "npm install error" in error:
        #    return {error:"apt-get install npm"}
        
        #Get first ten results from Google
        return jsonify(arg)

"""        results = search(error, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
        for result in results:
            print(result)
            if "stackoverflow.com" in result:
                print(self.parser.parse_result(result))
                return {error:self.parser.parse_result(result)}



        #If the error is new 
        if error not in solutions[error]:
            solutions[error] = list()

        for result in results:
            solutions[error].append(result)
            #Need to return dictionary for json conversion
        return {error:solutions[error]}"""

class Listen(Resource):
    def get(self):
        """
        
        """
        args = descparse.parse_args()

        return jsonify(args)
        

api.add_resource(Listen, '/req')

if __name__ == '__main__':
    app.run(debug=True)

