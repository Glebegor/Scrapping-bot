import requests
from bs4 import BeautifulSoup
import time

class ScrapNumbers:
    def __init__(self, array_of_symbols):
        self.array_of_symbols = array_of_symbols 

    def getNumbers(self,id):
        array_of_numbers = []

        # Adding numbers from database
        uareg = self.getFromUaRegion(id)
        if uareg != None:
            array_of_numbers.extend(self.getFromUaRegion(id))
        nomin = self.getFromNomis(id)
        if nomin != None:
            array_of_numbers.extend(nomin)
        opendata = self.getFromOpenData(id)
        if opendata != None:
            array_of_numbers.extend(opendata)

        filtered_array = self.notNone(array_of_numbers)
        filtered_array = list(set(filtered_array))
        if len(filtered_array) == 0:
            return ["Телефон не був знайдений"]
        if len(filtered_array) > 4:
            return filtered_array[:1]
        if len(filtered_array) > 5:
            return filtered_array[:2]
        if len(filtered_array) > 6:
            return filtered_array[:3]
        return filtered_array

    def notNone(self,array):
        filtered_array = []
        for val in array:
            if val != None :
                filtered_array.append(val)
        return filtered_array

    def getFromOpenData(self, id):
        # Creating request
        r = requests.get(f'https://opendatabot.ua/c/{id}?from=search', verify=False)
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
                    return [str(el["href"][4:])]
        return None

    def getFromNomis(self, id):
        # Creating request
        r = requests.get(f'https://nomis.com.ua/ru/{id}', verify=False)
        if str(r.status_code) == "404":
            return None
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Check if company found
        c = soup.find_all("div", {"class": "title"})
        if len(c) != 0 and c[0].text == "404":
            return None

        # Finding of element    
        try: 
            c = soup.find_all('div', {"class": "answ text col-xs-9 col-xxs-12 grey"})[1]
        except:
            return None
        numbers = c.text.replace("\n",'').split(";")
        filtered_numbers = []
        for i in range(len(numbers)-1):
            filtered_numbers.append(numbers[i].split(":")[1].replace(' ', '').replace('-', '').replace('(', '').replace(')', ''))
        
        if len(filtered_numbers)==0:
            return None

        for i in range(len(filtered_numbers)):
            if '@' in filtered_numbers[i]:
                filtered_numbers[i] = None
            elif len(filtered_numbers[i])==13:
                continue
            elif len(filtered_numbers[i]) < 9 or len(filtered_numbers[i]) > 13:
                filtered_numbers[i] = f"Неправильний номер телефону: {filtered_numbers[i]}"
            elif len(filtered_numbers[i])==9:
                filtered_numbers[i] = f"+380{filtered_numbers[i]}"
            elif len(filtered_numbers[i])==10:
                filtered_numbers[i] = f"+38{filtered_numbers[i]}"
            elif len(filtered_numbers[i])==11:
                filtered_numbers[i] = f"+3{filtered_numbers[i]}"
            elif len(filtered_numbers[i])==12:
                filtered_numbers[i] = f"+{filtered_numbers[i]}"

        return filtered_numbers 

    def getFromUaRegion(self, id):
        # Creating request
        r = requests.get(f'https://www.ua-region.com.ua/{id}', verify=False)
        if str(r.status_code) == "404":
            return None

        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Finding of element    
        c = soup.find_all(self.has_tel_href)

        array_of_numbers = []
        for i in range(len(c)):
            array_of_numbers.append(c[i]['href'][4:])

        if len(array_of_numbers)==0:
            return None

        return array_of_numbers

    def has_tel_href(self, tag):
        return tag.name == 'a' and tag.get('href', '').startswith('tel:')