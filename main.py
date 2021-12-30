#  Ti lascio amazon.py se vuoi vedere com'era la versione alpha del programma
#
#  Si avrei potuto evitare di utilizzare i dizzionari ma volevo imparare ad utilizare nuove strutture dati
#
#  istruzioni:
#  Non cambiare i file per nessuna ragione e, se vuoi,
#  importi questo file in un altro file .py e da la invochi la classe e i suoi metodi
#
#  Solamente per dire, hai bisogno di connetterti ad internet, sò che è ovvio ma non si sa mai
#
#  esistono 4 metodi in questa classe
#  __init__() : per caricare i dati e l'header
#  urL_menu() : per gestire i link che vorresti utilizzare
#  fetch() : per caricare tutti i link che hai messo convertendoli in un dizionario e poi salvarli in un file{'key': 'value'}
#  compare() : per vedere se ci sono degli sconti, controllando i dati dentro 'products' e il sito di amazon
#
#  questi metodi le ho rese così in tal modo che se vorresti decidere quando far apparire url_menu o attivare altre funzioni
#  lo potrai fare, invece di fare tutto in una botta o mettere tutto nel __init__() che secondo me, è un errore madornale
#
#  esempio:
#  amazonpy() --> quì verrà inizializzato la funzione __init__()
#
#  cosa ci sono nei file?
#
#  data_list --> i link che metterai
#  header --> l'user-agent (formato dizzionario)
#  path --> locazione di data_list (se percaso vorresti cambiare file oppure path)
#  products --> i prodotti in formato dizzionario che verrà generato durante la fase di fetch()
#
#  fatto da : Piantadosi Daniele
#  per un progetto estivo per impare python oltre a c++

# P.S
# non penso che il mio inglese sia stato scritto bene
# ma pursempre ci provo dato che ogni programmatore deve scrivere in inglese
#
#
# Se vedi che ci sono dei nodi (casini) in questo programma è perché ho voluto
# permettere all'esecutore di decidere dov'è il file e il suo defaulth_path
#
# L'ho testato e adesso dovrebbe funzionare bene
# TODO:
# Gli errori che adesso devo risolvere in questo è solamente che quando la lista è = 0
# non dirà nulla [riga 197]
# ho tentato di usare "len" ma sembra che non riesce a fare "if len(esempio_lista) == 0"
# non riesce ad andare in quella condizione


# Attenzione:
# Se il programma non parte, controllare se si ha installato le seguenti librerie:
# bs4 (Beautifull soup 4)
# request

import json
import logging
import re
import threading
import webbrowser
from datetime import datetime
from os import execlp

import matplotlib.pyplot as plt
import mysql.connector
import requests
from bs4 import BeautifulSoup
from pypika import Field, MySQLQuery, Query, Table

