from flask_sqlalchemy import SQLAlchemy

class DatabaseController():

    def __init__(self,dbinstance) -> None:
        self.dbinstance = dbinstance
    
    def insertar_heroe(self,heroe):

        try:    
            self.dbinstance.session.add(heroe)
            self.dbinstance.session.commit()
            return True

        except Exception as e:
            return False

    def leer_heroe(self,super_id,Super_Heroe):
        try:
            return  Super_Heroe.query.filter_by(id=super_id).first()           
        except:
            return False

    def leer_heroes(self,Super_Heroe):
        try:
            heroes_query_result= self.dbinstance.session.execute(
                self.dbinstance.select(Super_Heroe).order_by(Super_Heroe.id)
                ).scalars()
            heroes = heroes_query_result.fetchall()
            return heroes
        except:
            return False

    def actualizar_heroe(self, Super_Heroe, super_id, super_name):
        
        try:
            heroe= self.leer_heroe(super_id,Super_Heroe)
            heroe.name=super_name
            self.dbinstance.session.commit()
            return heroe
        except Exception as e:
            print(e)
            return {}
    
    def eliminar_heroe(self, heroe_hallado):
        try:
            self.dbinstance.session.delete(heroe_hallado)
            self.dbinstance.session.commit()

            return True
        except:

            return False

        
