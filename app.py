from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
import threading
import time
import webbrowser
import os
import requests

class Client:
    def __init__(self, fonts,sizeW,sizeH, app):
        # 1-header, 2-text, 3-nessesary info
        self.fonts = fonts

        self.sizeH = sizeH
        self.sizeW = sizeW
        # Creating main window
        self.client = Tk()
        self.client.title("Скрапінг компаній")
        self.client.geometry(f"{self.sizeW}x{self.sizeH}")
        self.client.resizable(False, False)
        self.client.configure(background="#fff")

        # Setting options of frame
        self.main_style = ttk.Style()
        self.main_style.configure("MainFrame", background="#fff")
        self.main_style.configure('MainFrame.TFrame', background='#fff')

        self.main_frame = ttk.Frame(self.client, style="MainFrame.TFrame", padding=10)
        self.main_frame.grid()

        self.app = app
        
        # Async functions
        self.event = threading.Event()
        self.event.set()

        title = ttk.Label(self.main_frame, background="#fff", text="Программа для завантаження даних про компанії в гугл таблиці!", font=self.fonts[0], wraplength=400).grid(column=0,row=0)
        container = ttk.Frame(self.main_frame, style="MainFrame.TFrame")
        l1, i1 = self.createInputAndLable(container, "Введіть ім`я таблиці")
        l1.grid(pady=(10,0),column=0,row=5, sticky="w")
        i1.grid(column=0,row=6, sticky="w")
        l2, i2 = self.createInputAndLable(container, "Введіть ім`я аркуша таблиці")
        l2.grid(pady=(10,0),column=0,row=7, sticky="w")
        i2.grid(column=0,row=8, sticky="w")
        l3, i3 = self.createInputAndLable(container, "Введіть з якого рядка почати парсинг(Нічого не вводіть якщо хочете щоб вибрався перший незаповнений рядок в колонці 'Ім`я директора')")
        l3.grid(pady=(10,0),column=0,row=9, sticky="w")
        i3.grid(column=0,row=10, sticky="w")
        self.button = ttk.Button(container, text="Почати парсинг", command=lambda: self.start_call_back(i1.get(), i2.get(), i3.get()))
        self.button_stop = ttk.Button(container, text="Закінчити", command=self.stop_call_back)
        self.button_help = ttk.Button(self.main_frame, text="Як це працює?", command=self.openHelpFile)
        self.button_paste1 = ttk.Button(container, text="Вставити", command=lambda: i1.event_generate("<<Paste>>"))
        self.button_paste2 = ttk.Button(container, text="Вставити", command=lambda: i2.event_generate("<<Paste>>"))
        self.button_paste3 = ttk.Button(container, text="Вставити", command=lambda: i3.event_generate("<<Paste>>"))
        self.button.grid(pady=(20,0),padx=(0,70),column=0, row=11)
        self.button_stop.grid(pady=(20,0),padx=(100,0),column=0, row=11)
        self.button_help.grid(pady=(20,0),padx=(10,0),column=0, row=3)
        self.button_paste1.grid(padx=(190,0), column=0, row=6 )
        self.button_paste2.grid(padx=(190,0), column=0, row=8 )
        self.button_paste3.grid(padx=(190,0), column=0, row=10 )
        container.grid(pady=20)
        self.button_stop.config(state=tk.DISABLED)

    def pasteInfo(self, button):
        pass

    def Run(self):
        self.client.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.client.mainloop()

    def createInputAndLable(self, frame, text):
        label = ttk.Label(frame, background="#fff", text=text, font=self.fonts[1], wraplength=200, anchor="w", justify="left")
        inputPole = ttk.Entry(frame, background="#fff", font=self.fonts[2])
        return (label, inputPole)
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Ви точно хочете вийти?"):
            self.event.set()
            self.button_stop.config(state=tk.DISABLED)
            self.client.destroy()
            
    def call_back(self, tableName, tablePage, startRow):
        self.app.tbBot.get_info_from_user(tableName, tablePage, startRow)
            
        err = self.app.tbBot.setTable(tableName, tablePage)
        if err != None:
            print(err)
            self.event.set()
            self.button_stop.config(state=tk.DISABLED)
            self.button.config(state=tk.NORMAL)
            messagebox.showerror("Помилка", err)
            return
        else:
            print("All good")

        count_of_repeat = self.app.tbBot.getMaxSizeTable(3)
        if startRow == '':
            self.app.tbBot.setStartRow(self.app.tbBot.getMaxSizeTable(8))
            start_of_repeat = int(self.app.tbBot.start_row)+1
        else:
            self.app.tbBot.setStartRow(startRow)
            start_of_repeat = int(self.app.tbBot.start_row)

            
        # Main cyclus
        i = start_of_repeat if start_of_repeat != '' else 0
        while i < count_of_repeat+1:
            try:
                if self.event.is_set():
                    print("Function ended working")
                    self.button.config(state=tk.NORMAL)
                    # self.client.destroy()
                    break
                print("App working")

                id_of_company = self.app.tbBot.getId(i)
                if self.event.is_set():
                    print("Function ended working")
                    self.button.config(state=tk.NORMAL)
                    # self.client.destroy()
                    break
                listInfo = self.app.scBot.getInfo(str(id_of_company.value))
                if self.event.is_set():
                    print("Function ended working")
                    self.button.config(state=tk.NORMAL)
                    # self.client.destroy()
                    break
            except requests.exceptions.ConnectTimeout:
                messagebox.showerror('Проблема на стороні сервера', 'Триває повторне підключення до серверу!')
            except:
                messagebox.showerror('Проблема на стороні сервера', 'Немає підключення до інтернету!')
                messagebox.showinfo("Кінець програми", "Опрацювання даних перервано")
                self.event.clear()
                self.button.config(state=tk.NORMAL)
                self.button_stop.config(state=tk.DISABLED)
                return

            try:
                self.app.tbBot.addToTable(listInfo=listInfo, rowId=i)
                if self.event.is_set():
                    print("Function ended working")
                    self.button.config(state=tk.NORMAL)
                    # self.client.destroy()
            except requests.exceptions.ConnectTimeout:
                messagebox.showerror('Проблема на стороні сервера', 'Триває повторне підключення до таблиці!')
            except:
                messagebox.showerror('Проблема на підключенні до Таблиці', 'Немає підключення до інтернету!')
            time.sleep(5)

            if self.event.is_set():
                print("Function ended working")
                self.button.config(state=tk.NORMAL)
                # self.client.destroy()
                break
        messagebox.showinfo("Кінець програми", "Опрацювання даних закінчено")
        self.event.clear()
        self.button.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.DISABLED)
        return

    def start_call_back(self, tableName, tablePage, startRow):
        if tableName == '':
            messagebox.showerror('Ім`я таблиці', 'Будь ласка, введіть справжнє ім`я гугл таблиці!')
            return
        if tablePage == '':
            messagebox.showerror('Ім`я аркуша', 'Будь ласка, введіть справжнє ім`я аркуша гугл таблиці!') 
            return
        if startRow != '':
            try:
                if type(int(startRow)) == int:
                    pass   
            except:
                messagebox.showerror('Число рядка', 'Будь ласка, введіть число, чи можете нічого не писати і буде автоматично обран останній заповнений рядочок') 
                return
        self.event.clear()
        self.button.config(state=tk.DISABLED)
        self.button_stop.config(state=tk.NORMAL)
        thread = threading.Thread(target=self.call_back, args=(tableName, tablePage, startRow))
        thread.start()

    def stop_call_back(self):
        self.event.set()
        self.button_stop.config(state=tk.DISABLED)
        print("Please wait on end of the function...")
        messagebox.showinfo("Кінець програми", 'Почекайте, будь ласка, на закінчення працювання програми, не закривайте вікно.')

    def openHelpFile(self):
        webbrowser.open_new_tab(f'file://{os.getcwd()}/assets/index.html')