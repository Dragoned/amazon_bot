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
import pickle
import webbrowser
import requests
import matplotlib.pyplot as plt
from pynput import keyboard

from datetime import datetime
from bs4 import BeautifulSoup


class amazonpy():
    product = None  # --> product = json.load(file)

    # --settings--
    settings = json.load(open("./settings.json"))
    # --settings--

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

        self.product = json.load(open(self.settings["productfile"]))

        while True:
            try:
                # checks the user agent
                page = requests.get("https://www.google.com", headers=self.settings["header"])

                if not page.status_code == 200:
                    print("connection error "+page.status_code+" with the sequent user agent "+self.settings["header"])
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
        changed = False
        if len(self.product) == 0:
            print("There's no url")

        while True:
            print("What would you like to do?\n1 --> add link        2 --> delete link\n3 --> modify link     4 --> show link\n5 --> fetch     0 --> exit url_menu")
            # you chose how to manipulate your list

            option = int(input("-->"))
            if option == 1:
                self.add_product(input("Insert a link -->"))
                changed = True
            elif option == 2:
                self.show_products()
                self.remove_product(int(input("Select which number would you like to delete")) - 1)
                changed = True
            elif option == 3:
                # ToDo self.url_list[int(input("Select which number would you like to modify")) - 1] = input("Insert the link --> ")
                changed = True
            elif option == 4:
                self.show_products()
            elif option == 5:
                bot.fetch()
                print("Fetch process done")

            elif option == 0:
                if not changed:
                    return

                while True:
                    print("Would you like save you changes? [y/n]")
                    save = input("-->")
                    if save == 'y':
                        json.dump(self.product, open(self.settings["productfile"], "w"))
                        return
                    elif save == 'n':
                        return

                    else:
                        print("Error, invalid comand, please try again")

            else:
                print("Error, invalid input")

    def fetch(self):
        if len(self.product) == 0:
            print("You can't fetch if there's no data")
            return

        for i in range(len(self.product)):
            try:
                self.new_detection(i)
            except:
                print(f"Error, invalid link number  {i}  ")

    def compare(self):
        comp_file = open("products", "rb")
        self.product = pickle.load(comp_file, encoding='bytes')

        # converting the dictionary in a list (only the values)
        price_list = list(self.product.values())
        for x in range(len(self.url_list)):
            try:
                # takes the intire page data
                page = requests.get(self.url_list[x], headers=self.header)

                # bs4 will try to take all the html content
                soup = BeautifulSoup(page.content, 'html.parser')

                # by using bs4 we can ask it to find the title in the html file
                title = soup.find(id='productTitle').get_text()

                price = soup.find(id='priceblock_ourprice').get_text()
                price = price.replace(',', '.')
                price = "".join(i for i in price if i != '€')
                converted_price = float(price)

                print(f"Product's n{x} (Before): {price_list[x]} ||| Product's price (Now) {converted_price}")
                if (price_list[x] > converted_price):
                    print(
                        f"!!!Found discount in product's [{title.strip()}] differenze: {price_list[x] - converted_price} euros!!!")
                    open_choice = input("Would you like to see the discounted product?  y | n \n--->")
                    if (open_choice == 'y'):
                        webbrowser.open(self.url_list[x])
                    else:
                        continue
            except:
                print(f"Error could not find the price in link n{x}")

    def add_product(self, url):
        page = requests.get(url, headers=self.settings["header"])

        if not page.status_code == 200:
            print("connection error "+page.status_code+" try later")
            return

        soup = BeautifulSoup(page.content, 'html.parser')
        
        new_product = { 
            "productname":soup.find(id='productTitle').get_text().replace("\n", ""),
            "url":url,
            "tag": soup.find(class_="a-link-normal a-color-tertiary").get_text().replace("  ", "").replace('\n', ''),
            "detectionprice":[]
            }
        self.product.append(new_product)

        json.dump(self.product, open(self.settings["productfile"], "w"))

    def new_detection(self, i):
        page = requests.get(self.product[i]["url"], headers=self.settings["header"])

        if not page.status_code == 200:
            print("connection error "+page.status_code+" try later")
            return



        price = self.find_product(page)
        if not price:
            return
        # price convertion to string to float
        price = price.replace(',', '.')
        price = price[:price.index("€")] #"".join(i for i in price if i != '€')  # price[price.index("€")+1:] by P.
        converted_price = float(price)

        self.product[i]["detectionprice"].append({
                "price":converted_price,
                "date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            })

        json.dump(self.product, open(self.settings["productfile"], "w"))

    def remove_product(self, i):
        self.product.remove(self.product[i])  
        json.dump(self.product, open(self.settings["productfile"], "w"))

    def show_products(self):
        for x in range(len(self.product)):
            print(f'{x + 1}. {self.product[x]["productname"]}\n')

    def find_product(self, page):
        # 1st try
        soup = BeautifulSoup(page.content, 'html.parser')
        price = soup.find(id='priceblock_saleprice')

        if not price:
            # 2nd try
            price = soup.find(class_='a-price a-text-price a-size-medium apexPriceToPay')
            if not price:
                print("nessun prezzo rilevato")
                print("Si può ipotizzare che il prodotto non è più disponibile")
            else:
                print(price)

        return price.get_text()

    def start_continuous_fetch(self, time=1):
        cont = 1
        while(True):
            for i in range(len(self.product)):
                self.new_detection(i)
                print("fecting list process number:", cont)
                cont += 1
                sleep(time)

    def drow_graph(self, i):
        #todo: fix plot data 
        fig, ax = plt.subplots()

        prices = []

        for price in self.product[i]["detectionprice"]:
            prices.append(price["price"])

        n, bins, patches = ax.hist(prices, len(self.product), density=True)
        plt.show()


bot = amazonpy()


def main():
    bot.url_menu()

if __name__ == "__main__":
    main()
