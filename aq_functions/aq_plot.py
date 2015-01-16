import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import openfunctions


def timeseries_histogram_simple(sample):
    '''Takes dataframe from openfunctions.data_to_pandas_dataframe and
    produces a timeseries plot and a histogram of the data within'''
    sample.plot()
    sample.hist()
    plt.show()
    
def nice_fill_plot(filepath):
    ''' Produce area plot of .nas file given by filepath '''
    testDF = openfunctions.data_to_pandas_dataframe(filepath)
    dictionary = openfunctions.read_and_clean(filepath)
    testDF[dictionary['component']].plot(kind='area',color='#7c8c93')
    plt.ylabel(dictionary['units'])
    plt.xlabel('Date of observation')
    plt.show()


