import pandas as pd
import sqlite3
import plotly.express as px
import plotly.offline as py




conn = sqlite3.connect("Trips_and_vendors.db")

#Query to get the total amount of money raised p/ Vendor, ordered by money raised
query = '''SELECT vendor_id, SUM(total_amount) as total_money_raised
FROM Trips
GROUP BY vendor_id
ORDER BY total_money_raised desc
LIMIT 3
'''

#Reading the query result into a dataframe
temp_df = pd.read_sql(query, conn)

fig = px.bar(temp_df, x='vendor_id', y='total_money_raised', title='3 Biggest Money Raising Vendors ')
py.plot(fig)