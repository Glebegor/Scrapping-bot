import requests
from bs4 import BeautifulSoup
import time

class ScrapperBot:
    def __init__(self, scrapNumbers, scrapNames, scrapSites, scrapAddress):
        self.scrapNumbers = scrapNumbers
        self.scrapNames = scrapNames
        self.scrapSites = scrapSites    
        self.scrapAddress = scrapAddress    

    def getInfo(self, id):
        numbers = self.scrapNumbers.getNumbers(id)
        time.sleep(5)
        names = self.scrapNames.getNames(id)
        time.sleep(5)
        sites = self.scrapSites.getSites(id)
        time.sleep(5)
        address = self.scrapAddress.getAddress(id)

        return {"Numbers": numbers, "Name": names, "Site": sites, "Address": address}

    