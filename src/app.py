from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from decouple import config
import requests
from controllers.db_controller import DatabaseController

API_KEY = config('APIKEY')
API_HASH = config('HASH')
MYSQL_PASS = config('MYSQL_PASS')
MYSQL_USER = config('MYSQL_USER')
mysql_connection_string=f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@localhost/SuperHeroesbd'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = mysql_connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

dbInstance = SQLAlchemy(app)
marshmallow_instance = Marshmallow(app)


#Models
class Super_Heroe(dbInstance.Model):
    id = dbInstance.Column(dbInstance.Integer, primary_key=True)
    name = dbInstance.Column(dbInstance.String(70), unique=True)
    description = dbInstance.Column(dbInstance.String(500))

    def __init__(self, id, name, description) -> None:
        self.id = id
        self.name = name 
        self.description = description

with app.app_context():
    dbInstance.create_all()

dbcontroller = DatabaseController(dbInstance)

class Super_Heroe_Schema(marshmallow_instance.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

super_heroe_schema= Super_Heroe_Schema()
super_heroes_schema= Super_Heroe_Schema(many=True)


@app.route('/consultarHeroesApi', methods=['GET'])
def consultar_heroes_api():
    try:
        payload = {'ts': '1', 'apikey':API_KEY, 'hash':API_HASH}
        url = 'https://gateway.marvel.com/v1/public/characters'
        respuesta_api_marvel = requests.get(url, params=payload)
        registros_creados = []
        registros_actualizados = []

        if not respuesta_api_marvel:
            return jsonify({'msg': 'no existe la ruta'}), 404

        respuesta_parseada = respuesta_api_marvel.json()
        respuesta_iterable = respuesta_parseada['data']['results']

        for heroe in respuesta_iterable:

            heroe_hallado  = dbcontroller.leer_heroe(heroe['id'],Super_Heroe)
            if not heroe_hallado:

                nuevo_heroe= Super_Heroe(heroe['id'], heroe['name'], heroe['description'])
                dbcontroller.insertar_heroe(nuevo_heroe)
                registros_creados.append(heroe['name'])
            else:
                heroe_parseado = super_heroe_schema.dump(heroe_hallado)

                if heroe_parseado['name'] != heroe['name']:
                    heroe_actualizado = dbcontroller.actualizar_heroe(Super_Heroe,heroe['id'], heroe['name'])
                    
                    if heroe_actualizado:
                        registros_actualizados.append(heroe['name'])

        return jsonify({'registros_agregados': registros_creados, 
                        'registros_actualizados':registros_actualizados,
                        'numero de registros agregados': len(registros_creados), 
                        'numero de registros actualizados': len(registros_actualizados)
                        })
    except :
        return jsonify({'msg': 'Error al crear registros'}), 500


@app.route('/actualizarHeroes', methods=['PUT'])
def actualizar_heroe_ruta():
    try:
        if not request.json['id'] or not request.json['name']:
            return jsonify({'msg': 'datos faltantes'}), 400

        super_id = request.json['id']
        super_name = request.json['name']

        heroe = dbcontroller.actualizar_heroe(Super_Heroe, super_id, super_name)
        
        return super_heroe_schema.jsonify(heroe)
        
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Error al crear registro'}), 500
    

@app.route('/obtenerHeroes', methods =['GET'])
def obtener_heroes():

    heroes = dbcontroller.leer_heroes(Super_Heroe)
    if(heroes):
        return super_heroes_schema.jsonify(heroes)
    else:
        return jsonify({'msg': 'heroe no encontrado'}), 400


@app.route('/obtenerHeroe/<id>', methods =['GET'])
def obtener_heroe(id):

    heroe_hallado  = dbcontroller.leer_heroe(id,Super_Heroe)
    if(heroe_hallado):
        hero = super_heroe_schema.dump(heroe_hallado)
        return jsonify(hero)
    else:
        return jsonify({'msg': 'heroe no encontrado'}), 400

@app.route('/borrarHeroes', methods =['DELETE'])
def borrar_heroe():

    super_id = request.json['id']

    if not super_id:
        return jsonify({'msg': 'datos faltantes'}), 400
    
    heroe_hallado = dbcontroller.leer_heroe(super_id,Super_Heroe)

    if not heroe_hallado:
        mensaje =f'heroe con id {super_id} no encontrado'
        return jsonify({'msg': mensaje}), 400

    if dbcontroller.eliminar_heroe(heroe_hallado):
        heroe_eliminado = super_heroe_schema.dump( heroe_hallado)

        return jsonify({"eliminado":True, "heroe": heroe_eliminado})
    else:
        return jsonify({"eliminado":False, "msg": 'Error al eliminar heroe'}), 501
    


if __name__ == "__main__":
    app.run(debug=True)
