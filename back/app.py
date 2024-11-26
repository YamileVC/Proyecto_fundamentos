from flask import Flask, request, jsonify #De flask importamos
from flask_cors import CORS #Intercambio de recursos entre orígenes

app = Flask(__name__) #Inicializa la aplicacion de flask
CORS(app, origins=["http://192.168.1.8:5000"]) #autoriza el envío de solicitudes únicamente desde una dirección IP particular.
# CORS(app, resources={r"/*": {"origins": ["http://localhost:5500", "https://mi-dominio.com"]}})
# CORS(
#     app,
#     supports_credentials=True,
#     origins=["http://localhost:5500"],
# )

@app.before_request #Para revisar las solicitudes
def before_request(): #Función por la que debe pasar la solicitud
    headers = { 
        'Access-Control-Allow-Origin': '*', #Cualquier página web puede hacer solicitudes al servidor
        'Access-Control-Allow-Methods': "GET, POST", #Define los métodos HTTP permitidos
        'Access-Control-Allow-Headers': "Content-Type" #Permite ciertos encabezados como Content-Type (Indica el tipo de medio en el contenido)
    }
    if request.method == 'OPTIONS' or request.method == 'options': #Para verificar si la solicitud cuenta con métodos permitidos en el servidos. (Get y Post)
        return jsonify(headers), 200 #Si se cumple, la solicitud se procesó correctamente

listado_productos = [
    {
        "id": 1, #Identificador del producto
        "nombre": "Mocca",
        "descripcion": "Este café es una mezcla deliciosa de espresso, leche vaporizada y jarabe de chocolate. Su sabor combina el amargor del café con la dulzura del chocolate, siempre decorado con crema batida.",
        "imagen": "img/food1.png", #Ruta a una imágen del producto
        "comentarios": [
            "La comida fue espectacular. Claramente, regresaré.", #Lista de los comentarios sobre el producto
        ],
    },
    {
        "id": 2,
        "nombre": "Cappuccino",
        "descripcion": "Bebida de café que combina partes iguales de espresso, leche vaporada y espuma de leche. Su textura cremosa y sabor equilibrado entre el café y la leche lo hacen muy popular. Se le espolvorea con cacao o canela por encima para darle un toque extra de sabor.",
        "imagen": "img/food2.png",
        "comentarios": [
            "Deliciosa bebida.",
        ],
    },
    {
        "id": 3,
        "nombre": "Latte",
        "descripcion": "Bebida que combina leche vaporizada y un toque de espresso, creando un contraste visual y de sabor. Se caracteriza por su textura cremosa, un ligero sabor a café y un aspecto atrayente, con capas distintas de leche y café.",
        "imagen": "img/food3.jpg",
        "comentarios": [
            "Me encanta el amor con el que preparan en esta cafetería.",
        ],
    },
]


@app.route("/productos", methods=["GET"]) #La ruta responde solo a metodo Get
def get_productos(): #Esta recibiendo solicitud get para solicitar datos en la ruta productos
    return jsonify(listado_productos) #Pide la lista de productos, convierte Json y la devuelve

@app.route("/productos", methods=["POST"]) #Crearemos producto, Define que la ruta solo responde a metodo Post
def crear_producto(): #Si se accede al URL "/productos" se ejecuta la función
    idNuevoProducto = len(listado_productos) + 1 #se genera un nuevo ID para el producto que se va a crear +1 pasa a siguiente
    listado_productos.append({ #Se agrega el producto a la lista
        "id": idNuevoProducto, #ID del nuevo producto
        "nombre": request.form["nombre"], #se obtiene del formulario a través de request.form["nombre"], el n ya existe
        "descripcion": request.form["descripcion"], #Se obtiene del formulario
        "imagen": request.form["imagen"], #Se obtiene del formulario
        "comentarios": [] #Lista vacía, no hay comentarios a la creación del nuevo producto
    })
    return jsonify({"mensaje": "OK"}), 200 #Devuelve ok al cliente si la operación fue exitosa.

@app.route("/productos/<int:producto_id>", methods=["GET"]) #<int:producto_id>: En la URL solo acepta enteros.
def get_producto(producto_id):
    producto = next((item for item in listado_productos if item["id"] == producto_id), None)#next: Busca en listado_productos un producto con el ID
    if producto:
        return jsonify(producto) #Si encuentra el producto lo devuelve en JSON; si no, responde con un error 404.
    return jsonify({"error": "Producto no encontrado"}), 404 #Sino hay p retorna error


@app.route("/productos/<int:producto_id>/comentario", methods=["POST"])
def comentar_producto(producto_id): #Busca un producto por su ID
    producto = next((item for item in listado_productos if item["id"] == producto_id), None) #Busca el producto con ID (next), si no encuentra lanza None
    if producto: #Si p existe
        comentario = request.get_data().decode("utf-8") #recupera el comentario y transf. a cadena utf-8
        producto["comentarios"].append(comentario) #Agrega el comentario a lista_comentarios
        return jsonify(producto), 201 #Si esta bien retorna el comentario
    return jsonify({"error": "Producto no encontrado"}), 404 #Si no hay p returna error


if __name__ == "__main__": #Solo ejecuta como programa principal
    app.run(host='0.0.0.0', debug=True) #app.run inicial la aplic. web
#Host: servidos accesible desde cualq lugar
#activa modo depuración, reinicia el servidor automat.ante cambios de código y muestra los errores.