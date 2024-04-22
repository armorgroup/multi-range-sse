# import argparse
    
# parser = argparse.ArgumentParser(description='Process some integers.')

# parser.add_argument('-dim', '--dimensions', type= int, required= False, default= 2)
# parser.add_argument('-dmv', '--dimsvalue', type= int, required= False, default= 16)
# parser.add_argument('-s', '--slab', type= int, required= False, default= 16)
# parser.add_argument('-smp', '--sample_num', type= str, required= False, default= '1000')
# parser.add_argument('-ot', '--outlier', type= str, required= False, default= 'max')
# parser.add_argument('-od', '--outlier_dim', type= int, required= False, default= 0)
# parser.add_argument('-dr', '--d_range', type= int, required= False, default= 3)

# arg_cli = parser.parse_args()

# # DataSet configuration
# class args:
#     datagen = None
#     encrypt = None
#     kdisk = None
#     shuffle = None
#     report = True
#     # [num_dimensions, dim1, dim2, dim3, dim4]
#     datadim = [arg_cli.dimensions if i == 0 else arg_cli.dimsvalue if i <= arg_cli.dimensions else 0 for i in range(5)] 
#     slabdim = [arg_cli.slab]*datadim[0] # slab dimensions
#     slab_size = slabdim[0]**datadim[0] # slab size, devided row shuffling scheme, sliding partition size
#     query = [None]
#     rangequery = [index for i in range(datadim[0]) for index in (0, 2)] # range query default

# # query generator configuration
# class query_config:
#     # number of samples
#     sample_num = arg_cli.sample_num

#     # outlier configurations
#     outlier_type = arg_cli.outlier  # Change to 'min' for minimum outlier
#     outlier_dim_idx = arg_cli.outlier_dim  # Index of the dimension to have the outlier width
#     d_range = arg_cli.d_range  # Range for generating the outlier

# # print args and query_config properties
# print( 'args.datadim', args.datadim)
# print( 'args.slabdim', args.slabdim)
# print( 'args.slab_size', args.slab_size)
# print( 'query_config.sample_num', query_config.sample_num)
# print( 'query_config.outlier_type', query_config.outlier_type)
# print( 'query_config.outlier_dim_idx', query_config.outlier_dim_idx)
# print( 'query_config.d_range', query_config.d_range)
# print( 'range query', args.rangequery)


# DataSet configuration
class args:
    datagen = None
    encrypt = None
    kdisk = None
    shuffle = None
    report = True
    datadim = [3 , 64, 64, 64, 0] # [num_dimensions, dim1, dim2, dim3, dim4]
    slabdim = [8] * datadim[0] # slab dimensions
    slab_size = slabdim[0]**datadim[0] # slab size, devided row shuffling scheme, sliding partition size
    query = [None]
    rangequery = [0, 2, 0, 2, 0, 2] # range query default

# query generator configuration
class query_config:
    # number of samples
    sample_num = 1000

    # outlier configurations
    outlier_type = 'max'  # Change to 'min' for minimum outlier
    outlier_dim_idx = 0  # Index of the dimension to have the outlier width
    d_range = 4  # Range for generating the outlier

    log2_scale = 18 # dataset size in log2 scale