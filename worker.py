import requests
import datetime
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup

count = 1
BASE = "http://127.0.0.1:5000/"
url = 'https://mosmetro.ru/press/news/'
current_data = []

def convert_time(time):
    data = datetime.today()
    splitted_time = time.split()
    if splitted_time[1] == 'неделя' or splitted_time[1] == 'недели' or splitted_time[1] == 'недель':
        days = int(splitted_time[0])*7     
        data = datetime.today() - timedelta(days=days)
    
    elif splitted_time[1] == 'дня' or splitted_time[1] == 'дней' or splitted_time[1] == 'день':
        days = int(splitted_time[0])     
        data = datetime.today() - timedelta(days=days)
    
    elif splitted_time[1] == 'месяц' or splitted_time[1] == 'месяца' or splitted_time[1] == 'месяцев':
        days = int(splitted_time[0])*30
        data = datetime.today() - timedelta(days=days)
    return data

def parse_news(item):
    header = item.find('span', {'class':'newslist__text-title'}).text
    img_src = item.find('img', {'class':'newslist__image'}).get('src')
    published_date = item.find('span', {'class':'newslist__text-time'}).text
    date = convert_time(published_date)
    parsed_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    #parsed_time = datetime.now()
    return header, img_src, date.strftime("%Y-%m-%d"), parsed_time
    #return header, img_src, date, parsed_time
  

while(True):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    links = soup.find_all('a', {'class': 'newslist__link'})
    #response = requests.put(BASE + "news/1", {'header':'header', 'img_src' : 'img_src', 'published_date' :'sadasd', 'parsed_date':'sad'})
    #print(response.json())


    for item in links:
        header, img_src, published_date, parsed_date = parse_news(item)
        json_news = {'header':header, 'img_src' : img_src, 'published_date' :published_date}
        if json_news not in current_data:
            current_data.append(json_news)
            response = requests.put(BASE + "metro/news/" + str(count), {'header':header, 'img_src' : img_src, 'published_date' :published_date, 'parsed_date':parsed_date})
            count += 1
            print(response.json())
        else:
            print('No news to add')
    time.sleep(5)
#response = requests.get(BASE + "news/1", {'header':'HHHDDRRR', 'published_date' :'1111', 'img_src' : 'https:', 'parsed_date':'222'})

#print(response.json())
