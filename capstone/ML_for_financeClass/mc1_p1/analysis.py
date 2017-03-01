"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality

def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):
    #allocs=A list of allocations to the stocks, must sum to 1.0
    #rfr=The risk free rate for the entire period
    #sf=Sampling frequency per year

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later



    # Get daily portfolio value
    # TODO: add code here to compute daily portfolio values
    port_val = prices[syms[0]]*allocs[0]+\
                prices[syms[1]]*allocs[1]+\
                prices[syms[2]]*allocs[2]+\
                prices[syms[3]]*allocs[3]


    # Get portfolio statistics (note: std_daily_ret = volatility)
    # TODO:add code here to compute stats
    cr= port_val[-1]/port_val[0]-1 # Cumulative return
    adr= compute_daily_returns(port_val).mean() #adr: Average daily return
    sddr= compute_daily_returns(port_val).std() #sddr: Standard deviation of daily return
    sr=(adr-rfr)/sddr #Sharpe Ratio


    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # TODO:add code to plot here
        port_val=normarlize_data(port_val)
        prices_SPY=normarlize_data(prices_SPY)
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp , title="Daily portfolio vs. SPY", ylabel="Normalized price")

    #TODO: Add code here to properly compute end value
    ev = sv #sv:Start value of the portfolio ev:End value of portfolio

    return cr, adr, sddr, sr, ev

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    # TODO: Returned DataFrame must have the same number of rows
    daily_returns=df.copy()
    daily_returns[1:]=(df[1:]/df[:-1].values)-1
    daily_returns.ix[0]=0
    return daily_returns

def normarlize_data(df):
    return df/df.ix[0]

def test_code():
    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]

    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
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
