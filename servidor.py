
from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(__name__)

# Inicializa la base de datos SQLite
def init_db():
    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            contraseña TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Función para hashear contraseñas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registro de usuario
@app.route('/registro', methods=['POST'])
def registrar():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = hash_password(data.get('contraseña'))

    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)', (usuario, contraseña))
        conn.commit()
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 400
    finally:
        conn.close()

# Inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contraseña = hash_password(data.get('contraseña'))

    conn = sqlite3.connect('tareas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?', (usuario, contraseña))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"mensaje": f"Bienvenido, {usuario}"}), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401

# Ruta para mostrar HTML de bienvenida
@app.route('/tareas', methods=['GET'])
def tareas():
    return '''
        <h1>Bienvenido a tu Gestor de Tareas</h1>
        <p>Has iniciado sesión correctamente.</p>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
