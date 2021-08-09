from spiders.craigslist_spider import craig
import json
import time
from os.path import exists
import os
import sqlite3

"""
This program will be used to process the data recieved from spiders
and write this information to a JSON file and a database.
"""

class pipeline():


    def output(self):
        """Replaces all content in "carData.json" and "test.db" with fresh scraped data"""
        self.craig = craig()
        if exists("carData.json"):
            os.remove("carData.json")
            with open("carData.json", mode='w', encoding='utf-8') as f1:
                json.dump([], f1)

        self.create_conn()
        self.create_table()        

        SCRAPE_CAP = 200
        scrape_count = 0
        for data in self.craig.parse():
            self.writeJSON(data, file_name="carData.json")
            self.store_db(data)
            if scrape_count == SCRAPE_CAP: break
            time.sleep(.5)

    def writeJSON(self, data: dict, file_name="carData.json"):
        with open(file_name, mode='r') as f2:
            load = json.load(f2)
            load.append(data)
        with open(file_name, "w", encoding='utf-8') as f3:
            json.dump(load, f3, indent=1)

    def create_conn(self):
        self.conn = sqlite3.connect("carData.db")
        self.curr = self.conn.cursor()
        
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS cars""")
        self.curr.execute("""create table cars(
            title text,
            year text,
            make text,
            model text,
            odometer text,
            paintcolor text,
            titlestatus text,
            price text
        )""")

    # def process_item(self, item):
    #     self.store_db(item)
    #     print("Pipelines = " + item['title'] + " " + item['price'] )
    #     return item

    def store_db(self, item):
        self.curr.execute("""INSERT into cars values(?,?,?,?,?,?,?,?)""",(
            item['title'],
            item['year'],
            item['make'],
            item['model'],
            item['odometer'],
            item['paintcolor'],
            item['titlestatus'],
            item['price']
        ))
        self.conn.commit()

if __name__ == '__main__':
    p = pipeline()
    p.output()