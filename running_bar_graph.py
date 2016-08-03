from flask import Flask
from flask import *
import json
import MySQLdb
import monetdb.sql
import decimal

app = Flask(__name__)

# Flask(__name__, template_folder="templates/bar_graph_full.html")

'''
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
'''

@app.route('/')
def run_bar_graph():

    return render_template('bar_graph_full.html')


@app.route('/hello')
def hello_world():
    return 'Hello world!'


@app.route('/data.json')
def return_json():
    connection = monetdb.sql.connect(username="monetdb", password="monetdb", hostname="localhost", database="simple")
    cursor = connection.cursor()
    cursor.arraysize = 100
    cursor.execute("SELECT l_returnflag, l_linestatus, sum(l_quantity) AS sum_qty, sum(l_extendedprice) AS sum_base_price, sum(l_extendedprice * (1 - l_discount)) \
    AS sum_disc_price, sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS sum_charge, avg(l_quantity) AS avg_qty, avg(l_extendedprice) AS avg_price, avg(l_discount) \
    AS avg_disc, count(*) AS count_order FROM lineitem WHERE l_shipdate <= date '1998-12-01' - interval '90' day (3) GROUP BY l_returnflag, l_linestatus ORDER BY \
    l_returnflag, l_linestatus")
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

    return Response(json.dumps(a, default=decimal_default), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
