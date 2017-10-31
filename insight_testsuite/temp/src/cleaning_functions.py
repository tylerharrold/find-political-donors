import numpy as np
import math

# helper function to ensure other_id is clean
def clean_other_id(incoming_value):
    if not incoming_value:
        return ''
    else:
        return incoming_value

# helper function to ensure that transaction_dt is a valid string
def clean_transaction_dt(incoming_value):
    if not incoming_value:
        return ''
    else:
        return str(incoming_value)

# helper function to ensure that transaction_amt is an integer value in our data
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
