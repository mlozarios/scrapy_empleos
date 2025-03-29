# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

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

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO empleos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["data_id"],
            item["url"],
            item["name"],
            item["empresa"],
            item["ubicacion"],
            item["tipo"],
            item["requisitos"],
            item["fecha_publicacion"],
            item["fecha_vencimiento"],
            " ".join(item["job_descripcion"]),
            item["fecha_guardar"]
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()


# para la limpieza de datos con scrappy
import logging
from datetime import datetime

class LimpiezaDatosPipeline:
    def process_item(self, item, spider):
        """
        Procesa cada ítem antes de guardarlo, validando y limpiando sus valores.
        """
        item["name"] = self.limpiar_texto(item.get("name"))
        item["empresa"] = self.limpiar_texto(item.get("empresa"))
        item["ubicacion"] = self.limpiar_texto(item.get("ubicacion"))
        item["tipo"] = self.limpiar_texto(item.get("tipo"))
        item["requisitos"] = self.limpiar_texto(item.get("requisitos"))
        item["fecha_publicacion"] = self.limpiar_fecha(item.get("fecha_publicacion"))
        item["fecha_vencimiento"] = self.limpiar_fecha(item.get("fecha_vencimiento"))
        item["job_descripcion"] = self.limpiar_descripcion(item.get("job_descripcion"))

        return item

    def limpiar_texto(self, valor):
        """Limpia espacios en blanco y caracteres especiales en textos."""
        if valor:
            valor = valor.strip()  # Elimina espacios al inicio y fin
            valor = re.sub(r'\s+', ' ', valor)  # Sustituye múltiples espacios por uno
            return valor
        return "No especificado"

    def limpiar_fecha(self, valor):
        """Convierte fechas a formato estándar YYYY-MM-DD."""
        if valor:
            try:
                return datetime.strptime(valor, "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                logging.warning(f"Fecha inválida: {valor}")
        return "No especificado"

    def limpiar_descripcion(self, lista):
        """Limpia y une las líneas de descripción en un solo texto."""
        if lista and isinstance(lista, list):
            texto_limpio = " ".join([self.limpiar_texto(linea) for linea in lista])
            return texto_limpio
        return "No especificado"        