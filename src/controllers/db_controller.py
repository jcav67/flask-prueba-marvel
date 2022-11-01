
class DatabaseController():

    def __init__(self,dbinstance) -> None:
        self.dbinstance = dbinstance
    
    def insertar_heroe(self,heroe) -> bool:
        """
            Permite insertar heroes en la base de datos

            Args:
                heroe (Super_Heroe): Super heroe a insertar

            Returns:
                bool: Estado de la inserción. True = exitoso.
        """
        try:    
            self.dbinstance.session.add(heroe)
            self.dbinstance.session.commit()
            return True

        except :
            return False

    def leer_heroe(self,super_id,Super_Heroe)  :
        """
            Permite leer un heroe de la base de datos mediante su id

            Args:
                super_id (int): Super heroe a insertar
                Super_Heroe(Super_Heroe): instancia de la clase Super_Heroe

            Returns:
                Super_Heroe: objeto de la clase Super_heroe.

            Raise:
                Error interno en la consulta de la base de datos
        """
        try:
            return  Super_Heroe.query.filter_by(id=super_id).first()           
        except :
            raise RuntimeError("Fallo en la consulta en la base de datos")

    def leer_heroes(self,Super_Heroe):
        """
            Permite leer todos los heroes de la base de datos 

            Args:
                Super_Heroe(Super_Heroe): instancia de la clase Super_Heroe

            Returns:
                heroes: lista de resultados de la consulta de la base de datos
            Raise:
                Error interno en la consulta de la base de datos
        """
        try:
            heroes_query_result= self.dbinstance.session.execute(
                self.dbinstance.select(Super_Heroe).order_by(Super_Heroe.id)
                ).scalars()
            heroes = heroes_query_result.fetchall()
            return heroes
        except:
            raise RuntimeError("Fallo en la consulta en la base de datos")

    def actualizar_heroe(self, Super_Heroe, super_id, super_name):
        """
            Permite actualizar el nombre un heroe de la base de datos mediante su id

            Args:
                Super_Heroe(Super_Heroe): instancia de la clase Super_Heroe
                super_id (int): Id del Super heroe que se desea actualizar
                super_name (String): Nombre del Super heroe que se desea actualizar

            Returns:
                heroe: heroe de tipo Super_Heroe con los datos actualizados
            Raise:
                Error interno en la consulta de la base de datos
        """
        
        try:
            heroe= self.leer_heroe(super_id,Super_Heroe)
            heroe.name=super_name
            self.dbinstance.session.commit()
            return heroe
        except :
            raise RuntimeError("Fallo en la consulta en la base de datos")
    
    def eliminar_heroe(self, heroe_hallado):
        """
            Permite eliminar un heroe de la base de datos 

            Args:
                heroe_hallado(Super_Heroe): instancia de Super_Heroe con la informacion del Super heroe que se desea eliminar

            Returns:
                bool: Estado de la eliminación. True = exitoso.
        """
        try:
            self.dbinstance.session.delete(heroe_hallado)
            self.dbinstance.session.commit()

            return True
        except:

            return False
