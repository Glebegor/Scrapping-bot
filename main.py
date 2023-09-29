from tb import TableBot
from sb import ScrapperBot
from packages.numbers import ScrapNumbers
from packages.names import ScrapNames
from packages.sites import ScrapSites
from packages.address import ScrapAddress
import time

class App:
    def __init__(self, scBot, tbBot):
        self.scBot = scBot
        self.tbBot = tbBot

    def Run(self):
        count_of_repeat = self.tbBot.getMaxSizeTable(3)
        
        # Settign start row
        self.tbBot.setStartRow(self.tbBot.getMaxSizeTable(8)+1)
        
        # Main cyclus
        for i in range(self.tbBot.start_row, count_of_repeat):
            print("App working")
            id_of_company = self.tbBot.getId(i)

            listInfo = self.scBot.getInfo(str(id_of_company.value))
            self.tbBot.addToTable(listInfo=listInfo, rowId=i)
            time.sleep(5)
        return

    def Test(self):
        id_of_company = input("Get id from user: ")
        listInfo1 = self.scBot.getInfo(str(id_of_company))
        listInfo2 = self.scBot.getInfo(str(id_of_company))
        listInfo3 = self.scBot.getInfo(str(id_of_company))
        listInfo4 = self.scBot.getInfo(str(id_of_company))
        listInfo5 = self.scBot.getInfo(str(id_of_company))
        print(listInfo1)
        print(listInfo2)
        print(listInfo3)
        print(listInfo4)
        print(listInfo5)
        if listInfo1 == listInfo2 == listInfo3 == listInfo4 == listInfo5:
            print("OK")


if __name__=="__main__":
    # Scrapping init 
    scrapNumb = ScrapNumbers(['-','(',')',';',' ',"\n"])
    scrapNames = ScrapNames()
    scrapSites = ScrapSites()
    scrapAddress = ScrapAddress()

    # Init app 
    scBot = ScrapperBot(scrapNumb, scrapNames, scrapSites, scrapAddress)
    tbBot = TableBot({"Address":'F', "Site":'G', "Name":'H', "Number1":"I", "Number2":"J", "Number3":"K"}, 0, "mainTable", "БГ Черк. Унік.")
    app = App(scBot,tbBot)

    err = app.Run()