import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

def build_assessment_index(csv_path='shl_assessments.csv'):
    """
    Build a searchable index from the SHL assessments CSV file.
    Uses TF-IDF to create vectors for each assessment.
    """
    try:
        # Load assessments data
        df = pd.read_csv(csv_path)
        
        # Clean and prepare text data
        df['text_features'] = df['name'] + ' ' + df['description']
        df['text_features'] = df['text_features'].fillna('')
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english', 
                                     max_features=5000, 
                                     ngram_range=(1, 2))
        
        # Fit and transform the assessments
        tfidf_matrix = vectorizer.fit_transform(df['text_features'])
        
        # Save the model and matrix
        with open('assessment_vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)
        
        with open('assessment_tfidf_matrix.pkl', 'wb') as f:
            pickle.dump(tfidf_matrix, f)
        
        # Save the processed dataframe
        df.to_csv('processed_assessments.csv', index=False)
        
        print(f"Successfully built index with {len(df)} assessments")
        return vectorizer, tfidf_matrix, df
    
    except Exception as e:
        print(f"Error building assessment index: {e}")
        return None, None, None

def search_assessments(query, top_n=10, 
                      vectorizer_path='assessment_vectorizer.pkl',
                      matrix_path='assessment_tfidf_matrix.pkl',
                      df_path='processed_assessments.csv'):
    """
    Search for assessments that match the given query.
    Returns top_n most relevant assessments.
    """
    try:
        # Check if model files exist
        if not os.path.exists(vectorizer_path) or not os.path.exists(matrix_path) or not os.path.exists(df_path):
            # If not, build the index first
            vectorizer, tfidf_matrix, df = build_assessment_index()
            if vectorizer is None:
                # If we couldn't build the index, return an empty DataFrame
                return pd.DataFrame()
        else:
            # Load the vectorizer, matrix and dataframe
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            
            with open(matrix_path, 'rb') as f:
                tfidf_matrix = pickle.load(f)
            
            df = pd.read_csv(df_path)
        
        # Transform the query
        query_vector = vectorizer.transform([query])
        
        # Calculate similarity
        similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Get indices of top results
        top_indices = np.argsort(similarity_scores)[::-1][:top_n]
        
        # Get top assessments (always return up to top_n results)
        top_assessments = df.iloc[top_indices].copy()
        
        # Add similarity score
        top_assessments['similarity'] = similarity_scores[top_indices]
        
        # Format percentage for display
        top_assessments['similarity_pct'] = (top_assessments['similarity'] * 100).round(2)
        
        return top_assessments
    
    except Exception as e:
        print(f"Error searching assessments: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    build_assessment_index()