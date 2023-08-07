"""

    """

import json
from dataclasses import dataclass
from pathlib import Path

class Conf :
    url = 'url'  # GitHub url of the target repo
    py_ver = 'py_ver'  # python version to use
    module = "module"  # module name to run

@dataclass
class UserRepo :
    user_name: str
    repo_name: str
    user_slash_repo: str
    user_und_repo: str

def get_user_repo_from_url(repo_url) :
    gu = repo_url.split('github.com/')[1]
    user_name = gu.split('/')[0]
    repo_name = gu.split('/')[1]
    user_slash_repo = f'{user_name}/{repo_name}'
    user_und_repo = f'{user_name}_{repo_name}'
    return UserRepo(user_name , repo_name , user_slash_repo , user_und_repo)

def read_json(fp) :
    # if fp is not entered with .json extension, add it
    fp = Path(fp).with_suffix('.json')

    # assume cd is the GitHub dir
    fp = Path.cwd() / 'auto-run-configs' / fp

    with open(fp , 'r') as f :
        return json.load(f)
