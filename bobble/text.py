## download nltk package using pip
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize 
import re

## download stopwords, wordnet
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

## our text
text = """Steve was born in Tokyo, Japan in 1950. He moved to London with his parents when he
was 5 years old. Steve started school there and his father began work at the hospital.
His mother was a house wife and he had four brothers.

He lived in England for 2 years then moved to Amman, Jordan where he lived there for
10 years. Steve then moved to Cyprus to study at the Mediterranean University.
Unfortunately, he did not succeed and returned to Jordan. His parents were very
unhappy so he decided to try in America.

He applied to many colleges and universities in the States and finally got some
acceptance offers from them. He chose Wichita State University in Kansas. His major
was Bio-medical Engineering. He stayed there for bout six months and then he moved
again to a very small town called Greensboro to study in a small college."""

## init PorterStemmer class
ps = PorterStemmer()

## init WordNetLemmatizer class
lemm = WordNetLemmatizer()

## lowercase text
lower_text  = text.lower()
print("1. Lowercase text:\n")
print(lower_text)

print("\n2. Remove Punctuations\n")
# remove punctuations and special characters
# define punctuation
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
no_punct = ""
for char in text:
    if char not in punctuations:
        no_punct = no_punct + char

# display the unpunctuated string
print(no_punct)

print("\n3. Remove Whitespace\n")
## remove whitespace
white_text = text.replace(' ', '')
white_text = white_text.replace('\n', '')
print(white_text)

print("\n4.Remove Stopwords\n")
stop_words = set(stopwords.words('english')) 
word_tokens = word_tokenize(no_punct) 
filtered_sentence = [w for w in word_tokens if not w in stop_words] 
filtered_sentence = [] 
for w in word_tokens: 
    if w not in stop_words: 
        filtered_sentence.append(w) 
print(filtered_sentence)

print("\n5. Stemming\n")
ps = PorterStemmer()   
for w in filtered_sentence: 
    print(w, " : ", ps.stem(w)) 

print("\n6. Lemmatize\n")
lemmatizer = WordNetLemmatizer() 
for w in filtered_sentence:
    print(w, ":", lemmatizer.lemmatize(w))
