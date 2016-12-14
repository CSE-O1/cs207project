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
    msg = {}
    for arg in request_string:
        arg_vals = parse_query(arg, request_string[arg])
        if arg == 'mean_in':
            # ts_queried = Timeseries
            # call for response
            msg['type'] = 'mean_in'
            msg['mean_in'] = [arg_vals[0], arg_vals[1]]
            return_msg = ts_client.query(msg)
            #return_msg should be a metadata array
            return jsonify({"mean_in" : return_msg})
        elif arg == 'level_in':
            msg['type'] = 'level_in'
            msg['level_in'] = arg_vals
            return_msg = ts_client.query(msg)
            #return_msg should be a metadata array
            #be careful, msg['level_in'] is a array
            return jsonify({"level_in" : return_msg})

    msg['type'] = 'all'
    return_msg = ts_client.query(msg)
    # return_msg should be all metadata
    return jsonify({"metadata_all": return_msg})


@app.route('/timeseries', methods=['POST'])
def post_timeseries():
    upload_data = request.get_json(force=True)
    if ('id' not in upload_data or 'time' not in upload_data or 'value' not in upload_data):
        return json.dumps("Invalid file.")

    # call for response
    # adds a new timeseries(stored in upload_data) into the database
    # 'id', 'time', 'value'
    msg = {}
    #upload_data['id'] is id
    #upload_data['value'] is the upload ts data's value
    #upload_data['time'] is the upload ts data's time
    msg['type'] = 'ts_data'
    #be careful 'id' may already exist, in this case update this ts
    msg['ts_data'] = [upload_data['id'], upload_data['value'], upload_data['time']]
    #return this ts
    return_msg = ts_client.query(msg)
    print("Successfully saved!")
    return json.dumps(return_msg)


@app.route('/timeseries/<id>')
def timeseries_id(id):
    # call for response
    # given id, return ts data and metadata
    msg = {}
    msg['type'] = 'id'
    msg['id'] = id

    print(id);
    print(msg);
    #return_msg format:
    #return_msg = { 'exist': "yes" or "no",
    #               'tsdata': xxxx,
    #               'metadata': xxxx}
    # if this id does not exit, return
    return_msg = ts_client.query(msg)
    if return_msg['exist'] == "no":
        return jsonify("Timeseries id does not exist!")

    return jsonify({"tsdata": return_msg['tsdata'], "metadata": return_msg['metadata']})


@app.route('/simquery', methods=['GET'])
def get_similar_ts():
    sim_id = request.args.get('id')
    n = request.args.get('n')
    if n is None:
        n = 5
    # call for response
    # return nth closest ts data to ts with sim_id
    msg = {}
    msg['type'] = 'ss_id'
    msg['id'] = id
    msg['n'] = n
    #return_msg should be a ts array
    #[ts1, ts2, ... , tsn]
    return_msg = ts_client.query(msg)
    if len(return_msg) == 0:
        return jsonify("Find nothing!")
    return jsonify({"similarity" : return_msg})


@app.route('/simquery', methods=['POST'])
def post_similar_ts():
    input_data = request.get_json(force=True)
    if 'n' not in input_data:
        input_data['n'] = 5
    n = input_data['n']
    # call for response
    # return nth closest ts data to input_data
    msg = {}
    msg['type'] = 'ss_tsdata'
    msg['tsdata'] = input_data
    msg['n'] = n
    # return_msg should be a id(ts) array
    # [id1, id2, ... , idn]
    return_msg = ts_client.query(msg)
    if len(return_msg) == 0:
        return jsonify("Find nothing!")
    return jsonify({"similarity_id": return_msg})
