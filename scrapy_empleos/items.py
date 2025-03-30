# Define here the models for your scraped items
#

import scrapy


class EmpleoItem(scrapy.Item):
    # define los campos para tu articulos aqui como un diccionario
    data_id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    empresa = scrapy.Field()
    ubicacion = scrapy.Field()
    tipo = scrapy.Field()
   # requisitos = scrapy.Field()
    fecha_publicacion = scrapy.Field()
    fecha_vencimiento = scrapy.Field()
    job_descripcion = scrapy.Field()
    fecha_guardar = scrapy.Field()




