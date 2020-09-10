import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml
import csv

from helpers import get_company_page_by_ticker, parse_company_page, save_company_news_into_csv, download_and_transform_history_data_csv


def run_app():
    while True:
        ticker = input("Please, enter company ticker to get data or 'q' for quit: ")

        if ticker == 'q':
            print("App stopped. Bye!")
            break
        else:
            print("Processing...")
            ticker = ticker.upper()
            company_page = get_company_page_by_ticker(ticker)
            company_data = parse_company_page(company_page)
            # saving news
            save_company_news_into_csv(company_data)
            # saving finance data
            download_and_transform_history_data_csv(company_data, ticker)
            print("Done")


if __name__ == "__main__":
    run_app()
