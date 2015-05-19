from random import randint
from types import GeneratorType


def return_valid_states(data, l, base=2):
    """
    Returns a valid iterable list of states.

    Arguments
    ---------
    data:       states to iterate
    l (int):    length of state
    base (int): base of state

    Returns
    ------
    states (list of lists)
    """
    if validate_state(list(data), l, base): return [data]
    elif type(data) == GeneratorType: return data #generator
    elif type(data) == str: #transform string to state
        state = str_to_state(data)
        if validate_state(state, l, base): return [state]
        else: raise TypeError('Invalid state list.')

    #if iterable (tuple, list even dic!)
    try: iterator = iter(data) #ducktyping! 
    except TypeError: raise TypeError('Invalid state list.') #not a duck
    states = []
    for d in data:
        if type(d) == str: #transform string to state
            d = str_to_state(d)
        try: 
            if validate_state(list(d), l, base): states.append( list(d) )
            else: raise TypeError('Invalid state list.')
        except TypeError: raise TypeError('Invalid state list.')
    return states


def validate_state(state, l, base=2):
    """
    Is the state valid?

    Arguments
    ---------
    data:       states to iterate
    l (int):    length of state
    base (int): base of state

    Returns
    -------
    True/False
    """

    if len(state) == l and all(type(i)==int or type(i)==bool for i in state) and max(state) < base: return True
    else: return False


def generate_all_base_array_states(nodes, base=2):
    """
    Returns all posible states given a network of n nodes where the state can be discrete with max base.

    Arguments
    ---------
    nodes (int): number of nodes
    base (int):  max value of nodes

    Yields
    ------
    state (list of int)
    """
    c = 0
    while c < base ** nodes :
        if base == 2: state = dec_to_bin_array(c, nodes)
        else: state = dec_to_base_array(c, base, nodes)
        c += 1
        yield state

def generate_random_base_array_states(n, nodes, base=2):
    """
    Returns n random states given a network of n nodes where the state can be discrete with max base.

    Arguments
    ---------
    n (int):     number of random states to generate
    nodes (int): number of nodes
    base (int):  max value of nodes

    Yields
    ------
    state (list of int)
    """
    while n > 0 :
        c = randint(0, base ** nodes -1)
        if base == 2: state = dec_to_bin_array(c, nodes)
        else: state = dec_to_base_array(c, nodes, base)
        n -= 1
        yield state

def dec_to_base_array(x, length, base=2):
    """Convert number in decimal to an array in a diferent base."""
    s, i = [0 for i in range(length)], 1
    while x > 0:
        s[-i], x = x%base, x/base
        i += 1
    return s

def base_array_to_dec(s, base=2):
    """Convert array in a given base to decimal."""
    dec , e = 0 , len(s)
    while e > 0:
        dec += s[-e] * (base ** (e -1))
        e -= 1
    return dec

def dec_to_bin_array(n, padding):
    """Convert number in decimal to a binary array."""
    return [int(i) for i in bin(n)[2:].zfill(padding) ]

def bin_array_to_dec(s):
    """Convert binary array to decimal."""
    return int(''.join([str(i) for i in s]), 2)

def state_to_str(a):
    """Convert array to string. If a number is > 10, transform to single uppercase letter"""
    #convert >10 to uppercase, solve booleans
    return ''.join(   [str(int(i)) if i<10 else chr(i+55) for i in a]   )

def str_to_state(s):
    """Convert string to array. Letters correspond to numbers bigger than 9"""
    return [ord(i)-48 if ord(i)<58 else ord(i.upper())-55 for i in s]