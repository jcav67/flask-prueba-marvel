# Prueba tecnica
Proyecto realizado en el framework flask de python, para esta prueba se creo una REST API, la cual permite llenar una base de datos consultado la api de *[Marvel developers](https://developer.marvel.com)* , también permite realizar las operaciones básicas de lectura, escritura, actualización y eliminación(CRUD) de la base de datos

# Requisitos
Antes de correr el proyecto se debe tener en cuenta lo siguiente:
- Se deben instalar los paquetes necesarios, los cuales se encuentran listados en el archivo "requirementes.txt", para se esto se puede correr el comando `pip install -r requirements.txt`
- Al trabajar con una base de datos local y por seguridad, algunas variables se trabajan como variables de entorno, se debe crear el archivo ".env" en la raiz del proyecto, siguiendo el ejemplo del archivo ".env.example" y asignar las variables correspondientes.
-La API de marvel requiere los siguientes parametros "`t=1`" correspondiente a un timestamp, `apikey=` la cual es la llave publicada proporcionada por la página mencionada anteriormente y el `hash= md5(ts+privateKey+publicKey)` el cual es un hash creado mediante el algoritmo de reducción criptografico md5

# Correr el proyecto

- Al estar creado en Flask este proyecto puede ejecutarse mediante el comando `flask --app src/app run` o `python src/app.py`

# Funciones principales

> /consultarHeroesApi método=GET
<br>

Permite consultar la API de Marvel y realizar el llenado y actualización de la base de datos, en caso de que los registros no existan, en caso de que los nombres no coincidan actualizará el registro con la información de la API

>/actualizarHeroes método=PUT
<br>

Permite al usuario modificar el nombre de un Heroe en la base de datos mediante su ID

>/obtenerHeroes método=GET
<br>

Permite consultar todos los registros en la base de datos

>/obtenerHeroe/<Id> método=GET
<br>

Permite consultar un Heroe en la base de datos mediante su ID

> /borrarHeroes método=DELETE
<br>

Permite borrar un Heroe a la vez de la base de datos 

# Autor

Proyecto creado por: Juan Camilo Arango Valle <br>
GitHub del repositorio: *[flask-pruebatecnica-marvel](https://github.com/jcav67/flask-prueba-marvel)*<br>
Fecha: 11/1/2022