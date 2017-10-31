import numpy as np

def clean_other_id(incoming_value):
    if not incoming_value:
        return ''
    else:
        return incoming_value

def clean_transaction_amt(incoming_value):
    if not incoming_value:
        return np.nan
    else:
        return int(incoming_value)
