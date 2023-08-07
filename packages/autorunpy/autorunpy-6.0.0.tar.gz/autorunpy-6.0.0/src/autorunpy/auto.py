"""

    """

import subprocess

from .github_release import download_latest_release
from .util import Conf
from .util import get_user_repo_from_url
from .util import read_json

c = Conf()

def make_venv(fp) :
    """ make virtualenv with pyenv, delete existing venv if it exists"""
    j = read_json(fp)

    py_ver = j[c.py_ver]
    url = j[c.url]
    ur = get_user_repo_from_url(url)

    subprocess.run(['pyenv' , 'install' , '--skip-existing' , py_ver])
    subprocess.run(['pyenv' , 'virtualenv-delete' , '-f' , ur.user_und_repo])
    subprocess.run(['pyenv' , 'virtualenv' , py_ver , ur.user_und_repo])

    print(ur.user_und_repo)

def dl_and_ret_dirpath(fp) :
    js = read_json(fp)
    rp_url = js[c.url]
    dirp = download_latest_release(rp_url)
    print(dirp)

def ret_module_2_run_name(fp) :
    js = read_json(fp)
    print(js[c.module])
