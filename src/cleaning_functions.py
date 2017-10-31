import numpy as np

def clean_transaction_amt(incoming_value):
    if not incoming_value:
        return np.nan
    else:
        return int(incoming_value)
