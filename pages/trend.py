#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:13:32 2025

@author: chunhan
"""
# Import all necessary libraries
import dash
from dash import html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc  

# Register the trend analysis page
dash.register_page(__name__, path="/trend")  

# Load the data
df = pd.read_csv("final.csv")

# Layout for two option buttons and a graph
'''
The graph shows overall electricity consumption trend in Singapore over the 
years. Since it is a time-series, line graph is used. Aside from yearly trend,
a monthly trend graph is also included for identification of seasonal variations.
'''
layout = html.Div([
    dbc.Container([
        html.H1("Electricity Trend Analysis", className="text-center my-4"),
        html.P("Select a category:", className="text-center"),

        dbc.Row([
            dbc.Col([
                dcc.RadioItems(options=["year", "month"],value='year', id="trend-radio-item", className="radio-group")
            ], width={"size": 6, "offset": 3}, className="d-flex justify-content-center mb-4")
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(figure={}, id="trend-graph")
            ])
        ])
    ])
])

# Callback 
@callback(
    Output("trend-graph", "figure"),
    Input("trend-radio-item", "value")
)

# Update the graph
def update_trend_graph(selected_trend):
    # Filter the data by year/month
    df_filtered = df.groupby(selected_trend)["kwh_per_acc"].mean().reset_index()

    # Create the graph 
    fig = px.line(
        df_filtered,
        x=selected_trend,
        y="kwh_per_acc",
        title=f"Electricity Data Trend by {selected_trend.capitalize()}",
        labels={selected_trend: selected_trend, "kwh_per_acc": "kWh per Account"},
        template="simple_white",
        markers=True 
    )
    fig.update_layout(
        title=dict(font=dict(size=20), x=0.5),
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),  
        font=dict(color="black") 
    )
    return fig