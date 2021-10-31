
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.offline as py
import plotly.graph_objects as go

conn = sqlite3.connect("Trips_and_vendors.db")


query='''
SELECT SUM(case when tip_amount>0 then 1 else 0 end) as n_tips, strftime('%Y-%m-%d', pickup_datetime) as date
FROM Trips
WHERE date BETWEEN DATE(   (SELECT strftime('%Y-%m-%d', pickup_datetime) as date
                           FROM Trips
                           ORDER BY date desc
                           LIMIT 1),  "-3 months") 
                           
                        and
                        
                        (SELECT strftime('%Y-%m-%d', pickup_datetime) as date
                        FROM Trips
                        ORDER BY date desc
                        LIMIT 1) 
GROUP BY date
ORDER BY date

'''

#Reading the query result into a dataframe
temp_df = pd.read_sql(query, conn)

x=temp_df['date']
y=temp_df['n_tips']


fig = go.Figure(data=go.Scatter(x=x, y=y))

y=temp_df['n_tips'].rolling(5).mean()

fig.add_trace(go.Scatter(x=x, y=y, name='M.A. 5 days'))
py.plot(fig)