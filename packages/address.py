import requests
from bs4 import BeautifulSoup
import time

class ScrapAddress:    
    def getAddress(self, id):
        array_of_address = []

        # Adding names from database
        array_of_address.append(self.getFromOpenData(id))
        array_of_address.append(self.getFromUaRegion(id))
        array_of_address.append(self.getClarity(id))
        return self.getFirstAddress(array_of_address)

    def getFirstAddress(self, array):
        for i in range(len(array)-1):
            if array[i] != None:
                return array[i]
        return ""

    def getFromOpenData(self, id):
        # Creating request
        r = requests.get(f'https://opendatabot.ua/c/{id}?from=search', verify=False)

        if str(r.status_code) == "404":
            return None
        
        soup = BeautifulSoup(r.content, 'html.parser')

        # Finding of element    
        c = soup.find_all('div', {"class": "col-12 col print-responsive"})
        for i in range(len(c)):
            if "Адреса" in c[i].text:
                return c[i].text.replace('Адреса', "")

    def getFromUaRegion(self, id):
        # Creating request 
        r = requests.get(f'https://www.ua-region.com.ua/{id}', verify=False)
        if str(r.status_code) == "404":
            return None

        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Finding of element    
        c = soup.find_all("div", {"class": "company-sidebar__item"})
        for i in range(len(c)):
            if "Юридична" in c[i].text:
                return c[i].text.replace('Юридична адреса', "").replace("\xa0", "")
    
    def getClarity(self, id):
        r = requests.get(f"https://clarity-project.info/edr/{id}", verify=False)
        if str(r.status_code) == "404":
            return None
        soup = BeautifulSoup(r.content, 'html.parser')
        c = soup.find_all("tr")
        for i in range(len(c)):
            if "Адреса:" in c[i].text:
                return c[i].find_all('div')[0].text.replace("\n", "").replace("Запис в ЄДР:","")
        