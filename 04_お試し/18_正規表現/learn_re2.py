# -*- coding: utf-8 -*-
"""
Created on Tue May 28 14:09:13 2019

@author: r00495138
"""

import re

form = 'Our greatest {1} is not in never failing, but in rising up every {2} we fail.'
src = 'Our greatest glory is not in never failing, but in rising up every time we fail.'

re_form = re.sub(
    r'{\d+}', r'(\\w+)', form
)

print(f're_form is "{re_form}"')

m = re.fullmatch(re_form, src)
print(list(m.groups()))