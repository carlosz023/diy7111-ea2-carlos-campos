import os
import time
from flask import Flask
import psycopg2

app = Flask(__name__)

def get_db_connection():
    for i in range(5):
        try:
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'vzeta-db'),
                database=os.environ.get('DB_NAME', 'vzeta_matrix'),
                user=os.environ.get('DB_USER', 'vzeta_user'),
                password=os.environ.get('DB_PASSWORD', 'vzeta_password')
            )
            return conn
        except psycopg2.OperationalError:
            time.sleep(2)
    return None

@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        return "Error al conectar con la Base de Datos VZeta", 500
    
    cur = conn.cursor()
    # Crear la tabla si no existe
    cur.execute('CREATE TABLE IF NOT EXISTS visitas (id SERIAL PRIMARY KEY, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')
    # Insertar un registro de visita
    cur.execute('INSERT INTO visitas DEFAULT VALUES;')
    conn.commit()
    
    # Contar las visitas totales
    cur.execute('SELECT COUNT(*) FROM visitas;')
    total_visitas = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>VZeta - Control de Visitas</title>
        <style>
            body {{ background-color: #f0f2f5; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ background-color: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 100%; }}
            h1 {{ color: #333; }}
            .counter {{ font-size: 3rem; font-weight: bold; color: #28a745; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Empresa VZeta</h1>
            <p>Monitoreo de Infraestructura Virtualizada</p>
            <div class="counter">{total_visitas}</div>
            <p>Visitas acumuladas (Persistencia Activa)</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
