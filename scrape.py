from bs4 import BeautifulSoup
import requests

req_headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br",
               "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/71.0.3578.98 Safari/537.36 ', "Connection": "keep-alive"}

DOMAIN = 'https://msk.kassir.ru/category?main=3000&sort=0&keyword='


def get_html(url):
    '''
    Gets lxml text from given url.
            Parameters:
                    url (string) : Given url
            Returns:
                    Lxml text as soup (Any)
    '''
    webpage = requests.get(url, headers=req_headers)
    if webpage.status_code != 200:
        return 'error'
    else:
        return (BeautifulSoup(webpage.content, "lxml"))


def get_url(name):
    '''
    Gets url using input (what user search for).
            Parameters:
                    name (string) : Input request
            Returns:
                    Url as string
    '''
    url = f'{DOMAIN}{name}'
    return url


def check_add_concert(concerts, name, links):
    '''
    Checks if concert performer is similar to input. Adds a link of a
    concert in links if true.
            Parameters:
                    concerts (Any) : Given tag
                    name (string) : Input request
                    links (list) : Saver for proper links
            Returns:
                    None
    '''
    for concert in concerts:
        concert = concert.find('div', {'class': 'title'})
        nm = concert.text.replace(' ', '+').lower()
        if name in nm:
            links.append(concert.find('a')['href'])


def get_concerts(name, soup):
    '''
    Find concerts on webpage and returns list of proper.
            Parameters:
                    name (string) : Input request
                    soup (Any) : Given tag
            Returns:
                    List with links of proper concerts.
    '''
    links = []
    concerts = soup.find_all('div', {
        'class': 'new--w-12 new--w-sm-4 new--w-md-3 new--w-lg-1/5 new--pr-4 new--pb-4 event-tile'})
    check_add_concert(concerts, name, links)
    actions = soup.find_all('div', {
        'class': 'new--w-12 new--w-sm-4 new--w-md-3 new--w-lg-1/5 new--pr-4 new--pb-4 action-tile'})
    check_add_concert(actions, name, links)
    return links


def inf_conv(info):
    '''
    Converts string from site to good view for a bot.
            Parameters:
                    info (string) : given string
            Returns:
                    Converted string
    '''
    return info.replace('\n', '').replace('\xa0', '')


def get_concert_info(link):
    '''
    Gets all necessary info from a concert cite.
            Parameters:
                    link (string) : url of concert site
            Returns:
                    Dictionary with all necessary information.
    '''
    infodict = {}
    infodict['status'] = 'Found'

    page = get_html(link)

    infodict['url'] = link

    concertname = page.find('h1', {'data-ajaxupdateable': 'title'}).text
    infodict['name'] = inf_conv(concertname)

    date = page.find('div', {'class': 'date'}).text
    infodict['date'] = inf_conv(date)

    place = page.find('div', {'class': 'place-name'}).text
    infodict['place'] = inf_conv(place)

    adress = page.find('div', {'class': 'place-adress'}).text
    infodict['adress'] = inf_conv(adress)

    price = page.find('div', {'class': 'cost rub'}).find('span', {'class': 'price'}).text
    infodict['price'] = inf_conv(price)

    return infodict


def search_for_concerts(performer):
    '''
    Gets all necessary information about concerts, where is given
     performer.
            Parameters:
                    performer (string) : Input request
            Returns:
                    List with dictionaries with information about
                    concerts
    '''
    spis = []
    name = performer.replace(' ', '+').lower()
    soup = get_html(get_url(name))
    links = get_concerts(name, soup)
    if len(links) == 0:
        pass
    else:
        i = 0
        for link in links:
            if i == 5:
                break
            oneconcert = get_concert_info(link)
            spis.append(oneconcert)
            i += 1
    return spis

