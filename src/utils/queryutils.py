import random

import numpy as np

def seed_every_thing(seed_num):
    np.random.seed(seed_num)
    random.seed(seed_num)
    
def random_range_calc(width, max_dim):
    start = np.random.randint( max_dim + 1 - width)
    return (start, start + width)

def random_isoquery_sample(max_dim, num_dimensions):
    width = np.random.randint(1, max_dim + 1)
    isoquery = [random_range_calc(width, max_dim) for _ in range(num_dimensions)]
    isoquery = np.random.permutation(isoquery)
    return tuple(map(tuple, isoquery))

def random_baquery_sample(max_dim, num_dimensions):

    # Generate widths for each group of dimensions
    widths = np.random.choice(range(1, max_dim + 1), 2, replace=False)

    # Split dimensions into two groups
    half_dim = num_dimensions // 2

    # Generate ranges for each dimension in group A
    ranges_a = [random_range_calc(widths[0], max_dim) for _ in range(half_dim)]
    # Generate ranges for each dimension in group B
    ranges_b = [random_range_calc(widths[1], max_dim) for _ in range(num_dimensions - half_dim)]   

    # Optionally shuffle within each group if needed
    baquery = np.random.permutation(ranges_a + ranges_b)

    return tuple(map(tuple, baquery))

def random_gaquery_sample(max_dim, num_dimensions):
    width = np.random.randint(1, int(max_dim / num_dimensions) + 1)
    c = np.random.randint(1, int((max_dim / num_dimensions) / width) + 1)

    gaquery = []
    for i in range(1, num_dimensions + 1):
        rn = random_range_calc(i * c * width, max_dim)
        gaquery.append(rn)
    gaquery = np.random.permutation(gaquery)
    return tuple(map(tuple, gaquery))

def random_oaquery_sample(max_dim, num_dimensions, outlier_dim_idx, d_range=5, outlier_type='max'):
    """
    Generates an OAQ sample with one dimension having an outlier width (either minimum or maximum within a specified range)
    and the others within a different range.
    
    :param max_dim: Maximum dimension size.
    :param num_dimensions: Total number of dimensions in the query.
    :param outlier_dim_idx: Index of the dimension to have the outlier width (0-indexed).
    :param d_range: Range for generating the non-outlier widths.
    :param outlier_type: 'max' for maximum outlier, 'min' for minimum outlier.
    :return: A tuple representing the OAQ.
    """
    assert 0 <= outlier_dim_idx < num_dimensions, "outlier_dim_idx out of range."
    
    if outlier_type == 'max':
        width_outlier = np.random.randint(max_dim - d_range, max_dim)
        width_others = np.random.randint(1, d_range + 1)
    else:  # Assume 'min' for any other value
        width_outlier = np.random.randint(1, d_range + 1)
        width_others = np.random.randint(max_dim - d_range, max_dim)

    ranges = [random_range_calc(width_others, max_dim) if i != outlier_dim_idx else random_range_calc(width_outlier, max_dim) 
              for i in range(num_dimensions)]
    return tuple(ranges)

from utils.utils import copy_and_rename_file
from plot import draw_violin_sh_schemes_parts

def copy_report_and_plot_violin(num_dimensions, query_shape, size):
    
    root_adrss = os.getcwd() + '/sample_data/'
    result_type = 'parts'
    file_name_csv = 'all_query_report_bucket'

    file_name_output_graph = root_adrss + f"{num_dimensions}d/{size}/{result_type}_{query_shape}_{size}_{num_dimensions}d"
    new_dir_csv = root_adrss + f"{num_dimensions}d/{size}/"
    new_file_name = f"{file_name_csv}_{query_shape}_{size}_{num_dimensions}d.csv"

    copy_and_rename_file(root_adrss+file_name_csv + '.csv', new_dir_csv, new_file_name )
    # deleting the report from the sample_data
    delete_file(root_adrss + file_name_csv + '.csv')

    draw_violin_sh_schemes_parts(new_dir_csv+new_file_name , file_name_output_graph)   


#  delete a file for a given file path
import os

def delete_file(file_path):

    try:
        os.remove(file_path)
        print(f"Removed {file_path}")
    except Exception as e:
        print(f"Error while deleting file {file_path}. Reason: {e}")   