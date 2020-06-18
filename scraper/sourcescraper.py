from bs4 import BeautifulSoup
import requests, datetime
try:
    from scraper.database import addToNews
    from scraper.categories import predict
except ModuleNotFoundError:
    from database import addToNews
    from categories import predict

def scraper_timesofindia():
    BASE = 'https://timesofindia.indiatimes.com'
    url = 'https://timesofindia.indiatimes.com/news'

    s = requests.Session()

    html = s.get(url,headers={'User-Agent': 'Mozilla/5.0'}).text

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('li')

    for tag in tags:
        tmp = tag.find('a')

        try:
            url_new = tmp['href']
        except:
            url_new = None

        if url_new and url_new.startswith('/') and url_new.endswith('.cms'):
            article_url = BASE+url_new

            with s.get(article_url, headers={'User-Agent': 'Mozilla/5.0'}) as newstry:
                country = url_new.split('/')[1]

                sp = BeautifulSoup(newstry.text, 'html.parser')

                try:
                    title = sp.find('h1').text

                    if country!='world' or country!='india':
                        country = 'india'

                    category = predict(title)

                    addToNews(
                        country, title, article_url, 'Times of India',
                        datetime.datetime.utcnow(), category
                    )
                except AttributeError:
                    continue

def scraper_bbc():

    url = 'https://www.bbc.com'

    s = requests.Session()

    html = s.get(url,headers={'User-Agent': 'Mozilla/5.0'}).text

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('a',{'class':'block-link__overlay-link'})

    for tag in tags:
        url_tag = tag['href']

        if url_tag.startswith('/'):
            article_url = url+url_tag

            with s.get(article_url, headers={'User-Agent': 'Mozilla/5.0'}) as newstry:
                lit = article_url.split('/')
                if lit[len(lit)-1].startswith('in-pictures'):
                    continue

                sp = BeautifulSoup(newstry.text, 'html.parser')

                try:
                    title = sp.find('h1', {'class': "story-body__h1"}).text

                    category = predict(title)

                    addToNews(
                        'world', title, article_url, 'BBC News',
                        datetime.datetime.utcnow(), category
                    )
                except AttributeError:
                    continue

if __name__ == "__main__":
    scraper_timesofindia()
    scraper_bbc()
