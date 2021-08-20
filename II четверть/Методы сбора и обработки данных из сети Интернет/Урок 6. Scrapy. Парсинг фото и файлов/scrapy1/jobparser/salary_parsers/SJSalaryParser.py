import re

class SJSalaryParser:
    def __init__(self, data):
        self.str = data

    def get_min_compensation(self):
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

    def get_max_compensation(self):
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
