# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 14:31:04 2024

@author: Controls and Callbacks
https://dash.plotly.com/tutorial
"""

# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv("final.csv")

# Initialize the app
app = Dash(__name__, use_pages=True)

# App layout
app.layout = html.Div([
    dash.page_container,  # This renders the content of the current page
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.RadioItems(options=["year", "month", "region"], value = 'year', id= 'controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='controls-and-graph'),
])

# Add controls to build the interaction


@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value")
)
def update_graph(col_chosen):
    agg_data = df.groupby(col_chosen)['kwh_per_acc'].mean().reset_index()
    # fig = px.histogram(df, x = col_chosen, y = "kwh_per_acc", histfunc="avg")
    fig = px.line(agg_data, x=col_chosen, y="kwh_per_acc")
    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
