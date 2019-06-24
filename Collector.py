from Scraper import scraper
from datefinder import datefinder
import numpy as np
import csv
import re

singles = []
artists = []

dates = datefinder('2018/05/25', '1951/11/11')

csv.register_dialect('myDialect', delimiter='~', quoting=csv.QUOTE_NONE)
FileS = open('singles.csv', 'a')
writerS = csv.writer(FileS, dialect='myDialect')
FileA = open('artists.csv', 'a')
writerA = csv.writer(FileA, dialect='myDialect')
FileD = open('dates.csv', 'a')
writerD = csv.writer(FileD, dialect='myDialect')

for date in dates:
    sngs, arts = scraper(date)
    songs = []
    artists = []
    for sng in sngs:
        songs.append(re.sub('[^A-Za-z0-9_]+', ' ', sng))
    for art in arts:
        artists.append(re.sub('[^A-Za-z0-9_]+', ' ', art))
    writerS.writerow(songs)
    writerA.writerow(artists)
    writerD.writerow(date)
    singles.append(songs)
    artists.append(artists)
    print(date)

