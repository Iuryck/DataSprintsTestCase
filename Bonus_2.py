import pandas as pd
import sqlite3
from colorcet import fire, kbc
import datashader as ds
import datashader.transfer_functions as tf
from datashader.utils import lnglat_to_meters as webm
from functools import partial
from datashader.utils import export_image
from datashader.colors import colormap_select, Greys9
from IPython.core.display import HTML, display
import plotly.express as px
import plotly.offline as py
from PIL import Image


conn = sqlite3.connect("Trips_and_vendors.db")


#Query to get all the coordinates we need for the year 2010
query='''SELECT pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude, strftime("%Y",pickup_datetime) as year
FROM Trips
WHERE year = "2010"
'''

#Reading the query result into a dataframe
temp_df = pd.read_sql(query, conn)


#Creating a new dataframe where we will store all coordinates
newdf = pd.DataFrame()
newdf['latitude'] = temp_df['pickup_latitude']
newdf['longitude'] = temp_df['pickup_longitude']

#Categorizing coordinates
newdf['type'] = 'pickup'


#Dataframe for all dropoffs
drop_df=pd.DataFrame()
drop_df['latitude'] = temp_df['dropoff_latitude']
drop_df['longitude'] = temp_df['dropoff_longitude']
drop_df['type'] = 'dropoff'

#Changing the index, since we cant append Series objects with equal index
drop_df.index = [c for c in range(newdf.shape[0], newdf.shape[0]+drop_df.shape[0])]

#Appending the dropoff dataframe to the pickup dataframe
newdf = newdf.append(drop_df)

del drop_df

#Setting a categorical column for ou categories
newdf['categorical'] = pd.Categorical(newdf['type'])

#Filtering just in case
types=['pickup','dropoff']
newdf = newdf[newdf['type'].isin(types)]

#Changing the type of coordinates to suit the needs of Datashader
lon = newdf['longitude']
lat = newdf['latitude']
newdf.loc[:, 'easting'], newdf.loc[:, 'northing'] = webm(lon,lat)

#image resolution
plot_width = int(1000)
plot_height = int(1000)

#Background color
background = "black"


export = partial(export_image, background = background, export_path="export")
cm = partial(colormap_select, reverse=(background!="black"))

display(HTML("<style>.container { width:100% !important; }</style>"))

#Setting the borders of the map view. We have some outliers in our dataset that go far from NYC, which we don't want to affect the map view, so we use quantiles.
y_range_min = lat.quantile(0.02)-0.10
y_range_max = lat.quantile(0.98)+0.10
x_range_min = lon.quantile(0.02)-0.10
x_range_max = lon.quantile(0.98)+0.10

#Passing the borders to the mapview
sw = webm(x_range_min,y_range_min)
ne = webm(x_range_max,y_range_max)
SF = zip(sw, ne)

#Color mapping for our categories, very important
color_key = {'dropoff': 'fuchsia', 'pickup': 'aqua'}


cvs = ds.Canvas(plot_width, plot_height, *SF)
agg = cvs.points(newdf, 'easting', 'northing',agg=ds.count_cat('categorical'))

export(tf.shade(agg, color_key =color_key, how='eq_hist'),"sf_biz_grey")
img = Image.open('export\sf_biz_grey.png')
img.show()


    