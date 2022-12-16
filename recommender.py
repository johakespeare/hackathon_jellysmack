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

import time

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
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + ' '.join(x['director'])+ ' ' + ' '.join(x['genres'])


def weighted_rating(x, m, C):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)

def prepare_df(metadata):
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
    return metadata



def get_recommendations_from_movie(metadata, indices, title, cosine_sim, nb_movies_out, filters_to_apply=None):
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
    Recommender class with 3 recommandations methods: naive, content-based from movie and content-based from profile
    
    output: dict of len nb_movies_out
    {index:{budget, cast, crew, director, genres, id, index, keywords, original_language, original_title, popularity, production_companies,
            production_countries, release_date, revenue, runtime, score, spoken_languages, status,
            tagline, title, vote_average, vote_count}}
    """
    def __init__(self):
        metadata_path='tmdb_5000_movies.csv'
        credits_path='tmdb_5000_credits.csv'
        self.metadata=pd.read_csv(metadata_path, low_memory=False)
        self.metadata.drop(['homepage'], axis=1, inplace=True)
        self.movie_credits=pd.read_csv(credits_path, low_memory=False)
        self.m=0
        self.C=0
        self.flag_cosine_sim_computed=False
        self.flag_data_prepared=False
        # Merge keywords and credits into your main metadata dataframe
        movie_credits=self.movie_credits.rename(columns={'movie_id':'id'})
        movie_credits.drop(['title'], axis=1, inplace=True)
        self.metadata = self.metadata.merge(movie_credits, on='id')
        self.flag_weighted_rating=False
        
    def get_movie_details(self, title):
        df_details=prepare_df(self.metadata)
        return df_details[df_details['title']==title]
        
    
    def recommendation_naive(self, nb_movies_out, filters_to_apply=None):
        '''
        
        Parameters
        ----------
        nb_movies_out : TYPE
            DESCRIPTION.
        filters_to_apply : List, optional
            DESCRIPTION. Filter by genre, director, cast or keywords [key_string, value_string]

        Returns
        -------
        recommendations : TYPE
            DESCRIPTION.

        '''
        
        if self.flag_data_prepared:
            metadata=self.prepared_metadata            
        else:        
            metadata=prepare_df(self.metadata)
            self.prepared_metadata=metadata
            self.flag_data_prepared=True
        
        if filters_to_apply:
            key=filters_to_apply[0]
            value=filters_to_apply[1]
            if key=='genres':
                mask = metadata.genres.apply(lambda x: any(item for item in value if item in x))
            elif key=='director':
                mask = metadata.director.apply(lambda x: any(item for item in value if item in x))
            elif key=='cast':
                mask = metadata.cast.apply(lambda x: any(item for item in value if item in x))
            elif key=='keywords':
                mask = metadata.keywords.apply(lambda x: any(item for item in value if item in x))
            metadata=metadata[mask]

        if not self.flag_weighted_rating:           
            C = metadata['vote_average'].mean()
            #filter above m number of votes
            m = metadata['vote_count'].quantile(0.90)    
            q_movies = metadata.copy().loc[metadata['vote_count'] >= m]
            #apply weigthed score
            q_movies['score'] = q_movies.apply(weighted_rating, args=(m,C), axis=1)
            #sort
            q_movies = q_movies.sort_values('score', ascending=False)
            self.q_movies=q_movies
            self.flag_weighted_rating=True;
            #take 10 best
        recommendations=self.q_movies.head(nb_movies_out)
        recommendations=recommendations.reset_index().to_dict(orient='index')

        return recommendations        
    
    def recommendation_from_movie(self, title, nb_movies_out, filters_to_apply=None):  
                
        #conversion into dicts
        metadata=clean_lists(self.metadata)
        
        if filters_to_apply:
            key=filters_to_apply[0]
            value=filters_to_apply[1]
            mask = metadata.genres.apply(lambda x: any(item for item in value if item in x))
            metadata=metadata[mask]
        
        if self.flag_data_prepared:
            metadata=self.prepared_metadata            
        else:        
            metadata=prepare_df(metadata)
            self.prepared_metadata=metadata
            self.flag_data_prepared=True
        
        metadata['soup'] = metadata.apply(create_soup, axis=1)
        
        #speedy stuff
        if self.flag_cosine_sim_computed:

            cosine_sim2=self.cosine_sim2
        else:           
            count = CountVectorizer(stop_words='english')
            count_matrix = count.fit_transform(metadata['soup'])
            cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
            self.cosine_sim2=cosine_sim2
            self.flag_cosine_sim_computed=True
            
        if filters_to_apply:
            key=filters_to_apply[0]
            value=filters_to_apply[1]
            metadata=metadata[value in metadata[key]]

        # Reset index of your main DataFrame and construct reverse mapping as before
        metadata = metadata.reset_index()
        indices = pd.Series(metadata.index, index=metadata['title'])
        
        recommendation=get_recommendations_from_movie(metadata, indices, title, cosine_sim2, nb_movies_out)
        recommendation=recommendation.reset_index().to_dict(orient='index')
        
        return recommendation
    
    def recommendation_from_profile(self, words_dict, nb_movies_out, filters_to_apply=None):
        '''

        Parameters
        ----------
        words_dict : dictionnary
            contains relevant information from user profile
            {keywords: string[], cast: string[], director: string, genres: string[]}
        nb_movies_out : int
            number of recommendations
        flag_update_profile: boolean
            False by default, set to True to make new recommandations when profile changes

        Returns
        -------
        recommendation : dict
            see class description

        '''
        #for fake_movie
        keywords=words_dict[0]['keywords']
        casts=words_dict[0]['cast']
        directors=words_dict[0]['director']
        genres=words_dict[0]['genres']
               
        #conversion into dicts
        metadata=clean_lists(self.metadata)
        
        if filters_to_apply:
            key=filters_to_apply[0]
            value=filters_to_apply[1]
            metadata=metadata[value in metadata[key]]
        
        if self.flag_data_prepared:
            metadata=self.prepared_metadata            
        else:        
            metadata=prepare_df(metadata)
            self.prepared_metadata=metadata
            self.flag_data_prepared=True
        
        #make fake movie from keywords
        fake_movie={'title': 'fake_movie', 'keywords': keywords, 'cast': casts, 'director': directors, 'genres': genres }
        
        fake_movie_row=pd.DataFrame([fake_movie])
        metadata=metadata.append(fake_movie_row, ignore_index=True).fillna("")
                
        metadata['soup'] = metadata.apply(create_soup, axis=1)
                
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(metadata['soup'])
        cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
        
        if filters_to_apply:
            key=filters_to_apply[0]
            value=filters_to_apply[1]
            metadata=metadata[metadata[key]==value]
                
        # Reset index of your main DataFrame and construct reverse mapping as before
        metadata = metadata.reset_index()
        indices = pd.Series(metadata.index, index=metadata['title'])
        
        recommendation=get_recommendations_from_movie(metadata, indices, 'fake_movie', cosine_sim2, nb_movies_out)
        recommendation=recommendation.reset_index().to_dict(orient='index')        
        
        return recommendation
        
    