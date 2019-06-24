import numpy as np
import pandas as pd
import csv
import datetime
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.io import output_file, show
from bokeh.layouts import layout, widgetbox
from bokeh.models import CustomJS, WidgetBox
from bokeh.models.widgets import RangeSlider, TextInput

# Singles array
singles = []
sngs = open('singles.csv', "rt", encoding='utf8')
sngs = csv.reader(sngs, delimiter='~', quoting=csv.QUOTE_NONE)

i = 0
numweeks = 0
indexes = []

for sng in sngs:
    i += 1
    sngls = sng
    if len(sngls):
        numweeks += 1
        indexes.append(i)
        if len(sngls) < 100:
            sngls += [''] * (100 - len(sngls))
        if len(sngls) > 100:
            sngls = sngls[:100]
        # singles = np.concatenate((singles, sngls), 0)
# singles = np.reshape(singles, (numweeks, 100))
print('singles loaded')

artists = []
arts = open('artists.csv', "rt", encoding='utf8')
arts = csv.reader(arts, delimiter='~', quoting=csv.QUOTE_NONE)

# Artist array
i = 0
for art in arts:
    i += 1
    artsts = art
    if len(artsts) and i in indexes:
        if len(artsts) < 100:
            artsts += [''] * (100 - len(artsts))
        if len(artsts) > 100:
            artsts = artsts[:100]
        artists = np.concatenate((artists, artsts), 0)
artists = np.reshape(artists, (numweeks, 100))
print('artists loaded')

# Date array
dates = []
dts = open('dates.csv', "rt", encoding='utf8')
dts = csv.reader(dts, delimiter='~', quoting=csv.QUOTE_NONE)

i = 0
for dt in dts:
    i += 1
    date = np.asarray(dt)
    if len(date) and i in indexes:
        date = np.array([''.join([str(i) for i in date])])
        dates = np.concatenate((dates, date), 0)
print(len(dates), 'weeks of charts found')

ddates = pd.to_datetime(dates, infer_datetime_format=True)

# Compile list of artists
artistlist = []
for artistz in artists:
    for artist in artistz:
        if artist not in artistlist:
            artistlist.append(artist)
print(len(artistlist), 'artists identified')


def artistgen(artist, artists, dates):
    artistpositions = np.ones(len(dates)) * 101
    wk = 0
    for weeksartists in artists:
        pos = 1
        for artist2 in weeksartists:
            if artist in artist2:
                if artistpositions[wk] < 101:
                    break  # highest chart position only
                artistpositions[wk] = pos
            pos += 1
        wk += 1
    print('Loaded')
    return artistpositions

c = 0
def update(attr, old, new):
    # Add new artist
    global c
    colours = ['blue', 'red', 'green', 'fuchsia', 'purple', 'orangered', 'aqua']
    c = c % len(colours)
    artist = text_input.value.upper()
    artistpositions = artistgen(artist, artists, dates)
    p.line(ddates, artistpositions, legend=artist, line_width=1.2, line_alpha=0.8, line_color = colours[c])
    c += 1

p = figure(
    tools="xpan, xzoom_in, xzoom_out, reset, save",
    x_range=[pd.to_datetime(20080101, format='%Y%m%d'), pd.to_datetime(20181231, format='%Y%m%d')],
    y_range=[100, 0],
    title="Chart History", x_axis_label='Date', y_axis_label='Peak Chart Position',
    x_axis_type='datetime'
)

text_input = TextInput(value="Enter artist to view", title="Artist:")
text_input.on_change("value", update)

widgets = WidgetBox(text_input)
p.line([ddates[0], ddates[len(ddates)-1]], [1, 1], line_width=1.2, line_alpha=0.6, line_color="gold")
p.line([ddates[0], ddates[len(ddates)-1]], [10, 10], line_width=1.2, line_alpha=0.6, line_color="silver")
p.line([ddates[0], ddates[len(ddates)-1]], [40, 40], line_width=1.2, line_alpha=0.6, line_color="chocolate")
p.legend.location = "top_left"
p.legend.click_policy = "hide"
lay = layout([[p], [widgets]])
curdoc().add_root(lay)

