from flask import Flask, request, jsonify
import os
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306)),
        connection_timeout=5
    )

@app.route('/')
def hello_world():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados)


@app.route("/api/modificar", methods=["POST"])
def modificar_producto():
    datos = request.get_json()
    identificador = datos["id"]
    nombre = datos["nombre"]
    precio = datos["precio"]
    consulta = "UPDATE productos SET nombre='"+str(nombre)+"', precio='"+str(precio)+"' WHERE id='"+str(identificador)+"';"
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







