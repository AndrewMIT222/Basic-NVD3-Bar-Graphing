from flask import Flask
from flask import *
import json
import MySQLdb
import monetdb.sql
import decimal
import urllib

app = Flask(__name__)

# Flask(__name__, template_folder="templates/bar_graph_full.html")


@app.route('/')
def run_bar_graph():

    return render_template('form.html')


@app.route('/hello')
def hello_world():
    return 'Hello world!'


@app.route('/form_submit')
def return_json():
    connection = monetdb.sql.connect(username="monetdb", password="monetdb", hostname="localhost", database="simple")
    cursor = connection.cursor()
    cursor.arraysize = 100
    c = request.args.get('query')
    cursor.execute(c)
    b = cursor.fetchall()
    '''
    a = {'yVals': [[37734107, 991417, 74476040, 37719753],
         [56586554400.73, 1487504710.38, 111701729697.74, 56568041380.9],
         [53758257134.87, 1413082168.05, 106118230307.61, 53741292684.6],
         [55909065222.83, 1469649223.19, 110367043872.5, 55889619119.83],
         [25.52, 25.52, 25.5, 25.51],
         [38273.13, 38284.47, 38249.12, 38250.86],
         [0.05, 0.05, 0.05, 0.05],
         [1478493, 38854, 2920374, 1478870]], 'xVals': ["AF", "NF", "NO", "RF"]}
    '''

    def decimal_default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError

    xVals = []
    yVals = []

    for x in b:
        xVals.append(x[0]+x[1])
    count = 2
    for x in range((len(b[0])) - 2):
        yInnerList = []
        for y in b:
            yInnerList.append(y[count])
        count += 1
        yVals.append(yInnerList)

    a = {"yVals": yVals, "xVals": xVals}

    return Response(json.dumps(a, default=decimal_default), mimetype='application/json'), urllib.quote(render_template('bar_graph_full.html'))


if __name__ == '__main__':
    app.run(debug=True)
