import json
import requests


def get_json_from_url(url):
    """
    Helper function to get information from a url

    :param url: URL to visit (must return a JSON parsable object)
    :return: Python Dict of data from URL
    """

    r = requests.get(url)
    dict_content = json.loads(r.content)
    return dict_content
