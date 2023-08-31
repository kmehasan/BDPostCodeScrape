from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

def getPostCodeFor(url):
    df = pd.read_html(url, header=0)[0]
    df = df.dropna(subset=['Post Code'])
    return df[["Post Office (English)","Post Code"]]


req = Request("https://bdpost.portal.gov.bd/site/page/f41a42bd-2540-4afa-8568-af56443c3df8")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

table = soup.find('table')

links = []

for row in table.find_all('tr'):
    for cell in row.find_all('td'):
        link = cell.find('a')
        if link:
            links.append(link['href'])

df = pd.DataFrame()
for url in links:
    df1 = getPostCodeFor(url)
    df = pd.concat([df, df1], axis=0)
df.to_csv("postcodes.csv", index=False)
