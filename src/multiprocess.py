import numpy as np
from tqdm import tqdm

from multiprocessing import Pool

from dsconfig import args, query_config
from utils.queryutils import random_gaquery_sample, seed_every_thing, copy_report_and_plot_violin
from utils.queryreport import report_hist

# Assuming `args` and `report_hist` are defined elsewhere in your code
# and that `range_list` is a list of ranges you want to process.
seed_every_thing(20)
sample_num = query_config.sample_num
max_dim = args.datadim[1]
num_dimensions = args.datadim[0]  # Change this to the desired number of dimensions

range_list = [random_gaquery_sample(max_dim, num_dimensions) for _ in range(sample_num)]
range_list = list(set(range_list))

# Ensuring unique samples meet the sample_num requirement
while len(range_list) < sample_num:
    sample_diff = sample_num - len(range_list)
    additional_samples = [random_gaquery_sample(max_dim, num_dimensions) for _ in range(sample_diff)]
    range_list.extend(additional_samples)
    range_list = list(set(range_list))

def process_range(single_range):
    """
    Function to be executed in parallel, wraps the loop body.
    """
    args.rangequery = list(np.array([list(dim_range) for dim_range in single_range]).flatten())
    report_hist(args, indx =  np.prod(args.datadim[1:num_dimensions+1]))    
    return True

def main():
    # Number of worker processes to use
    num_workers = 5
    # Create a Pool of workers
    with Pool(num_workers) as pool:
        # Use tqdm to create a progress bar. The `total` parameter is set to the length of `range_list`
        # to properly display progress. `imap` is used for lazy iteration over results.
        # print(range_list)
        results = list(tqdm(pool.imap(process_range,range_list), total=len(range_list)))
    # Copy report and plot violin
    copy_report_and_plot_violin(num_dimensions, 'gaq', query_config.log2_scale)

if __name__ == "__main__":
    main()
