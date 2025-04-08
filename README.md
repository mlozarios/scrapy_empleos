# scrapy_empleos
Nombre del proyecto scrapy_empleos

# Extrae la informacion de empleos usando Scrapy
    Extrae información de las paginas:
    - trabajando.com.bo
    - trabajito.com.bo
## se extrajeron los siguientes campos:
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
    

# Limpieza de datos
    - Normaliza caracteres mal codificados
    - Elimina todos los caracteres no alfanuméricos excepto espacios, tildes y la ñ"""
    - Normaliza caracteres mal codificados (tildes y ñ)
    - Reemplaza caracteres no alfanuméricos (excepto espacios y acentos)
    - Reemplaza múltiples espacios por un solo espacio
    - Eliminar emoticos y emojis
    - Elimina URLs
    - Convertir todos los textos a minúsculas y eliminar espacios innecesarios

 ## Realiza la conección con la bd posgrado
 - Luego de conectar a la bd posgrado 
 - Crea la tabla job_data
 - Inserta cada registro extraido a la tabla job_data

 ## ejecutar el programa
 - scrapy crawl empleo -o empleo.json
 - 
 - 
 

