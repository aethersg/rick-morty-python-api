from flask import Flask
from flask_restful import Resource, Api
import random
import json

app = Flask(__name__)
api = Api(app)


class RandomQuote(Resource):
    @staticmethod
    def get():
        with open("quotes.json") as data_file:
            data = json.load(data_file)

        r_quote = random.choice(data)
        return {"quote": r_quote}


api.add_resource(RandomQuote, '/')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
