from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="test",
        password="test",
        database="test_db"
    )

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/api/modificar", methods=["POST"])
def modificar_producto():
    datos = request.get_json()
    identificador = datos["id"]
    nombre = datos["nombre"]
    precio = datos["precio"]
    origen = datos["origen"]
    color = datos["color"]
    consulta = "UPDATE productos SET nombre='"+str(nombre)+"', precio='"+str(precio)+"', origen='"+str(origen)+"', color='"+str(color)+"' WHERE id='"+str(identificador)+"';"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(consulta)
    conn.commit()
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)

@app.route("/api/eliminar", methods=["DELETE"])
def eliminar_producto():
    identificador = request.args.get("id")
    consulta = "DELETE FROM productos WHERE id='"+str(identificador)+"'"
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(consulta)
    conn.commit()
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)
