import re
import json
import requests
from collections import Counter
from nltk.tokenize import word_tokenize
from utils.get_bill_text import get_bill


def get_features(bill_name):
    """
    Look up the keywords and the sponsors to get some information on the bill

    :param bill_name: The ID of the bill
    :return: information
    """

    keywords = get_keywords(bill_name).most_common(20)
    category, sponsors = get_sponsors(bill_name)
    return {
        'keywords': keywords,
        'category': category,
        'sponsors': sponsors,
        'search_keywords': list(set(category + [k[0] for k in keywords]))
    }


def get_keywords(bill_number):
    """
    Using nltk stopwords and basic term frequency, extract keywords

    :param bill_number: bill to look up
    :return: List of the keywords ordered by frequency
    """

    text = get_bill(str(bill_number))['full_text']
    c = create_dict_of_words(text)
    return c


def create_dict_of_words(text):
    """
    Create a dict of all words with frequency as the value to the key

    :param text: Full text
    :return: Dict of freq: value
    """

    with open('config/stopwords.txt', 'r') as F:
        stop_words = {w.replace('\n', '') for w in F.readlines()}
    t = remove_unimportant_characters(text)
    word_tokens = word_tokenize(t)
    filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stop_words]
    return Counter(filtered_sentence)


def remove_unimportant_characters(text):
    """
    Remove characters that don't matter (e.g. numbers)

    :param text: Full text
    :return: Full text only words
    """

    return re.sub('[^A-Za-z ]+', '', text)


def get_sponsors(bill_number):
    """

    :param bill_number: Look up this bill and pull the sponsors
    :return: Sponsors and their details
    """

    r = requests.get(url=f'https://bills-api.parliament.uk/api/v1/Bills/{bill_number}')
    dict_content = json.loads(r.content)
    return list({sponsor.get('organisation', {}).get('name') for sponsor in dict_content.get('sponsors')}), dict_content


if __name__ == '__main__':
    a = get_features('2836')
    print(a)
