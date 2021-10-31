import pandas as pd
import sqlite3
import plotly.express as px
import plotly.offline as py

conn = sqlite3.connect("Trips_and_vendors.db")

#Query to get trip distance from trips with a maximum of 2 passengers
query = '''SELECT trip_distance 
FROM Trips
WHERE passenger_count BETWEEN 1 and 2
'''

#Reading the query result into a temporary dataframe
temp_df = pd.read_sql(query, conn)

#Query to get the average of the trip distance, just to show knowledge of aggregating functions
query = '''SELECT AVG(trip_distance ) as avg_distance
FROM Trips
WHERE passenger_count <= 2
'''

#Reading the query result
avg = pd.read_sql(query, conn)['avg_distance'].values[0]

fig = px.histogram(temp_df, x='trip_distance', y='trip_distance', title='Max 2 Passengers Trip Distance Distribution', nbins=70)
fig.add_vline(x=avg, line_dash = 'dash', line_color = 'firebrick',annotation_text=f"Mean: {avg}")
py.plot(fig)
