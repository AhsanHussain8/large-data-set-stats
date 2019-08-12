# load modules
import pandas as pd
import time

# log start time
start_time = time.time()

# load input data set (Python pickle file)
df = pd.read_pickle(r'px.xz')

# USER CODE
# sort the dataframes so dates are ascending for each bbgid 
# this will make the comparison in the next step easier 
df = df.sort_values(by=['bbgid', 'dt'])

# create a new column named prev_dt 
# this column has the value of the previous row so comparison of dates can be quick
# the shift function is used on dt to move each date down a single row 
df['prev_dt'] = df.dt.shift()

# make a new column in the dataframe which holds the difference between the date in the row and the date in the previous row 
# convert the time delta to a float 
df['length'] = (df.dt - df.prev_dt).astype('timedelta64[D]')

# make a new column in the dataframe that has the value of bbgid from the previous row 
df['prev_bbgid'] = df.bbgid.shift()

# filter the dataframe so only rows which have the same bbgid in the previous row are remaining 
df = df[df.bbgid == df.prev_bbgid]

# sort the dataframe by the following columns: length descending, then bbgid ascending, then prev_dt ascending 
df = df.sort_values(by=['length','bbgid', 'prev_dt'], ascending=[False, True, True])

# only keep the top 1000 rows of the dataframe because the reference output has 1000 rows
df = df[0:1000]

# make 3 new series which will become the stats dataframe 
# the prev_dt column holds the day before the gap starts, so 1 day is added to denote the first day of the gap 
start = df.prev_dt + pd.DateOffset(1)

# the dt column holds the day after the gap ends, so 1 day is subtracted to denote the last day of the gap
end = df.dt - pd.DateOffset(1)

# the length column has the number of days between dt and prev_dt, which is one day more than the number of days in the gap. Subtract 1 from length to get the correct value of the gap 
length = df.length - 1

# the ids from the dataframe 
bbgid = df.bbgid

# make a new dataframe that holds the start, end, length, and ID
stats = pd.DataFrame({'start': start, 'end': end, 'length': length, 'bbgid': bbgid})

# export result to Excel
stats[0:1000].to_excel(r'px_stats.xlsx', index=False) 

# show execution time
print("--- %s seconds ---" % (time.time() - start_time))
