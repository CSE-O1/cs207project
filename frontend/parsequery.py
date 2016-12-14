def parse_query(arg_name, arg_val):
    """
    parse input query function
    """
    name_dict = {'mean_in': '-', 'level_in': ',', 'id': ','}
    name = name_dict[arg_name]
    return tuple(arg_val.split(name))