# from czaSpider.items import czaBaseItem, process_base_item
from czaSpider.czaTools import *
from .czaBaseItem import czaBaseItem, process_base_item


class Item(czaBaseItem):
    job_name = scrapy.Field()
    job_salary = scrapy.Field()
    job_palce = scrapy.Field()
    job_experience = scrapy.Field()
    job_education = scrapy.Field()
    job_welfare = scrapy.Field()
    company_name = scrapy.Field()
    company_nature = scrapy.Field()
    company_scale = scrapy.Field()

def jobPositionItem(**kwargs):
    item = Item()
    item.update(process_base_item(**kwargs))

    item["job_name"] = kwargs.pop('job_name', None)
    item["job_salary"] = kwargs.pop('job_salary', None)
    item["job_palce"] = kwargs.pop('job_palce', None)
    item["job_experience"] = kwargs.pop('job_experience', None)
    item["job_education"] = kwargs.pop('job_education', None)
    item["job_welfare"] = kwargs.pop('job_welfare', None)
    item["company_name"] = kwargs.pop('company_name', None)
    item["company_nature"] = kwargs.pop('company_nature', None)
    item["company_scale"] = kwargs.pop('company_scale', None)
    return item
