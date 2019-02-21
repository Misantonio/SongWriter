from scrapy.crawler import CrawlerProcess
from radiohead_song.settings import USER_AGENT
from radiohead_song.spiders.lyrics import LyricsScraper
import pandas as pd
import numpy as np

def artists_from_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    artists = []
    for line in lines:
        artist = line.replace('\n', '')
        artists.append(artist)
    return artists

def crawl_lyrics(artists):
    process = CrawlerProcess({
        'USER_AGENT': USER_AGENT
    })
    process.crawl(LyricsScraper, artists)
    process.start()

def build_corpus(file, col=None):
    df = pd.read_csv(file)
    if col:
        df = df[col]
    data = np.array(df)
    corpus  = ''
    for ix in range(len(data)):
        corpus += data[ix][0]
    corpus = corpus.encode('utf-8').strip()

    with open('corpus.txt', 'wb') as f:
        f.write(corpus)

def read_corpus():
    with open('corpus.txt', 'rb') as f:
        corpus = f.read()
    return corpus.decode('utf-8')


if __name__ == "__main__":
    # build_corpus('songs.csv', 'Lyrics')
    artists = artists_from_file('artists.txt')
    crawl_lyrics(artists)    