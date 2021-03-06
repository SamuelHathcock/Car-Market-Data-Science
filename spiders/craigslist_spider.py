"""Craigslist Spider"""
from bs4 import BeautifulSoup
import requests
import re
import os

script_dir = os.path.dirname( __file__ )

class craig():

    def __init__(self):
        #TODO: get more headers for use and put in better format than below
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'cl_b=4|c20bf27c9c68956426131a5afd788eef316e1d43|1625718568O8eFM; cl_tocmode=sss%3Agrid',
        'Host': 'phoenix.craigslist.org',
        'If-Modified-Since': 'Thu, 08 Jul 2021 04:29:28 GMT',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        self.mainURL = ['https://phoenix.craigslist.org/d/cars-trucks-by-owner/search/cto?s=', '0', '&postal=85249&search_distance=50']
        self.searchIndex = 0
        try:
            with open("spiders/car_manufacturers.txt", 'r') as file:
                self.manfac_list = [l.strip() for l in file.readlines()]
        except:
            print("Missing file 'car_manufacturers.txt'")
            exit()

    def parse(self):
        print('Parse Start')
        while(True):
            try:
                source = requests.get(''.join(self.mainURL), headers=self.headers)
                soup = BeautifulSoup(source.text, 'html.parser')
                links = soup.findAll('a', class_='result-image gallery')
                
                #Filtering a elements for the link text itself, which is under 'href'
                for i in range(len(links)):
                    links[i] = links[i]['href']
            except Exception as e:
                print(e)
                break

            for i in range(len(links)):
                try:
                    print('\n', links[i])

                    car_page = requests.get(links[i])
                    car_soup = BeautifulSoup(car_page.content, 'html.parser')
                    attributes = car_soup.find_all('p', class_='attrgroup')
            
                    #Finding car properties by parsing the spans and returning as dict.
                    car_properties = self.parse_spans(attributes[1])
                    
                    self.get_year_make_model(attributes[0].text)

                    dicc = {
                    'title': car_soup.find('span', id="titletextonly").text,
                    'year': self.year,
                    'make': self.make,
                    'model': self.model,
                    'odometer': self.get_odometer(car_properties),
                    'paintcolor': self.get_paint_color(car_properties),
                    'titlestatus': self.get_title_status(car_properties),
                    'price': car_soup.find('span', class_="price").text
                    }
                    yield dicc

                except Exception as e:
                    print(e)
                    continue
            
            self.getnextpage()

    def setURL(self, mainURL: str):
        self.mainURL = mainURL

    def parse_spans(self, attributes) -> dict:
        dicc = {}
        spans = attributes.find_all('span')
        for span in spans:
            text = span.text.replace(' ', '')
            arr = text.split(':')
            #Exception: odometer property can read 'odometerrolledover', and because it lacks a ':', it will create an array with 1 index.
            if (len(arr) == 1): dicc.update({'odometer': 'rolledover'})
            else: dicc.update({arr[0]: arr[1]})
        return dicc
 
    def get_year_make_model(self, attribute):
        attribute = self.clean(attribute)
        arr = attribute.split(' ') 
        arrLen = len(arr)
        try:
            self.year = re.findall('(\d{4})', attribute)[0]
        except:
            self.year = None
        try:
            make = ''
            self.make = None
            for m in self.manfac_list:
                match = re.findall(m, attribute)
                if len(match) != 0:
                    make = match[0]
                    if make == 'chevy':      self.make = 'chevrolet'
                    elif make == 'corvette': self.make = 'chevrolet'
                    else:                    self.make = make
                    break
        except:
            self.make = None
        try:
            self.model = arr[2]
        except:
            self.model = None
        
    def get_odometer(self, car_properties: dict):
        if 'odometer' in car_properties:
            if car_properties['odometer'] == 'rolledover':
                return -1
            return int(car_properties['odometer'])
        return None

    def get_paint_color(self, car_properties: dict):
        if 'paintcolor' in car_properties:
            return car_properties['paintcolor']
        return None

    def get_title_status(self, car_properties: dict):
        if 'titlestatus' in car_properties:
            return car_properties['titlestatus']
        return None

    def clean(self, dirty_string: str):
        temp = dirty_string.strip().lower()
        temp = temp.replace('\n', '')
        return temp

    def getnextpage(self):
        self.searchIndex += 120
        print('getting pages at index: ', self.searchIndex)
        self.mainURL[1] = str(self.searchIndex)
        

if __name__ == "__main__":  
    craig = craig()

