from bs4 import BeautifulSoup
import requests, datetime

try:
    from scraper.database import addToNews
    from scraper.categories import predict
except ModuleNotFoundError:
    from database import addToNews
    from categories import predict


def scraper_timesofindia():
    """
    TODO: modify the scraper to support the new website structure
    """

    BASE = 'https://timesofindia.indiatimes.com'
    url = 'https://timesofindia.indiatimes.com/news'

    s = requests.Session()

    for i in range(1, 4):
        if i == 1:
            html = s.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
        else:
            html = s.get(url + f"/{i}", headers={'User-Agent': 'Mozilla/5.0'}).text

        tags = BeautifulSoup(html, 'html.parser').find('ul', {'class': "cvs_wdt clearfix"}).find_all('li')

        for tag in tags:
            anchor = tag.find('a')
            title = anchor['title']
            category = predict(title)
            art_url = BASE + anchor['href']
            short_desc = tag.select("#li:nth-child(3) > span.w_desc")
            print(short_desc, i)


def scraper_bbc():
    WIDTH = 800
    URL = 'https://www.bbc.com'
    url = 'https://www.bbc.com/news'

    s = requests.Session()

    html = s.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text

    soup = BeautifulSoup(html, 'html.parser')
    tags = set(soup.find('nav', {'role': 'navigation', 'aria-label': 'news'}).find_all('a'))

    for tag in tags:
        url_tag = tag['href']

        if url_tag.startswith('/'):
            article_url = URL + url_tag

            with s.get(article_url, headers={'User-Agent': 'Mozilla/5.0'}) as newstry:
                lit = article_url.split('/')
                if lit[len(lit) - 1].startswith('in-pictures'):
                    continue

                sp = BeautifulSoup(newstry.text, 'html.parser').find('div', {'class': 'gel-layout gel-layout--equal'})

                if sp:
                    individual = set(sp.find_all('div', {
                        'class': "gs-c-promo gs-t-News nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m \
                                 nw-p-default gs-c-promo--inline gs-c-promo--stacked@xl gs-c-promo--flex"}))

                    if len(individual):
                        for article in individual:
                            title = article.find('h3').text.strip("'")
                            short_desc = article.find('p').text
                            category = predict(title)
                            img_url = article.find('img')['data-src'].format(width=WIDTH)
                            art_url = URL + article.find('a')['href']

                            addToNews(
                                'world', title, art_url, 'BBC News',
                                datetime.datetime.utcnow().strftime("%d-%m-%Y"), short_desc, img_url, category
                            )


if __name__ == "__main__":
    # scraper_timesofindia()
    scraper_bbc()
