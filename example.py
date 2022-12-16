# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:25:37 2022

@author: notta
"""
from recommender import Recommender
import time

rcm=Recommender()
#for testing
words_dict=[{'keywords':['knight','tank','war'],'cast':['garyoldman','johhnydepp'],'director':['stanleykubrick','stevenspielberg'], 'genres':['action']}]
words_dict2=[{'keywords':['disney','laughs','funny'],'cast':['garyoldman','johhnydepp'],'director':['johnlasseter','stevenspielberg'], 'genres':['animation','comedy']}]

#%%
films=rcm.recommendation_naive(10,filters_to_apply=['director',['stevenspielberg']])
#films=rcm.recommendation_from_profile(words_dict, 10)



#%%
start = time.time()
films=rcm.recommendation_from_movie('Top Gun', 5)
end = time.time()
print(end - start)

#films=rcm.recommendation_naive(10)

start = time.time()
films=rcm.recommendation_from_movie('Home Alone', 5)
end = time.time()
print(end - start)

#%%

start = time.time()
films=rcm.recommendation_from_profile(words_dict, 10)
end = time.time()
print("total execute time: ",end - start)


#%%

dets=rcm.get_movie_details('Top Gun')