import os

with open('config/stopwords.txt', 'r') as F:
    stop_words = {w.replace('\n', '') for w in F.readlines()}

settings = {
    'port': int(os.environ.get("PORT", 8080)),
    'bills': ['1838', '2620', '2731', '2822', '2836'],
    'stop_words': stop_words
}
