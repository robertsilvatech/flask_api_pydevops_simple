from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

technologies = []

class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World"}

class HealthCheck(Resource):
    def get(self):
        return {"message": "API is alive"}

class TechnologiesList(Resource):
    def get(self):
        return {"technologies": technologies}

class Technology(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('level', type=str, required=True, help='This field is missing')

    def get(self, name):
        technology = next(filter(lambda x: x['name'] == name, technologies), None)
        if technology:
            return {"technology": technology}
        else:
            return {"message": 'Technology not found'}, 404
        
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, technologies), None):
            return {"message": f"An technology with name {name} already exists"}, 400 #requisicao ruim
        data = Technology.parser.parse_args()
        technology = {"name": name, "level": data['level']}
        technologies.append(technology)
        return technology, 201

    def delete(self, name):
        global technologies
        technologies = list(filter(lambda x: x['name'] != name, technologies))
        print(technologies)
        return {"message": f"Technology {name} deleted"}

    def put(self, name):
        data = Technology.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, technologies), None)
        if item is None:
            technology = {"name": name, "level": data['level']}
            technologies.append(technology)
            return technology
        else:
            item.update(data)
        return item
   
api.add_resource(HelloWorld, '/')
api.add_resource(HealthCheck, '/healthcheck')
api.add_resource(TechnologiesList, '/technologies')
api.add_resource(Technology, '/technology/<string:name>')

app.run(debug=True)
