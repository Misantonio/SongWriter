import scrapy
import pandas as pd
from azlyrics import Azlyrics
import time
import os
import random
import _pickle as pickle


song_file_path = "/home/misael/Documentos/radiohead_song/"

class LyricsScraper(scrapy.Spider):
    name = "lyrics"
    site = "https://www.azlyrics.com"
    artists = []

    def __init__(self, artists):
        super(LyricsScraper).__init__()
        urls = []
        self.fileExists = 'songs.csv' in os.listdir(song_file_path)
        self.prev_artists = []
        if self.fileExists: 
            print('\nFile songs.csv found. Loading...')
            self.prev_songs_df = pd.read_csv('songs.csv')
            print('File loaded!')
            g = self.prev_songs_df.groupby('Artist').apply(list)
            self.prev_artists = g.index.to_list()

        for artist in artists:
            artist = artist.lower()
            if artist in self.prev_artists:
                print('Skipping {}'.format(artist))
            else:
                urls.append("{}/{}/{}.html".format(self.site, artist[0], artist))
        self.start_urls = urls

    def parse(self, response):
        print('\n**** Visited: {} ****\n'.format(response.url))
        artist = response.url.split('/')[-1].split('.')[0]
        songs = response.xpath('//div[@id="listAlbum"]/a').xpath('text()').extract()
        lyrics = self.get_songs_lyrics(artist, songs)
        artists = [artist]*len(lyrics)

        songs_df = pd.DataFrame(data={'Lyrics': lyrics, 'Song': songs, 'Artist': artists})      
            
        if self.fileExists:
            print("Concatening ...")
            songs_df = pd.concat([self.prev_songs_df, songs_df])
            print("Reindexing ...")
            songs_df = songs_df.reset_index(drop=True)

        print("Saving file ...")
        songs_df.to_csv("/home/misael/Documentos/radiohead_song/songs.csv", index=False, encoding='utf-8')
        print('{} added. File saved to disk!\n'.format(artist))
        
    def get_songs_lyrics(self, artist, songs):
        lyrics = []
        prev = time.time()
        for i, song in enumerate(songs):
            print('**** {}. SONG: {} ****'.format(i, song))
            try:
                lyric = Azlyrics(artist, song).get_lyrics()[0][2:]
            except Exception as e:
                lyric = ""
            lyrics.append(lyric)
            t = random.randint(5, 15)
            time.sleep(t)
        print("{} took {:.2f} minutes to crawl.".format(artist ,(time.time()-prev)/60))
        return lyrics