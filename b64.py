#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""  TODO: module description

Usage:  

Input:  

Output:  

Author: wenhai.pan

Create Time:    2020-08-12 11:39:31

"""

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import time
from datetime import datetime, timedelta
import base64

def main():
    
    rep_map = {}
    rep_map["~"] = "="
    rep_map["-"] = "/"
    rep_map["!"] = "+"

    in_str = "mYEksN0gtlFAQ2u7aqiE4fe7Df!SKKBzQ-QYTUFPNiH7XqMktIMhvb42X4!ADPPLLo0ASqFc0N6k!DtFXXKg3Dm2-dYvYOy4n-qhSj87J2dvviSOP-ed3m2qu6Wlq6txRDoPWMT3hq5bNFMg5H-G!yzIzCHU6XR81DaL5!KdevDUKbg5l8ot18Yqhov1DPA1wDE!fJUa-tddW19BM-xWwA~~"

    for symbol in rep_map:
        in_str = in_str.replace(symbol, rep_map[symbol])

    print(in_str)
    result = base64.b64decode(in_str)

    print(result)

    return

if __name__ == "__main__":
    main()


