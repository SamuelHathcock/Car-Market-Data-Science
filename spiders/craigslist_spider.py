"""Craigslist Spider"""
from bs4 import BeautifulSoup
import requests

class craig():

    def __init__(self):
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
        self.url = 'https://phoenix.craigslist.org/d/cars-trucks-by-owner/search/cto?postal=85249&search_distance=50'



    def parse(self):
        source = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(source.text, 'html.parser')
        links = soup.findAll('a', class_='result-image gallery')
        print('TTTTTTTTTTTTTTTTTTT') 

        #Filtering a elements for the link text itself, which is under 'href'
        for i in range(len(links)):
           links[i] = links[i]['href']
        
        # print(len(links), "\n")

        for i in range(0, len(links)):
            print('\n', links[i])

            car_page = requests.get(links[i])
            car_soup = BeautifulSoup(car_page.content, 'html.parser')
            attributes = car_soup.find_all('p', class_='attrgroup')
    
            #Finding car properties by parsing the spans and returning as dict.
            car_properties = self.parse_spans(attributes[1])
            self.make_year_make_model(attributes[0].text)
            dicc = {
            'title': car_soup.find('span', id="titletextonly").text,
            # 'year_make_model': self.make_year_make_model(attributes[0].text),
            'year': self.year,
            'make': self.make,
            'model': self.model,
            'odometer': self.get_odometer(car_properties),
            'paintcolor': self.get_paint_color(car_properties),
            'titlestatus': self.get_title_status(car_properties),
            'price': car_soup.find('span', class_="price").text
            }
            yield dicc

    def setURL(self, url: str):
        self.url = url

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

    def make_year_make_model(self, attribute):
        attribute = self.clean(attribute)
        arr = attribute.split(' ')
        #TODO: add try catch here in case len(arr) < 3
        self.year = arr[0]
        self.make = arr[1]
        self.model = arr[2]

    def get_odometer(self, car_properties: dict):
        if 'odometer' in car_properties:
            return car_properties['odometer']
        return '?'

    def get_paint_color(self, car_properties: dict):
        if 'paintcolor' in car_properties:
            return car_properties['paintcolor']
        return '?'

    def get_title_status(self, car_properties: dict):
        if 'titlestatus' in car_properties:
            return car_properties['titlestatus']
        return '?'

    def clean(self, html: str):
        temp = html
        temp = temp.replace('\n', '')
        return temp


if __name__ == "__main__":  
    craig = craig()
