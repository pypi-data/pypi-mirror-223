"""

    """

import re
import tarfile
from pathlib import Path

import requests

from .util import get_user_repo_from_url

def get_latest_release_tar_url(repo_url) :
    usrp = get_user_repo_from_url(repo_url)
    url = f'https://api.github.com/repos/{usrp.user_slash_repo}/releases/latest'
    r = requests.get(url)
    dct = r.json()
    return dct['tarball_url']

def get_filename_fr_github_resp(r) :
    hdr = r.headers
    cd = hdr['content-disposition']
    pat = 'attachment; filename=(.+)'
    mat = re.findall(pat , cd)
    return mat[0]

def download_latest_release_tarball(repo_url) :
    url = get_latest_release_tar_url(repo_url)

    r = requests.get(url)
    if r.status_code != 200 :
        return

    fn = get_filename_fr_github_resp(r)
    fp = Path.cwd() / fn

    with open(fp , 'wb') as f :
        f.write(r.content)

    return fp

def get_dirname_fr_github_tarball(fp) :
    with tarfile.open(fp) as tar :
        return tar.getnames()[0]

def download_latest_release(repo_url) :
    tar_fp = download_latest_release_tarball(repo_url)

    with tarfile.open(tar_fp) as f :
        f.extractall(tar_fp.parent)

    dirp = tar_fp.parent / get_dirname_fr_github_tarball(tar_fp)
    tar_fp.unlink()

    return dirp
