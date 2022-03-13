import re
import json
import requests
from collections import Counter
from config.conf import settings
from utils.get_bill_text import get_bill


def get_features(bill_name):
    """
    Look up the keywords and the sponsors to get some information on the bill

    :param bill_name: The ID of the bill
    :return: information
    """

    keywords = get_keywords(bill_name).most_common(40)
    category, sponsors = get_sponsors(bill_name)
    split_category = [
        c for cat in category
        for c in cat.lower().split(' ')
        if c not in settings['stop_words']
    ]

    return {
        'keywords': keywords,
        'category': category,
        'sponsors': sponsors,
        'search_keywords': list(set(split_category + [k[0].lower() for k in keywords]))
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

    t = remove_unimportant_characters(text)
    word_tokens = t.split(' ')
    filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in settings['stop_words']]
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
    result = list(
        sponsor.get('organisation', {})
        for sponsor in dict_content.get('sponsors')
    )
    print(result)
    res = [r.get('name') for r in result if isinstance(r, dict)]
    print(res)
    return res, dict_content


if __name__ == '__main__':
    a = get_features('2836')
    print(a)
