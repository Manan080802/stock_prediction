import requests
# import twilio
from twilio.rest import Client

STOCK_NAME = "TCS"
COMPANY_NAME = "TCS"


account_sid = ""
auth_token=""

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY=""
NEWS_API_KEY=""
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params={
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY

}

response = requests.get(STOCK_ENDPOINT,params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price=yesterday_data["4. close"]
print(yesterday_closing_price)

#TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday= data_list[1]
day_before_yesterday_closing_price=day_before_yesterday["4. close"]
print(day_before_yesterday_closing_price)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference=abs(float(yesterday_closing_price)-float(day_before_yesterday_closing_price))
print(difference)


#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent = (difference/float(yesterday_closing_price))*100
print(diff_percent)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if diff_percent >5:
    news_parms={
        "apiKey":NEWS_API_KEY,
        "qInTitle":COMPANY_NAME,
    }
    new_response = requests.get(NEWS_ENDPOINT,params=news_parms)
    new_response.raise_for_status()
    articles = new_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles,"\n\n\n\n")
    formatted_article = [f"Headline: {article['title']}. \n Brief: {article['description']}" for article in three_articles]
    print(formatted_article)
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=formatted_article,
        from_="",
        to=""
    )
    print(message.status)
    # print(new_response.json())
    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

