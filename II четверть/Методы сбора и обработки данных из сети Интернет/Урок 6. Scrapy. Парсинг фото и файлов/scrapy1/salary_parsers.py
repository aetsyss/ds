import  re

def getMinCompensation(str):
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

def getMaxCompensation(str):
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

#salary = 'от 250 000 руб.'
#salary = 'до 5000 USD'
#salary = '150000 – 220000 руб.'
#salary = 'з/п не указана'
salary = 'от 170 000 до 220 000 руб.'
print(getMinCompensation(salary))
print(getMaxCompensation(salary))