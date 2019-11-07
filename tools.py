from fake_useragent import UserAgent
from requests import get
from bs4 import BeautifulSoup, SoupStrainer
from lxml.html import fromstring
from time import sleep
from threading import Thread
from pymorphy2 import MorphAnalyzer
from PIL import Image
from torrentool.api import Torrent
from torrentool.exceptions import BencodeDecodingError
from os import remove
from libtorrent import session, torrent_info


URL = 'http://pickfilm.ru/search/{}/1.html'
fixWord = lambda word, num: MorphAnalyzer().parse(word)[0].make_agree_with_number(num).word
torrentSize = lambda name: round(Torrent.from_file(name).total_size / 1024 / 1024 / 1024, 2)


def torrentSize(name):
    try:
        T = Torrent.from_file(name)
        return round(T.total_size / 1024 / 1024 / 1024, 2)
    except BencodeDecodingError:
        return 0


def getData(url):
    user = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    #MASK = {'user-agent': UserAgent().random}
    MASK = {'user-agent': user}
    data = get(url, headers=MASK).content
    return data


def download(name, url):
    with open(name, 'wb') as file:
        file.write(getData(url))
        file.close()
    return name


def parse(url, *flt):
    data = getData(url)
    bs = list(BeautifulSoup(data, 'lxml', parse_only=SoupStrainer('a')))[1:]
    arr = list(filter(lambda x: x and all(i in x for i in flt), map(lambda x: x.get('href'), bs)))
    arr = list(map(lambda x: 'http://pickfilm.ru' + x, arr))[::2]
    return arr


class Filmer:
    def __init__(self, url):
        self.url = url
        data = getData(url)
        lxml = fromstring(data)
        xname = '//*[@id="content"]/div[1]/div/div[3]/table/tbody/tr/td[1]/h1'
        ximg = '//*[@id="film-image"]/a'
        name = lxml.find('.//title').text.strip()
        self.name = name[:name.find(')') + 1]
        self.img = lxml.xpath(ximg)[0].get('href')
        self.tors = parse(url, '.torrent')


def imgResize(name):
    img = Image.open(name)
    img = img.resize((352, 511), Image.ANTIALIAS)
    img.save(name)
    return name
