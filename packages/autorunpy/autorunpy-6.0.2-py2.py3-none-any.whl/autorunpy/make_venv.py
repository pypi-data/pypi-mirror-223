"""

    """

import sys

from .auto import make_venv


if __name__ == '__main__' :
    conf_fp = sys.argv[1]
    make_venv(conf_fp)
