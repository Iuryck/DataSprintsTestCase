import pandas as pd
import sqlite3
import dateutil.parser


#Creating empty dataframe to populate with the Trips data
trips_df = pd.DataFrame()

#Iterating through each year of the data files
for year in range(2009,2013):
    
    #Reading json file from the iterating year into a temporary dataframe
    df = pd.read_json(f'data-sample_data-nyctaxi-trips-{year}-json_corrigido.json', lines=True)
    
    #If trips_df is still empty, passes the temporary dataframe to the trips_df
    if trips_df.empty:
        trips_df = df
    
    #Else, appends the temporary dataframe to the end of the trips_df
    else:
        trips_df = trips_df.append(df)
    

#Parsing the ISO datetime format and getting the datetime object
datetimes = [dateutil.parser.isoparse(c) for c in trips_df['pickup_datetime']]

#Changing datetime format to a more conventional one that SQLite can read
datetimes = [c.strftime('%Y-%m-%d %H:%M:%S') for c in datetimes]
trips_df['pickup_datetime'] = datetimes

#Parsing the ISO datetime format and getting the datetime object
datetimes = [dateutil.parser.isoparse(c) for c in trips_df['dropoff_datetime']]

#Changing datetime format to a more conventional one that SQLite can read
datetimes = [c.strftime('%Y-%m-%d %H:%M:%S') for c in datetimes]
trips_df['dropoff_datetime'] = datetimes

trips_df = trips_df.drop('rate_code',axis=1)

#Creates new local database if one doesn't already exist
conn = sqlite3.connect("Trips_and_vendors.db")


#Storing dataframe in the database as table, removing tables if they already exist, for pushing changes.

try: trips_df.to_sql('Trips', conn)
except Exception as e:
    
    if "Table 'Trips' already exists." in str(e):
        conn.cursor().execute('DROP TABLE Trips')
        trips_df.to_sql('Trips', conn)
        
    else: raise e

