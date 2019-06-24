from bs4 import BeautifulSoup
import urllib.request


def scraper(date):

    date = str(date)
    baseurl = str('http://www.officialcharts.com/charts/singles-chart/')
    url = baseurl + date + '/7501/'
    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page, "lxml")

    singles = []
    artists = []

    for single in soup.findAll('div', {"class": "title"}):
        single = ''.join(single.text)
        single = single[1:-1]
        singles.append(single)

    for artist in soup.findAll('div', {"class": "artist"}):
        artist = ''.join(artist.text)
        artist = artist[1:-1]
        artists.append(artist)

    return singles, artists

