import requests
from bs4 import BeautifulSoup
import time


class ScrapNames:    
    def getNames(self, id):
        array_of_names = []

        # Adding names from database
        array_of_names.append(self.getFromOpenData(id))
        array_of_names.append(self.getFromNomis(id))
        array_of_names.append(self.getFromUaRegion(id))
        return self.getFirstName(array_of_names)

    def getFirstName(self, array):
        for i in range(len(array)-1):
            if array[i] != None:
                return array[i]
        return "Ім`я керівника не знайдено"

    def getFromOpenData(self, id):
        # Creating request
        r = requests.get(f'https://opendatabot.ua/c/{id}?from=search', verify=False)
        if str(r.status_code) == "404":
            return None
        soup = BeautifulSoup(r.content, 'html.parser')

        # Finding of element    
        c = soup.find_all('div', {"class": "col-sm-4 col-6 col print-responsive"})
        for i in range(len(c)):
            if "Директор" in c[i].text:
                return c[i].text.replace("Директор", '') 

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
        c = soup.find_all('div', {"class": "row line-description"})
        nameOfMan = ''

        for i in range(len(c)):
            if "Директор:" in c[i].text:
                nameOfMan = c[i].text.replace("Директор:", "").split("(")[0].replace('\n', '')
                break

        nameOfMan = nameOfMan.strip().split()

        # Join the words back together with a single space between them
        nameOfMan = ' '.join(nameOfMan)
        return nameOfMan

    def getFromUaRegion(self, id):
        # Creating request
        r = requests.get(f'https://www.ua-region.com.ua/{id}', verify=False)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Finding of element    
        c = soup.find_all("div", {"class": "company-sidebar__item"})
        for i in range(len(c)):
            if "Керівник" in c[i].text:
                return c[i].text.replace("Керівник", '')