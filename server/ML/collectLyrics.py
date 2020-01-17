import pandas as pd
import os
import csv

df = pd.read_csv('./songdata.csv')

lyrics = {}

for index, row in df.iterrows():
    if not row['artist'] in lyrics:
        lyrics[row['artist']] = row['text']
    else:
        lyrics[row['artist']] += row['text']

w = csv.writer(open('lyrics.csv', 'w'))
for key, val in lyrics.items():
    w.writerow([key, val])


        