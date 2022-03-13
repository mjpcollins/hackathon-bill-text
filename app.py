from flask import Flask, jsonify, render_template
from flask_cors import CORS
from config.conf import settings
# from utils.get_amendment_test import get_change
from utils.keywords import get_features
from utils.get_bill_text import (
    get_bill,
    get_amendments,
    split_amendments,
    search_titles
)

from utils.newsfeed import newsfeed as get_newsfeed

app = Flask(__name__)
CORS(app)


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
    bill_info = get_bill(bill_id)
    amendments = get_amendments(bill_id)
    if amendments:
        split_out_amendments = split_amendments(amendments)
        bill_info['amendments'] = split_out_amendments
        bill_info['status'] = 'OK'
        return jsonify(bill_info)
    bill_info['status'] = 'No amendments found'
    return jsonify(bill_info)


@app.route('/search/<keyword>')
def search(keyword):
    print(f'Searching for {keyword}...')
    bills = []
    bills_ids = []
    for bill_id in settings['bills']:
        res = get_features(bill_id)
        for word in res['search_keywords']:
            if keyword.lower() == word.lower():
                bills_ids.append(bill_id)
                break

    bills_ids += search_titles(keyword)

    for bill_id in bills_ids:
        bill_info = get_bill(bill_id)
        bills.append(bill_info)

    print(f'Found {len(bills)} results')
    return jsonify({'search_results': bills})


@app.route('/amendments/<bill_id>')
def change(bill_id):
    print(bill_id)
    return get_change(bill_id)

@app.route('/newsfeed')
def newsfeed():
    nf = get_newsfeed()
    return render_template('newsfeed.html', feed=nf)


def run():
    app.run(
        host='0.0.0.0',
        port=settings['port'],
        debug=True
    )


def debug():
    app.run(
        host='0.0.0.0',
        port='5000'
    )


if __name__ == '__main__':
    run()
