# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import sqlite3
from itemadapter import ItemAdapter
from datetime import datetime
import re
import unicodedata

import os
from datetime import date

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv


from itemadapter import ItemAdapter

class SQLitePipeline:
    def open_spider(self, spider):
        self.conn = sqlite3.connect("empleos.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleos (
                data_id TEXT PRIMARY KEY,
                url TEXT,
                name TEXT,
                empresa TEXT,
                ubicacion TEXT,
                tipo TEXT,
                requisitos TEXT,
                fecha_publicacion TEXT,
                fecha_vencimiento TEXT,
                job_descripcion TEXT,
                fecha_guardar TEXT
                            

            )
        """)
        self.conn.commit()

#conección a postgres

class JobCollectorPipeline:
    def __init__(self) -> None:
        """Inicializa la conexión con la base de datos PostgreSQL."""
        try:

            # Conectar a la base de datos
            self.connection = psycopg2.connect(
                database="posgrado", 
                user="postgres", 
                host="localhost",
                password="Sarita_1",
                port=5432
            )
            self.cur = self.connection.cursor()
            print("✅ Conexión a PostgreSQL establecida correctamente.")

            # Crear la tabla si no existe
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS job_data (
                    id SERIAL PRIMARY KEY,
                    url TEXT UNIQUE,
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
            self.connection.commit()
            print(" Tabla `job_data` verificada o creada.")

        except psycopg2.Error as e:
            print(f"Error de conexión a PostgreSQL: {e}")
            raise

    def process_item(self, item, spider):
        """Inserta los datos extraídos en PostgreSQL."""
        try:
            query = sql.SQL("""
                INSERT INTO job_data (url, name, empresa, ubicacion, tipo, fecha_publicacion, 
                            fecha_vencimiento, job_descripcion, fecha_guardar)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """)

            values = (
                item.get('url'),
                item.get('name'),
                item.get('empresa'),
                item.get('ubicacion'),
                item.get('tipo'),
                item.get('fecha_publicacion'),
                item.get('fecha_vencimiento'),
                item.get('job_descripcion'),
                item.get('fecha_guardar')
            )

            self.cur.execute(query, values)
            self.connection.commit()
            print(f"✅ Insertado en PostgreSQL: {item.get('title')}")
            return item

        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"❌ Error al insertar en PostgreSQL: {e}")
            return item

    def close_spider(self, spider):
        """Cierra la conexión con PostgreSQL al finalizar el spider."""
        try:
            self.cur.close()
            self.connection.close()
            print("✅ Conexión a PostgreSQL cerrada correctamente.")
        except psycopg2.Error as e:
            print(f"❌ Error al cerrar la conexión: {e}")


# para la limpieza de datos con scrappy
from itemadapter import ItemAdapter

class LimpiezaDatosPipeline:

    
    def normalize_text(self, text):
        """
        Normaliza caracteres mal codificados, por ejemplo:
        - 'á' (a + tilde separado) → 'á'
        - 'ñ' (n + tilde separado) → 'ñ'
        """
        return unicodedata.normalize('NFC', text)
    
       
    def clean_text(self, text):
    ##Elimina todos los caracteres no alfanuméricos excepto espacios, tildes y la ñ"""
        if not text or not isinstance(text, str):
            return None  # Devuelve None si el texto es vacío o no es una cadena

    # Normaliza caracteres mal codificados (tildes y ñ)
        text = unicodedata.normalize('NFC', text)


    # Reemplaza caracteres no alfanuméricos (excepto espacios y acentos)
        text = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]', '', text)

    # Reemplaza múltiples espacios por un solo espacio
        text = re.sub(r'\s+', ' ', text).strip()

    # Eliminar emoticos y emojis
        #text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = re.sub(r'[^\w\s.,;:!?¿¡áéíóúÁÉÍÓÚñÑüÜ-]', '', text)
    
        return 
    

def remove_links(self, text):	#Elimina URL desde texto
	if not text:
		return text
    
	#comun patron URL
	url_pattern = r'http[s]?://[a-zA-Z]|[$-_@.&+]|(?:%[0-9a-fA-F]))+'

	# elimina URLs
	text = re.sub(url_pattern,'',text)
	# trat de remover otros posibles formatos
	text = re.sub(r'www\[^\s]+', '', text)
	return text.strip()


def process_item(self, item, spider):
        adapter = ItemAdapter(item)
    

        # Convertir todos los textos a minúsculas y eliminar espacios innecesarios
        for key in adapter.keys():
            if adapter[key] and isinstance(adapter[key], str):
                adapter[key] = adapter[key].strip().lower()

      

        # Validación de fecha: si está vacía, se reemplaza con "fecha desconocida"
        if not adapter.get("fecha_publicacion"):
            adapter["fecha_publicacion"] = "fecha desconocida"
        if not adapter.get("fecha_vencimiento"):
            adapter["fecha_vencimiento"] = "fecha desconocida"
        if not adapter.get("fecha_guardar"):
            adapter["fecha_guardar"] = datetime.now().isoformat()
        

        #Validacion de job_descripcion: si está vacía, se reemplaza con "descripcion desconocida"
        if not adapter.get("job_descripcion"):
            adapter["job_descripcion"] = "descripcion desconocida"
        #Si tiene emojis los elimina
        if adapter.get("job_descripcion"):
            adapter["job_descripcion"] = self.clean_text(adapter["job_descripcion"])

        if adapter.get("job_descripcion"):
            adapter["job_descripcion"] = self.remove_links(adapter["job_descripcion"])

        # Normalizar texto
        return item  # ⬅️ Devuelve el item limpio para su almacenamiento

# def limpiar_fecha(fecha):
#     """
#     Limpia la fecha eliminando caracteres no deseados y convirtiéndola a un formato estándar.
#     """
#     if not fecha:
#         return None  # Devuelve None si la fecha es vacía
#     elif 'horas' in fecha:
#         return date.today()
#     else:
        
#     # Elimina caracteres no deseados (ejemplo: "2023-09-15T00:00:00Z" → "2023-09-15")
#     fecha_limpia = re.sub(r'[^0-9\-]', '', fecha)

#     # Convierte a formato estándar (ejemplo: "2023-09-15" → "YYYY-MM-DD")
#     return fecha_limpia