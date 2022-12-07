# Dynamically scrap stock data from Bareksa's website w/ BeautifulSoup
import requests
from bs4 import BeautifulSoup
import random

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

r = requests.get('https://www.bareksa.com/id/saham/sector', headers={'User-Agent': random.choice(user_agents_list)})
soup = BeautifulSoup(r.text, 'html.parser')
trs = soup.find_all('tr')

stock_data = []
stock_name = []
stock_current_price = []
for tds in trs:
    i = 0
    for td in tds.find_all('td'):
        if (i == 1):
            stock_name.append(td.contents[0].contents[0])
        if (i == 7):
            stock_current_price.append(td.contents[0])
        i+=1

for i in range(len(stock_name)):
    data = {
        "name" : stock_name[i],
        "current_price" : stock_current_price[i]
    }
    stock_data.append(data)


