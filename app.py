from flask import Flask, jsonify
from config.conf import settings
from utils.get_amendment_test import get_change
from utils.keywords import get_features
from utils.get_bill_text import get_bill

app = Flask(__name__)


@app.route('/')
def home():
    return 'OK'


@app.route('/bill/<bill_id>')
def bill(bill_id):
    print(bill_id)
    return jsonify(get_bill(bill_id))


@app.route('/bill-features/<bill_id>')
def bill_features(bill_id):
    print(bill_id)
    res = get_features(bill_id)
    return jsonify(res)


@app.route('/bill-amendments/<bill_id>')
def bill_amends(bill_id):
    print(bill_id)
    return jsonify({})


@app.route('/search/<keyword>')
def search(keyword):
    bills = []
    for bill_id in settings['bills']:
        res = get_features(bill_id)
        for word in res['search_keywords']:
            if keyword.lower() == word.lower():
                bills.append(bill_id)
    return jsonify({'search_results': bills})

@app.route('/amendments/<bill_id>')
def change(bill_id):
    print(bill_id)
    return get_change(bill_id)

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
