import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def load_and_compute_similarity(file_path='data/movie.db.csv'):
    # Load the dataset
    movies_df = pd.read_csv(file_path)

    # Process the dataset
    movie = movies_df[['id', 'title', 'genres', 'overview', 'original_title', 'keywords']]
    movie['tags'] = movie['title'] + ' ' + movie['genres'] + ' ' + movie['overview'] + ' ' + movie['original_title'] + ' ' + movie['keywords']
    movie['tags'] = movie['tags'].apply(lambda x: x.lower())
    movie['tags'] = movie['tags'].str.replace(',', '', regex=False)

    # Stemming the tags
    ps = PorterStemmer()
    movie['tags'] = movie['tags'].apply(lambda x: ' '.join([ps.stem(word) for word in x.split()]))

    # Vectorization
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(movie['tags']).toarray()

    # Compute cosine similarity
    similarity = cosine_similarity(vector)

    # Save the processed data and similarity matrix
    pickle.dump(movie, open('OTT/movie_list.pkl', 'wb'))
    pickle.dump(similarity, open('OTT/similarity.pkl', 'wb'))

    return movie, similarity

def recommend_similar_movies(movie_name, movie, similarity):
    # Find the index of the given movie in the DataFrame
    index = movie[movie['title'] == movie_name].index[0]

    # Calculate similarity distances
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    # Get the top 10 recommended movies (excluding the first one which is the movie itself)
    recommended_movies = [movie.iloc[i[0]].title for i in distances[1:11]]

    return recommended_movies

def main():
    # Load data and compute similarity matrix
    movie, similarity = load_and_compute_similarity()

    # Get recommendations for two movies
    recommendations1 = recommend_similar_movies('Toy Story', movie, similarity)
    recommendations2 = recommend_similar_movies('Alien', movie, similarity)

    # Print recommendations
    print("\033[1mRecommended Movies For 'Toy Story':\033[0m")
    for rec in recommendations1:
        print(rec)
    
    print("\033[1mRecommended Movies For 'Alien':\033[0m")
    for rec in recommendations2:
        print(rec)

if __name__ == "__main__":
    main()