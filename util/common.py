# -*- coding: utf-8 -*-
import  decimal
def conver_type(x):
    if isinstance(x,decimal.Decimal):
        return float(x)
    else:
        return x
