

def label_state(state, functions=None, node_names=None, str_functions=None, additive=True, sep='/', no_label="*"):

    """
    Return the label of a state given a set of labeling functions. Labels are additive, if more than one function applies all labels will be added.

    Arguments
    ---------
    state (list):    state to label, most be ordered according to original node_names
    functions (dic, optional):      dictionary of label with its respective boolean function
    node_names (list, optional):    ordered name of nodes
    str_functions (str, optional):  multiline string of boolean functions.
        format: label = boolean labeling function
    additive (bool, optional):      use all appropiate labels, if false only the first label will be used
    sep (string, optional):     string to separate multiple labels

    Returns
    -------
    label (str):  label of state
    """

    state = [int(s) for s in state] #clean state
    if functions == None: functions = create_label_functions(node_names, str_functions) #create functions if none given

    label = []
    for f in functions: #evaluate functions to find apliable labels
        if functions[f](state): label.append(f)
    if len(label) == 0: return no_label
    if additive: 
        label = list(set(label)) #remove duplicates
        return sep.join(label) 
    else: return label[0]


def create_label_functions(node_names, data):
    """
    Declare labeling function from a multiline string of boolean functions.

    Arguments
    ---------
    node_names (list of str): names of the nodes in order
    data (str):  multiline string of boolean functions.
        format: label = boolean labeling function

    Returns
    -------
    functions (dic):    dictionary of label with its respective boolean function
    """

    functions = {}
    data = data.strip().split('\n')
    data = [x.strip() for x in data if not x.strip().startswith('#')] #remove comented lines

    #generate functions
    for d in data:
        d = d.split('=')
        #generate lambda function
        node_lambda = eval("lambda (" +','.join(node_names) +') : ' +d[1].strip()) 
        #declare function
        functions [d[0].strip()] = node_lambda

    return functions