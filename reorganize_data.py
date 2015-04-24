#This script reorganizes the turnstile data for a single datafile, calculates
#morning/evening/total entries/exits for each day, for each station, converts
#dates into days of the week and into weekday/weekend (binary var), and prints
#the resulting dataframe to a csv file.

import pandas as pd

#Imports a data file for a single week and reads it into a pandas dataframe.
dir = "/Users/ilya/metis/week1/"
filename = "turnstile_150321.txt"
file = dir + filename
data = pd.read_csv(file)
data = data.rename(columns = lambda x: x.strip())
for x in data['EXITS']:
    x = str(x).strip()

#This function puts metainfo (STATION/SCP/DATE) and morn/eve entry/exit counts
#into a new dataframe:
def frame_builder(df, metainfo, morn_entries, morn_exits, eve_entries, 
    eve_exits):
    df.loc[len(df)] = [metainfo[0], metainfo[1], metainfo[2], morn_entries, morn_exits, eve_entries, eve_exits]
    return df

grouped_data = pd.DataFrame(columns = ('STATION', 'SCP', 'DATE', 
    'morn_entries', 'morn_exits', 'eve_entries', 'eve_exits'))
#Group data by turnstile and calculate morning and afternoon counts:
grouped = data.groupby(by = ['STATION', 'SCP', 'DATE'])
for name, group in grouped:
    #Pull entry/exit data for a given station/scp/date:
    try:
        metainfo = name
        dat = group[['EXITS','ENTRIES']]
        #Find the cumulative counts for the second, fourth and sixth timeslots:
        second_time = dat.iloc[1]
        fourth_time = dat.iloc[3]
        sixth_time = dat.iloc[5]
        morn_entries = abs(fourth_time[1] - second_time[1])
        morn_exits = abs(fourth_time[0] - second_time[0])
        eve_entries = abs(sixth_time[1] - fourth_time[1])
        eve_exits = abs(sixth_time[0] - fourth_time[0])
    except:
        pass
    frame_builder(grouped_data, metainfo, morn_entries, morn_exits, 
        eve_entries, eve_exits)

import numpy as np
grouped = grouped_data.groupby(by = ['STATION', 'DATE'])
final_df = pd.DataFrame(columns = ('STATION', 'DATE', 'morn_entries',
    'morn_exits', 'eve_entries', 'eve_exits'))
for name, group in grouped:
    metainfo = name 
    morn_entries = int(np.sum(group[['morn_entries']]))
    morn_exits = int(np.sum(group[['morn_exits']]))
    eve_entries = int(np.sum(group[['eve_entries']]))
    eve_exits = int(np.sum(group[['eve_exits']]))
    final_df.loc[len(final_df)] = [metainfo[0], metainfo[1], morn_entries,
        morn_exits, eve_entries, eve_exits]

#Sum entries and exits across morn and night, for each row:
final_df['entry_total'] = final_df['morn_entries'] + final_df['eve_entries']
final_df['exit_total'] = final_df['morn_exits'] + final_df['eve_exits']

#Convert dates to datetime objects, then determine day of the week and whether
#or not it's a weekday for each row:
import datetime
import dateutil.parser
final_df['day_of_week'] = [dateutil.parser.parse(x).weekday() for x in\
 final_df['DATE']]
final_df['weekday'] = [1 if x < 5 else 0 for x in final_df['day_of_week']]

final_df.to_csv(path_or_buf = 
    "/Users/ilya/metis/week1/group_project_week_1/150321_reorganized.csv")




