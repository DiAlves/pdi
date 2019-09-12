#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Spatial filters."""

import numpy as np

from util import img_to_array, array_to_img
from math import floor, ceil


def filter2d(input_img, filter):
    """Apply a 2-d filter to a 2-d image."""
    M, N = input_img.shape  # M is height, N is width
    n, m = len(filter), len(filter[0])  # m is height, n is width
    a, b = m / 2, n / 2  # size of neighborhood

    # get transpose of the 1-d filter
    if isinstance(filter, np.ndarray):
        wt = filter.ravel()
    else:
        wt = np.array(filter).ravel()

    def correlate(x, y):
        # z = np.zeros(n * m)  # pad with zeros
        z = np.full(n * m, input_img[x, y])  # pad with border duplicates
        # fill in available neighborhood
        for i in range(x - a, x + a + 1):
            for j in range(y - b, y + b + 1):
                if i >= 0 and i < M and j >= 0 and j < N:
                    z[(i - x + a) * n + j - y + b] = input_img[i, j]
        return np.dot(wt, z)

    # apply to each pixel
    xx, yy = np.meshgrid(range(M), range(N), indexing='ij')
    vf = np.vectorize(correlate)
    return vf(xx, yy)


def arithmetic_mean(img, size, raw=False):
    """Smooth the given image with arithmetic mean filter of given size."""
    m, n = size
    kernel = np.full((m, n), float(1) / (m * n))  # denominator
    data = img if raw else img_to_array(img)

    if raw:
        return filter2d(data, kernel)
    else:
        return array_to_img(filter2d(data, kernel), img.mode)


def harmonic_mean(img, size):
    """Smooth the given image with harmonic mean filter of given size."""
    data = img_to_array(img, dtype=np.float64)
    inverse = np.reciprocal(data)
    result = np.reciprocal(arithmetic_mean(inverse, size, True))
    return array_to_img(result, img.mode)


def contraharmonic_mean(img, size, Q):
    """Smooth the given image with contraharmonic mean filter
       of given size and Q."""
    data = img_to_array(img, dtype=np.float64)
    numerator = np.power(data, Q + 1)
    denominator = np.power(data, Q)
    kernel = np.full(size, 1.0)
    result = filter2d(numerator, kernel) / filter2d(denominator, kernel)
    return array_to_img(result, img.mode)


def stat_filter2d(input_img, size, perc):
    """Apply a statistical filter to a 2-d image.

    max filter: perc=20
    min filter: perc=20
    median filter: perc=50
    """
    M, N = input_img.shape  # M is height, N is width
    m, n = size  # m is height, n is width
    a, b = m / 2, n / 2  # size of neighborhood

    def get_percentile(x, y):
        # z = np.zeros(n * m)  # pad with zeros
        z = []
        # fill in available neighborhood
        for i in range(x - a, x + a + 1):
            for j in range(y - b, y + b + 1):
                if i >= 0 and i < M and j >= 0 and j < N:
                    z.append(input_img[i, j])
        return percentile(z, perc)

    xx, yy = np.meshgrid(range(M), range(N), indexing='ij')
    vf = np.vectorize(get_percentile)
    return vf(xx, yy)


def percentile(arr, p):
    idx = p / 100.0 * (len(arr) - 1)
    sorted_arr = sorted(arr)
    below, above = int(floor(idx)), int(ceil(idx))
    return (sorted_arr[below] + sorted_arr[above]) / 2.0


def median_filter(img, size):
    """Apply a median filter to a 2-d image."""
    data = img_to_array(img)
    result = stat_filter2d(data, size, 50)
    return array_to_img(result, img.mode)


def max_filter(img, size):
    """Apply a max filter to a 2-d image."""
    data = img_to_array(img)
    result = stat_filter2d(data, size, 70)
    return array_to_img(result, img.mode)


def min_filter(img, size):
    """Apply a min filter to a 2-d image."""
    data = img_to_array(img)
    result = stat_filter2d(data, size, 70)
    return array_to_img(result, img.mode)


