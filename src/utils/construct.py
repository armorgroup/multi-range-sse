import logging
import os
import csv


import numpy as np
from crypto import permute

from utils.utils import event_duration, user_response_exe, path, query_report, query_yes_no, query_yes_no_exe, rename_path
from datagen.datagent import datagen, datagenHdf5, create_kdtree, create_kdtree_slab_shuffled, create_kdtree_slab_matrix_shuffled
from dataloader.dataloader import dataload


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)") 
ed = event_duration(scale='milli', log=True)

def construct(args, prompt = True, indx=''):
    if prompt == True:
        user_response = query_yes_no(f"If the file already exists, do you want to overwrite it?")
    else:
        user_response = True

    path_inst = path()
    path_inst = rename_path(path_inst, indx)

    #-----------------datadim calculation based on the number of dimensions-----------------
    if args.datadim[0] == 2:
        datadim = args.datadim[:3]
    elif args.datadim[0] == 3:
        datadim = args.datadim[:4]
    elif args.datadim[0] == 4:
        datadim = args.datadim[:5]
    
    ds_size = np.prod(datadim[1:])

    # --------------------- Generating the sample data ---------------------
    # --------------------- txt ---------------------
    dataGenerator_org = datagen(path_inst.org_data,
                            data_dim=args.datadim[0],
                            lat_dim=args.datadim[1],
                            long_dim=args.datadim[2],
                            height_dim=args.datadim[3],
                            time_dim=args.datadim[4])
    # datagen=='txt' and encrypt==None and shuffle==None
    user_response_exe(path_inst.org_data,  user_response, dataGenerator_org.generate_data)
    # datagen=='txt' and encrypt==True and shuffle==None
    user_response_exe(path_inst.org_encrypted, user_response, 
                        dataGenerator_org.generate_encryptData_from_txt, path_inst.org_encrypted, 'AES_XTS')
    # datagen=='txt' and encrypt==True and shuffle=='sh'
    ds_pos=list(range(2,ds_size+2))
    user_response_exe(path_inst.mapping, user_response, permute.prf, ds_pos, 
                        path_inst.mapping, datadim, path_inst.line_2_ijkm)
    user_response_exe(path_inst.encrypted_shuffled, user_response, permute.permute, 
                        path_inst.org_encrypted, path_inst.encrypted_shuffled, path_inst.mapping)

    # datagen=='txt' and encrypt==True and shuffle=='shs', devided-Row shufflling
    user_response_exe(path_inst.mapping_slab, user_response, permute.prf_slab, args.slab_size, ds_size, path_inst.mapping_slab)
    user_response_exe(path_inst.encrypted_shuffled_slab, user_response, permute.permute_slab,
                        path_inst.org_encrypted, path_inst.encrypted_shuffled_slab, 
                        path_inst.mapping_slab, args.slab_size)
    
    # datagen=='txt' and encrypt==True and shuffle=='shsm', slab matrix shufflling 
    slab_set_dim = tuple([int(datadim[i+1]/args.slabdim[i]) for i in range(len(datadim[1:]))])
    org_data = list(range(1,np.prod(slab_set_dim)+1))
    user_response_exe(path_inst.mapping_slab_matrix, user_response, permute.prf_general, org_data, path_inst.mapping_slab_matrix)
    user_response_exe(path_inst.encrypted_shuffled_slab_matrix, user_response, permute.permute_slab_matrix,
                        path_inst.org_encrypted, path_inst.encrypted_shuffled_slab_matrix, 
                        path_inst.mapping_slab_matrix, args.slabdim, datadim)    

    # --------------------- kdtree ---------------------

    # datagen=='kdtree' and encrypt==True and shuffle==None and kdisk==None, kdtree in memory without shuffling
    user_response_exe(path_inst.kdtree_encrypted_obj, user_response, create_kdtree, datadim, 
                        path_inst.org_encrypted, path_inst.kdtree_encrypted_obj, 'memory')

    # datagen=='kdtree' and encrypt==True and shuffle=='sh' and kdisk==None, kdtree in memory with element-wise shuffling
    user_response_exe(path_inst.kdtree_encrypted_shuffled_obj, user_response, create_kdtree, 
                        datadim, path_inst.encrypted_shuffled, 
                        path_inst.kdtree_encrypted_shuffled_obj, 'memory')
    
    # datagen=='kdtree' and encrypt==True and shuffle=='shs' and kdisk==None, kdtree in memory with devided-row shuffling
    user_response_exe(path_inst.kdtree_encrypted_shuffled_slab, user_response, create_kdtree_slab_shuffled,
                       datadim, path_inst.encrypted_shuffled_slab, path_inst.kdtree_encrypted_shuffled_slab, args.slab_size)
    
    # datagen=='kdtree' and encrypt==True and shuffle=='shsm' and kdisk==None, kdtree in memory with slab matrix shuffling
    user_response_exe(path_inst.kdtree_encrypted_shuffled_slab_matrix, user_response, create_kdtree_slab_matrix_shuffled, datadim, 
                        path_inst.encrypted_shuffled_slab_matrix, path_inst.kdtree_encrypted_shuffled_slab_matrix, args.slabdim)    

    report_dict = {'kdtree':{ 'en_no_no':[], 'en_sh_ram':[], 'en_shs_ram':[], 'en_shsm_ram':[]}}

    # --------------------- Querying the data ---------------------
    i_start = tuple(args.rangequery[0::2])
    i_finish = tuple(args.rangequery[1::2])
    dataLoader = dataload(path_inst.org_data,
                        data_dim=args.datadim[0],
                        lat_dim=args.datadim[1],
                        long_dim=args.datadim[2],
                        height_dim=args.datadim[3],
                        time_dim=args.datadim[4],
                        encrypted=None)
    args.query, args.encrypt, args.shuffle = 'txt', None, None
    queryResult, _ = query_report(args, ed, [], dataLoader.load_slabs, i_start, i_finish)

    # query=='kdtree' and encrypt==True and shuffle==None and kdisk==None
    dataLoader = dataload(path_inst.org_encrypted,
                        data_dim=args.datadim[0],
                        lat_dim=args.datadim[1],
                        long_dim=args.datadim[2],
                        height_dim=args.datadim[3],
                        time_dim=args.datadim[4],
                        encrypted = None)
    args.query, args.encrypt, args.shuffle = 'kdtree', True, None
    _, report_dict['kdtree']['en_no_no'] = query_report(args, ed, queryResult[0], dataLoader.range_query_kdtree, 
                            i_start, i_finish, path_inst.kdtree_encrypted_obj, 'ram')
    report_dict['kdtree']['en_no_no'] = add_info(report_dict['kdtree']['en_no_no'], path_inst.kdtree_encrypted_obj, datadim, dataLoader.buckets_ctr, part_nums=dataLoader.part_nums)
    
    # query=='kdtree' and encrypt==True and shuffle=='sh' and kdisk==None
    dataLoader = dataload(path_inst.encrypted_shuffled,
                        data_dim=args.datadim[0],
                        lat_dim=args.datadim[1],
                        long_dim=args.datadim[2],
                        height_dim=args.datadim[3],
                        time_dim=args.datadim[4],
                        encrypted = None,
                        shuffled='element',
                        map_dir=path_inst.mapping)
    args.query, args.encrypt, args.shuffle = 'kdtree', True, 'sh'
    _, report_dict['kdtree']['en_sh_ram'] = query_report(args, ed, queryResult[0], dataLoader.range_query_kdtree, 
                        i_start, i_finish, path_inst.kdtree_encrypted_shuffled_obj, 'ram')
    report_dict['kdtree']['en_sh_ram'] = add_info(report_dict['kdtree']['en_sh_ram'], path_inst.kdtree_encrypted_shuffled_obj, datadim, dataLoader.buckets_ctr, part_nums=dataLoader.part_nums)

    # query=='kdtree' and encrypt==True and shuffle=='shs' and kdisk==None
    dataLoader = dataload(path_inst.encrypted_shuffled_slab,
                        data_dim=args.datadim[0],
                        lat_dim=args.datadim[1],
                        long_dim=args.datadim[2],
                        height_dim=args.datadim[3],
                        time_dim=args.datadim[4],
                        encrypted = None,
                        shuffled='slab',
                        map_dir=path_inst.mapping_slab)
    args.query, args.encrypt, args.shuffle = 'kdtree', True, 'shs'
    _, report_dict['kdtree']['en_shs_ram'] = query_report(args, ed, queryResult[0], dataLoader.range_query_kdtree_slab, 
                        i_start, i_finish, path_inst.kdtree_encrypted_shuffled_slab, args.slab_size)
    report_dict['kdtree']['en_shs_ram'] = add_info(report_dict['kdtree']['en_shs_ram'], path_inst.kdtree_encrypted_shuffled_slab, datadim, dataLoader.buckets_ctr, part_nums=dataLoader.part_nums)
    
    # query=='kdtree' and encrypt==True and shuffle=='shsm' and kdisk==None
    dataLoader = dataload(path_inst.encrypted_shuffled_slab_matrix,
                    data_dim=args.datadim[0],
                    lat_dim=args.datadim[1],
                    long_dim=args.datadim[2],
                    height_dim=args.datadim[3],
                    time_dim=args.datadim[4],
                    encrypted = None,
                    shuffled='slab_matrix',
                    map_dir=path_inst.mapping_slab_matrix)
    # range_query_kdtree_slab_matrix(self, r_start, r_finish, kdtree_filePath, slab_dim, data_dim)
    args.query, args.encrypt, args.shuffle = 'kdtree', True, 'shsm'
    _, report_dict['kdtree']['en_shsm_ram'] = query_report(args, ed, queryResult[0], dataLoader.range_query_kdtree_slab_matrix, 
                        i_start, i_finish, path_inst.kdtree_encrypted_shuffled_slab_matrix, args.slabdim, datadim)
    report_dict['kdtree']['en_shsm_ram'] = add_info(report_dict['kdtree']['en_shsm_ram'], path_inst.kdtree_encrypted_shuffled_slab_matrix, datadim, dataLoader.buckets_ctr, part_nums=dataLoader.part_nums)


    # Fixed parts of the header
    header = ['query', 'time', 'valid', 'query_size', 'file_size']
    # Dynamically add dimension labels
    dimension_labels = [f'dim{i+1}' for i in range(len(datadim[1:]))]
    header.extend(dimension_labels)
    # Append the last fixed part
    header.append('data_set_size')

    if prompt == True:    
        query_yes_no_exe(path_inst.report, write_report, report_dict, path_inst.report, header)
        query_yes_no_exe(path_inst.report_bucket, write_report_2, report_dict, path_inst.report_bucket, args)
    else:
        write_report(report_dict, path_inst.report, header)
        write_report_2(report_dict, path_inst.report_bucket, args)

