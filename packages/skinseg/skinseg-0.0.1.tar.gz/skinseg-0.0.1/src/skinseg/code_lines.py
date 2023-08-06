#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 03:04:22 2023

@author: dev
"""

import os

cwd = os.getcwd()
sloc = 0
for file in os.listdir(cwd):
    if file[-3:] == '.py':
        f = open(file)
        num_lines = len(f.readlines())
        print('file: ', file, 'num_lines: ', num_lines)
        sloc += num_lines
print()
print('Total lines of code: ', sloc)

input('Press Enter to exit...')