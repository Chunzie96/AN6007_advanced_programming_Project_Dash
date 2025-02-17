#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:13:32 2025

@author: chunhan
"""

from dash import html, dcc, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc  # Import Bootstrap components

dash.register_page(__name__, path="/trend")  # Register the trend analysis page

# Load the data
df = pd.read_csv("final.csv")

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Electricity Data Trend Analysis", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.P("Select a category to analyze the electricity data trend:", className="text-center"), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dcc.RadioItems(
                options=[
                    {"label": "Yearly Trend", "value": "year"},
                    {"label": "Monthly Trend", "value": "month"}
                ],
                value="year",  # Default selection
                id="trend-radio-item",
                className="radio-group"  # Add a custom class for styling
            ),
            width={"size": 6, "offset": 3},  # Center the radio buttons
            className="d-flex justify-content-center mb-4"
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure={}, id="trend-graph"),  # Placeholder for the graph
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Button("Go to Home Page", href="/", color="primary", className="me-2"),
            width="auto"
        ),
        dbc.Col(
            dbc.Button("Go to Data Page", href="/data", color="secondary", className="me-2"),
            width="auto"
        ),
        dbc.Col(
            dbc.Button("Go to Graph Page", href="/graph", color="info", className="me-2"),
            width="auto"
        )
    ], className="d-flex justify-content-center mt-4")
], fluid=True)  # Use fluid=True for a responsive layout

# Callback to update the graph based on user selection
@callback(
    Output("trend-graph", "figure"),
    Input("trend-radio-item", "value")
)
def update_trend_graph(selected_trend):
    # Group data by the selected trend (year or month) and calculate the mean
    agg_data = df.groupby(selected_trend)['kwh_per_acc'].mean().reset_index()

    # Create a line chart to show the trend
    fig = px.line(
        agg_data,
        x=selected_trend,
        y="kwh_per_acc",
        title=f"Electricity Data Trend by {selected_trend.capitalize()}",
        labels={selected_trend: selected_trend.capitalize(), "kwh_per_acc": "kWh per Account"},
        template="plotly_dark",  # Use a dark theme for the graph
        markers=True  # Add markers to the line chart
    )
    fig.update_layout(
        title=dict(font=dict(size=20), x=0.5),  # Center the title
        xaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=16), tickfont=dict(size=12)),
        plot_bgcolor="#1e2130",  # Background color for the plot
        paper_bgcolor="#1e2130",  # Background color for the graph container
        font=dict(color="white")  # Font color
    )
    return fig