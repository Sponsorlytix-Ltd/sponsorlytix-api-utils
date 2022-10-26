from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')
# Let's get a list of stop words from the NLTK library
stop = stopwords.words('english')
# These words are important for our problem. We don't want to remove them.
excluding = ['against', 'not', 'don', "don't", 'ain', 'aren', "aren't", 'couldn', "couldn't",
             'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
             'haven', "haven't", 'isn', "isn't", 'mightn', "mightn't", 'mustn', "mustn't",
             'needn', "needn't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
             "weren't", 'won', "won't", 'wouldn', "wouldn't"]
# New stop word list
stop_words = [word for word in stop if word not in excluding]
snow = SnowballStemmer('english')


def text_cleansing(text: str):
    # Check if the sentence is a missing value
    if isinstance(text, str) == False:
        text = ""
    filtered_sentence = []
    text = text.lower()  # Lowercase
    text = text.strip()  # Remove leading/trailing whitespace
    text = re.sub('\s+', ' ', text)  # Remove extra space and tabs
    text = re.compile('<.*?>').sub('', text)  # Remove HTML tags/markups:
    for w in word_tokenize(text):
        # Check if it is not numeric and its length > 2 and not in stop words
        if(not w.isnumeric()) and (len(w) > 2) and (w not in stop_words):
            # Stem and add to filtered list
            filtered_sentence.append(snow.stem(w))
    final_string = " ".join(filtered_sentence)  # final string of cleaned words

    return final_string
