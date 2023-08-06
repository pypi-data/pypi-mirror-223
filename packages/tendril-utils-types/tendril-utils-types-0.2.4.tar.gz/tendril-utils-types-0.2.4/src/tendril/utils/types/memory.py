

import re
from .unitbase import NumericalUnitBase


class MemorySize(NumericalUnitBase):
    _regex_std = re.compile(r"^(?P<numerical>[\d]+\.?[\d]*)\s?(?P<order>[kMGT]?B?)(?P<residual>[\d]*)$")  # noqa
    _ostrs = ['B', 'kB', 'MB', 'GB', 'TB']
    _dostr = 'B'
    _osuffix = 'B'
