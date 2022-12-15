# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:25:37 2022

@author: notta
"""
from recommender import Recommender
import pandas as pd

rcm=Recommender()
#for testing
words_dict=[{'keywords':['plane','crash','war'],'cast':['tomcruise','johhnydepp'],'director':'tonyscott', 'genres':['action']}]

#films=rcm.recommendation_from_profile(words_dict, 10)
films=rcm.recommendation_from_movie('Top Gun', 5)
#films=rcm.recommendation_naive(10)

