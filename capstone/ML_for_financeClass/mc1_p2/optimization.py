"""MC1-P2: Optimize a portfolio."""
#http://quantsoftware.gatech.edu/MC1-Project-2-archive

import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo


def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    allocs = find_optimal_allocations(prices,syms) # TODO:add code here to find the allocations

    # Get daily portfolio value
    port_val = get_portfolio_value(prices, syms, allocs, start_val=1000000) # TODO:add code here to compute daily portfolio values
    cr, adr, sddr, sr = get_portfolio_stats(port_val, 0, 252) #  TODO:add code here to compute stats

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        #  TODO:add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_normalized_data(df_temp, title="Daily portfolio value vs. SPY", xlabel="Time", ylabel="normalized prices")

    return allocs, cr, adr, sddr, sr

def get_portfolio_value(prices, syms, allocs, start_val=1000000): #start_val=1000000
    #Compute daily portfolio value given stock prices, allocations and starting value.
    #Ensure that it returns a pandas Series or DataFrame (with a single column).

    Xshare_0=(start_val*allocs[0])/prices[syms[0]][0]
    Xshare_1=(start_val*allocs[1])/prices[syms[1]][0]
    Xshare_2=(start_val*allocs[2])/prices[syms[2]][0]
    Xshare_3=(start_val*allocs[3])/prices[syms[3]][0]
    Xshare_4=(start_val*allocs[4])/prices[syms[4]][0]

    port_val = prices[syms[0]]*Xshare_0+\
                prices[syms[1]]*Xshare_1+\
                prices[syms[2]]*Xshare_2+\
                prices[syms[3]]*Xshare_3+\
                prices[syms[4]]*Xshare_4
    print "port_val==",port_val
    return port_val


def get_portfolio_stats(port_val, daily_rf, samples_per_year):
    #Calculate statistics on daily portfolio value, given daily risk-free rate and data sampling frequency.
    #This function should return a tuple consisting of the following statistics (in order):
    #cumulative return, average daily return, standard deviation of daily return, Sharpe ratio
    #Note: The return statement provided ensures this order.
    cr= port_val[-1]/port_val[0]-1 # Cumulative return
    adr= compute_daily_returns(port_val).mean() #Average daily return
    sddr= compute_daily_returns(port_val).std() #Standard deviation of daily return
    sr=math.sqrt(samples_per_year)*(compute_daily_returns(port_val)-daily_rf).mean()/sddr #daily Sharpe Ratio
    return cr,adr,sddr,sr

def func_min(port_val,daily_rf=0.0):
    #Y=-1.0*(port_val[-1]/port_val[0]) #max cum return
    #max sharpe's ratio
    daily_returns=port_val.copy()
    daily_returns[1:]=(port_val[1:]/port_val[:-1])-1
    daily_returns[0]=0
    volatility=max(daily_returns.std(),1e-4)
    Y=-1.0*(daily_returns-daily_rf).mean()/volatility
    return Y

def plot_normalized_data(df, title, xlabel, ylabel):
    #Normalize given stock prices and plot for comparison.
    #This is used to create a chart that illustrates the value of your portfolio over the year and compares it to SPY.
    #Note: Before plotting, portfolio and SPY values should be normalized to 1.0 at the beginning of the period.
    #Also, use the plot_data() utility function to generate and show your plot.
    df=normarlize_data(df)
    plot_data(df, title="Daily portfolio vs. SPY", ylabel="Normalized price")

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # TODO: Returned DataFrame must have the same number of rows
    daily_returns=df.copy()
    daily_returns[1:]=(df[1:]/df[:-1].values)-1
    daily_returns.ix[0]=0
    return daily_returns

def normarlize_data(df):
    return df/df.ix[0]

def find_optimal_allocations(prices,syms):
    #initial guess
    n=len(syms)
    init_allocs=[1.0/n for x in range(len(syms))]

    #,args=(prices,),
    bnds= tuple((0,1) for x in range(len(syms)))
    cons=({ 'type': 'ineq', 'fun': lambda x: np.sum(x)-1})
    #'Nelder-Mead' can not hangle constrains and bounds
    result=spo.minimize(fun=func_min,x0=init_allocs,method='SLSQP',\
                        bounds=bnds,\
                        constraints=cons,\
                        options={'disp':True})
    return result.x

def test_code():
    # Define input parameters
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio

    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date,\
                                                        ed = end_date,\
                                                        syms = symbols,\
                                                        gen_plot = True)
    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
