# -*- coding: utf-8 -*-

# this is the code I used to scrape a time series of all straight bets from bestfightodds
# the script takes paramter inputs to determine how to split the data and which split dataset to take
# I wrote it this way so that I can scrape from multiple browsers in parallel 
# I did not include prop bets and event bets because bestfightodds using javascript
# to pull the time series, and so scraping must be done in a remote browser which 
# is prohibitively slow

# you should run the code from the command line with 3 arguments
# the first argument is the number of datasets the dataset with all events should be partitioned into
# the second argument is the 0 based index to run the code for the one of the n datasets.
# the third argument is the lag between each click. some lag is needed to give the website time
# to pull the data 
# For example, running the code with arguments 3 0 .3 would split all the events into 3 
# equal sized datasets, run the scraping code for the first of the 3 datasets
# and pause for .3 seconds between each click while scraping
# the code checks for events that were already scraped and skips them

# executing python 3_bestfightoddspull_time_series_straight_bets.py 3 0 .3
# python 3_bestfightoddspull_time_series_straight_bets.py 3 1 .3
# and python 3_bestfightoddspull_time_series_straight_bets.py 3 3 .3
# would pull all the events using 3 browsers concurrently
# this will take several hours

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from selenium import webdriver
import os 
import itertools
os.environ["PATH"] += os.pathsep + r'./gecko driver/' # have to add geckodriver file path here
import time
from itertools import compress
import sys


def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0,parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

events = pd.read_csv("../../data/bestfightodds_data/bestfightodds_urls.csv")
events = events.loc[(events['fight_odds_url'].notna()) & (events['fight_odds_url'] != '') , :]
events['output'] = events['Event'].apply(lambda x: re.sub(r"[^A-Za-z0-9_]", "_", x))
events['output'] = events['output'].apply(lambda x:"ordinarybet_datatest_"+x+".csv")

alreadydone = os.listdir("../../data/bestfightodds_data/straight_bets/")
events = events.loc[ events['output'].isin(alreadydone) == False  , : ]


def run_process(df, sleeptime = .01):
    driver = webdriver.Firefox()
    urls = df['fight_odds_url']
    event_names = df['Event']
    for event_index in range(len(urls)):
        try:
            event_name = event_names.iat[event_index]
            url = urls.iat[event_index]
            page = requests.get(url)
            driver.get(url)
            soup = BeautifulSoup(page.text, 'lxml')
            columns = ['class']+[t.text for t in soup.find_all('table',class_ = 'odds-table')[1].thead.tr.find_all('th')][0:-1]+['meanodds']
            rowtable = soup.find_all('table',class_ = 'odds-table')[1].tbody.find_all('tr')
    
            #filter to only non prop bets. comment line below if prop bets are needed
            rowtable = list(compress(rowtable, [row['class'][0]  in ['even', 'odd'] for row in rowtable]))
            # loop over betting rows to extract info
            urldfs = []
            date_cell = driver.find_element_by_xpath(xpath_soup(soup.find(class_ = "table-header-date"))) 
            fighter1 = np.nan
            fighter2 = np.nan
    
            for rownum, row in enumerate(rowtable):  
                rowclass = row['class'][0]
                betname = row.find('th').text
                bets = row.find_all('td')
                meancell = xpath_soup(bets[-2])
                if betname.lower() == 'event props':
                    break
    
                if rowclass == 'even':
                    fighter1 = betname
                    fighter2 = rowtable[rownum + 1].find('th').text
                
                
                bets = bets[0:-2]
                bets.append(meancell)
                lastcolindex = len(bets) - 1
                # for each bet get the time series
                for index, bet in enumerate(bets):
        
                    if index == lastcolindex:
                        driver.find_element_by_xpath(meancell).click()
                        driver.switch_to.active_element
                        time.sleep(sleeptime)
                    else:   
                        #get chart to appear
                        #sometimes field is populated with a nonsense value and must be skiped over
                        try:
                            # skip betting sites that didn't offer the bet
                            if bet.text == '':
                                continue
                            betid = bet.span.span["id"]
                            driver.find_element_by_id(betid).click()
                            driver.switch_to.active_element
                        except:
                            continue
                        else:
                            pass
    
    
                    chart_number = driver.find_element_by_id('chart-area').get_attribute('data-highcharts-chart')
                    chart_data = driver.execute_script('return Highcharts.charts[' + chart_number + '].series[0].options.data')
                    # pull chart data
                    dates = [None] * len(chart_data)
                    vals = [None] * len(chart_data)
                    for i, point in enumerate(chart_data):
                        e = driver.execute_script('return oneDecToML('+ str(point.get('y')) + ')')
                        dates[i] = point.get('x')
                        vals[i] = e
    
                    celldf = pd.DataFrame({'dates':dates, 'odds':vals, \
                                       'Bet':[betname] * len(chart_data), 'betsite':[columns[2 + index]] * len(chart_data),
                                           'fighter1':[fighter1] * len(chart_data), \
                                               'fighter2':[fighter2]* len(chart_data), 'class':[rowclass]*len(chart_data)},
                                          columns = [ 'Bet', 'betsite', 'dates', 'odds', 'fighter1', 'fighter2', 'class'])
                    urldfs.append(celldf)
                    try:
                        date_cell.click() # make chart disappear so it can't cover up the next cell
                    except:
                         driver.find_element_by_id("search-box1").click()
                         time.sleep(sleeptime)
                
                
                # comment/uncomment to expand prop bet rows if desired
        #             if rowclass == "even":
        #                 driver.find_element_by_xpath(xpath_soup(bets[-1])).click()
    
            # concatenate the dfs to get all data for this urls
            urldf = pd.concat(urldfs)
            urldf['url'] = url
            event_name_cleaned = re.sub(r"[^A-Za-z0-9_]", "_", event_name)
            urldf.to_csv("../../data/bestfightodds_data/straight_bets/ordinarybet_datatest_" + event_name_cleaned + ".csv", index = False)
        except:
            print(url)
            print(args)
            driver.close()
            time.sleep(sleeptime)
            driver = webdriver.Firefox()
            time.sleep(sleeptime)
            continue
        else:
            pass
 

           
args = sys.argv
eventlist = np.array_split(events, int(args[1]))
run_process(eventlist[int(args[2])], float(args[3]))



