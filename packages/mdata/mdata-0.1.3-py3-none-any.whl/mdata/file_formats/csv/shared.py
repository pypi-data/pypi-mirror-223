import os
from typing import Literal, Union

from mdata.core.util import StringEnumeration


def mk_filename_pair(basepath, header_format='csv'):
    p, e = os.path.splitext(basepath)
    return p + '_header.' + header_format, p + '_data.csv'


class HeaderFileFormat(StringEnumeration):
    CSV = 'csv'
    JSON = 'json'
    YAML = 'yaml'


DictHeaderFormatLiterals = Literal['json', 'yaml']
HeaderFormatLiterals = Union[Literal['csv'], DictHeaderFormatLiterals]
