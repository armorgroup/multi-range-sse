import time
import logging
import os
import sys
import confuse

import numpy as np


class event_duration:
    def __init__(self, scale='nano', log=None):
        self.scale = scale
        self.log = log
        
        if self.log:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)") 

        if  self.scale=='nano':
            self.scale_n = 1
        elif  self.scale=='milli':
            self.scale_n = 1e-6

    def event_start(self):
        self.start = time.time_ns()
        if self.log:
            logging.info(f'event duration measuring started')

    def event_finish(self, n_repeat=1):
        self.finish = time.time_ns()
        if self.log:
            logging.info(f'duration: {round((self.finish-self.start)*self.scale_n/n_repeat)} {self.scale} sec, repeat: {n_repeat}')
        return (self.finish-self.start)*self.scale_n/n_repeat
    
    def repeat_a_fun(self, n, fun, *arg):
        self.event_start()
        for _ in range(n):
            res = fun(*arg)
        self.event_finish(n_repeat=n)
        return res


def query_yes_no(question, default="yes"):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)") 
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        logging.info(question + prompt)
        # sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            logging.info("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
            # sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def query_yes_no_exe(path_org_data, func, *args):
    if not os.path.exists(path_org_data):
        func(*args)
    else:
        user_response = query_yes_no(f"The {path_org_data} file already exists. Do you want to overwrite it?")    
        if user_response:
            func(*args)
        else:
            pass

def user_response_exe(path_org_data, user_response, func, *args):
    if not os.path.exists(path_org_data):
        func(*args)
    else:
        if user_response:
            func(*args)
        else:
            pass

def query_yes_no_exe_hdf5(path_org_data, path_hdf5_data, func, *args):
    if os.path.exists(path_org_data):
        query_yes_no_exe(path_hdf5_data, func, *args)
    else:
        logging.error(f"The {path_org_data} does not exist!")



def query_report(args, ed, queryResult0, fun, *args_fun):
    if len(queryResult0)>0:
        # print('-'*20, f'query report start {args.query}-encrypt:{args.encrypt}-shuffle:{args.shuffle}', '-'*20)
        ed.event_start()
        queryResult,qrtime = fun(*args_fun)
        time = round(ed.event_finish(), 2)
        # result_true = sorted(queryResult0.tolist())==sorted(queryResult.tolist())
        result_true = True
        # print(f'# The query result match: {result_true}')    
        # print('# range query result size: ', len(queryResult), ", shape: ", queryResult.shape)
        # print('# range query first 10 of sorted data: ', '\n', np.round(sorted(queryResult.tolist()), 3)[:10])
        # print('-'*20, f'query report finish {args.query}-encrypt:{args.encrypt}-shuffle:{args.shuffle}', '-'*20)
        return queryResult, [round(qrtime, 2), result_true, len(queryResult)]
    else:
        return fun(*args_fun), 0


