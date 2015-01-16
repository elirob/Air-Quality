import numpy as np
import pandas as pd
import matplotlib as plt
import aq_functions.openfunctions as opener


#DATA IN
random_data = np.random.rand(52)
dates = pd.date_range('20030101',periods=52,freq='W')
sample = pd.Series(random_data,index=dates)
sample = opener.data_to_pandas_dataframe(r'GB0046R.20030107080000.20040302000000.low_vol_sampler.pm10_mass.pm10.6mo.1w.NO01L_lvs_uk17.NO01L_Thermo_Optical-Sunset_Lab.lev2.nas')
species = 'pm10_mass'



#Plot graph Routine
def plotgraph(sample,dates,species):
    """plots time series data for the entire year in weekly intervals"""

    #Assertions
    
    #Plot graph
    timeseries = pd.DataFrame(sample,columns=[species],index=dates)
    timeseries.plot(kind='area')


# Stats calculation Routine
def stats_calc(sample,dates):
    """calculates some summary stats of the dataset"""    
    
    #Assertions
    
    #Calculate summary stats
    mins = np.nanmin(sample)
    maxs = np.nanmax(sample)
    mu = np.nanmean(sample)
    sigma = np.nanstd(sample)

    return mins, maxs, mu, sigma

# Histogram routine
def plot_hist(sample,mu,sigma):
    """create frequency histogram from summary stats"""
    
    #Assertions

    #find frequency
    x = mu + sigma * sample
    hist, bins = np.histogram(x, bins=10)

    #create parameters
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2

    # plot histogram
    plt.pyplot.bar(center, hist, align='center', width=width)

