from flask import Flask
from flask import *

app = Flask(__name__)

# Flask(__name__, template_folder="templates/bar_graph_full.html")


@app.route('/')
def run_bar_graph():

    return render_template('bar_graph_full.html')


@app.route('/hello')
def hello_world():
    return 'Hello world!'

@app.route('/json')
def return_json():
    return send_from_directory('static', 'nv.d3_example_graph1.json')


if __name__ == '__main__':
    app.run(debug=True)