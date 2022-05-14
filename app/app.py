
# imports

import streamlit as lit
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
#import plotly.express as px

with open('data/artists.p', 'rb') as fp:
    artists = pickle.load(fp)
    
with open('data/genres.p', 'rb') as fp:
    genres = pickle.load(fp)

with open('data/genres_clean.p', 'rb') as fp:
    genres_clean = pickle.load(fp)
    
with open('data/artists_clean.p', 'rb') as fp:
    artists_clean = pickle.load(fp)

lit.set_page_config(page_title='Searching For The Sound', layout='wide')

def make_artist_vector(genres, artists, seed_artist):
    
    '''
    Inputs 
    - genres: list of genres by name
    - artists: dict with artists as keys and a list of their genres as values
    '''
    
    arr = np.zeros(len(genres), dtype=bool)
    
    if seed_artist in artists:
        styles = artists[seed_artist]
        style_pos = []
        
        for idx,genre in enumerate(genres):
            if genre in styles:
                pos = idx
                style_pos.append(pos)
        
        np.put(arr, style_pos, 1)
        return arr, seed_artist
    
    else:
        lit.write('Sorry, that artist does not exist in this dataset.')

def compare_artist(genres, artists_dict, seed, seed_arr):
    
    similarities = []
    artist_names = []
    
    for artist in artists_dict:
        if artist != seed:
            artist_names.append(str(artist))
            comp_arr = np.zeros(len(genres), dtype=bool)
            styles = artists_dict[artist]
            style_pos = []
            
            for idx,genre in enumerate(genres):
                if genre in styles:
                    pos = idx
                    style_pos.append(pos)
            
            np.put(comp_arr, style_pos, 1)
            sim = cosine_similarity(seed_arr.reshape(1,-1), comp_arr.reshape(1,-1))
            similarities.append(sim)
        else:
            continue
    
    #return similarities
    artist_sims = []
    
    for a,artist in zip(similarities,artist_names):
        for b in a:
            for c in b:
                tup = (artist, c) 
                artist_sims.append(tup)       
    
    return artist_sims

def sort_tuple(tup): 
  
    #reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    tup.sort(key = lambda x: x[1], reverse=True) 
    return tup[:10]   

title = 'Searching For The Sound'
lit.title(title)

lit.write('Hello! Welcome to Searching For The Sound, a new means of discovering music in the post-genre reality of 2022')
lit.markdown("##")

seed_artist = lit.text_input('Who do you want to find similar bands for?')

step1 = make_artist_vector(genres_clean, artists, seed_artist=seed_artist)
user_band = step1[1]
user_band_arr = step1[0]
lit.write(f"You entered {user_band}. Let's see what we can find!")

similar_artists = compare_artist(genres_clean, artists, user_band, user_band_arr)

top10 = sort_tuple(similar_artists)

lit.write(f'Here are some artists similar to {user_band}:')

for i in top10:
    lit.write(i[0])



