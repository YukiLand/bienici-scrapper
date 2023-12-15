from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Gestion d'une base de données
import sqlalchemy as db
import openai

class DataBase():
    def __init__(self, name_database='myimo'):
        self.name = name_database
        self.url = f"sqlite:///{name_database}.db"
        self.engine = db.create_engine(self.url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = self.engine.table_names()


    def create_table(self, name_table, **kwargs):
        colums = [db.Column(k, v, primary_key = True) if 'id_' in k else db.Column(k, v) for k,v in kwargs.items()]
        db.Table(name_table, self.metadata, *colums)
        self.metadata.create_all(self.engine)
        # print(f"Table : '{name_table}' are created succesfully")

    def read_table(self, name_table, return_keys=False):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine)
        if return_keys:table.columns.keys()
        else : return table


    def add_row(self, name_table, **kwarrgs):
        name_table = self.read_table(name_table)

        stmt = (
            db.insert(name_table).
            values(kwarrgs)
        )
        self.connection.execute(stmt)
        # print(f'Row id added')

    def select_table(self, name_table):
        name_table = self.read_table(name_table)
        stm = db.select([name_table])
        return self.connection.execute(stm).fetchall()
    


def collect_data(articles):
    datas = []
    print(len(articles))
    for article in articles:
        # print(article)
        data = {}
        img = ""
        link = ""
        price  = ""
        name = ""
        address = ""
        sqprice = ""
        # pattern = keyword



        try:
            img = article.find_element(By.CLASS_NAME, "img__image img__image--fit-to-parent".replace(' ', '.')).get_attribute("src")
        except:
            pass
        try:
            link = article.find_element(By.CLASS_NAME, "detailedSheetLink").get_attribute("href")
        except:
            pass
        try:
            price = article.find_element(By.CLASS_NAME, "ad-price__the-price").text
        except:
            pass
        try:
            name = article.find_element(By.CLASS_NAME, "ad-overview-details__ad-title ad-overview-details__ad-title--small".replace(' ','.')).text
        except:
            pass
        try:
            address = article.find_element(By.CLASS_NAME, "ad-overview-details__address-title ad-overview-details__address-title--small".replace(' ', '.')).text
        except:
            pass
        try:
            sqprice = article.find_element(By.CLASS_NAME, "ad-price__price-per-square-meter".replace(' ', '.')).text
        except:
            pass

        data = {
            "img": img,
            "link": link,
            "price": price,
            "name": name,
            "address": address,
            "sqprice": sqprice
        }
        # print(data)
        if data['link'] != "" and data['price'] != "" and data['name'] != "" and data['address'] != "" and data['sqprice'] != "":
            datas.append(data)
    return datas

def search_ads(city, price_min, price_max, nb_page):
    driver = webdriver.Chrome("./chromedriver")
    driver.get("https://www.bienici.com/")

    time.sleep(1.5)

    driver.find_element(By.ID, "didomi-notice-agree-button").click()

    time.sleep(0.5)

    driver.find_element(By.ID, "hpDoSearch").click()

    time.sleep(1.5)

    driver.find_element(By.CLASS_NAME, "bootstrap-tagsinput").click()

    driver.find_element(By.CLASS_NAME, "tt-input").send_keys(Keys.BACK_SPACE*100)
    driver.find_element(By.CLASS_NAME, "tt-input").send_keys(city)

    time.sleep(0.5)

    driver.find_element(By.CLASS_NAME, "tt-input").send_keys(Keys.ARROW_DOWN)
    driver.find_element(By.CLASS_NAME, "tt-input").send_keys(Keys.ARROW_UP)
    driver.find_element(By.CLASS_NAME, "tt-input").send_keys(Keys.ENTER)

    time.sleep(1.5)

    driver.find_element(By.CLASS_NAME, "filterHelper dropdown".replace(' ', '.')).click()

    driver.find_element(By.CLASS_NAME, "inputWithUnits inputMax".replace(' ', '.')).send_keys(price_max)
    driver.find_element(By.CLASS_NAME, "inputWithUnits inputMin".replace(' ', '.')).send_keys(price_min)

    time.sleep(0.5)

    driver.find_element(By.CLASS_NAME, "inputWithUnits inputMin".replace(' ', '.')).send_keys(Keys.ENTER)

    currentURL = driver.current_url
    # print(currentURL)

    time.sleep(3)

    i = 0 # not 0 because if we do +1 we will scrap the first page twice
    dataCollected = []
    time.sleep(0.5)
    while i < nb_page:
        i += 1
        driver.get(currentURL + "&page={}".format(i))

        selection = driver.find_elements(By.CLASS_NAME, "sideListItem".replace(' ', '.'))
        if selection == []:
            time.sleep(2)
            selection = driver.find_elements(By.CLASS_NAME, "sideListItem".replace(' ', '.'))
            time.sleep(2)
        dataCollected += collect_data(selection)
        # time.sleep(2)

    class Ads:
        def __init__(self, img:str, link:str, price:str, name:str, address:str, sqprice:str):
            self.img = img
            self.link = link
            self.price = price
            self.name = name
            self.address = address
            self.sqprice = sqprice
        
        def show_data(self, *args):
            for arg in args:
                print(arg)

        def show_data_kwargs(self, **kwargs):
            print(kwargs)

    time.sleep(2)
    database = DataBase('data')
    database.create_table('adsimo', img=db.String, link=db.String, price=db.String, name=db.String, address=db.String, sqprice=db.String)
    
    i = 0
    for line in range(len(dataCollected)):
        database.add_row('adsimo', **dataCollected[i])
        i += 1

    database.select_table('adsimo')

    print("Data collected", len(dataCollected))

    return dataCollected