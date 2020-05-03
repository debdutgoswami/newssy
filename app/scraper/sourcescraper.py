from bs4 import BeautifulSoup
import requests
try:
    from scraper.database import addToNews
except ModuleNotFoundError:
    from database import addToNews

def timesofindia():
    url = 'https://timesofindia.indiatimes.com'

    s = requests.Session()

    html = s.get(url,headers={'User-Agent': 'Mozilla/5.0'}).text

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('li')

    for tag in tags:
        tmp = tag.find('a')

        try:
            url_new = tmp['href']
        except TypeError:
            url_new = None

        if url_new and url_new.startswith('/') and url_new.endswith('.cms'):
            final = url+url_new
            with s.get(final, headers={'User-Agent': 'Mozilla/5.0'}) as newstry:
                country = url_new.split('/')[1]
                print(final)
                sp = BeautifulSoup(newstry.text, 'html.parser')

                try:
                    title = sp.find('h1').text.encode('utf-8')
                    body = sp.find('div', {'class': "_3WlLe clearfix"}).text.encode('utf-8')

                    if country!='world' or country!='india':
                        country = 'india'

                    addToNews(country, title, body)
                except AttributeError:
                    continue

if __name__ == "__main__":
    timesofindia()

