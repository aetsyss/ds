# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from jobparser.salary_parsers.HHSalaryParser import HHSalaryParser
from jobparser.salary_parsers.SJSalaryParser import SJSalaryParser


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies

    def process_item(self, item, spider):
        salary = item['salary']

        salary_min = None
        salary_max = None

        if spider.name == 'hhru':
            salary_parser = HHSalaryParser(salary.replace('\xa0', ' '))
            salary_min = salary_parser.get_min_compensation()
            salary_max = salary_parser.get_max_compensation()

        if spider.name == 'sjru':
            salary_parser = SJSalaryParser(salary)
            salary_min = salary_parser.get_min_compensation()
            salary_max = salary_parser.get_max_compensation()

        item['salary_min'] = salary_min
        item['salary_max'] = salary_max

        item.pop('salary', None)

        collection = self.mongo_base['jobs']
        collection.insert_one(item)

        return item
