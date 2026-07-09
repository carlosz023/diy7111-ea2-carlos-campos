import os
import time
from flask import Flask
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'vzeta-db')
DB_USER = os.environ.get('DB_USER', 'vzeta_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'vzeta_password')
DB_NAME = os.environ.get('DB_NAME', 'vzeta_db')

def init_db():
    # Paso 1: Conectarse a la DB base 'postgres' para asegurar que 'vzeta_db' exista
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database='postgres',
                user=DB_USER,
                password=DB_PASSWORD
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            
            # Verificar si existe vzeta_db
            cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}';")
            exists = cur.fetchone()
            if not exists:
                cur.execute(f"CREATE DATABASE {DB_NAME};")
                print(f"Base de datos {DB_NAME} creada con éxito.")
            
            cur.close()
            conn.close()
            break
        except Exception as e:
            print("Esperando inicialización de Postgres...", e)
            time.sleep(2)

    # Paso 2: Conectarse a 'vzeta_db' y crear la tabla de visitas
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS visitas (
                    id SERIAL PRIMARY KEY,
                    contador INTEGER DEFAULT 0
                );
            ''')
            cur.execute("SELECT COUNT(*) FROM visitas;")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO visitas (contador) VALUES (0);")
            conn.commit()
            cur.close()
            conn.close()
            print("Tabla de visitas e inicialización completada.")
            break
        except Exception as e:
            print("Configurando tablas en vzeta_db...", e)
            time.sleep(2)

@app.route('/')
def hello():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute("UPDATE visitas SET contador = contador + 1 WHERE id = 1 RETURNING contador;")
        count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Error en la base de datos: {e}", 500
    
    return f"""
    <html>
    <head>
        <title>VZeta - Control de Visitas</title>
        <style>
            body {{ background-color: #f0f2f5; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: center; }}
            h1 {{ color: #1a73e8; }}
            .counter {{ font-size: 48px; font-weight: bold; color: #34a853; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Evaluación Final Transversal - VZeta</h1>
            <p>Estudiante: Carlos Campos</p>
            <div class="counter">{count}</div>
            <p>Visitas registradas en PostgreSQL de forma persistente.</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
