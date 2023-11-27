import requests
from bs4 import BeautifulSoup
import time

class ScrapSites:    
    def getSites(self, id):
        # Adding sites from database
        return self.getFromNomis(id)

    def getFromNomis(self, id):
        # Creating request
        r = requests.get(f'https://nomis.com.ua/ru/{id}', verify=False)
        if str(r.status_code) == "404":
            return 'Сайт не був знайдений'
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Check if company found
        c = soup.find_all("div", {"class": "title"})
        if len(c) != 0 and c[0].text == "404":
            return 'Сайт не був знайдений'

        # Finding of element    
        c = soup.find_all('div', {"class": "row line-description paper_block"})
        for i in range(len(c)):
            if "Веб-сайт:" in c[i].text:
                siteName = c[i].text.replace("Веб-сайт:", "").replace(" ", "").replace('\n','').replace(";", "; ")
                if siteName == "Информацияуточняется" or siteName == None or siteName == " " or siteName == '':
                    return "Інформація уточнюється" 
                return siteName
        return 'Сайт не був знайдений'