config = confuse.Configuration('app')
config.set_file('conf.yaml')
sample_data = config['sample_data']
root_dir = sample_data['root_dir'].get(str)
class path:
    org_data = root_dir+sample_data['org_data'].get(str)
    hdf5_org = root_dir+sample_data['hdf5_org'].get(str)
    org_encrypted = root_dir+sample_data['org_encrypted'].get(str)
    hdf5_encrypted = root_dir+sample_data['hdf5_encrypted'].get(str)
    encrypted_shuffled = root_dir+sample_data['encrypted_shuffled'].get(str)
    hdf5_encrypted_shuffled = root_dir+sample_data['hdf5_encrypted_shuffled'].get(str)
    mapping = root_dir+sample_data['mapping'].get(str)
    line_2_ijkm = root_dir+sample_data['line_2_ijkm'].get(str)
    encrypted_shuffled_index0 = root_dir+sample_data['encrypted_shuffled_index0'].get(str)
    hdf5_encrypted_shuffled_index0 = root_dir+sample_data['hdf5_encrypted_shuffled_index0'].get(str)
    mapping_index0 = root_dir+sample_data['mapping_index0'].get(str)
    encrypted_shuffled_index1 = root_dir+sample_data['encrypted_shuffled_index1'].get(str)
    hdf5_encrypted_shuffled_index1 = root_dir+sample_data['hdf5_encrypted_shuffled_index1'].get(str)
    mapping_index1 = root_dir+sample_data['mapping_index1'].get(str)
    encrypted_shuffled_index2 = root_dir+sample_data['encrypted_shuffled_index2'].get(str)
    hdf5_encrypted_shuffled_index2 = root_dir+sample_data['hdf5_encrypted_shuffled_index2'].get(str)
    mapping_index2 = root_dir+sample_data['mapping_index2'].get(str)
    encrypted_shuffled_slab = root_dir+sample_data['encrypted_shuffled_slab'].get(str)
    hdf5_encrypted_shuffled_slab = root_dir+sample_data['hdf5_encrypted_shuffled_slab'].get(str)
    mapping_slab = root_dir+sample_data['mapping_slab'].get(str)
    encrypted_shuffled_slab_matrix = root_dir+sample_data['encrypted_shuffled_slab_matrix'].get(str)
    hdf5_encrypted_shuffled_slab_matrix = root_dir+sample_data['hdf5_encrypted_shuffled_slab_matrix'].get(str)
    mapping_slab_matrix = root_dir+sample_data['mapping_slab_matrix'].get(str)
    kdtree_encrypted_obj = root_dir+sample_data['kdtree_encrypted_obj'].get(str)
    kdtree_encrypted = root_dir+sample_data['kdtree_encrypted'].get(str)
    kdtree_encrypted_shuffled_obj = root_dir+sample_data['kdtree_encrypted_shuffled_obj'].get(str)
    kdtree_encrypted_shuffled = root_dir+sample_data['kdtree_encrypted_shuffled'].get(str)
    kdtree_encrypted_shuffled_slab = root_dir+sample_data['kdtree_encrypted_shuffled_slab'].get(str)
    kdtree_encrypted_shuffled_slab_matrix = root_dir+sample_data['kdtree_encrypted_shuffled_slab_matrix'].get(str)
    report = config['report']['all_query_report'].get(str)
    report_bucket = config['report']['all_query_report_bucket'].get(str)


def rename_path(path_inst, index):
    all_attribute = [a for a in dir(path_inst) if not a.startswith('__')]
    all_attribute = [a for a in all_attribute if not a.startswith('report')]
    for i in all_attribute:
        a = eval(f'path_inst.{i}')
        a = a.split('.')
        a = ['.',*a[:-1], f'_{index}.', a[-1]]
        a = ''.join(a)
        exec(f'path_inst.{i} = "{a}"')
    return path_inst


def index2number(INDEX, index):
    INDEX, index = tuple(INDEX), tuple(index)
    INDEX = INDEX + (1,)
    number = 0
    for i in range(len(index)):
        number += index[i]*np.prod(INDEX[i+1:])
    return number+1

def number2index(INDEX, number):
    INDEX = tuple(INDEX)
    INDEX = INDEX
    index = [0]*len(INDEX)
    number -= 1
    for i in range(len(INDEX)-1):
        index[i] = number//np.prod(INDEX[i+1:])
        number = number%np.prod(INDEX[i+1:])
    index[-1] = number
    return tuple(index)

def ijkm_2_line(i, dimensions):
    dim = len(i)
    if dim == 2:
        return i[0]*dimensions[1]+i[1]+2
    elif dim == 3:
        return i[0]*dimensions[1]*dimensions[2] + i[1]*dimensions[2] + i[2]+2
    elif dim == 4:
        return i[0]*dimensions[1]*dimensions[2]*dimensions[3] + i[1]*dimensions[2]*dimensions[3] + i[2]*dimensions[3] + i[3]+2


# copy and rename file
import shutil
import os

def copy_and_rename_file(source_path, destination_dir, new_file_name):
    # Ensure the destination directory exists, create if it doesn't
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Construct the full destination path including the new file name
    destination_path = os.path.join(destination_dir, new_file_name)
    
    # Copy and rename the file to the new destination
    shutil.copy2(source_path, destination_path)
    
    print(f"File copied and renamed to: {destination_path}")
