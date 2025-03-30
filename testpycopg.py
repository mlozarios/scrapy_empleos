import psycopg2
from psycopg2 import OperationalError
from psycopg2 import sql

try:
    conn = psycopg2.connect(
        database="posgrado", 
        user="postgres", 
        host="localhost",
        password="Sarita_1",
        port=5432
    )
    cur = conn.cursor()
    print("Conexión a PostgreSQL establecida correctamente.")

    # Crear la tabla si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_data (
            id SERIAL PRIMARY KEY,
            url TEXT,
            name TEXT,
            empresa TEXT,
            ubicacion TEXT,
            tipo TEXT,
            fecha_publicacion TEXT,
            fecha_vencimiento TEXT,
            job_descripcion TEXT,
            fecha_guardar TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    query = sql.SQL("""
                INSERT INTO job_data (url, name, empresa, ubicacion, tipo, fecha_publicacion, 
                            fecha_vencimiento, job_descripcion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               
            """)

    values = (
                'www.test.com',
                'test_name',
                'test_empresa',
                'test_ubicacion',
                'test_tipo',
                'test_fecha_publicacion',
                'test_fecha_vencimiento',
                'test_job_descripcion'
            )

    cur.execute(query, values)
    conn.commit()
    print("Tabla `job_data` verificada o creada.")

except psycopg2.Error as e:
    print(f"Error de conexión a PostgreSQL: {e}")
    raise
finally:
    cur.close()
    conn.close()