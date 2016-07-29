from flask import Flask
from flask import *

app = Flask(__name__)

#Flask(__name__, template_folder="templates/bar_graph_full.html")


@app.route('/')
def run_bar_graph():

    return "test" + render_template('bar_graph_full.html')


@app.route('/hello')
def hello_world():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(debug=True)