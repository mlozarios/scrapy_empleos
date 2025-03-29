import scrapy
import uuid
from datetime import datetime
from scrapy_empleos.items import EmpleoItem
#from data_web import CITIES, BASE_URLS, ALLOWED_DOMAINS, HEADERS

class EmpleoSpider(scrapy.Spider):
    name = "empleo"
    start_urls = ["https://trabajando.com.bo/trabajo", "https://trabajito.com.bo/trabajo"]

    def parse(self, response):
        url_site = response.url
        if 'trabajando' in url_site:
            empleo_page_links = response.css("h2.views-field-title a::attr(href)").getall()
            yield from response.follow_all(empleo_page_links, self.parse_trabajando)
            yield from response.follow_all(response.css('a[title="Ir a la página siguiente"]'), self.parse)

        elif 'trabajito' in url_site:
            for job in response.css("div.job-block"):
                job_link = job.css("h4 a::attr(href)").get()
                tipo = job.css("li.time::text").get(default="No especificado").strip()
                if job_link:
                    yield response.follow(job_link, self.parse_trabajito, meta={"tipo": tipo})
            yield from response.follow_all(response.css('a[rel="next"]'), self.parse)

    def parse_trabajando(self, response):
        item = EmpleoItem()
        item["data_id"] = str(uuid.uuid4())
        item["url"] = response.url
        item["name"] = response.css("h1.trabajando-page-header > span::text").get(default="").strip()
        item["empresa"] = response.css("div.views-field-field-nombre-empresa a::text").get(default="").strip()
        item["ubicacion"] = response.css("div.views-field-field-ubicacion-del-empleo > div::text").get(default="No especificado").strip()
        item["tipo"] = response.css("div.views-field-field-tipo-empleo > div::text").get(default="No especificado").strip()
        item["requisitos"] = response.xpath("//li[h5[contains(text(),'Requisitos:')]]/span/text()").get(default="No especificado")
        item["fecha_publicacion"] = response.css("div.views-field-created time::text").get(default="No especificado").strip()
        item["fecha_vencimiento"] = response.css("div.views-field-field-fecha-empleo-1 > div::text").get(default="No especificado").strip()
        item["job_descripcion"] = response.css('div.field--type-text-with-summary div.field--item p::text').getall()
        item["fecha_guardar"] = datetime.now().isoformat()
        yield item

    def parse_trabajito(self, response):
        item = EmpleoItem()
        item["data_id"] = str(uuid.uuid4())
        item["url"] = response.url
        item["name"] = response.css("h1.JobViewTitle::text").get(default="").strip()
        item["empresa"] = response.css("h2::text").get(default="No especificado").strip()
        item["ubicacion"] = response.xpath("//li[h5[contains(text(),'Ubicación:')]]/span/text()").get(default="No especificado")
        item["tipo"] = response.meta.get("tipo", "No especificado")
        item["fecha_publicacion"] = response.xpath("//li[h5[contains(text(),'Fecha de publicación:')]]/span/text()").get(default="No especificado")
        item["fecha_vencimiento"] = response.xpath("//li[h5[contains(text(),'Fecha de caducidad:')]]/span/text()").get(default="No especificado")
        item["job_descripcion"] = response.css('div.job-detail.only-text p::text').getall()
        item["fecha_guardar"] = datetime.now().isoformat()
        yield item