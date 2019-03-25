# -*- coding: utf-8 -*-
import unicodedata

def format_name(movie_name):
    movie_name = movie_name.strip().replace(" ","+")
    movie_name = unicodedata.normalize('NFKD', movie_name).encode('ASCII', 'ignore')    
    return movie_name