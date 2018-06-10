import random, base32_crockford
from itertools import chain
from fields_dicts import *

def split_str(entry, delimiter = ';'):
    """
    Split a string and strip extra spaces
    args:
    (str) entry: string; (str) delimiter: delimiter, ';' by default
    returns: (list) entries: split values
    """
    if entry  == False:
        return False
    elif entry == '':
        return ''
    else:
        return [item.strip() for item in entry.split(delimiter)]

def ext_len(entry, len_o):
    """
    add '' to the entry list extend the length
    args:
    (list) entry: list of entry; (int) len_o: optimized length
    """
    entry = entry + [''] * (len_o - len(entry))
    return entry

def val_con(entry, vol):
    """
    Verify whether the value is in the list of controlled values (if applicable)
    if the code is used, convert it to corresponding text
    args:
    (str) entry: the entry/sub-field; (dict) vol: list of controlled values
    returns:
    (str) entry: the validated entry
    """
    try:
        entry = int(entry)
        entry = vol[entry]
    except:
        pass
    if entry == '':
        return ''
    else:
        if entry not in list(vol.values()):
            return False
        else:
            return entry

def gen_doi(prefix):
    """
    Generate a random alphanumeric string (Format: xxxx-xxxx)
    as the suffix of a DOI.
    args: (str) prefix: prefix of the DOI
    returns: (str) DOI: the string of DOI
    """
    number = random.randrange(32**(8))
    suffix = base32_crockford.encode(number, split=4).lower()
    DOI = '{}/{}'.format(prefix,suffix)
    return DOI
