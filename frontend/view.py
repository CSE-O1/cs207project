from flask import Flask, request, abort, jsonify, make_response
#from app import app, db, models
from parsequery import parse_query
app = Flask(__name__)


# index
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',title='Home')

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


@app.route('/timeseries', methods=['POST'])
def get_timeseries():
    #data = request.get_json(force = True)
    pass


@app.route('/timeseries/<id>')
def timeseries_id(id):
    #response = communicationWithDB(id) id is DB's key
    x = [1, 2, 3]
    y = [4, 5, 6]
    matrix = [x, y]
    return jsonify(matrix)


@app.route('/simquery', methods=['POST','GET'])
def get_similar_ts():
    pass


@app.route('/timeseries/<id>', methods=['POST'])
def create_timeseries():
    #ts_id = request.query.get(id)
    pass
    #_generate_metadata(ts_id, ts_data)
