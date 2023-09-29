import requests
from bs4 import BeautifulSoup
import time

class ScrapNumbers:
    def __init__(self, array_of_symbols):
        self.array_of_symbols = array_of_symbols 

    def getNumbers(self,id):
        array_of_numbers = []

        # Adding numbers from database
        array_of_numbers.append(self.getFromOpenData(id))
        array_of_numbers.append(self.getFromNomis(id))
        array_of_numbers.append(self.getFromUaRegion(id))

        array_of_numbers = self.deleteNone(array_of_numbers)
        # long mess test
        for i in range(len(array_of_numbers)-1):
            if len(array_of_numbers[i]) != 13:
                array_of_numbers.pop(i)

        filtered_array = self.getArrayNotRepeat(array_of_numbers)
        if len(filtered_array) == 1 and filtered_array[0] == None:
            return ["Телефон не був знайдений"]
        return filtered_array

    def getArrayNotRepeat(self, array):
        for i in range(len(array)-1):
            for j in range(len(array)-1):
                if array[i] == array[j]:
                    array.pop(j)
        return array

    def deleteNone(self, array):
        for i in range(len(array)-1):
            if array[i] == None:
                array.pop(i)
        if len(array) == 1:
            return ["Телефон не був знайдений"]
        return array

    def getFromOpenData(self, id):
        # Creating request
        r = requests.get(f'https://opendatabot.ua/c/{id}?from=search')
        if str(r.status_code) == "404":
            return None

        soup = BeautifulSoup(r.content, 'html.parser')

        # Finding of element    
        c = soup.find_all('a', {"data-v-d1614ea6": ""})
        for el in c:
            # Check if href not empty
            if not len(el.get_text()) == 0 :
                if el.get_text()[0] == "+":
                    # Getting nubmer
                    return el["href"][4:]
        return None

    def getFromNomis(self, id):
        # Creating request
        r = requests.get(f'https://nomis.com.ua/ru/{id}')
        if str(r.status_code) == "404":
            return None
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Check if company found
        c = soup.find_all("div", {"class": "title"})
        if len(c) != 0 and c[0].text == "404":
            return None

        # Finding of element    
        c = soup.find_all('div', {"class": "answ text col-xs-9 col-xxs-12 grey"})[1]
        number = c.text.split(':')[1].split(';')[0]
        for i in range(len(self.array_of_symbols)-1):
            number = number.replace(self.array_of_symbols[i], "")
        if number[0] == "+":
            if number[1] == "3" and number[2] == "8" and number[3] == "0":
                return number
        else:
            if number[0] == "3" and number[1] == "8" and number[2] == "0":
                return "+" + number
            else:
                return "+38" + number

    def getFromUaRegion(self, id):
        # Creating request
        r = requests.get(f'https://www.ua-region.com.ua/{id}')
        if str(r.status_code) == "404":
            return None

        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Finding of element    
        c = soup.find(self.has_tel_href)
        if c == None:
            return None
        return c['href'][4:]

    def has_tel_href(self, tag):
        return tag.name == 'a' and tag.get('href', '').startswith('tel:')