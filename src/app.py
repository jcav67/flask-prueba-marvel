from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:Camilo67.com@localhost/softpymesbd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

dbInstance = SQLAlchemy(app)
marshmallow_instance = Marshmallow(app)

class Super_Heroe(dbInstance.Model):
    id = dbInstance.Column(dbInstance.Integer, primary_key=True)
    name = dbInstance.Column(dbInstance.String(70), unique=True)
    description = dbInstance.Column(dbInstance.String(100))

    def __init__(self, id, name, description) -> None:
        self.id = id
        self.name = name 
        self.description = description
        
dbInstance.create_all()

class Super_Heroe_Schema(marshmallow_instance.Schema):
    class Meta:
        fields = ('id', 'name', 'description')

super_heroe_schema= Super_Heroe_Schema()
super_heroes_schema= Super_Heroe_Schema(many=True)
