# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:25:37 2022

@author: notta
"""
from recommender import Recommender


rcm=Recommender()

films=rcm.recommendation_keywords(5)

#kw=films.loc[0]['cast']

