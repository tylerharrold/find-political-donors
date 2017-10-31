import numpy as np
import math

def clean_other_id(incoming_value):
    if not incoming_value:
        return ''
    else:
        return incoming_value

def clean_transaction_dt(incoming_value):
    if not incoming_value:
        return ''
    else:
        return str(incoming_value)

def clean_transaction_amt(incoming_value):
    if not incoming_value:
        return np.nan
    else:
        return int(incoming_value)

# helper function to assist rounding, as python's round method defaults .5 to round down
def round_custom(value):
    upper = math.ceil(value)
    lower = math.floor(value)
    if (upper - value) <= (value - lower):
        return upper
    else:
        return lower
