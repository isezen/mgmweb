#!/usr/bin/env python
# -*- coding: utf-8 -*-

%load_ext autoreload
%autoreload 2

# import sys
from mgm import webserv as ws
# ws = reload(sys.modules[ws.__module__])

iller = ws.province()
mid = [il['merkezId'] for il in iller]
mid2 = [[ilce['merkezId'] for ilce in ws.district(il['il'])] for il in iller]
mid2 = [item for sublist in mid2 for item in sublist]


[[float(y) for y in x] for x in l]

for il in iller:
    # print il['il']
    ilceler = ws.district(il['il'])
    [ilce['ilce'] for ilce in ilceler]
        # print '    ' + ilce['ilce']


ws.station('yozgat', 'sarıkaya')
ws.station('istanbul', 'bakırköy')
