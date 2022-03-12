from flask import Flask
from config.conf import settings
from utils.get_amendment_test import get_change
from utils.get_bill_text import get_bill
app = Flask(__name__)


@app.route('/')
def home():
    return 'OK'


@app.route('/bill/<bill_id>')
def bill(bill_id):
    print(bill_id)
    return get_bill(bill_id)

@app.route('/amendments/<bill_id>')
def change(bill_id):
    print(bill_id)
    return get_change(bill_id)

def run():
    app.run(host='0.0.0.0',
            port=settings['port'])


def debug():
    app.run(host='0.0.0.0',
            port='5000')


if __name__ == '__main__':
    run()
