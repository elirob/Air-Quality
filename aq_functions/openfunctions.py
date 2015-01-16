#this is a python script for opening .NAS files

def filename_unpack(filename):
'''Reads a .NAS filename and returns the start date, duration, 
frequency and component '''
    list_of_values = filename.split('.')
    start_date = list_of_values[1]
    duration = list_of_values[6]
    frequency = list_of_values[7]
    component = list_of_values[4]
return(start_date, duration, frequency, component)


def read_nas(filepath):
'''Reads a file and returns the lat/long, and raw data'''
    with open(filepath, 'rt') as opened_file:
        opened_lines = opened_file.readlines()
    
    latlon_ = []
    for line in opened_lines[31:33]:
        split_line = re.split(r': *',line)
        if split_line[0] == '':
            split_line.pop(0)
        latlon_.append(float(split_line[1][:-2]))

    lat, lon = latlon_
    
    start_index = []
    end_index = []
    data = []
    data_flag = []
    for line in opened_lines[45:]:
        split_line = re.split(r' *',line)
        if split_line[0] == '':
            split_line.pop(0)
        start_index.append(float(split_line[0]))
        end_index.append(float(split_line[1]))
        data.append(float(split_line[2]))
        data_flag.append(float(split_line[3][:-2]))
        
    return({'lat':lat,'lon':lon,'start_index':start_index,
            'end_index':end_index,'data':data,'data_flag':data_flag})
