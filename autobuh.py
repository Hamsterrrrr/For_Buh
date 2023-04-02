from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from buh_data_db import *
import time
import lxml
import os
from contextlib import contextmanager

engine = create_engine("postgresql+psycopg2://postgres:b,hf20043004@localhost/database")
session = Session(bind=engine)

class Pars_fsgs:
        

    def get_inns_from_db(self):
        result = session.query(Inns.inn).all()
        return [row[0] for row in result]
    
    @contextmanager
    def get_webdriver(self):
        driver = webdriver.Firefox()
        try:
            yield driver
        finally:
            driver.close()
    
    def scrape_website(self):
        self.inns = self.get_inns_from_db()
        data = []
        url = "https://websbor.gks.ru/online/info"
        for inn in self.inns:
            with self.get_webdriver() as driver:
                driver.get(url=url)
                try:
                    elem = driver.find_element(By.ID, "inn")
                    elem.send_keys(inn)
                    elem.send_keys(Keys.RETURN)
                    driver.execute_script("window.scrollBy(0, 100000)")
                    elem.send_keys(Keys.PAGE_DOWN)
                    time.sleep(3)
                    page = driver.page_source
                    data.append(self.select_data(page=page))
                except Exception as ex_:
                    print(ex_)
                    # Delete invalid INN value from database
                    session.query(Inns).filter(Inns.inn == inn).delete()
                    session.commit()
        return data

    def select_data(self, page):
        soup = BeautifulSoup(page, "lxml")
        codes_data = soup.find("tbody").find_all("td")
        codes_sort_data = [text.get_text() for text in codes_data]
        if codes_data == AttributeError:
            print("неверный инн")
        else:
            json_codes_data = {
                "OKPO": codes_sort_data[0],
                "OGRN": codes_sort_data[1],
                "DATA_registration": codes_sort_data[2],
                "INN": codes_sort_data[3],
                "OKATO_faction": codes_sort_data[4],
                "OKATO_registration": codes_sort_data[5],
                "OKTMO_faction": codes_sort_data[6],
                "OKTMO_registration": codes_sort_data[7],
                "OKOGU": codes_sort_data[8],
                "OKFS": codes_sort_data[9],
                "OKOPF": codes_sort_data[10],
            }
            
            formes_data = soup.find("table", class_="table table-responsive table-hover table-sm ng-star-inserted").find_all("td")
            sort_formes_data = [text.get_text() for text in formes_data]
            
            json_formes_data = {
                "Index": sort_formes_data[0::8],
                "Names_formes": sort_formes_data[1::8],
                "Periodes_formes": sort_formes_data[2::8],
                "Deadline": sort_formes_data[3::8],
                "Reporting_period": sort_formes_data[4::8],
                "Comments": sort_formes_data[5::8],
                "OKUD": sort_formes_data[6::8]
            }
            
            return json_formes_data, json_codes_data
    
    def insert_db(self):
        data = self.scrape_website()
        for json_formes_data, json_codes_data in data:
            inn_value = json_codes_data["INN"]
            inn_record = session.query(Inns).filter(Inns.inn==inn_value).first()

            if inn_record:
                inn_id = inn_record.ID
                add_codes_data = Codes_data()
                add_formes_data = Formes_data()
                for key, value in json_formes_data.items():
                    setattr(add_formes_data, key, value)
                for key, value in json_codes_data.items():
                    setattr(add_codes_data, key, value)
                session.add_all([add_formes_data, add_codes_data])
                add_codes_data.inn_id = inn_id
                add_formes_data.inn_id = inn_id

                session.add_all([add_formes_data, add_codes_data])
            else:
                print(f"No record found in Inns, table with inn value: {inn_value}")


        session.commit()
        session.close()
        
if __name__=="__main__":
    parser = Pars_fsgs()
    parser.insert_db()