import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe


def get_data_udemy():
    data_udemy = {}
    url = 'https://scraping-for-beginner.herokuapp.com/udemy'
    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    soup.find_all('p', {'class': 'subscribers'})

    n_subscriber = soup.find('p', {'class': 'subscribers'}).text
    n_subscriber = int(n_subscriber.split('：')[1])

    n_review = soup.find('p', {'class': 'reviews'}).text
    n_review = int(n_review.split('：')[1])
    return {
        'n_subscriber': n_subscriber,
        'n_review': n_review
    }

def main():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = Credentials.from_service_account_file(
        'service_account.json',
        scopes=scopes
    )
    gc = gspread.authorize(credentials)    
    SP_SHEET_KEY = '1MlEQ5RfMJanndDRZVdpxRR7QMxThs0nbbvcFUGhovpk'
    sh = gc.open_by_key(SP_SHEET_KEY)    
    
    SP_SHEET = 'db'
    worksheet = sh.worksheet(SP_SHEET)    
    data= worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    
    data_udemy = get_data_udemy()

    today = datetime.date.today()
    data_udemy['date'] = datetime.date.today().strftime('%Y/%m/%d')    
    df = df.append(data_udemy, ignore_index=True)
    
    first_row = 1
    first_col = 1
    
    set_with_dataframe(worksheet, df, row=first_row, col=first_col)
    
if __name__ == '__main__':
    main()
