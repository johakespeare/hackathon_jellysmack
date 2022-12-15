# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:25:37 2022

@author: notta
"""
from recommender import Recommender
import pandas as pd

rcm=Recommender()
words_dict=[{'keywords':'plane crash war','cast':'tomcruise johhnydepp','director':'tonyscott', 'genres':'action'}]

films=rcm.recommendation_from_profile(words_dict, 10)
#films=rcm.recommendation_keywords('Home Alone', 5)

#kw=films.loc[0]['cast']

