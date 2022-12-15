# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 10:15:00 2022

@author: notta
"""

import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_lists(metadata):
    #removes empty lists from metadata
    metadata = metadata.drop(metadata[metadata.astype(str)['cast'] == '[]'].index, axis=0)
    metadata = metadata.drop(metadata[metadata.astype(str)['crew'] == '[]'].index, axis=0)
    metadata = metadata.drop(metadata[metadata.astype(str)['genres'] == '[]'].index, axis=0)
    metadata = metadata.drop(metadata[metadata.astype(str)['keywords'] == '[]'].index, axis=0)
    metadata = metadata.drop(metadata[metadata.astype(str)['production_companies'] == '[]'].index, axis=0)
    metadata = metadata.drop(metadata[metadata.astype(str)['spoken_languages'] == '[]'].index, axis=0)
    return metadata

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])


def weighted_rating(x, m, C):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)

def get_recommendations(metadata, indices, title, cosine_sim, nb_movies_out):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the nb_movies_out most similar movies
    sim_scores = sim_scores[1:nb_movies_out+1]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return metadata.iloc[movie_indices]

class Recommender():
    """
    Recommender class with 3 recommandations methods: naive, content based and collaborative filtering
    """
    def __init__(self):
        metadata_path='tmdb_5000_movies.csv'
        credits_path='tmdb_5000_credits.csv'
        self.metadata=pd.read_csv(metadata_path, low_memory=False)
        self.movie_credits=pd.read_csv(credits_path, low_memory=False)
        self.m=0
        self.C=0
    
    def recommendation_naive(self, nb_movies_out):
        C = self.metadata['vote_average'].mean()
        #filter above m number of votes
        m = self.metadata['vote_count'].quantile(0.90)    
        q_movies = self.metadata.copy().loc[self.metadata['vote_count'] >= m]
        #apply weigthed score
        q_movies['score'] = q_movies.apply(weighted_rating, args=(m,C), axis=1)
        #sort
        q_movies = q_movies.sort_values('score', ascending=False)
        #take 10 best
        print(q_movies)
        recommendations=q_movies[['title', 'vote_count', 'vote_average', 'score']].head(nb_movies_out)
        return recommendations
    
    def recommendation_keywords(self, nb_movies_out):  
        # Merge keywords and credits into your main metadata dataframe
        movie_credits=self.movie_credits.rename(columns={'movie_id':'id'})
        movie_credits.drop(['title'], axis=1, inplace=True)
        metadata = self.metadata.merge(movie_credits, on='id')
        #conversion into dicts
        metadata=clean_lists(metadata)
        
        features = ['cast', 'crew', 'keywords', 'genres','production_companies','spoken_languages']
        for feature in features:
            metadata[feature]=metadata[feature].apply(lambda x: literal_eval(x))
            
        metadata['director'] = metadata['crew'].apply(get_director)
        
        features = ['cast', 'keywords', 'genres']
        for feature in features:
            metadata[feature] = metadata[feature].apply(get_list)
            
        features = ['cast', 'keywords', 'director', 'genres']
        for feature in features:
            metadata[feature] = metadata[feature].apply(clean_data)
        metadata['soup'] = metadata.apply(create_soup, axis=1)
        #begin the county stuff
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(metadata['soup'])
        cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
        
        # Reset index of your main DataFrame and construct reverse mapping as before
        metadata = metadata.reset_index()
        indices = pd.Series(metadata.index, index=metadata['title'])
        
        recommendation=get_recommendations(metadata, indices, 'The Dark Knight Rises', cosine_sim2, nb_movies_out)
        recommendation=recommendation.reset_index().to_dict(orient='index')
        return recommendation
    
    def recommandations_from_profile(self, words_dict, nb_movies_out):
        word
    
    

    
        
        
            

        
        
        
        