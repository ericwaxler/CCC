# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
import csv

def get_price(currency):

    i_date = datetime.today() - timedelta(days=1)

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)

    str_date1 = i_date.date().strftime("%Y%m%d")
    str_date2 = datetime.today().date().strftime("%Y%m%d")
    # Visit the site
    base_url = 'https://coinmarketcap.com/currencies/'
    url = base_url + currency + '/historical-data/?start=' + str_date1 + '&end=' + str_date2
    print(url)

    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    resp = []

    for x in soup.select('table tr.text-right'):
        date = x.select_one('table td.text-left').text
        data = x.select('table td[data-format-value]')
        p_open = data[0]['data-format-value']
        p_high = data[1]['data-format-value']
        p_low = data[2]['data-format-value']
        p_close = data[3]['data-format-value']
        volume = data[4]['data-format-value']
        m_cap = data[5]['data-format-value']
        d_dict = {'Currency': currency, 'Date': date, 'Open': p_open, 'High': p_high, 'Low': p_low, 'Close': p_close, 'Volume': volume, 'Market Cap': m_cap}
        print(d_dict)
        resp.append(d_dict)

    browser.quit()
    return resp

monitored_currencies = ['bitcoin','litecoin','ripple','stellar','tether','ethereum','eos','bitcoin-cash','binance-coin','cardano']

for i in monitored_currencies:
    with open('target.csv','a') as cd:
        fieldnames = ['Currency','Date','Open','High','Low','Close','Volume','Market Cap']
        csv_writer = csv.DictWriter(cd, delimiter=',', quotechar='"', fieldnames=fieldnames)
        response = get_price(i)
        for x in response:
            print(x)
            csv_writer.writerow(x)