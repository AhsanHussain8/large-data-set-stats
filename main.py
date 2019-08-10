# load modules
import pandas as pd
import time

# log start time
start_time = time.time()

print(start_time)

# load input data set (Python pickle file)
df = pd.read_pickle(r'px.xz') # replace <path> with proper file path

# USER CODE
# sort so that dates are ascending for each bbgid 
# this will make the comparison in the next step easier 
df = df.sort_values(by=['bbgid', 'dt'])

# make a new series to hold calculated values 
stats_series = {}

# make a new column in the dataframe which holds the difference between the row and the previous row 
# convert the time delta to a float 
df['length'] = (df.dt - df.dt.shift()).astype('timedelta64[D]')

# sort the new column by length of days descending
df['length'] = df['length'].sort_values(ascending=False)

# only keep the top 1000 values of the dataframe because the reference output 
# only needs the top 1000 values
df = df[0:1000]

# make a new dataframe that holds the start, end, length, and ID
stats = pd.DataFrame({'start': df.dt.shift(-1), 'end': df.dt - pd.DateOffset(1), 'length': df.length, 'bbgid': df.bbgid})

# export result to Excel
stats.to_excel(r'px_stats.xlsx', index=False) # replace <path> with proper file path

# show execution time
print("--- %s seconds ---" % (time.time() - start_time))
