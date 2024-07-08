import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix, save_npz, load_npz, vstack
import pickle
import os
from nltk.stem import PorterStemmer

# Initialize the PorterStemmer
ps = PorterStemmer()

def process_chunk(chunk):
    chunk = chunk.fillna('')
    chunk['tags'] = chunk['title'] + ' ' + chunk['genres'] + ' ' + chunk['overview'] + ' ' + chunk['original_title'] + ' ' + chunk['keywords']
    chunk['tags'] = chunk['tags'].apply(lambda x: x.lower())
    chunk['tags'] = chunk['tags'].str.replace(',', '', regex=False)
    chunk['tags'] = chunk['tags'].apply(lambda x: ' '.join([ps.stem(word) for word in x.split()]))
    return chunk[['id', 'title', 'tags']]

def load_similarity_data():
    if os.path.exists('pkl_data/movie_list.pkl'):
        with open('pkl_data/movie_list.pkl', 'rb') as f:
            movie_df = pickle.load(f)
        similarity_files = sorted([f'pkl_data/{file}' for file in os.listdir('pkl_data') if file.startswith('similarity_') and file.endswith('.npz')])
        similarity_chunks = [load_npz(f) for f in similarity_files]
        return movie_df, similarity_chunks
    else:
        return None, None

def compute_similarity_data(file_path='data/movie_db.csv', chunksize=1000, max_features=5000):
    if not os.path.exists('pkl_data'):
        os.makedirs('pkl_data')
        
    combined_features_list = []
    titles_list = []
    ids_list = []
    similarity_chunks = []
    chunk_index = 0

    reader = pd.read_csv(file_path, chunksize=chunksize)
    
    for chunk in reader:
        processed_chunk = process_chunk(chunk)
        combined_features_list.extend(processed_chunk['tags'])
        titles_list.extend(processed_chunk['title'])
        ids_list.extend(processed_chunk['id'])
        
        # Vectorization
        cv = CountVectorizer(max_features=max_features, stop_words='english')
        vector = cv.fit_transform(processed_chunk['tags'])
        vector = csr_matrix(vector)  # Convert to sparse matrix

        # Compute cosine similarity for the chunk
        chunk_similarity = cosine_similarity(vector, vector)
        similarity_chunks.append(csr_matrix(chunk_similarity))
        save_npz(f'pkl_data/similarity_{chunk_index}.npz', csr_matrix(chunk_similarity))
        chunk_index += 1

    # Create the DataFrame for movies
    movie_df = pd.DataFrame({'id': ids_list, 'title': titles_list, 'tags': combined_features_list})

    # Save the processed data
    with open('pkl_data/movie_list.pkl', 'wb') as f:
        pickle.dump(movie_df, f)

    return movie_df, similarity_chunks

def recommend_similar_movies(movie_name, movie_df, similarity_chunks, top_n=10):
    # Find the index of the given movie in the DataFrame
    index = movie_df[movie_df['title'] == movie_name].index[0]

    # Determine the chunk and local index within the chunk
    chunk_size = len(movie_df) // len(similarity_chunks)
    chunk_index = index // chunk_size
    local_index = index % chunk_size

    # Calculate similarity distances from the appropriate chunk
    chunk_similarity = similarity_chunks[chunk_index].toarray()
    distances = sorted(list(enumerate(chunk_similarity[local_index])), reverse=True, key=lambda x: x[1])

    # Get the top N recommended movies (excluding the first one which is the movie itself)
    recommended_movies = [movie_df.iloc[i[0] + chunk_index * chunk_size].title for i in distances[1:top_n+1]]

    return recommended_movies

def main():
    # Load existing data if available, otherwise compute it
    movie_df, similarity_chunks = load_similarity_data()
    if movie_df is None or similarity_chunks is None:
        movie_df, similarity_chunks = compute_similarity_data()

    # Get recommendations for two movies
    recommendations1 = recommend_similar_movies('Toy Story', movie_df, similarity_chunks)
    recommendations2 = recommend_similar_movies('Alien', movie_df, similarity_chunks)

    # Print recommendations
    print("Recommended Movies For 'Toy Story':")
    for rec_idx in range(len(recommendations1)):
        print(f'{rec_idx+1}. {recommendations1[rec_idx]}')
    
    print("Recommended Movies For 'Alien':")
    for rec_idx in range(len(recommendations2)):
        print(f'{rec_idx+1}. {recommendations2[rec_idx]}')

if __name__ == "__main__":
    main()
