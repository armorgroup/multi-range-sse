import pickle
import linecache
import logging
from itertools import product

import numpy as np
from tqdm import tqdm

from dataloader.dataloader import number2slab_matrix, slab_matrix2numbers
from utils.utils import ijkm_2_line

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)") 

def prf(old_pos: list, map_dir, data_dim, line_2_ijkm_dir):
    new_pos = np.random.permutation(old_pos)
    map_pos = {key: val for key, val in zip(old_pos, new_pos)}
    with open(map_dir, 'wb') as handle:
        pickle.dump(map_pos, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # line to ijkm mapping
    line_2_ijkm = {}
    ranges = [range(dim) for dim in data_dim[1:]]  # Generate ranges for each dimension excluding the first one
    for coords in product(*ranges):  # Generate all possible combinations of coordinates
        linepos = ijkm_2_line(coords, data_dim[1:])
        line_2_ijkm[linepos] = coords

    # for i in range(data_dim[1]):
    #     for j in range(data_dim[2]):
    #         for k in range(data_dim[3]):
    #             for m in range(data_dim[4]):
                    # linepos = ijkm_2_line((i, j, k, m), data_dim[1:])
                    # line_2_ijkm[linepos] = (i, j, k, m)

    with open(line_2_ijkm_dir, 'wb') as handle:
        pickle.dump(line_2_ijkm, handle, protocol=pickle.HIGHEST_PROTOCOL)


def prf_block(map_dir, data_dim,dim):
    old_indx = list(range(0, data_dim[dim]))
    new_indx = np.random.permutation(old_indx)
    map_indx = {key: val for key, val in zip(old_indx, new_indx)}
    with open(map_dir, 'wb') as handle:
        pickle.dump(map_indx, handle, protocol=pickle.HIGHEST_PROTOCOL)




def permute(fileNameTXT, shuffled_fileNameTXT, map_dir):

    with open(map_dir, 'rb') as handle:
        map_pos = pickle.load(handle)
    map_pos_rvrs = {val: key for key, val in map_pos.items()}

    with open(shuffled_fileNameTXT, "w") as file:
        line = linecache.getline(fileNameTXT, 1)
        file.write(line)
        for i in tqdm(sorted(list(map_pos.values()))):
            line = linecache.getline(fileNameTXT, map_pos_rvrs[i])
            file.write(line)

    logging.info(f'The {shuffled_fileNameTXT} generated!')    
# shuffling the file based on first dimention--> col 0-->indx_0
def permute_indx_0(fileNameTXT, shuffled_fileNameTXT, map_dir, data_dim):

    with open(map_dir, 'rb') as handle:
        map_indx_0 = pickle.load(handle)
    map_indx_0_rvrs = {val: key for key, val in map_indx_0.items()}

    with open(shuffled_fileNameTXT, "w") as file:
        line = linecache.getline(fileNameTXT, 1)
        file.write(line)
        for i in tqdm(sorted(list(map_indx_0.values()))):
            for j in range(data_dim[2]):
                for k in range(data_dim[3]):
                    for m in range(data_dim[4]):
                        line = linecache.getline(fileNameTXT,  ijkm_2_line((map_indx_0_rvrs[i], j, k, m), data_dim[1:]) )
                        file.write(line)
    
    logging.info(f'The {shuffled_fileNameTXT} generated!')    
# shuffling the file based on second dimention--> col 1-->indx_1
def permute_indx_1(fileNameTXT, shuffled_fileNameTXT, map_dir, data_dim):

    with open(map_dir, 'rb') as handle:
        map_indx_1 = pickle.load(handle)
    map_indx_1_rvrs = {val: key for key, val in map_indx_1.items()}

    with open(shuffled_fileNameTXT, "w") as file:
        line = linecache.getline(fileNameTXT, 1)
        file.write(line)
        for i in tqdm(range(data_dim[1])):
            for j in sorted(list(map_indx_1.values())):
                for k in range(data_dim[3]):
                    for m in range(data_dim[4]):
                        line = linecache.getline(fileNameTXT,  ijkm_2_line((i,map_indx_1_rvrs[j], k, m), data_dim[1:]) )
                        file.write(line)
    logging.info(f'The {shuffled_fileNameTXT} generated!')   
# shuffling the file based on third dimention--> col 2-->indx_2
def permute_indx_2(fileNameTXT, shuffled_fileNameTXT, map_dir, data_dim):

    with open(map_dir, 'rb') as handle:
        map_indx_2 = pickle.load(handle)
    map_indx_2_rvrs = {val: key for key, val in map_indx_2.items()}

    with open(shuffled_fileNameTXT, "w") as file:
        line = linecache.getline(fileNameTXT, 1)
        file.write(line)
        for i in tqdm(range(data_dim[1])):
            for j in range(data_dim[2]):
                for k in sorted(list(map_indx_2.values())):
                    for m in range(data_dim[4]):
                        line = linecache.getline(fileNameTXT,  ijkm_2_line((i,j, map_indx_2_rvrs[k], m), data_dim[1:]) )
                        file.write(line)
    logging.info(f'The {shuffled_fileNameTXT} generated!')   
# shuffling the file based on 4th dimention--> col 3-->indx_3
def permute_indx_3(fileNameTXT, shuffled_fileNameTXT, map_dir, data_dim):

    with open(map_dir, 'rb') as handle:
        map_indx_3 = pickle.load(handle)
    map_indx_3_rvrs = {val: key for key, val in map_indx_3.items()}

    with open(shuffled_fileNameTXT, "w") as file:
        line = linecache.getline(fileNameTXT, 1)
        file.write(line)
        for i in tqdm(range(data_dim[1])):
            for j in range(data_dim[2]):
                for k in range(data_dim[3]):
                    for m in sorted(list(map_indx_3.values())):
                        line = linecache.getline(fileNameTXT,  ijkm_2_line((i, j, k, map_indx_3_rvrs[m]), data_dim[1:]) )
                        file.write(line)              
    logging.info(f'The {shuffled_fileNameTXT} generated!')

# permute slab locations map: old to new
def prf_slab(slab_size: int, db_size, map_dir) -> None:
    """
    Shuffling the slab locations
    input:
    slab_size: the size of each slab
    db_size: the size of the database
    map_dir: the path to save the mapping
    
    output:
    map_indx: the mapping from the old slab location to the new slab location
    """
    old_indx = list(range(2,db_size+2 ,slab_size))
    new_indx = np.random.permutation(old_indx)
    map_indx = {key: val for key, val in zip(old_indx, new_indx)}
    with open(map_dir, 'wb') as handle:
        pickle.dump(map_indx, handle, protocol=pickle.HIGHEST_PROTOCOL)

# shuffling the file based on the slab size
def permute_slab(fileNameTXT, shuffled_fileNameTXT, map_dir, slab_size):
    with open(map_dir, 'rb') as handle:
        map_slab = pickle.load(handle)
    map_slab_rvrs = {val: key for key, val in map_slab.items()}

    with open(shuffled_fileNameTXT, "w") as file:
        line = linecache.getline(fileNameTXT, 1)
        file.write(line)
        for i in tqdm(sorted(list(map_slab.values()))):
            for j in range(slab_size):
                line = linecache.getline(fileNameTXT, map_slab_rvrs[i]+j )
                file.write(line)
    
    logging.info(f'The {shuffled_fileNameTXT} generated!')

def prf_general(org_data, mapping_dir):
    shuffled_data = np.random.permutation(org_data)
    mapping = {key: val for key, val in zip(org_data, shuffled_data)}
    with open(mapping_dir, 'wb') as handle:
        pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)

# shuffling the file based on the slab size
def permute_slab_matrix(fileNameTXT, shuffled_fileNameTXT, mapping_dir, slab_dim, datadim):
    with open(mapping_dir, 'rb') as handle:
        map_slab = pickle.load(handle)
    map_slab_rvrs = {val: key for key, val in map_slab.items()}

    all_lines_number = np.prod(datadim[1:])

    with open(shuffled_fileNameTXT, "w") as file:
        line = linecache.getline(fileNameTXT, 1)
        file.write(line)
        for i in tqdm(range(1, all_lines_number+1)):
            slab_num, slab_index = number2slab_matrix(tuple(datadim[1:]), slab_dim, i)
            slab_num_org = map_slab_rvrs[slab_num]
            i_org = slab_matrix2numbers(tuple(datadim[1:]), slab_dim, slab_num_org, slab_index)
            line = linecache.getline(fileNameTXT, i_org+1 )
            file.write(line)
    
    logging.info(f'The {shuffled_fileNameTXT} generated!')

