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
from bs4 import BeautifulSoup


class amazonpy():
    # default stands for the location of the files
    product = {}  # --> product = json.load(file)
    url_list = []
    default_path = "path"
    default_header = "header"

    # --settings--
    settings = json.load(open("./settings.json"))
    # --settings--

    # header is none just to declare a variable
    header = None

    def __init__(self):
        # 1 path choise
        # 2 loads the the existent list from the file 'data_list'
        # 3 checks if there's any data in it
        # 4 checks your user-agent for making sure that you can use the code

        path_choice = ""
        header = pickle.load(open(self.default_header, "rb"), encoding='bytes')
        print("Would you like to change header?[y/n]")
        while (True):
            new_header = input()

            if path_choice == 'y':
                try:
                    file_path = input("Insert the name of the file -->  ")
                    file = open(file_path, "rb")
                    self.url_list = pickle.load(file, encoding='bytes')
                    file.close()
                except:
                    print("Error, could not find the file")

                print("would you like to set it as your default path?[y/n]")
                while (True):

                    path_default = input()

                    if path_default == 'y':

                        self.default_path = file_path
                        pickle.dump(path_default, open(self.default_path, "wb"))
                        break

                    elif path_default == 'n':
                        break

                    else:
                        print("Error, Invalid input, try again")
                break


            elif path_choice == 'n':

                # taking the location of the data from the file 'path'

                file = open(self.default_path, "rb")
                data_file = pickle.load(file, encoding='bytes')
                file.close()
                # taking data from the path's data
                # in sintesi leggi path per prendere la locazione dei dati della lista

                print(data_file)
                file = open(data_file, "rb")
                self.url_list = pickle.load(file, encoding='bytes')
                file.close()
                break

        changed = False
        while (True):
            try:
                # checks the user agent
                page = requests.get("https://www.google.com", headers=header)
                self.header = header

                if not changed:
                    break

                print("Would you like to set it as your default user agent?")
                while (True):
                    choice = input()
                    if choice == 'y':

                        pickle.dump(new_header, open(self.default_header, "wb"))
                        break
                    elif choice == 'n':
                        break
                    else:
                        print("Error, invalid input")
            except:
                print(
                    "Error, invalid user agent plese insert another user agent(you can find it by typing on google 'what's my user agent')")
                new_header = input()

                # for using this library the user-agent must be put in a dictionary
                # if the the executor for some reason mess up for 2 or more time
                # you'll be always overwriting the dictionary's value (user-agent)

                # dictionary structure:

                # dict = {'key' : 'value'}
                #
                # my_car = {"Tesla" : 4000,
                #           "Lamborghini" : 20000}
                #
                # print(dict[Tesla])
                # output: 4000

                header["User-Agent"] = new_header
                changed = True
                continue

        if len(self.url_list) == 0:
            print("There's no data in this file")
        else:
            print(f'Loaded file, found  {len(self.url_list)}  links')

    def url_menu(self):
        # this is the part where you manage the links
        changed = False
        if self.url_list == 0:
            print("There's no url")

        print(
            "What would you like to do?\n1 --> add link        2 --> delete link\n3 --> modify link     4 --> show link\n5 --> save            0 --> exit url_menu")
        while True:

            # you chose how to manipulate your list

            option = int(input("-->"))
            if option == 1:
                self.url_list.append(input("Insert a link -->"))
                changed = True
            elif option == 2:
                self.url_list.pop(int(input("Select which number would you like to delete")) - 1)
                changed = True
            elif option == 3:
                self.url_list[int(input("Select which number would you like to modify")) - 1] = input(
                    "Insert the link --> ")
                changed = True
            elif option == 4:
                for x in range(len(self.url_list)):
                    print(f'{x + 1}. {self.url_list[x]}')
            elif option == 5:

                # extration of the path's data
                path_file = open(self.default_path, "rb")
                path = pickle.load(path_file)
                file = open(path, "wb")

                # saving process
                pickle.dump(self.url_list, file)
                path_file.close()
                file.close()
                print("Data has been saved")
                changed = False

            elif option == 0:
                if not changed:
                    return

                print("Would you like save you changes? [y/n]")
                while True:
                    save = input("-->")
                    if save == 'y':
                        # extration of the path's data
                        path_file = open(self.default_path, "rb")
                        path = pickle.load(path_file)

                        # saving process
                        file = open(path, "wb")
                        pickle.dump(self.url_list, file)
                        path_file.close()
                        file.close()
                        break
                    elif save == 'n':
                        break
                    else:
                        print("Error, invalid comand, please try again")


            else:
                print("Error, invalid input")

    def fetch(self):
        if self.url_list == 0:
            print("You can't fetch if there's no data")
            return

        for i in range(len(self.url_list)):
            try:

                # taking the html page code
                page = requests.get(self.url_list[i], headers=self.header)
                soup = BeautifulSoup(page.content, 'html.parser')
                title = soup.find(id='productTitle').get_text()
                price = soup.find(id='priceblock_ourprice').get_text()

                # price convertion to string to float
                price = price.replace(',', '.')
                price = "".join(i for i in price if i != '€')  # price[price.index("€")+1:] by P.
                converted_price = float(price)

                print(f"{title.strip()} = {converted_price} €")

                # inserting everything into a dictionary
                self.product[title.strip()] = converted_price

            except:
                # just for helping the user which link is wrong
                # maybe changing it won't go in this expect block
                print(f"Error, invalid link number  {i}  ")
                continue

        # saving process
        file = open("products", "wb")
        pickle.dump(self.product, file)
        file.close()

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

    def monitor(products, time, period_in_minutes=5):
        # monitors for a period of time a specific product
        # time is in minutes
        # default refresh time is 5 minutes

        pass


bot = amazonpy()


def main():
    # ricordati di uscire da questa funzione premendo 0 dopo che hai modificato i link
    bot.url_menu()

    print("Would you like to fetch or compare the data? [f/c] or [exit] for kill the program")
    while (True):
        choice = input("-->")
        if choice == 'f':
            bot.fetch()
            print("Fetch process done")
        elif choice == 'c':
            bot.compare()
            print("comparing process done")
        elif choice == "exit":
            break
        else:
            print("Error, invalid input")


if __name__ == "__main__":
    main()