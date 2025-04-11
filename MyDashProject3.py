import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_excel("Large_Sales_Data.xlsx")
df['Date'] = pd.to_datetime(df['Date'])

df['Month'] = df['Date'].dt.to_period('M').astype(str)
df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
df['Day'] = df['Date'].dt.date

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Summary Dashboard"),

    dcc.Tabs(id="tabs", value= 'month', children=[
        dcc.Tab(label= 'Month-wise Summary', value='month'),
        dcc.Tab(label = 'Quarter-wise Summary', value='quarter'),
        dcc.Tab(label='Day-wise Summary', value='day'),
        dcc.Tab(label='City-wise Summary', value='city'),
        dcc.Tab(label='Product-wise Summary', value='product'),
    ]
    ),
    dcc.Graph(id='summary-graph')
])

@app.callback(
    Output('summary-graph', 'figure'),
    Input('tabs', 'value')
)
def update_graph(tab):
    if tab == 'month':
        summary = df.groupby('Month')['Sales'].sum().reset_index()
        return px.bar(summary, x='Month', y='Sales', title='Month-wise Sales')
    
    elif tab == 'quarter':
        summary = df.groupby('Quarter')['Sales'].sum().reset_index()
        return px.bar(summary, x='Quarter', y='Sales', title = 'Quarter-wise Sales')
    elif tab == 'day':
        summary = df.groupby('Day')['Sales'].sum().reset_index()
        return px.line(summary, x='Day', y='Sales', title = 'Day-wise Growth')
    elif tab == 'city':
        summary = df.groupby('City')['Sales'].sum().reset_index()
        return px.bar(summary, x='City', y='Sales', title='City-wise Sales')
    elif tab == 'product':
        summary = df.groupby('Product')['Sales'].sum().reset_index()
        return px.pie(summary, names = 'Product', values='Sales', title= 'Product-wise Sales')
    return{}
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=10000)