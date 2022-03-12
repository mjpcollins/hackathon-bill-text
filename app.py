from flask import Flask
from config.conf import settings
from utils.keywords import get_features
from utils.get_bill_text import get_bill
import nltk
nltk.download('stopwords')
app = Flask(__name__)


@app.route('/')
def home():
    return 'OK'


@app.route('/bill/<bill_id>')
def bill(bill_id):
    print(bill_id)
    return get_bill(bill_id)


@app.route('/bill-features/<bill_id>')
def bill_features(bill_id):
    print(bill_id)
    return get_features(bill_id)


@app.route('/bill-amendments/<bill_id>')
def bill_amends(bill_id):
    print(bill_id)
    return {}


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
