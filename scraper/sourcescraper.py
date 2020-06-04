from bs4 import BeautifulSoup
import requests, datetime
try:
    from scraper.database import addToNews
except ModuleNotFoundError:
    from database import addToNews

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
        except KeyError:
            url_new = None
        except TypeError:
            url_new = None

        if url_new and url_new.startswith('/') and url_new.endswith('.cms'):
            final = BASE+url_new

            with s.get(final, headers={'User-Agent': 'Mozilla/5.0'}) as newstry:
                country = url_new.split('/')[1]

                sp = BeautifulSoup(newstry.text, 'html.parser')

                try:
                    title = sp.find('h1').text.encode('utf-8')
                    body = sp.find('div', {'class': "_3WlLe clearfix"}).text.encode('utf-8')

                    if country!='world' or country!='india':
                        country = 'india'

                    addToNews(country, title, final, body, 'Times of India', datetime.datetime.utcnow())
                except AttributeError:
                    continue

def scraper_bbc():

    IGNORE = ['Email','Facebook','Messenger','Twitter','Pinterest','WhatsApp','LinkedIn','Copy this link','These are external links and will open in a new window', 'Share this with']
    url = 'https://www.bbc.com'

    s = requests.Session()

    html = s.get(url,headers={'User-Agent': 'Mozilla/5.0'}).text

    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('a',{'class':'block-link__overlay-link'})

    for tag in tags:
        url_tag = tag['href']

        if url_tag.startswith('/'):
            final = url+url_tag

            with s.get(final, headers={'User-Agent': 'Mozilla/5.0'}) as newstry:
                lit = final.split('/')
                if lit[len(lit)-1].startswith('in-pictures'):
                    continue
                # print(final)
                sp = BeautifulSoup(newstry.text, 'html.parser')

                try:
                    title = sp.find('h1', {'class': "story-body__h1"}).text.encode('utf-8')
                    # body_tag_div = sp.find('div', {'property':"articleBody"})
                    body_tag_p = sp.find_all('p')
                    body = "".encode('utf-8')
                    for tag_p in body_tag_p:
                        p = tag_p.text.encode('utf-8')
                        flag = False
                        for ele in IGNORE:
                            if p.decode().startswith(ele):
                                flag = True
                                break
                        if flag:
                            continue
                        body+=p

                    addToNews('world', title, final, body, 'BBC News', datetime.datetime.utcnow())
                except AttributeError:
                    continue

if __name__ == "__main__":
    scraper_timesofindia()
    scraper_bbc()

