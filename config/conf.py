import os
from bills import bills

with open('config/stopwords.txt', 'r') as F:
    stop_words = {w.replace('\n', '') for w in F.readlines()}

settings = {
    'port': int(os.environ.get("PORT", 8080)),
    'bills': list(bills.keys()),
    'stop_words': stop_words
}
