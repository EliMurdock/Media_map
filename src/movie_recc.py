import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix, save_npz, load_npz
import pickle
import os
from nltk.stem import PorterStemmer

class MovieRecommender:
    def __init__(self):
        self.ps = PorterStemmer()
        self.movie_df, self.similarity_chunks = self.load_similarity_data()
        if self.movie_df is None or self.similarity_chunks is None:
            self.movie_df, self.similarity_chunks = self.compute_similarity_data()

    def process_chunk(self, chunk):
        chunk = chunk.fillna('')
        chunk['tags'] = chunk['title'] + ' ' + chunk['genres'] + ' ' + chunk['overview'] + ' ' + chunk['original_title'] + ' ' + chunk['keywords']
        chunk['tags'] = chunk['tags'].apply(lambda x: x.lower())
        chunk['tags'] = chunk['tags'].str.replace(',', '', regex=False)
        chunk['tags'] = chunk['tags'].apply(lambda x: ' '.join([self.ps.stem(word) for word in x.split()]))
        return chunk[['id', 'title', 'tags']]

    def load_similarity_data(self):
        if os.path.exists('pkl_data/movie_list.pkl'):
            with open('pkl_data/movie_list.pkl', 'rb') as f:
                movie_df = pickle.load(f)
            similarity_files = sorted([f'pkl_data/{file}' for file in os.listdir('pkl_data') if file.startswith('similarity_') and file.endswith('.npz')])
            similarity_chunks = [load_npz(f) for f in similarity_files]
            return movie_df, similarity_chunks
        else:
            return None, None

    def compute_similarity_data(self, file_path='data/movie_data.csv', chunksize=1000, max_features=5000):
        if not os.path.exists('pkl_data'):
            os.makedirs('pkl_data')
        
        combined_features_list = []
        titles_list = []
        ids_list = []
        similarity_chunks = []
        chunk_index = 0

        reader = pd.read_csv(file_path, chunksize=chunksize)
        
        for chunk in reader:
            processed_chunk = self.process_chunk(chunk)
            combined_features_list.extend(processed_chunk['tags'])
            titles_list.extend(processed_chunk['title'])
            ids_list.extend(processed_chunk['id'])
            
            cv = CountVectorizer(max_features=max_features, stop_words='english')
            vector = cv.fit_transform(processed_chunk['tags'])
            vector = csr_matrix(vector)

            chunk_similarity = cosine_similarity(vector, vector)
            similarity_chunks.append(csr_matrix(chunk_similarity))
            save_npz(f'pkl_data/similarity_{chunk_index}.npz', csr_matrix(chunk_similarity))
            chunk_index += 1

        movie_df = pd.DataFrame({'id': ids_list, 'title': titles_list, 'tags': combined_features_list})

        with open('pkl_data/movie_list.pkl', 'wb') as f:
            pickle.dump(movie_df, f)

        return movie_df, similarity_chunks

    def recommend_movies(self, movie_name):
        index = self.movie_df[self.movie_df['title'] == movie_name].index[0]
        chunk_size = len(self.movie_df) // len(self.similarity_chunks)
        chunk_index = index // chunk_size
        local_index = index % chunk_size

        chunk_similarity = self.similarity_chunks[chunk_index].toarray()
        distances = sorted(list(enumerate(chunk_similarity[local_index])), reverse=True, key=lambda x: x[1])

        movie_indexes = [i[0] + chunk_index * chunk_size for i in distances[0:11]]
        recommended_movies = self.lookup_movies(movie_indexes)

        return recommended_movies

    def lookup_movies(self, movie_indexes):
        movie_data_file = 'data/movie_data.csv'
        movie_data = pd.read_csv(movie_data_file)

        columns_to_return = ['id', 'title', 'vote_average', 'vote_count', 'status', 'release_date', 
                             'revenue', 'runtime', 'adult', 'backdrop_path', 'budget', 'homepage', 
                             'imdb_id', 'original_language', 'original_title', 'overview', 
                             'popularity', 'poster_path', 'tagline', 'genres', 'production_companies', 
                             'production_countries', 'spoken_languages', 'keywords']

        movies = []
        for idx in movie_indexes:
            movie = {col: movie_data.iloc[idx][col] for col in columns_to_return}
            movies.append(movie)

        return movies

# Testing the class
def main():
    recommender = MovieRecommender()
    recommended_movies = recommender.recommend_movies('Alien')

    print("Recommended Movies For 'Alien':")
    for rec_idx, movie in enumerate(recommended_movies):
        print(f'{rec_idx + 1}. {movie["title"]}')

if __name__ == "__main__":
    main()
