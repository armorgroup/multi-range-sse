
import confuse

config = confuse.Configuration('App')
config.set_file('../../conf.yaml')
dir = config['sample_data']['dir'].get()


def load_file():
    array = []
    with open(dir, 'r') as the_file:
        i=0
        for line in the_file:
            if i==0:
                i+=1
                continue    
            line = line.strip('\n').split('\t\t')        
            array.insert(i,line)
            i+=1
        return array