import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import altair as alt

def get_data_ec():
    url_ec = 'http://scraping.official.ec/'
    res = requests.get(url_ec)
    soup = BeautifulSoup(res.text, 'html.parser')
    itemList = soup.find('ul', {'id': 'itemList'})

    data_ec = []
    items = itemList.find_all('li')
    for item in items:
        datum_ec = {}
        datum_ec['title'] = item.find('p', {'class': 'items-grid_itemTitleText_b58666da'}).text
        price = item.find('p', {'class': 'items-grid_price_b58666da'}).text
        datum_ec['price'] = int(price.replace('¥ ', '').replace(',', ''))
        datum_ec['link'] = item.find('a')['href']
        is_stock = item.find('p', {'class': 'items-grid_soldOut_b58666da'}) == None
        datum_ec['is_stock'] = '在庫あり' if is_stock == True else '在庫なし'
        data_ec.append(datum_ec)
    
    df_ec = pd.DataFrame(data_ec)
    return df_ec

df_ec = get_data_ec()
df_udemy = pd.read_csv('data.csv')

st.title('Webスクレイピング活用アプリ')

st.write('## Udemy情報')

ymin1 = df_udemy['n_subscriber'].min() - 10
ymax1 = df_udemy['n_subscriber'].max() + 10

ymin2 = df_udemy['n_review'].min() - 10
ymax2 = df_udemy['n_review'].max() + 10

base = alt.Chart(df_udemy).encode(
    alt.X('date:T', axis=alt.Axis(title=None))
)

line1 = base.mark_line(opacity=0.3, color='#57A44C').encode(
    alt.Y('n_subscriber',
          axis=alt.Axis(title='登録者数', titleColor='#57A44C'),
          scale=alt.Scale(domain=[ymin1, ymax1]))
)

line2 = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
    alt.Y('n_review',
          axis=alt.Axis(title='レビュー数', titleColor='#5276A7'),
          scale=alt.Scale(domain=[ymin2, ymax2]))
)

chart = alt.layer(line1, line2).resolve_scale(
    y = 'independent'
)

st.altair_chart(chart, use_container_width=True) # グラフ化している


st.write('## EC在庫情報', df_ec)

