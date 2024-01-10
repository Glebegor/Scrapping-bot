import requests
from bs4 import BeautifulSoup
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

class TableBot:
    def __init__(self, working_columns, start_column, table_name, page):
        # TableBot info
        self.working_columns = working_columns
        self.start_row = start_column
        self.table_name = table_name
        self.page = page

        # TableBot objects
        self.sbh = None
        self.sheet = None
        self.worksheet = None

    # Main func to add info to table 
    def addToTable(self, listInfo, rowId):
        for value in listInfo:
            if value == "Numbers":
                for i in range(len(listInfo["Numbers"])):
                    self.add(rowId, self.working_columns[f'Number{i+1}'], listInfo[value][i])
            else:
                self.add(rowId, self.working_columns[value], listInfo[value])
        return "End"

    # Max size 
    def getMaxSizeTable(self, column):
        return len(self.worksheet.col_values(column))

    # Getting of id
    def getId(self, rowId):
        return self.worksheet.cell(rowId, 3)
    
    # Add elements to table
    def add(self, rowId, col, value):
        self.worksheet.update(f"{col}{rowId}", value)

    # Set table
    def setTable(self, name, page): 
        # GetScope
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        except:
            return "Credentials.json не був знайдений чи є неправильний"

        # authorize the clientsheet 
        try:
            self.sba = gspread.authorize(credentials)
        except:
            return "Неправильний файл credentials.json"
        
        try:
            self.sheet = self.sba.open(name)
        except: 
            return "Таблиця не була знайдена чи ви не маєте доступу, також перевірте інтернет з'єднання."
        
        try:
            self.worksheet = self.sheet.worksheet(page)
        except:
            return "Аркуш в таблиці не був знайдений"
        return None

    def setStartRow(self, row):
        self.start_row = row

    def get_info_from_user(self, tableName, tablePage,startRow):
        self.table_name = tableName
        self.page = tablePage
        self.start_row = startRow
