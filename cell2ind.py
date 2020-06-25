# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 22:12:42 2020

@author: zhaoz
"""
#
def cell2ind(celltype,celltags):
    indices = [n for n, x in enumerate(celltags) if x == celltype]    
    return indices

