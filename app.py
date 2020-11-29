import pandas as pd
from flask import Flask, redirect, url_for, render_template, request

METADATA = pd.read_csv('C:/Users/User/Documents/python_project/flask/IMDBdata_MainData2.csv', low_memory=False)

app = Flask(__name__)

def imdb_rating_recommendation(n):
    metadata_cleaned = METADATA.dropna(subset = ['imdbRating'])
    metadata_sorted = metadata_cleaned.sort_values('imdbRating', ascending=False)
    return metadata_sorted[['Title', 'imdbRating']].head(n)                                                

def metascore_rating_recommendation(n):
    metadata_cleaned = METADATA.dropna(subset = ['Metascore'])
    metadata_sorted = metadata_cleaned.sort_values('Metascore', ascending=False)
    return metadata_sorted[['Title', 'Metascore']].head(n)

def averaged_ratings_recommendation(n):
    metadata_cleaned = METADATA.dropna(subset = ['imdbRating', 'Metascore'])
    metadata_cleaned['averagedRating'] = (
        (metadata_cleaned['Metascore']  / 10.0) + 
        metadata_cleaned['imdbRating']) / 2.0
    metadata_sorted = metadata_cleaned.sort_values('averagedRating', ascending=False)
    return metadata_sorted[['Title', 'averagedRating']].head(n)

def filter_by_type(input_type):
    #example input: series, movie
    metadata_cleaned = METADATA.dropna(subset = ['Type'])
    return metadata_cleaned[METADATA['Type'] == input_type]

def filter_by_genre(input_genre):
    input_genre = input_genre.lower()
    metadata_cleaned = METADATA.dropna(subset = ['Genre'])
    return metadata_cleaned[metadata_cleaned['Genre'].str.lower().str.contains(input_genre)]

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/', methods=['POST'])
def response():
    if request.method == 'POST':
        print(request.form)
        number_str = request.form['inputNumber']
        number = int(number_str)
        if request.form['submit_button'] == 'imdb':
            return render_template("index.html", table=imdb_rating_recommendation(number).to_html())
        elif request.form['submit_button'] == 'metascore':
            return render_template("index.html", table=metascore_rating_recommendation(number).to_html())
        elif request.form['submit_button'] == 'average':
            return render_template("index.html", table=averaged_ratings_recommendation(number).to_html())
    else:
        return render_template("index.html")

#print(imdb_rating_recommendation(5))
#print(ratings_value_recommendation(5))
#print(metascore_rating_recommendation(5))
#print(averaged_ratings_recommendation(5))

if __name__ == '__main__':
	app.run()
