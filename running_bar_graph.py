from flask import Flask
from flask import *
import json
# import MySQLdb
import monetdb.sql
import sys
if sys.platform == 'linux2':
    import voodoo.sql
import decimal
# import urllib

app = Flask(__name__)

# Flask(__name__, template_folder="templates/bar_graph_full.html")

# runOnVoodoo = False


# this was the initial first page while the application was still based on a two-page layout
@app.route('/trial')
def run_bar_graph():
        return render_template('form.html')


# another beginning trial page
@app.route('/hello')
def hello_world():
    return 'Hello world!'


@app.route('/')
def return_json():
    def decimal_default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError

    query = request.args.get('query')
    if query == None:
        a = {"yVals": [], "xVals": [], "runTime": 0}

        data = json.dumps(a, default=decimal_default)

        a = json.loads(data)
    else:
        runningOn = request.args.get('option')
        if runningOn == 'voodoo':
            dbconnector = voodoo
        else:
            dbconnector = monetdb

        connection = dbconnector.sql.connect(username="monetdb", password="monetdb", hostname="localhost", database="simple")
        cursor = connection.cursor()
        cursor.execute(query)
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

        cursor2 = connection.cursor()
        d = "trace " + request.args.get('query')
        cursor2.execute(d)
        e = cursor2.fetchall()

        xVals = []
        yVals = []

        column_descriptions = cursor.description
        chartNames = []
        for x in column_descriptions:
            chartNames.append(x[0])

        for x in b:
            xVals.append(x[0]+x[1])
        count = 2
        for x in range((len(b[0])) - 2):
            yInnerList = []
            for y in b:
                yInnerList.append(y[count])
            count += 1
            yVals.append(yInnerList)

        timeTook = e[-1][0]

        a = {"chartNames": chartNames, "yVals": yVals, "xVals": xVals, "runTime": timeTook}

        data = json.dumps(a, default=decimal_default)

        a = json.loads(data)

    return render_template("bar_graph_full.html", data=a, timeTook=a.get("runTime"))


# page to return data in a json format; not fully functional
@app.route('/get_data.json')
def return_json_get_data():

    runOnVoodoo = request.form.get('dbsystem')
    if runOnVoodoo:
        dbconnector = voodoo
    else:
        dbconnector = monetdb

    connection = dbconnector.sql.connect(username="monetdb", password="monetdb", hostname="localhost", database="simple")
    cursor = connection.cursor()
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

    cursor2 = connection.cursor()
    d = "trace " + request.args.get('query')
    cursor2.execute(d)
    e = cursor2.fetchall()

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

    timeTook = e[-1][0]

    a = {"yVals": yVals, "xVals": xVals, "runTime": timeTook}

    data = json.dumps(a, default=decimal_default)

    a = json.loads(data)

#    resp = Response(a, status=200, mimetype='application/json')

#    return resp

    return jsonify(a)

if __name__ == '__main__':
    app.run(debug=True)