logging.basicConfig(format='%(asctime)s %(levelname)s - %(funcName)s:%(message)s',
                    filename='amazon_bot.log', encoding='utf-8', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')


class amazonpy():
    product = None  # --> product = json.load(file)

    # --settings--
    settings = json.load(open("./settings.json"))

    amazon_db = mysql.connector.connect(
        host=settings["DBIP"],
        user=settings["DBUser"],
        password=settings["DBPass"],
        database=settings["DB"]
    )

    amazon_db_cursor = amazon_db.cursor()

    def __init__(self):
        # 1 path choise
        # 2 loads the the existent list from the file 'data_list'
        # 3 checks if there's any data in it
        # 4 checks your user-agent for making sure that you can use the code

        changed = False
        path_choice = ""
        print("Would you like to change header?[y/n]")
        while True:
            new_header = input()

            if path_choice == 'y':
                new_header = input("inserisci in nuovo header: ")
                if not new_header == "":
                    self.settings["header"]["User-Agent"] = new_header
                    changed = True

                new_prod_file = input("inserisci in nuovo file prodotti: ")
                if not new_prod_file == "":
                    self.settings["header"]["productfile"] = new_prod_file
                    changed = True

            break

        prodtable = Table('AmazonBotSites_product')

        query = MySQLQuery.from_(prodtable).select(
            prodtable.ID, prodtable.LINK)

        self.amazon_db_cursor.execute(query.get_sql())

        self.product = self.amazon_db_cursor.fetchall()

        while True:
            try:
                # checks the user agent
                page = requests.get("https://www.google.com",
                                    headers=self.settings["header"])

                if not page.status_code == 200:
                    print("connection error "+page.status_code +
                          " with the sequent user agent "+self.settings["header"])
                    return

                if not changed:
                    break

                print("Would you like to save the settings?")
                while True:
                    choice = input()
                    if choice == 'y':
                        json.dump(self.settings, open("./settings.json"))
                        break
                    elif choice == 'n':
                        break
                    else:
                        print("Error, invalid input")
            except:
                print("Error, invalid user agent plese insert another user agent(you can find it by typing on google 'what's my user agent')")
                return

        if len(self.product) == 0:
            print("There's no data in this file")
        else:
            print(f'Loaded file, found  {len(self.product)}  links')

    def url_menu(self):
        # this is the part where you manage the links

        while True:
            print("What would you like to do?\n1 --> add link        2 --> delete link\n3 --> modify link     4 --> show link\n5 --> fetch     0 --> exit url_menu")
            # you chose how to manipulate your list

            option = int(input("-->"))
            if option == 1:
                self.add_product(input("Insert a link -->"))

            elif option == 2:
                self.show_products()
                self.remove_product(
                    int(input("Select which number would you like to delete")) - 1)

            elif option == 3:
                # ToDo self.url_list[int(input("Select which number would you like to modify")) - 1] = input("Insert the link --> ")
                pass
            elif option == 4:
                self.show_products()

            elif option == 5:
                bot.fetch()
                print("Fetch process done")

            else:
                print("Error, invalid input")

    def add_product(self, url):
        try:
            page = requests.get(url, headers=self.settings["header"])

        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error:", errh)

        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)

        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:", errt)

        except requests.exceptions.RequestException as err:
            logging.error("OOps: Something Else", err)

        else:
            soup = BeautifulSoup(page.content, 'html.parser')

            # inserisci prodotto
            prodtable = Table('AmazonBotSites_product')

            query = MySQLQuery.into(prodtable).columns(prodtable.Name, prodtable.Link).insert(
                soup.find(id='productTitle').get_text().replace("\n", "").replace("'", "\'"), url)

            self.amazon_db_cursor.execute(query.get_sql())

            self.amazon_db.commit()

            prodId = self.amazon_db_cursor.lastrowid

            # inserisci categoria
            for query in self.settings["catquery"]:
                catname = soup.find(class_=query)
                if not catname == None:
                    catname = catname.get_text().replace(
                        "  ", "").replace('\n', '').replace("'", "\'")
                    break

            if catname == None or catname == "":
                return

            categtable = Table('AmazonBotSites_category')

            cetquery = MySQLQuery.from_(categtable).select(
                "*").where(categtable.Name == catname)

            self.amazon_db_cursor.execute(cetquery.get_sql())

            catresult = self.amazon_db_cursor.fetchall()

            # add if not exist
            if len(catresult) == 0:

                query = MySQLQuery.into(categtable).columns(
                    categtable.Name).insert(catname)

                self.amazon_db_cursor.execute(query.get_sql())

                self.amazon_db.commit()

                cateId = self.amazon_db_cursor.lastrowid
            else:
                cateId, nomecat = catresult[0]

            # agginugi categoria a prodotto
            categtable = Table('AmazonBotSites_category_product')

            query = MySQLQuery.into(categtable).columns(
                categtable.product_id, categtable.category_id).insert(prodId, cateId)

            self.amazon_db_cursor.execute(query.get_sql())

            self.amazon_db.commit()

    def new_detection(self, prod):

        Id, Link = prod

        try:
            page = requests.get(
                Link, headers=self.settings["header"])

        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error:", errh)

        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)

        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:", errt)

        except requests.exceptions.RequestException as err:
            logging.error("OOps: Something Else", err)

        else:

            price = self.find_price(page)
            if not price or price == "":
                return

            if not re.findall("[0-9]+,[0,9]+", price):
                price = "0.0€"

            # price convertion to string to float
            price = price.replace(',', '.')
            price = re.findall("[0-9]+.[0,9]+", price)[0]
            converted_price = float(price)

            # add price to db
            pricetable = Table('AmazonBotSites_price')

            query = MySQLQuery.into(pricetable).columns(pricetable.Datetime, pricetable.Price, pricetable.ID_product_id).insert(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), converted_price, Id)

            self.amazon_db_cursor.execute(query.get_sql())

            self.amazon_db.commit()

    def remove_product(self, i):
        self.product.remove(self.product[i])
        json.dump(self.product, open(self.settings["productfile"], "w"))

    def show_products(self):
        for x in range(len(self.product)):
            print(f'{x + 1}. {self.product[x]["productname"]}\n')

    def find_price(self, page):
        # 1st try
        soup = BeautifulSoup(page.content, 'html.parser')

        for query in self.settings["serchQuery"]:
            price = soup.find(class_=query)
            if not (price == None or price == ""):
                return price.get_text()

        logging.warn('prenzo non trovato verra effetuato un report')
        logging.warn(page.url)
        return "0.0€"

    def start_continuous_fetch(self):
        prodtable = Table('AmazonBotSites_product')

        query = MySQLQuery.from_(prodtable).select(
            prodtable.ID, prodtable.LINK)

        self.amazon_db_cursor.execute(query.get_sql())

        self.product = self.amazon_db_cursor.fetchall()

        logging.info("numero prodotti: "+str(len(self.product)))
        for prod in self.product:
            self.new_detection(prod)

        self.product = None

        t = threading.Timer(60*5, self.start_continuous_fetch)
        t.start()

    def drow_graph(self, i):
        # todo: fix plot data
        fig, ax = plt.subplots()

        prices = []

        for price in self.product[i]["detectionprice"]:
            prices.append(price["price"])

        n, bins, patches = ax.hist(prices, len(self.product), density=True)
        plt.show()


bot = amazonpy()


def main():
    t1 = threading.Timer(0, bot.start_continuous_fetch)
    #t2 = threading.Timer(0, bot.url_menu)
    #t2.start()
    t1.start()


if __name__ == "__main__":
    main()
