from flask import Flask, request, jsonify # Flask para la aplicación web
from flask_sqlalchemy import SQLAlchemy   # SQLAlchemy para la base de datos
from flask_cors import CORS               # CORS para permitir comunicación con el frontend
import os # Para manejar rutas de archivos de forma segura

app = Flask(__name__)

# Habilita CORS para toda la app
CORS(app)

# --- Configuración de la Base de Datos ---
# Obtiene la ruta absoluta del directorio donde se encuentra este archivo (app.py)
basedir = os.path.abspath(os.path.dirname(__file__))
# Configura la URI de la base de datos para SQLite.
# 'sqlite:///' indica que es un archivo SQLite local.
# os.path.join(basedir, 'database.db') construye la ruta al archivo 'database.db'
# en el mismo directorio que app.py.
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
# Deshabilita una función de seguimiento de modificaciones que consume recursos y no es necesaria
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa SQLAlchemy con la aplicación Flask
db = SQLAlchemy(app)

# --- Definición del Modelo de Tarea (Task) ---
# Esta clase representa la tabla 'task' en tu base de datos
class Task(db.Model):
    # Columna 'id': Clave primaria, entera y autoincremental
    id = db.Column(db.Integer, primary_key=True)
    # Columna 'title': Cadena de texto de hasta 100 caracteres, no puede ser nula (vacía)
    title = db.Column(db.String(100), nullable=False)
    # Columna 'completed': Booleano (True/False), por defecto es False
    completed = db.Column(db.Boolean, default=False)

    # Método para una representación legible del objeto Task (útil para depuración)
    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

    # Método para convertir una instancia de Task a un diccionario Python.
    # Esto es crucial para convertir el objeto de la base de datos a formato JSON
    # que puede ser enviado al frontend.
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

# --- Rutas de la Aplicación Flask (por ahora, solo la de prueba) ---
@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

# --- Ejecución de la Aplicación y Creación de la Base de Datos ---
if __name__ == '__main__':
    # Este bloque asegura que las tablas de la base de datos se creen
    # si no existen, antes de que se inicie el servidor de Flask.
    # El 'app.app_context()' es necesario para que db.create_all()
    # sepa a qué aplicación de Flask y base de datos se refiere
    # cuando se ejecuta fuera de una solicitud web.
    with app.app_context():
        db.create_all() # Crea las tablas definidas por tus modelos (ej. 'Task')
    app.run(debug=True) # Inicia el servidor de desarrollo de Flask en modo depuración
