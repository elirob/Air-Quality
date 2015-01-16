#this is a python script for opening .NAS files

import re
import numpy as np
from datetime import timedelta, datetime
import os
import pandas as pd


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
    
    split_line = re.split(r': *',opened_lines[30])
    name = (split_line[1])
    name = name[:-2]

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
        
    return({'lat':lat,'lon':lon,'station_name':name,
            'start_index':start_index,'end_index':end_index,
            'data':data,'data_flag':data_flag})

def read_and_clean(filepath):
    raw_info = read_nas(filepath)
    filename = os.path.split(filepath)[-1]
    file_info = filename_unpack(filename)
    
    ## Clean 9999 flag to np.nan type
    raw_info['data'] = np.array(raw_info['data'])
    raw_info['data'] = np.where(raw_info['data']==999.99,np.nan,raw_info['data'])
    raw_info['data'] = np.where(raw_info['data']==9999,np.nan,raw_info['data'])
    dt_str = file_info[0]
    start_dt = datetime(int(dt_str[:4]),int(dt_str[4:6]),int(dt_str[6:8]),int(dt_str[8:10]))
    for i,d in enumerate(raw_info['start_index']):
        day = timedelta(days=d)
        date = start_dt + day
        raw_info['start_index'][i] = date
    for i,d in enumerate(raw_info['end_index']):
        day = timedelta(days=d)
        date = start_dt + day
        raw_info['end_index'][i] = date
    raw_info.update({'component':file_info[3]})
    return(raw_info)
    
def data_to_pandas_dataframe(filepath):
    data_info = read_and_clean(filepath)
    slim_data = {data_info['component']:data_info['data']}
    return(pd.DataFrame(slim_data,index=data_info['start_index']))