import  re

class HHSalaryParser:
    def __init__(self, data):
        self.str = data

    def getMinCompensation(self):
        try:
            numbers = re.findall(r'\d+', self.str.replace(' ', ''))
            if len(numbers) == 2:
                return int(numbers[0])
            if 'до' in self.str:
                return None
            else:
                return int(numbers[-1]) if 'от' in self.str else int(numbers[0])
        except:
            return None

    def getMaxCompensation(self):
        try:
            numbers = re.findall(r'\d+', self.str.replace(' ', ''))
            if len(numbers) == 2:
                return int(numbers[-1])
            if 'от' in self.str:
                return None
            else:
                return int(numbers[0]) if 'до' in self.str else int(numbers[-1])
        except:
            return None

#salary = 'от 250 000 руб.'
#salary = 'до 5000 USD'
#salary = '150000 – 220000 руб.'
#salary = 'з/п не указана'
salary = 'от 170 000 до 220 000 руб.'

hh = HHSalaryParser(salary)
print(hh.getMinCompensation())
print(hh.getMaxCompensation())