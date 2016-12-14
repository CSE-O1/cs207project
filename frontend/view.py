from flask import Flask, request, abort, jsonify, make_response, render_template
import json
from frontend.parsequery import parse_query
from server.DBClient import DBClient

app = Flask(__name__)

ts_client = DBClient(50000)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


# @app.route('/timeseries', methods=['GET'])
# def get_default_ts():
#     ts_client = DBClient(50000)
#     return_ts = ts_client.query(31)
#     return make_response(str(return_ts))


@app.route('/timeseries', methods=['GET'])
def get_timeseries():
    """
    mean_in = request.args.get('mean_in')
    std_in = request.args.get('std_in')
    blarg_in = request.args.get('blarg_in')
    level_in = request.args.get('level_in')
    level = request.args.get('level')
    """
    request_string = request.args
    for arg in request_string:
        arg_vals = parse_query(arg, request_string[arg])
        if arg == 'mean_in':
            # ts_queried = Timeseries
            # call for response
            msg = {}
            msg['type'] = 'mean_in'
            msg['min'] = arg[0]
            msg['max'] = arg[1]
            return_msg = ts_client.query(msg)
            #do something on return_msg
            

        elif arg == 'level_in':
            # call for response
            pass
    temp = "waiting"
    return jsonify(temp)


@app.route('/timeseries', methods=['POST'])
def post_timeseries():
    upload_data = request.get_json(force=True)
    if ('id' not in upload_data or 'time' not in upload_data or 'value' not in upload_data):
        return json.dumps("Invalid file.")
    # call for response
    # adds a new timeseries(stored in upload_data) into the database
    # 'id', 'time', 'value'

    print("Successfully saved!")


@app.route('/timeseries/<id>')
def timeseries_id(id):
    # testcases for Amy
    # x = [1, 2, 3]
    # y = [4, 5, 6]
    # matrix = [x, y]
    # return jsonify(matrix)


    # call for response
    # given id, return ts data and metadata
    ts = "ts"
    met = "met"
    return jsonify({"timeseries": ts, "metadata": met})


@app.route('/simquery', methods=['GET'])
def get_similar_ts():
    sim_id = request.args.get('id')
    n = request.args.get('n')
    if n is None:
        n = 5
    # call for response
    # return nth closest ts data to ts with sim_id
    temp = "waiting"
    return jsonify(temp)


@app.route('/simquery', methods=['POST'])
def post_similar_ts():
    input_data = request.get_json(force=True)
    if 'n' not in input_data:
        input_data['n'] = 5
    # call for response
    # return nth closest ts data to input_data
    temp = "waiting"
    return jsonify(temp)
