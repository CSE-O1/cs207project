from flask import Flask, request, abort, jsonify, make_response, render_template
import json
from frontend.parsequery import parse_query
from server.DBClient import DBClient

app = Flask(__name__)


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
    ts_client = DBClient(50000)
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
            length = len(return_msg)
            return jsonify({"length" : length, "mean_in1" : return_msg[0], "mean_in2" : return_msg[-1]})
        elif arg == 'level_in':
            msg['type'] = 'level_in'
            msg['level_in'] = arg_vals
            return_msg = ts_client.query(msg)
            #return_msg should be a metadata array
            #be careful, msg['level_in'] is a array
            length = len(return_msg)
            return jsonify({"length" : length, "level_in1" : return_msg[0], "level_in2" : return_msg[-1]})

    msg['type'] = 'all'
    return_msg = ts_client.query(msg)
    length = len(return_msg)
    # return_msg should be all metadata
    return jsonify({"length" : length, "metadata_1": return_msg[0], "metadata_2": return_msg[-1]})


@app.route('/timeseries', methods=['POST'])
def post_timeseries():
    ts_client = DBClient(50000)
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
    ts_client = DBClient(50000)
    # call for response
    # given id, return ts data and metadata
    msg = {}
    msg['type'] = 'id'
    msg['id'] = id

    #return_msg format:
    #return_msg = { 'exist': 1 or 0,
    #               'tsdata': xxxx,
    #               'metadata': xxxx}
    # if this id does not exit, return
    return_msg = ts_client.query(msg)
    if return_msg['exist'] == 0:
        return jsonify("Timeseries id does not exist!")

    ts_time = list(return_msg['tsdata'].times)
    ts_value = list(return_msg['tsdata'].values)

    ts = [[t, v] for t, v in zip(ts_time, ts_value)]
    return jsonify({"ts": ts, "metadata": return_msg['metadata']})


@app.route('/simquery/<id>')
def get_similar_ts(id):
    ts_client = DBClient(50000)
    sim_id = id#request.args.get('id')
    #k = request.args.get('k')
    #if k is None:
    k = 3
    # call for response
    # return nth closest ts data to ts with sim_id
    msg = {}
    msg['type'] = 'ss_id'
    msg['id'] = sim_id
    msg['k'] = k
    #return_msg should be a ts array
    #[ts1, ts2, ... , tsn]
    return_msg = ts_client.query(msg)
    if not return_msg or len(return_msg) == 0:
        return jsonify("Find nothing!")
    print(return_msg)
    ids = [msg[1] for msg in return_msg]
    return jsonify({"tsid": ids})


@app.route('/simquery', methods=['POST'])
def post_similar_ts():
    ts_client = DBClient(50000)
    input_data = request.get_json(force=True)
    #if 'k' not in input_data:
    #    input_data['k'] = 5
    k = 3
    # call for response
    # return nth closest ts data to input_data
    msg = {}
    msg['type'] = 'ss_tsdata'
    msg['tsdata'] = input_data['tsdata']
    msg['k'] = k
    # return_msg should be a id(ts) array
    # [id1, id2, ... , idn]
    return_msg = ts_client.query(msg)
    if not return_msg or len(return_msg) == 0:
        return jsonify("Find nothing!")

    tst1 = list(return_msg[0].times)
    tsv1 = list(return_msg[0].values)

    tst2 = list(return_msg[1].times)
    tsv2 = list(return_msg[1].values)

    tst3 = list(return_msg[2].times)
    tsv3 = list(return_msg[2].values)

    return jsonify({"tst1": tst1, "tsv1": tsv1, "tst2": tst2, "tsv2": tsv2, "tst3": tst3, "tsv3": tsv3})