def add_info(list_info, file_path, datadim, backet_ctr = None, part_nums = 0):
    added_data = [os.path.getsize(file_path)]
    added_data.extend(datadim[1:])
    added_data.extend([np.prod(datadim[1:]), backet_ctr, part_nums])
    list_info.extend(added_data)
    return list_info

def write_report(report_dict, file_path, header):
    values = []
    for k,v in report_dict.items():
        for k2,v2 in v.items():
            row = [k+'_'+k2,*v2[:-1]]
            values.append(row)

    if not os.path.exists(file_path):
        with open(file_path, 'w'):
                pass
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(values)

    logging.info(f"The report is written in the {file_path}")


def write_report_2(report_dict, file_path, args):

    # Start with the fixed header parts
    header = ['method_name', 'bucket_count', 'query size', 'response_size', 
                'bucket_count/response_size', 'part numbers']

    # Dynamically generate headers for dimensions
    width_headers = [f'width{i+1}' for i in range(args.datadim[0])]
    start_finish_headers = [header for i in range(args.datadim[0]) for header in (f'start{i+1}', f'finish{i+1}')]

    # Combine all parts of the header
    final_header = header + width_headers + start_finish_headers

    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(final_header) 
            
    for k,v in report_dict.items():
        for k2,v2 in v.items():
            width = [e-i for i,e in zip(args.rangequery[0::2], args.rangequery[1::2])]
            #final repoted data in the row
            query_title = [k+'_'+k2, len(v2[-2].keys()), np.prod(width), sum(v2[-2].values()),
                            round(len(v2[-2].keys())/sum(v2[-2].values()),2),v2[-1], *width, *args.rangequery]
                
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(query_title)