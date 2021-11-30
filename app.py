from model import *
import json

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/index')
def index():  # put application's code here
    return json.dumps({'feedback': 'index page'})


if __name__ == '__main__':
    app.run()
