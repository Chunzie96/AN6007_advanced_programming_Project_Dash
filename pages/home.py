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
import plotly.graph_objects as go
import dash_bootstrap_components as dbc  
from datetime import datetime, timedelta

# Register the home page
dash.register_page(__name__, path="/")  

# Load the data
df = pd.read_csv("final.csv")

# Layout with 3 dropdowns and 1 graph
'''
The graph shows monthly electricity consumption for the past 12 months. However, since 
dataset does not contain a MeterID, we use the combination of Region-Area-Dwelling_type 
as the unique identifier. 
- Bar graph is chosen to represent the monthly variations in electricity consumption, 
identifying certain seasonal patterns.
- Benchmark against similar dwelling types in the region can become a comparison for the user
to know if their energy consumption is above or below the standard.
If the consumption is consistently above average, user can explore ways to serve their energy.
'''
layout = html.Div([
    dbc.Container([
        html.H1("Electricity Consumption", className="text-center my-4"),
        
        dbc.Row([
            dbc.Col([
                html.Label("Select Region"),
                dcc.Dropdown(options=[each for each in df["Region"].unique()], value = df['Region'].iloc[1], id='region-dropdown')
            ], width=4),
            dbc.Col([
                html.Label("Select Area"),
                dcc.Dropdown(id='area-dropdown')
            ], width=4),
            dbc.Col([
                html.Label("Select Dwelling Type"),
                dcc.Dropdown(options=[each for each in df["dwelling_type"].unique()], value = df['dwelling_type'].iloc[1], id='dwelling-dropdown')
            ], width=4)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id="electricity-graph")
            ])
        ])
    ])
])

# Add callback for area options to ensure only areas within selected region are shown
@callback(
    Output('area-dropdown', 'options'),
    Output('area-dropdown', 'value'),
    Input('region-dropdown', 'value')
)
def update_area_dropdown(selected_region):
    areas = df[df["Region"] == selected_region]["Area"].unique()
    return [{'label': area, 'value': area} for area in areas], areas[0]

# Callback
@callback(
    Output('electricity-graph', 'figure'),
    [Input('region-dropdown', 'value'),
     Input('area-dropdown', 'value'),
     Input('dwelling-dropdown', 'value')]
)

# Update the graph function
def update_graph(selected_region, selected_area, selected_dwelling):
    # Create a date column in df for easy sorting
    df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))

    # Filter the df based on selections, choose only the data from past 12 months 
    df_filtered = df[
        (df["Region"] == selected_region) &
        (df["Area"] == selected_area) &
        (df["dwelling_type"] == selected_dwelling)
    ]
    displayed_data = df_filtered.sort_values("date").tail(12)

    # Filter df for the regional average line, similarly, only take data from past 12 months
    regional_avg = df[
        (df["Region"] == selected_region) &
        (df["dwelling_type"] == selected_dwelling)
    ].groupby("date")["kwh_per_acc"].mean().reset_index()
    regional_avg = regional_avg.tail(12)

    # Initialize the figure, add bars and lines
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=displayed_data["date"],
        y=displayed_data["kwh_per_acc"],
        name="kWh",
        marker_color='rgb(255, 164, 91)'
    ))

    fig.add_trace(go.Scatter(
        x=regional_avg["date"],
        y=regional_avg["kwh_per_acc"],
        name="Regional Average",
        line=dict(color='rgb(144, 238, 144)', width=2) 
    ))

    # Customize the xaxis and yaxis, as well as the plot style
    fig.update_layout(
        title="Electricity Consumption",
        xaxis=dict(
            title="Month",
            tickformat='%b %y',
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)"
        ),
        yaxis=dict(
            title="kWh",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.1)",
            range=[0, max(displayed_data["kwh_per_acc"].max(),
                         regional_avg["kwh_per_acc"].max()*1.2)]
        ),
        plot_bgcolor="white",
        hovermode="x unified",
        barmode="overlay",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Add annotation
    for i in range(len(displayed_data)):
        fig.add_annotation(
            x=displayed_data["date"].iloc[i],
            y=displayed_data["kwh_per_acc"].iloc[i],
            text=str(round(displayed_data["kwh_per_acc"].iloc[i])),
            showarrow=False,
            yshift=10
        )

    return fig