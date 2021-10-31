import pandas as pd
import sqlite3
import plotly.express as px
import plotly.offline as py




conn = sqlite3.connect("Trips_and_vendors.db")


query='''SELECT AVG((julianday(dropoff_datetime) - julianday(pickup_datetime))* 24 * 60) as avg_trip_time,
            cast (strftime('%w', pickup_datetime) as integer) as week_day
FROM Trips
WHERE week_day == 0 or week_day==6
GROUP BY week_day
'''

#Reading the query result into a dataframe
temp_df = pd.read_sql(query, conn)

#Labeling the days of the week, that are returned as integers by the query
temp_df.loc[temp_df['week_day']==0,'week_day'] = 'Sunday'
temp_df.loc[temp_df['week_day']==6,'week_day'] = 'Saturday'

#Getting the highest average trip time between both days
avg = temp_df['avg_trip_time'].max()

fig = px.bar(temp_df, x='week_day', y='avg_trip_time', title='AVG trip time in minutes by day')
fig.add_hline(y=avg, line_dash = 'dash', line_color = 'firebrick',annotation_text=f"Highest avg: {avg}")
py.plot(fig)