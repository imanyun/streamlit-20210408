import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

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
    data_udemy = get_data_udemy()
    today = datetime.date.today()
    data_udemy['date'] = datetime.date.today().strftime('%Y/%m/%d')    
    df = pd.read_csv('data.csv')
    df = df.append(data_udemy, ignore_index=True)
    df.to_csv('data.csv', index=False)

if __name__ == '__main__':
    main()