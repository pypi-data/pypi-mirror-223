import json
from dataclasses import dataclass
from pathlib import Path

import requests

class Const :
    # local GitHub token filename
    lg = '.gt.json'

    # local directories for GitHub token json file
    ld = {
            'mac'          : '/Users/mahdi/Dropbox/0-Arch/' ,
            'teias-ubuntu' : '/home/mahdi/Downloads/' ,
            'datalore'     : '/data/workspace_files/.private/.gt.json'
            }

k = Const()

@dataclass
class KeyVal :
    key: str
    val: str

def ret_github_url_for_private_access_to_file(user ,
                                              token ,
                                              target_usr ,
                                              target_repo ,
                                              branch ,
                                              filename
                                              ) -> str :
    """
    Makes a raw GitHub url for private access to a file in a repo

    :user: the user who has the access to the target repo
    :token: the token of has the access to the target repo
    """

    return f'https://{user}:{token}@raw.githubusercontent.com/{target_usr}/{target_repo}/{branch}/{filename}'

def read_json(filepath) -> dict :
    """ Reads a json file and returns a dict """
    with open(filepath , 'r') as f :
        return json.load(f)

def ret_val_by_key_fr_dict(dct: dict , key = None) -> KeyVal :
    """
    Returns a KeyVal object with the provided key and corresponding
    value in the provided dict, if no key is provided, the first key and value
    is returned.
    """

    if key is None and len(dct) > 0 :
        return KeyVal(key = list(dct.keys())[0] , val = list(dct.values())[0])

    return KeyVal(key = key , val = dct[key])

def ret_val_by_key_fr_json_file(filepath , key = None) -> KeyVal :
    js = read_json(filepath)
    return ret_val_by_key_fr_dict(js , key = key)

def ret_local_github_token_filepath() -> Path :
    """
    Returns the local filepath of the GitHub token file (.gt.json)
        needed to access the private repo containing all the tokens.
    """
    for dyr in k.ld.values() :
        fp = Path(dyr) / k.lg
        if fp.exists() :
            return fp

def get_all_tokens_fr_tokens_repo(gtok_fp) -> dict :
    """ Gets all tokens from the private tokens repo """
    tok = ret_val_by_key_fr_json_file(gtok_fp)
    url = ret_github_url_for_private_access_to_file(tok.key ,
                                                    tok.val ,
                                                    tok.key ,
                                                    'tokens' ,
                                                    'main' ,
                                                    'main.json')
    r = requests.get(url)
    j = r.json()
    return j

def get_token(key_in_all_tokens = None) -> str :
    """ Gets the token/value by a key from the private tokens repo """

    # find the local GitHub token file
    gtfp = ret_local_github_token_filepath()

    # If no token file is found, ask for the token itself
    if gtfp is None :
        return input('Enter GitHub Token:')

    # If the key is None, return the GitHub token of the default user (first)
    if key_in_all_tokens is None :
        return ret_val_by_key_fr_json_file(gtfp).val

    # Get all tokens from the private tokens repo
    all_toks = get_all_tokens_fr_tokens_repo(gtfp)

    # get the value of the key from the private tokens repo
    wanted_tok = all_toks[key_in_all_tokens]

    return wanted_tok
