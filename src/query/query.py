
import pickle


def query_2_range(i_start,i_finish):
        # i_start = (0,0,0,0)
        # i_finish = (10,10,10,10)
        for i,inx in enumerate(i_finish):
            if i_finish[i]<=i_start[i]:    
                print("Incorrect range!")
                return []
                
        queryRange=[]
        if len(i_start)==2:
            for i in range(i_start[0], i_finish[0]):
                queryRange.append([(i,i_start[1]),(i,i_finish[1])])            
        elif len(i_start)==3:
            for i in range(i_start[0], i_finish[0]):
                for j in range(i_start[1], i_finish[1]):
                    queryRange.append([(i,j,i_start[2]),(i,j, i_finish[2])])            
        elif len(i_start)==4:
            for i in range(i_start[0], i_finish[0]):
                for j in range(i_start[1], i_finish[1]):
                    for k in range(i_start[2], i_finish[2]):
                        queryRange.append([(i,j,k,i_start[3]),(i,j,k,i_finish[3])])

        return queryRange

       
def query_2_range_shuffled(i_start,i_finish,map_dir):        
    with open(map_dir, 'rb') as handle:
        map_indx_0 = pickle.load(handle)     

    for i,inx in enumerate(i_finish):
        if i_finish[i]<=i_start[i]:    
            print("Incorrect range!")
            return []
            
    queryRange=[]
    for i in range(i_start[0], i_finish[0]):
        for j in range(i_start[1], i_finish[1]):
            for k in range(i_start[2], i_finish[2]):
                queryRange.append([(map_indx_0[i],j,k,i_start[3]),(map_indx_0[i],j,k,i_finish[3])])

    return queryRange

# Transfer the range query on original file to the subranges  on shuffled file based on second dimension
def query_2_range_shuffled_index_1(i_start,i_finish,map_dir):        
    with open(map_dir, 'rb') as handle:
        map_indx_1 = pickle.load(handle)     

    for i,inx in enumerate(i_finish):
        if i_finish[i]<=i_start[i]:    
            print("Incorrect range!")
            return []
            
    queryRange=[]
    for i in range(i_start[0], i_finish[0]):
        for j in range(i_start[1], i_finish[1]):
            for k in range(i_start[2], i_finish[2]):
                queryRange.append([(i,map_indx_1[j],k,i_start[3]),(i,map_indx_1[j],k,i_finish[3])])

    return queryRange

# Transfer the range query on original file to the subranges  on shuffled file based on 3th dimension
def query_2_range_shuffled_index_2(i_start,i_finish,map_dir):        
    with open(map_dir, 'rb') as handle:
        map_indx_2 = pickle.load(handle)     

    for i,inx in enumerate(i_finish):
        if i_finish[i]<=i_start[i]:    
            print("Incorrect range!")
            return []
            
    queryRange=[]
    for i in range(i_start[0], i_finish[0]):
        for j in range(i_start[1], i_finish[1]):
            for k in range(i_start[2], i_finish[2]):
                queryRange.append([(i,j,map_indx_2[k],i_start[3]),(i,j,map_indx_2[k],i_finish[3])])

    return queryRange

