from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random
from dateutil.relativedelta import relativedelta
import threading 
import secrets
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

### Dummy forecast data
# Find forecast data (dummy data)
def find_forecast_data(time, amount):
    if time == "week":
        forecast_week_stock_data = []
        # Loop through the list of dictionaries and update the current_price field in each dictionary
        for dictionary in current_stock_data:
            updated_dict = dictionary.copy()  # Create a copy of the dictionary
            updated_dict['current_price'] += (random.randint(1, 100) * (1 + (amount/10)))  # Add a random number between 1 and 1000 to the current_price field in the copy
            forecast_week_stock_data.append(updated_dict)  # Append the updated dictionary to the new list
        return forecast_week_stock_data
    if time == "month":
        forecast_month_stock_data = []
        # Loop through the list of dictionaries and update the current_price field in each dictionary
        for dictionary in current_stock_data:
            updated_dict = dictionary.copy()  # Create a copy of the dictionary
            updated_dict['current_price'] += (random.randint(100, 500) * (1 + (amount/10)))  # Add a random number between 1 and 1000 to the current_price field in the copy
            forecast_month_stock_data.append(updated_dict)  # Append the updated dictionary to the new list
        return forecast_month_stock_data
    if time == "year":
        forecast_year_stock_data = []
        # Loop through the list of dictionaries and update the current_price field in each dictionary
        for dictionary in current_stock_data:
            updated_dict = dictionary.copy()  # Create a copy of the dictionary
            updated_dict['current_price'] += (random.randint(500, 1000) * (1 + (amount/10)))  # Add a random number between 1 and 1000 to the current_price field in the copy
            forecast_year_stock_data.append(updated_dict)  # Append the updated dictionary to the new list
        return forecast_year_stock_data
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
        new_price = new_data["current_price"]
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
        return next_date.strftime("%Y-%m-%d")
    if type=="month":
        current_datetime = datetime.now()
        next_date = current_datetime + relativedelta(months=amount)
        return next_date.strftime("%Y-%m-%d")
    if type=="year":
        current_datetime = datetime.now()
        next_date = current_datetime + relativedelta(years=amount)
        return next_date.strftime("%Y-%m-%d")

# Fetch forecast data from Eagan's API
# Send a GET request to the API endpoint
# datas = []
# def fetch_data():
#     for i in available_stock_name:
#         response = requests.get('https://api.genderize.io?name='+i)

#         # Check the status code of the response
#         if response.status_code == 200:
#         # Access the response data
#             data = response.json()
#             datas.append(data)
#         else:
#             print('Failed to fetch data')

# # Create a new thread
# thread = threading.Thread(target=fetch_data)

# # Start the thread
# thread.start()

# # Wait for the thread to finish
# thread.join()


