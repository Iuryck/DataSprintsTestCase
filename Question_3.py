import pandas as pd
import sqlite3
import plotly.express as px
import plotly.offline as py

conn = sqlite3.connect("Trips_and_vendors.db")


query='''SELECT payment_type, strftime('%m', pickup_datetime) as month
FROM Trips
WHERE lower(payment_type) like "%cash%"
ORDER BY month asc
'''

#Reading the query result into a dataframe
temp_df = pd.read_sql(query, conn)

#Making the column into 1 values because the histogram needs numbers, can be interpreted as boolean for Cash 
temp_df['payment_type'] = 1

fig = px.histogram(temp_df, x='month', y='payment_type', title='Trips paid with Cash Distribution by Month ')
py.plot(fig)