import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml
import csv


def get_company_page_by_ticker(ticker):
    page = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'
    try:
        response = requests.get(page)
        print(f"Company page: {page}")
        return response
    except requests.exceptions.RequestException as ex:
        print(f"Oops! Something wrong. Could not access the page: {page}")
        raise SystemExit(ex)


def parse_company_page(html_response):
    soup = BeautifulSoup(html_response.text, features="lxml")
    company_name = soup.find(
        "div", id="Lead-3-QuoteHeader-Proxy").h1.contents[0]
    # news
    news = soup.find("li", class_="js-stream-content").find('a')
    news_link = "https://finance.yahoo.com" + news["href"]
    news_title = news.text
    # result
    parsed_data = {"company_name": company_name,
                   "news": {"link": news_link, "title": news_title}}
    return parsed_data


def save_company_news_into_csv(parsed_data):
    file_name = parsed_data["company_name"] + '_news_' + '.csv'
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['link', 'title']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(parsed_data["news"])


def download_and_transform_history_data_csv(parsed_data, ticker):
    file_name = parsed_data["company_name"] + '.csv'
    # downloading data
    df = yf.download(ticker, period="max")
    # adding transformed 'Close' column
    day3_before_change = df['Close'] / df['Close'].shift(-3)
    df['3day_before_change'] = day3_before_change
    # saving into csv
    df.to_csv(file_name)
    print("Data saved!")
