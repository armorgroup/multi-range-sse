import os
import numpy as np

from dsconfig import args
from utils.construct import construct
from utils.queryutils import delete_file

# Construct the dataset
construct(args, prompt = False, indx =  np.prod(args.datadim[1:args.datadim[0]+1]))


delete_file(os.getcwd() + '/sample_data/all_query_report_bucket.csv')
delete_file(os.getcwd() + '/sample_data/all_query_report.csv')