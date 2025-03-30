# Scrapy settings for scrapy_empleos project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
BOT_NAME = "scrapy_empleos"

SPIDER_MODULES = ["scrapy_empleos.spiders"]
NEWSPIDER_MODULE = "scrapy_empleos.spiders"

ROBOTSTXT_OBEY = True

DB_HOST = 'localhost'  # O la IP del servidor
DB_DATABASE = 'posgrado'
DB_USER = 'admin'
DB_PASSWORD = 'Sarita_1' \
#POSTGRES_PORT = '5432'  # Puerto por defecto

# Middleware de Pipelines
ITEM_PIPELINES = {
  #  "scrapy_empleos.pipelines.SQLitePipeline": 300,
    'scrapy_empleos.pipelines.LimpiezaDatosPipeline': 300,  #dato nuevo insertado
    'scrapy_empleos.pipelines.JobCollectorPipeline': 300,
    
}



# Configuración para ejecutar cada 2 días con un cronjob
FEED_FORMAT = "json"
FEED_URI = "empleos.json"
