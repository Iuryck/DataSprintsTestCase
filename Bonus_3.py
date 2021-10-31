import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import json
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
from collections import deque




class Transaction:
    
    def __init__(self):
        pass
    
    def connect(self):
        """Function to connect to local database and pull the data necessary for the data streaming task
        """
        query = '''SELECT vendor_id, total_amount as total_money_raised, dropoff_datetime
                    FROM Trips
                    ORDER BY dropoff_datetime
                    
                '''
        
        try: self.conn.cursor()
        except: self.conn = sqlite3.connect("Trips_and_vendors.db")
        
        #Reading the query result into a dataframe
        self.df = pd.read_sql(query, self.conn)
        self.row = 0
        
        
        

    def serialize(self):
        """Function to mock retrieval of a row from a stream of data

        :raises AttributeError: Error for when the Transaction class doesn't have attributes, meaning the connect function 
        was not used.
        :return: A row of data from the class dataframe in JSON format, row by row as a stream.
        :rtype: json string
        """        
        try:
            #restarts from row 0 if we reach end of dataframe
            if self.row == self.df.shape[0]: self.row = 0 

            #Gets a row slice of dataframe and transforms into json format
            data = self.df.iloc[self.row].to_json()
            self.row = self.row+1

            return data
        except AttributeError: raise AttributeError('No data to retrieve, please run the connect function first')

#Deques are lists that have a maximum length, and as soon as they reach that length, they start popping out the first entries to it.
#Perfect for our purposes
X = deque(maxlen=20)
Y = deque(maxlen=20)

#Total money that will be summed up over time as the data stream comes
total_money = 0

#starting stream
stream = Transaction()
stream.connect()



#Creating the Dash app for our live data plot
app = dash.Dash(__name__)

app.layout= html.Div([
    
    dcc.Graph(id='live-graph', animate=True),
    
    #interval of 1 second -> 1000 miliseconds
    dcc.Interval(id='graph-update', interval=1000, n_intervals=0)
    
    
])


#Callback function that updates our graph in the given interval
@app.callback(Output('live-graph','figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph(*args):
    
    #Now, there probably is a better way to reference these variables, but just to make the plot work, let's 
    #leave it like this
    global X
    global Y
    global total_money 
    
    #Reading data from the stream
    data = stream.serialize()
    a_json = json.loads(data)
    
    #Summing up the money collected by taxi trips
    total_money = total_money + a_json['total_money_raised']
    
    #Appending our data to the deques
    Y.append(total_money)
    X.append(a_json['dropoff_datetime'])
    
    #Line plot for our data
    data=go.Scatter(x = list(X),
                y=list(Y),
                name='scatter',
                mode='lines+markers'
               )
    
    #Returns updated attributes for our figure/plot
    return {'data':[data],
            'layout': go.Layout(yaxis = dict(range=[min(Y), max(Y)]),
                               xaxis = dict(range=[X[0], X[-1]]))}
#Running Dash app
app.run_server(debug=False)