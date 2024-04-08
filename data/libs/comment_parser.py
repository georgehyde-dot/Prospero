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




def load_data_from_file(file_path):
    """Load and return the data from the file."""
    with open(file_path, 'r') as file:
        data_string = file.read()
        data = ast.literal_eval(data_string)  # Safely evaluate the string to a Python object
    return data

def clean_text(text):
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Optionally, you might want to remove multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text.strip()

def get_all_comment_text(data):
    comments = ''
    search_list = ['love','like','great','fun','interesting','favorite','awesome','exciting','immersive'] 
    for comment in data['game']['comments']:
        with open('search_words_comments_updated.txt', 'a') as file:
            for word in search_list:
                if word in comment['comment']:
                    file.write(f'User: {comment['username']}, Rating {comment['rating']}\nNext Comment: {comment['comment']}\n\n')
                    break
        if comment['rating'] != 'n/a':
            if float(comment['rating']) > 7:    
                comments += f"{comment['comment']}\n"
    return comments

def parse_raw_text(text):
    tokens = nltk.word_tokenize(text)
    #words_to_remove = ['metal','coins', 'green', 'star', 'stretch','terrain','upgrade','upgraded','collectible', 'pack','onboardolympics', 'token']
    #filtered_tokens = [token for token in tokens if token.lower() not in words_to_remove]
    stop_words = set(stopwords.words('english'))
    # print(stop_words)
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    search_list = ['love','like','great','fun','interesting','favorite','awesome','exciting','immersive']
    
    
    # Process n-grams for lengths 1-8
    for n in range(2, 6):
        ngram_finder = ngrams(filtered_tokens, n)
        frequency_distribution = FreqDist(ngram_finder)
        
        # Get the 10 most common n-grams of this length
        most_common_ngrams = frequency_distribution.most_common(20)
        # final_ngrams = []
        # for word in search_list:
        #     for ngram in most_common_ngrams:
        #         if word in ngram[0]:
        #             if ngram not in final_ngrams:
        #                 final_ngrams.append(ngram)
        
        # print(f"Top 20 {n}-grams:")
        with open('top_words.txt', 'a') as file:                
            for ngram in most_common_ngrams:
                file.write(f"{' '.join(ngram[0])}\n\n")
            
# def main():
#     file_path = 'usabel.txt'  # Update this to the path of your file
#     data = load_data_from_file(file_path)
#     #print(data['game'])
    
#     user_comments = get_all_comment_text(data)
#     cleaned_comments = clean_text(user_comments)
#     #parse_raw_text(cleaned_comments) 

# if __name__ == "__main__":
#     main()