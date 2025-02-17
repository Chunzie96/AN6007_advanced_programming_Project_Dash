#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 20:07:20 2025

@author: chunhan
"""

from dash import html, dcc, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px
import json  # To load GeoJSON data
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable

dash.register_page(__name__, path="/map")  # Register the map page

# Load the electricity data
df = pd.read_csv("final.csv")

# Load the updated GeoJSON file
with open("singapore_regions.geojson", "r") as f:
    singapore_geojson = json.load(f)

# Get unique dwelling types for the dropdown
dwelling_types = df["dwelling_type"].unique()

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Singapore Electricity Usage by Region", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id="dwelling-type-dropdown",
                options=[{"label": dt, "value": dt} for dt in dwelling_types],
                value=dwelling_types[0],  # Default selection
                placeholder="Select a Dwelling Type",
                className="mb-4"
            ),
            width=6
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="singapore-map"),  # Placeholder for the map
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.H4("Filtered Data Table", className="text-center text-secondary mt-4 mb-2"),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            DataTable(
                id="filtered-data-table",
                columns=[
                    {"name": "Region", "id": "Region"},
                    {"name": "Average kWh per Account", "id": "kwh_per_acc"}
                ],
                style_table={"overflowX": "auto"},  # Allow horizontal scrolling
                style_header={
                    "backgroundColor": "rgb(230, 230, 230)",
                    "fontWeight": "bold"
                },
                style_cell={
                    "textAlign": "center",
                    "padding": "10px"
                },
                page_size=10  # Display 10 rows per page
            ),
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
        ),
        dbc.Col(
            dbc.Button("Go to Trend Analysis Page", href="/trend", color="success", className="me-2"),
            width="auto"
        )
    ], className="d-flex justify-content-center mt-4")
], fluid=True)

# Callback to render the map and update the table based on the selected dwelling type
@callback(
    [Output("singapore-map", "figure"),
     Output("filtered-data-table", "data")],
    Input("dwelling-type-dropdown", "value")
)
def update_map_and_table(selected_dwelling_type):
    # Filter the data by the selected dwelling type
    filtered_data = df[df["dwelling_type"] == selected_dwelling_type]

    # Aggregate electricity data by region
    region_summary = filtered_data.groupby("Region")["kwh_per_acc"].mean().reset_index()

    # Handle empty data
    if region_summary.empty:
        return px.choropleth_mapbox(
            pd.DataFrame({"Region": [], "kwh_per_acc": []}),
            geojson=singapore_geojson,
            locations="Region",
            featureidkey="properties.Region",
            color="kwh_per_acc",
            mapbox_style="carto-positron",
            center={"lat": 1.3521, "lon": 103.8198},
            zoom=10
        ), []

    # Create a choropleth map
    fig = px.choropleth_mapbox(
        region_summary,
        geojson=singapore_geojson,
        locations="Region",  # Column in the data that matches GeoJSON "properties.Region"
        featureidkey="properties.Region",  # Key in GeoJSON that matches the data
        color="kwh_per_acc",  # Column to color by
        color_continuous_scale="Viridis",  # Color scale
        opacity=0.7,
        title=f"Average Electricity Usage by Region for {selected_dwelling_type}",
        mapbox_style="carto-positron",  # Map style
        center={"lat": 1.3521, "lon": 103.8198},  # Center the map on Singapore
        zoom=10,  # Zoom level
        hover_name="Region",  # Show region name on hover
        hover_data={"kwh_per_acc": ":.2f"}  # Show electricity usage on hover
    )

    # Update layout for better visuals
    fig.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    coloraxis_colorbar=dict(
        title="kWh per Account",
        tickformat=".2f",
        thickness=15,
        len=0.9,
        bgcolor='rgba(255,255,255,0.8)',
        ),
    mapbox=dict(
        zoom=10,
        center={"lat": 1.3521, "lon": 103.8198}
        )
    )

    # Prepare data for the table
    table_data = region_summary.to_dict("records")

    return fig, table_data