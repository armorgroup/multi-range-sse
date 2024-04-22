import argparse

import numpy as np
from tqdm import tqdm
from multiprocessing import Pool

from dsconfig import args, query_config
from utils.queryutils import random_oaquery_sample, seed_every_thing, copy_report_and_plot_violin
from utils.queryreport import report_hist

    
parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-ot', '--outliertype', type= str, required= False, default= 'max')

arg_cli = parser.parse_args()

seed_every_thing(20)

sample_num = query_config.sample_num
max_dim = args.datadim[1]
num_dimensions = args.datadim[0]  # Change this to the desired number of dimensions

outlier_dim_idx = query_config.outlier_dim_idx
d_range = query_config.d_range
outlier_type = arg_cli.outliertype


range_list = []
range_list.append(random_oaquery_sample(max_dim, num_dimensions, outlier_dim_idx, d_range, outlier_type))
range_list = list(set(range_list))

# Ensure the list has exactly `sample_num` unique elements
while len(range_list) < sample_num:
    sample_diff = sample_num - len(range_list)
    for _ in range(sample_diff):
        range_list.append(random_oaquery_sample(max_dim, num_dimensions, outlier_dim_idx,d_range,outlier_type))
    range_list = list(set(range_list))

for single_range in tqdm(range_list):
    args.rangequery = list(np.array([list(dim_range) for dim_range in single_range]).flatten())
    report_hist(args, indx =  np.prod(args.datadim[1:num_dimensions+1]))

# Copy report and plot violin
copy_report_and_plot_violin(num_dimensions, f"oaq_{outlier_type}", query_config.log2_scale)

# def process_range(single_range):
#     """
#     Function to be executed in parallel, wraps the loop body.
#     """
#     args.rangequery = list(np.array([list(dim_range) for dim_range in single_range]).flatten())
#     report_hist(args, indx =  np.prod(args.datadim[1:num_dimensions+1]))    
#     return True

# def main():
#     # Number of worker processes to use
#     num_workers = 5
#     # Create a Pool of workers
#     with Pool(num_workers) as pool:
#         # Use tqdm to create a progress bar. The `total` parameter is set to the length of `range_list`
#         # to properly display progress. `imap` is used for lazy iteration over results.
#         # print(range_list)
#         results = list(tqdm(pool.imap(process_range,range_list), total=len(range_list)))
#     # Copy report and plot violin
#     copy_report_and_plot_violin(num_dimensions, f"oaq_{outlier_type}", query_config.log2_scale)

# if __name__ == "__main__":
#     main()