import json
import nltk
nltk.download('genesis')
nltk.download('punkt')
nltk.download('stopwords')
import re
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
import ast
from nltk.util import ngrams
from nltk import FreqDist
from nltk.corpus import stopwords
import spacy
from collections import Counter

import numpy as np


nlp = spacy.load('en_core_web_md')

def load_data_from_file(file_path):
    """Load and return the data from the file."""
    with open(file_path, 'r') as file:
        data_string = file.read()
        data = ast.literal_eval(data_string)  # Safely evaluate the string to a Python object
    return data

def clean_text(text):
    # Preserve punctuation necessary for sentence parsing
    # This regex will remove digits and symbols except for common punctuation marks
    cleaned_text = re.sub(r'[^a-zA-Z,.!?;:\'"\s]', '', text)
    
    # Optionally, normalize whitespace to a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text.strip()

def extract_noun_chunks(text, exclusion_words):
    # Process the text with spaCy to extract noun chunks
    
    doc = nlp(text)
    noun_chunks = list(doc.noun_chunks)
    
    # Optionally, filter out stop words from noun chunks
    stop_words = set(stopwords.words('english'))
    filtered_chunks = []
    skip_chunks = exclusion_words
    for chunk in noun_chunks:
        chunk_text = ' '.join(token.text for token in chunk if token.text.lower() not in stop_words)
        if chunk_text not in skip_chunks:
            filtered_chunks.append(chunk_text)

    
    return filtered_chunks

def parse_chunks(chunks):
    chunk_frequencies = Counter(chunks)
    most_common = chunk_frequencies.most_common()
    print(most_common)

def cluster_similar_chunks(noun_chunks):
    clusters = []
    similarity_threshold=0.50
    length = len(noun_chunks)
    count = 1
    for chunk in noun_chunks:
        chunk_doc = nlp(chunk)
        # Attempt to fit the chunk into existing clusters
        fit_found = False
        for cluster in clusters:
            # Use the first item in each cluster as the representative for comparison
            representative_doc = nlp(cluster[0])
            if chunk_doc.similarity(representative_doc) > similarity_threshold:
                cluster.append(chunk)
                fit_found = True
                count += 1
                print(f'{count}/{length}')
                break  # Stop looking if we've found a fit for this chunk
        
        if not fit_found:
            # Start a new cluster with this chunk
            clusters.append([chunk])
            count += 1
            print(f'{count}/{length}')
    return clusters

def format_cluster_data(clusters):
    clusters_data = []
    for i, cluster in enumerate(clusters, start=1):
        cluster_info = {
            'cluster_id': i,
            'size': len(cluster),
            'phrases': cluster
        }
        clusters_data.append(cluster_info)

    cluster_json = json.dumps(clusters_data, ensure_ascii=False, indent=4)
    return cluster_json

def parse_cluster_json():
        # Load clusters from JSON file
    with open('clusters_data2.json', 'r', encoding='utf-8') as file:
        clusters = json.load(file)

    summaries = []

    for cluster in clusters:
        phrases = cluster['phrases']
        cluster_id = cluster['cluster_id']
        size = cluster['size']

        # Calculate frequency of phrases within the cluster
        phrase_freq = Counter(phrases)
        most_common_phrases = phrase_freq.most_common(1)  # Adjust as needed

        # Calculate average words per phrase
        avg_words_per_phrase = np.mean([len(phrase.split()) for phrase in phrases])

        # Define cluster weight (Example: size of the cluster * average words per phrase)
        cluster_weight = size * avg_words_per_phrase
        weighted_phrases = []
        # Append summary information for this cluster
        if size >= 4:     
            summaries.append({
                'cluster_id': cluster_id,
                'size': size,
                'phrases': phrases,
                'avg_words_per_phrase': avg_words_per_phrase,
                'weight': cluster_weight
            })
            
        
    # Optionally, sort summaries by their weight for prioritization
    summaries.sort(key=lambda x: x['weight'], reverse=True)
    with open('weighted_clusters2.json', 'w', encoding='utf-8') as file:
            json.dump(summaries, file, ensure_ascii=False, indent=4)
            
    return summaries

def cluster_chunks(text, exclusions):
    cleaned_text = clean_text(text)
    
    parsed_chunks = extract_noun_chunks(cleaned_text, exclusions)
    
    clusters = cluster_similar_chunks(parsed_chunks)
    
    return format_cluster_data(clusters)

# def main():
#     file_path = 'usabel.txt'  # Update this to the path of your file
#     data = load_data_from_file(file_path)
#     #print(data['game'])
    
#     user_comments = get_all_comment_text(data)
#     cleaned_comments = clean_text(user_comments)
#     # parse_raw_text(cleaned_comments) 
#     chunks = extract_noun_chunks(cleaned_comments)
#     # parse_chunks(chunks)
#     clusters = cluster_similar_chunks(chunks)

# # Sort clusters by their size to find the largest groups of similar phrases
#     format_and_save_cluster_data(clusters)

#     summaries = parse_cluster_json()
#     print(summaries)

# if __name__ == "__main__":
#     main()


