# load modules
import pandas as pd
import numpy as np
import time

# log start time
start_time = time.time()

# load input data set (Python pickle file)
df = pd.read_pickle(r'px.xz') # replace <path> with proper file path

# USER CODE
# sort so that dates are ascending for each bbgid 
# this will make the comparison in the next step easier 
df = df.sort_values(by=['bbgid', 'dt'])

df['prev_dt'] = df.dt.shift()
# make a new column in the dataframe which holds the difference between the row and the previous row 
# convert the time delta to a float 
df['length'] = (df.dt - df.prev_dt).astype('timedelta64[D]')

# filter the dataframe to only the values that have the same bbgid 
df['prev_bbgid'] = df.bbgid.shift()
df = df[df.bbgid == df.prev_bbgid]

# sort the new column by length of days descending
df = df.sort_values(by='length', ascending=False)

# only keep the top 1000 values of the dataframe because the reference output 
# only needs the top 1000 values
df = df[0:1001]

# make a new dataframe that holds the start, end, length, and ID
stats = pd.DataFrame({'start': (df.prev_dt + pd.DateOffset(1)).dt.date, 'end': (df.dt - pd.DateOffset(1)).dt.date, 'length': df.length - 1, 'bbgid': df.bbgid}).sort_values(by=['length', 'bbgid', 'start'], ascending=[False, True, True])

# export result to Excel
stats[0:1000].to_excel(r'px_stats.xlsx', index=False) # replace <path> with proper file path

# show execution time
print("--- %s seconds ---" % (time.time() - start_time))
