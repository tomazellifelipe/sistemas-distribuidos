from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
COUNT = 0


class Eco(Resource):
    def get(self):
        return {"count": COUNT}


    def put(self, msg):
        global COUNT
        COUNT += 1
        return {"resp": msg + "_eco"}


api.add_resource(Eco, "/eco", "/eco/<string:msg>")

if __name__ == "__main__":
    app.env = "development"
    app.run(port=5001, debug=True)
