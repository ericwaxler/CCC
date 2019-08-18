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

    if (i_date.date() == parse(soup.select_one('table td.text-left').text).date()):
        p_open = soup.select('table td[data-format-value]')[0]['data-format-value']
        p_high = soup.select('table td[data-format-value]')[1]['data-format-value']
        p_low = soup.select('table td[data-format-value]')[2]['data-format-value']
        p_close = soup.select('table td[data-format-value]')[3]['data-format-value']
        volume = soup.select('table td[data-format-value]')[4]['data-format-value']
        m_cap = soup.select('table td[data-format-value]')[5]['data-format-value']
        
        
        #resp = {'Currency': currency, 'Date': str_date1, 'Open': p_open, 'High': p_high, 'Low': p_low, 'Close': p_close, 'Volume': volume, 'MarketCap': m_cap}
        resp = [currency,str_date1,p_open,p_high,p_low,p_close,volume,m_cap]
        browser.quit()
        return resp
    else:
        browser.quit()
        return None

monitored_currencies = ['bitcoin','litecoin','ripple','stellar','tether','ethereum','eos','bitcoin-cash','binance-coin','cardano']

for x in monitored_currencies:
    with open('target.csv','a') as cd:
        csv_writer = csv.writer(cd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(get_price(x))