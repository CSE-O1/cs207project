from flask import Flask, request, abort, jsonify, make_response
#from app import app, db, models
app = Flask(__name__)

def parse_query(arg_name, arg_val):
    name_dict = {'mean_in': '-', 'level_in': ',', 'id': ','}
    name = name_dict[arg_name]
    return tuple(arg_val.split(name))

# index
@app.route('/')
def render_index():
    return make_response('Hello World!')

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
        #res = Timeseries.query().all()
        if arg == 'id':
            pass
        elif arg == 'mean_in':
            #ts_queried = Timeseries
            pass
        elif arg == 'level_in':
            pass
    #arg_res [arg.serialize() ]
    return jsonify(request_string)


@app.route('/timeseries/<id>', methods=['POST'])
def create_timeseries():
    #ts_id = request.query.get(id)
    pass
    #_generate_metadata(ts_id, ts_data)
