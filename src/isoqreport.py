import numpy as np
from tqdm import tqdm

from dsconfig import args, query_config
from utils.queryutils import random_isoquery_sample, seed_every_thing, copy_report_and_plot_violin
from utils.queryreport import report_hist

seed_every_thing(20)
sample_num = query_config.sample_num
max_dim = args.datadim[1]
num_dimensions = args.datadim[0]  # Change this to the desired number of dimensions

range_list = [random_isoquery_sample(max_dim, num_dimensions) for _ in range(sample_num)]
range_list = list(set(range_list))

# Ensuring unique samples meet the sample_num requirement
while len(range_list) < sample_num:
    sample_diff = sample_num - len(range_list)
    additional_samples = [random_isoquery_sample(max_dim, num_dimensions) for _ in range(sample_diff)]
    range_list.extend(additional_samples)
    range_list = list(set(range_list))

for single_range in tqdm(range_list):
    args.rangequery = list(np.array([list(dim_range) for dim_range in single_range]).flatten())
    report_hist(args, indx =  np.prod(args.datadim[1:num_dimensions+1]))


# Copy report and plot violin
copy_report_and_plot_violin(num_dimensions, 'isoq', query_config.log2_scale)