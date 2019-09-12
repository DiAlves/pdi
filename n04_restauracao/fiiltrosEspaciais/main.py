#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from PIL import Image

from filter import arithmetic_mean, geometric_mean
from filter import harmonic_mean, contraharmonic_mean
from filter import median_filter, max_filter, min_filter
from filter import adaptive_median_filter, adaptive_lnr_filter


def test_filter(filename, result_dir):
    """2.2 Image Filtering"""
    im = Image.open(filename)

    def savewith(result, name):
        result_path = os.path.join(result_dir, name)
        result.save(result_path)
        print ('[Saved] ' + result_path)

    # 1. filter with 3 x 3 and 9 x 9 arithmetic mean filters
    a_mean_cases = [(3, 3), (9, 9)]
    for size in a_mean_cases:
        result = arithmetic_mean(im, size)
        savewith(result, 'arithmetic-mean-%d-%d.png' % size)

    # 2. filter  with 3 x 3 and 9 x 9 harmonic mean filters
    h_mean_cases = [(3, 3), (9, 9)]
    for size in h_mean_cases:
        result = harmonic_mean(im, size)
        savewith(result, 'harmonic-mean-%d-%d.png' % size)

    # 2. filter  with 3 x 3 and 9 x 9 contraharmonic mean filters
    #    with Q = -1.5.
    c_h_mean_cases = [(3, 3), (9, 9)]
    for size in c_h_mean_cases:
        result = contraharmonic_mean(im, size, -0.75)
        savewith(result, 'contraharmonic-mean-%d-%d.png' % size)
        
    # 2. filter  with 3 x 3 and 9 x 9 median filters
        median_cases = [(3, 3), (9, 9)]
    for size in median_cases:
        result = median_filter(im, size)
        savewith(result, 'median-filter-%d-%d.png' % size)

    # 2. filter  with 3 x 3 and 9 x 9 max filters
        max_cases = [(3, 3), (9, 9)]
    for size in max_cases:
        result = max_filter(im, size)
        savewith(result, 'max-filter-%d-%d.png' % size)

    # 2. filter  with 3 x 3 and 9 x 9 min filters
        min_cases = [(3, 3), (9, 9)]
    for size in min_cases:
        result = min_filter(im, size)
        savewith(result, 'min-filter-%d-%d.png' % size)
        
    # 2. filter  with 3 x 3 and 9 x 9 median filters
        geometric_mean_cases = [(3, 3), (9, 9)]
    for size in geometric_mean_cases:
        result = geometric_mean(im, size)
        savewith(result, 'geometric-mean-filter-%d-%d.png' % size)
        
    # 2. filter  with 3 x 3 and 9 x 9 median filters
        adaptive_median_cases = [(3, 3)]
    for s in adaptive_median_cases:    
        result = adaptive_median_filter(im,s,s_max=7)
        savewith(result, 'adaptative-median-filter-%d-%d.png' % size)        

    # 2. filter  with 3 x 3 and 9 x 9 median filters
    if __name__ == "__main__":
        subimage = im[240:290, 100:200]
    var_g = np.var(subimage)
    adaptive_lnr_cases = [(3, 3), (9, 9)]
    for size in adaptive_lnr_cases:    
        result = adaptive_lnr_filter(im, var_g, size)
        savewith(result,  'adaptative-lnr-filter-%d-%d.png'  % size)


def main():
    # ------------ Ensure the project directory structure ---------
    file_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir, _ = os.path.split(file_dir)
    source_path = os.path.join(parent_dir, 'img')
    result_dir = os.path.join(parent_dir, 'result')

    print ('Source path: ' + source_path)
    if not os.path.exists(source_path):
        raise Exception("Source path doesn't exist!")
    print ('Result directory: ' + result_dir)
    if not os.path.exists(result_dir):
        print ("Result directory does not exist, created.")
        os.makedirs(result_dir)

    # source image paths
    task_1_srcpath = os.path.join(source_path, 'image_04.png')
    #task_2_srcpath = os.path.join(source_path, 'task_2.png')
    #hist_srcpath = os.path.join(source_path, '02.png')

    # result paths
    task_1_destpath = os.path.join(result_dir, 'image_04')
    #task_2_destpath = os.path.join(result_dir, 'task2')
    #gauss_path = os.path.join(task_2_destpath, 'gauss')
    #salt_path = os.path.join(task_2_destpath, 'salt')
    #sap_path = os.path.join(task_2_destpath, 'sap')
    #hist_path = os.path.join(result_dir, 'hist')

    # make sure result paths exist
    destpaths = [task_1_destpath]
    for path in destpaths:
        if not os.path.exists(path):
            print ("Created", path)
            os.makedirs(path)
        

    # ------------ Generate results ---------

    # Task 2.2 Image Filtering
    test_filter(task_1_srcpath, task_1_destpath)

if __name__ == "__main__":
    main()
