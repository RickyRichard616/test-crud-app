from flask import Flask, request, jsonify
import os
import mysql.connector

app = Flask(__name__)
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
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






