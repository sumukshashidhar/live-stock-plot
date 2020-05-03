# Author: Sumuk Shashidhar
# License: BSD
# You must credit the author / link the source if you decide to use this

## Imports

import urllib.request
import json
from datetime import date
import time
import argparse

## this url puts the ticker variable into the yahoo query1 api
def stdout(price_data, market_time,stock_name):
    try:
        f = open(str("./data/"+stock_name+'_'+str(date.today())+ ".csv"), 'a')
    except FileNotFoundError:
        try:
            f = open(str("./data/"+stock_name+'_'+str(date.today())+ ".csv"), 'w')
        except:
            print("You are running the file directly from the source directory. \n This is not supported at the time \n  Please run it from the root directory of the repo")
    finally:
        f.write(str(str(market_time) + ',' + str(price_data)))
        f.write('\n')
        f.close()



def data_parse(new_data):
    string = new_data.read().decode('utf-8')
    data_parsed = json.loads(string)
    data_parsed = data_parsed["quoteResponse"]["result"][0]
    # print(json.dumps(data_parsed, indent=4)) ## for debugging purposes
    stdout(data_parsed["regularMarketPrice"], data_parsed["regularMarketTime"], ticker)

def get_new_data():
    new_data = urllib.request.urlopen(url)
    data_parse(new_data)


def periodic_fetch_loop():
    while(True):
        ## try fetching every 10 seconds
        get_new_data()
        time.sleep(9)


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--ticker", help="Add the ticker")
args = parser.parse_args()

if args.ticker == None:
    print("Please pass in the ticker argument for this to work")
    exit()
else:
    ticker = args.ticker
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="+ ticker + "&range=1d&interval=5m&indicators=close&includeTimestamps=false&includePrePost=false&corsDomain=finance.yahoo.com&.tsrc=finance"
    print("\n\n\n\n")
    print("Pass this as an argument to the plotting module for it to start up \n \n"+ "./../../data/"+ticker+'_'+str(date.today())+ ".csv")
    periodic_fetch_loop()
