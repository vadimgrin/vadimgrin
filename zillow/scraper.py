import time
from datetime import datetime
from urllib import request
from bs4 import BeautifulSoup
from random import randint
import os, re, pandas as pd
from decimal import Decimal
import webbrowser
import tempfile

homes = {
    "5 Godfrey":    "https://www.redfin.com/what-is-my-home-worth?propertyId=35751147",
    "233 Kelton":   "https://www.redfin.com/what-is-my-home-worth?propertyId=9000913",
    "15-50 Plaza":  "https://www.redfin.com/what-is-my-home-worth?propertyId=113729375",
    "15-11 Plaza":  "https://www.redfin.com/what-is-my-home-worth?propertyId=35727264",
    "15-17 Plaza":  "https://www.redfin.com/what-is-my-home-worth?propertyId=35727268",
    "58 Ellsworth": "https://www.redfin.com/what-is-my-home-worth?propertyId=35751944",
    "71 Lowell Rd": "https://www.redfin.com/what-is-my-home-worth?propertyId=35748911"
}
user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]


def scrape(html_bytes, pattern):
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, features="html.parser")
    amounts = re.findall(pattern, soup.prettify())
    if amounts:
        return Decimal(amounts[-1].split(":")[-1])
    else:
        return Decimal('0')


def webprint(values):
    hist_file = 'C:/Temp/houseValues.xlsx'
    try:
        df_hist = pd.read_excel(hist_file, parse_dates=[1])
        df_hist['Date'] = pd.to_datetime(df_hist['Date'])
    except Exception as e:
        print(f'Failed to read historical data from {hist_file} due to {e}... Initializing to default frame')
        df_hist = pd.DataFrame(Columns=['Date' + homes.keys()])
    finally:
        df_hist = df_hist.append(values, ignore_index=True)
        df_hist.to_excel(hist_file, float_format='%.0f', index=False)
        with tempfile.TemporaryFile(suffix='.html', delete=False) as fp:
            fp.write(bytes(df_hist.to_html(float_format="{:>10,.2f}".format, index=False).replace('<tr>', '<tr align="right">'), 'utf-8'))
        print(fp.name)
        webbrowser.open(fp.name)
        time.sleep(2)
        os.unlink(fp.name)


def report():
    opener = request.build_opener()
    opener.addheaders = [('User-agent', user_agent_list[randint(0, 4)])]
    pattern = re.compile('"predictedValue\\\\":[0-9.]+')
    total = 0
    date_column = datetime.today().strftime("%Y-%m-%d")
    values = {'Date': date_column}
    for k, v in homes.items():
        page = opener.open(v)
        amount = int(scrape(page.read(), pattern))
        total += amount
        values[k] = amount
        print(f"{k:12}: {amount:>14,.2f}")
    webprint(values)


if __name__ == '__main__':
    report()
