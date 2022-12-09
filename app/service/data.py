from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random
from dateutil.relativedelta import relativedelta
import threading 
import time


user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

url = 'https://www.bareksa.com/id/saham/sector'

# Dynamically scrap stock data from Bareksa's website w/ BeautifulSoup
trs = []
while len(trs) == 0:
    r = requests.get(url, headers={'User-Agent': random.choice(user_agents_list)})
    soup = BeautifulSoup(r.text, 'html.parser')
    trs = soup.find_all('tr')
    time.sleep(1)

stock_data = []
stock_name = []
stock_current_price = []

for tds in trs:
    i = 0
    for td in tds.find_all('td'):
        if len(td) > 0:
            if (i == 1):
                stock_name.append(td.contents[0].contents[0])
            if (i == 7):
                stock_current_price.append(td.contents[0])  
            i+=1

for i in range(len(stock_name)):
    int_stock_current_price = stock_current_price[i].replace(".","")
    data = {
        "name" : stock_name[i],
        "current_price" : int_stock_current_price
    }
    stock_data.append(data)

available_stock_name = ['ADRO','AMRT','ANTM','ASII','BBCA','BBNI','BBRI','BBTN','BFIN','BMRI','BRPT','BUKA','CPIN','EMTK','ERAA','EXCL','GGRM','HMSP','HRUM','ICBP','INCO','INDF','ITMG','JPFA','KLBF','MDKA','MEDC','MIKA','MNCN','PGAS','PTBA','PTBA','PTPP','SMGR','TBIG','TINS','TKIM','TLKM','TOWR','TPIA','UNTR','UNVR','WIKA','WSKT']

available_stock_data = []
for data in stock_data:
    if data["name"] in available_stock_name:
        available_stock_data.append(data)

current_stock_data = []
for data in available_stock_data:
    int_price = int(data["current_price"])
    data["current_price"] = int_price
    current_stock_data.append(data)

### Fetch forecast data from Eagan's API
loginHeader = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

loginData = {
  "username": "bryanbryan",
  "password": "eaganeagan"
}
loginResponse = requests.post("http://128.199.149.182:8000/user/login",headers=loginHeader,json=loginData)

token = ""
if loginResponse.status_code == 200:
    # Access the loginResponse data
    data = loginResponse.json()
    token = data["token"]
else:
    print('Failed to fetch data')

def fetch_data(datas,forecast_data):
    header = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    for data in datas:
        response = requests.post("http://128.199.149.182:8000/prediction/stockforecast",headers=header,json=data)
        if response.status_code == 200:
            # Access the response data
            data = response.json()
            forecast_data.append(data)
        else:
            print(response)
            print('Failed to fetch data')


### Dummy forecast data
# Find forecast data (dummy data)
def find_forecast_data(time, amount):
    if time == "week":
        req_datas = []
        for data in current_stock_data:
            name_data = data["name"]
            year_data = find_date("week",amount).year
            month_data = find_date("week",amount).month
            day_data = find_date("week",amount).day
            req_data = {
                "stockCode": name_data,
                "year": year_data,
                "month": month_data,
                "date": day_data
            }
            req_datas.append(req_data)
        # Create a new thread
        forecast_data = []
        thread = threading.Thread(target=fetch_data(req_datas,forecast_data))

        # Start the thread
        thread.start()

        # Wait for the thread to finish
        thread.join()

        return forecast_data

    if time == "month":
        req_datas = []
        for data in current_stock_data:
            name_data = data["name"]
            year_data = find_date("month",amount).year
            month_data = find_date("month",amount).month
            day_data = find_date("month",amount).day
            req_data = {
                "stockCode": name_data,
                "year": year_data,
                "month": month_data,
                "date": day_data
            }
            req_datas.append(req_data)
        # Create a new thread
        forecast_data = []
        thread = threading.Thread(target=fetch_data(req_datas,forecast_data))

        # Start the thread
        thread.start()

        # Wait for the thread to finish
        thread.join()

        return forecast_data
    if time == "year":
        req_datas = []
        for data in current_stock_data:
            name_data = data["name"]
            year_data = find_date("year",amount).year
            month_data = find_date("year",amount).month
            day_data = find_date("year",amount).day
            req_data = {
                "stockCode": name_data,
                "year": year_data,
                "month": month_data,
                "date": day_data
            }
            req_datas.append(req_data)
        # Create a new thread
        forecast_data = []
        thread = threading.Thread(target=fetch_data(req_datas,forecast_data))

        # Start the thread
        thread.start()

        # Wait for the thread to finish
        thread.join()

        return forecast_data
    if amount == 0:
        return None
    else:
        return None

def find_highest_profit(time, amount): ## Placeholder
    forecast_data = find_forecast_data(time, amount)
    if (forecast_data is None):
        return "Wrong format"
    profit_list = []
    for old_data, new_data in zip(current_stock_data, forecast_data):
        old_price = old_data["current_price"]
        new_price = new_data["stock price"]
        name = old_data["name"]
        profit = (new_price - old_price) / old_price * 100
        profit_list.append({'name': name, 'profit': profit})

    profit_list = sorted(profit_list, key=lambda d: d["profit"], reverse=True)

    recommedation_list = []
    for d in profit_list[:5]:
        recommedation_list.append(d)
    return recommedation_list

# find_highest_profit("week")
# print()
# find_highest_profit("month")
# print()
# find_highest_profit("year")
    


# Print the original and updated lists
# print(current_stock_data[0])
# print(forecast_week_stock_data[0])
# print(forecast_month_stock_data[0])
# print(forecast_year_stock_data[0])

# Function for finding future dates
# Example : find_date("week",1) = Find next week's date
def find_date(type:str, amount:int):
    if type=="week":
        current_datetime = datetime.now()
        next_date = current_datetime + relativedelta(weeks=amount)
        formatted_date = next_date.strftime("%Y-%m-%d")
        date_format = '%Y-%m-%d'
        date = datetime.strptime(formatted_date, date_format)
        return date
    if type=="month":
        current_datetime = datetime.now()
        next_date = current_datetime + relativedelta(months=amount)
        formatted_date = next_date.strftime("%Y-%m-%d")
        date_format = '%Y-%m-%d'
        date = datetime.strptime(formatted_date, date_format)
        return date
    if type=="year":
        current_datetime = datetime.now()
        next_date = current_datetime + relativedelta(years=amount)
        formatted_date = next_date.strftime("%Y-%m-%d")
        date_format = '%Y-%m-%d'
        date = datetime.strptime(formatted_date, date_format)
        return date