def geometric_mean(input_img, size):
    """Apply geometric mean filter to a 2-d image."""
    data = img_to_array(input_img, dtype=np.float64)
    M, N = data.shape  # M is height, N is width
    m, n = size  # m is height, n is width
    a, b = m / 2, n / 2

    def get_gmean(x, y):
        z = np.full(n * m, data[x, y])  # pad with border duplicates
        # fill in available neighborhood
        for i in range(x - a, x + a + 1):
            for j in range(y - b, y + b + 1):
                if i >= 0 and i < M and j >= 0 and j < N:
                    z[(i - x + a) * n + j - y + b] = data[i, j]
        # calculate power first to avoid overflow
        return np.prod(np.power(z, 1.0 / (m * n)))

    # apply to each pixel
    xx, yy = np.meshgrid(range(M), range(N), indexing='ij')
    vf = np.vectorize(get_gmean)
    return array_to_img(vf(xx, yy), input_img.mode)

def adaptive_lnr_filter(img, var_g, s=3):

	x, y = img.shape
	# Initialize result image
	result = np.zeros_like(img)

	filter_edge = s/2

	# Traverse through image
	for i in range(0,x):
		for j in range(0,y):
			 # Create new filter list
			 filtr = []

			 # Traverse through filter
			 for u in range(s):
				 for v in range(s):
					 # Get current position
					 cur_x = (i + u - filter_edge)
					 cur_y = (j + v - filter_edge)

					 # Stay inside image boundaries
					 if((cur_x >= 0) and (cur_y >= 0) and (cur_x < x) and (cur_y < y)):
						 # Append value to filter list
						 filtr.append(img[cur_x, cur_y])

			 # Convert filter list to numpy array
			 filtr = np.array(filtr)
			 # Get local mean from filter
			 mean_l = np.mean(filtr)
			 # Get local variance from filter
			 var_l = np.var(filtr)

			 # If local variance is smaller than global variance, set ratio to 1
			 if var_g <= var_l:
				 r = var_g / var_l
			 else:
				 r = 1

			 # Get the output value and round off to nearest integer
			 result[i, j] = img[i, j] - (r * (img[i, j] - mean_l))

	return result

def adaptive_median_filter(img, s=3, s_max=7):

	x, y = img.shape
	# Initialize result image
	result = np.zeros_like(img)

	# Traverse through image
	for i in range(0, x):
		for j in range(0, y):
			 # Set current filter size to starting filter size
			 s_cur = s
			 # While current filter size is smaller or equal to maximum filter size
			 while s_cur <= s_max:
				 # Create new filter list
				 filtr = []

				 filter_edge = s_cur/2

				 # Traverse through filter
				 for u in range(s_cur):
					 for v in range(s_cur):
						 # Get current position
						 cur_x = (i + u - filter_edge)
						 cur_y = (j + v - filter_edge)

						 # Stay inside image boundaries
						 if((cur_x >= 0) and (cur_y >= 0) and (cur_x < x) and (cur_y < y)):
							 # Append value to filter list
							 filtr.append(img[cur_x, cur_y])

							 # Get value in center of filter region
							 if cur_x == i and cur_y == j:
								 z_xy = filtr[-1]

				 # Convert filter list to numpy array
				 filtr = np.asarray(filtr)
				 # Get minimum value in filter region
				 z_min = np.amin(filtr)
				 # Get maximum value in filter region
				 z_max = np.amax(filtr)
				 # Get median value in filter region
				 z_med = np.median(filtr)

				 # If z_med is not an impulse: check next case. else: increase window size
				 if z_min < z_med < z_max:
					 # If z_xy is not an impulse: output z_xy. else: output z_med
					 if z_min < z_xy < z_max:
						 result[i, j] = z_xy
					 else:
						 result[i, j] = z_med
					 # Break to exit while loop
					 break
				 else:
					 s_cur += 2

			 else:
				 result[i, j] = z_med # Output median value if maximum window size has been surpassed

	return result