from flask import Flask, jsonify
from config.conf import settings
from utils.keywords import get_features
from utils.get_bill_text import (
    get_bill,
    get_amendments,
    split_amendments
)

app = Flask(__name__)


@app.route('/')
def home():
    return 'OK'


@app.route('/bill/<bill_id>')
def bill(bill_id):
    print(f'Getting information on {bill_id}')
    print(bill_id)
    print(f'Here is the information for {bill_id}')
    return jsonify(get_bill(bill_id))


@app.route('/bill-features/<bill_id>')
def bill_features(bill_id):
    print(bill_id)
    print(f'Finding amendments for {bill_id}')
    res = get_features(bill_id)
    print(f'Here are the features for {bill_id}')
    return jsonify(res)


@app.route('/bill-amendments/<bill_id>')
def bill_amends(bill_id):
    print(f'Finding amendments for {bill_id}')
    amendments = get_amendments(bill_id)
    split_out_amendments = split_amendments(amendments)
    return jsonify(split_out_amendments)


@app.route('/search/<keyword>')
def search(keyword):
    print(f'Searching for {keyword}...')
    bills = []
    for bill_id in settings['bills']:
        res = get_features(bill_id)
        for word in res['search_keywords']:
            if keyword.lower() == word.lower():
                bills.append(res)
    print(f'Found {len(bills)} results')
    return jsonify({'search_results': bills})


def run():
    app.run(
        host='0.0.0.0',
        port=settings['port']
    )


def debug():
    app.run(
        host='0.0.0.0',
        port='5000'
    )


if __name__ == '__main__':
    run()
