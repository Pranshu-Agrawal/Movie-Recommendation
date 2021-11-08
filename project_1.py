from flask import Flask
from flask import request
from flask import render_template
from bokeh.embed import components
from bokeh.plotting import figure
import pandas as pd
import numpy as np
import math
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from bokeh.io import output_file
from datetime import datetime, timedelta
app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def index():
    # table = pd.read_csv('NIFTY50_all.csv')
    # stock_symbols = table.Symbol.unique()
    
    if request.method == 'GET':
        return render_template('Login.html')

@app.route('/new_user',methods = ['GET','POST'])
def new_user():
    # table = pd.read_csv('NIFTY50_all.csv')
    # stock_symbols = table.Symbol.unique()
    
    if request.method == 'GET':
        return render_template('new_user.html')

@app.route('/new_movie',methods = ['GET','POST'])
def new_movie():
    # table = pd.read_csv('NIFTY50_all.csv')
    # stock_symbols = table.Symbol.unique()
    
    if request.method == 'GET':
        return render_template('New_Movie.html')

@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
    table = pd.read_csv('archive/movies.csv', encoding = "latin")
    movie_names = table.title.unique()
    if request.method == 'GET':
        return render_template('view.html', movie_names=movie_names)
    elif request.method =='POST':
        movie = request.form['movie']
        if(movie == "other") :
            return render_template('New_Movie.html')
        
        try :
            li = get_movie_recommendation(movie)['Title']
            return render_template('view.html', movie_names=movie_names, movie_list=li, movie=movie, rating=request.form['rating'])
        except IndexError :
            return render_template('view.html', movie=movie, movie_names=movie_names, rating=request.form['rating'], er="Doesn't have enough ratings to recommend!")


movies = pd.read_csv("archive/movies.csv", encoding = "latin")
ratings = pd.read_csv("archive/ratings.csv")
final_dataset = ratings.pivot(index='movieId',columns='userId',values='rating')
final_dataset.fillna(0,inplace=True)

no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted = ratings.groupby('userId')['rating'].agg('count')
final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 5].index,:]
final_dataset=final_dataset.loc[:,no_movies_voted[no_movies_voted > 5].index]

csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)

def get_movie_recommendation(movie_name):
    n_movies_to_reccomend = 10
    movie_list = movies[movies['title'] == movie_name]  
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
        return df.sort_values(by=['Distance'],ascending=True, ignore_index=True)
    else:
        return "No movies found. Please check your input"

# print(get_movie_recommendation('Toy Story (1995)'))

if __name__ == "__main__" :
    app.run(debug=True)