# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies1

    def process_item(self, item, spider):
        salary = item['salary']
        salary_min, salary_max = self.process_salary(salary.replace('\xa0', ' '))

        item['salary_min'] = salary_min
        item['salary_max'] = salary_max

        item.pop('salary', None)

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        return (self.getMinCompensation(salary), self.getMaxCompensation(salary))

    def getMinCompensation(self, str):
        try:
            numbers = re.findall(r'\d+', str.replace(' ', ''))
            if len(numbers) == 2:
                return int(numbers[0])
            if 'до' in str:
                return None
            else:
                return int(numbers[-1]) if 'от' in str else int(numbers[0])
        except:
            return None

    def getMaxCompensation(self, str):
        try:
            numbers = re.findall(r'\d+', str.replace(' ', ''))
            if len(numbers) == 2:
                return int(numbers[-1])
            if 'от' in str:
                return None
            else:
                return int(numbers[0]) if 'до' in str else int(numbers[-1])
        except:
            return None