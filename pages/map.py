#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:13:32 2025

@author: chunhan
"""
# Import all necessary libraries
import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json

dash.register_page(__name__, path='/map')

# Load the electricity data
df = pd.read_csv("final.csv")
to_delete = ['East Region', 'North Region', 'Central Region', 'West Region', 'North East Region', 'Downtown']
df = df[df['Area'].isin(to_delete) == False]

# Calculate the average consumption in specific area for every dwelling type
df_agg = df.groupby(['Area', 'dwelling_type'])['kwh_per_acc'].mean().reset_index()

# Load the geojson
with open("MasterPlan2019PlanningAreaBoundaryNoSea.geojson", 'r') as f:
    singapore_geojson = json.load(f)

# Create a dictionary of areas: longlat based on the geojson
singapore_coordinates = {}
for feature in singapore_geojson["features"]:
    description = feature["properties"]["Description"]
    index1 = description.find("<td>")
    index2 = description.find("</td>")
    area = description[(index1+4):index2].title()
    coordinates = feature["geometry"]["coordinates"][0][0]
    singapore_coordinates[area] = {"lon": coordinates[0], "lat": coordinates[1]}

# Create lat and long columns in df
df_agg["lat"] = df_agg["Area"].map(lambda x: singapore_coordinates[x]["lat"])
df_agg["lon"] = df_agg["Area"].map(lambda x: singapore_coordinates[x]["lon"])

# Layout with 1 dropdown and 1 map
'''
Map is chosen to identify which area is consuming more than the others by dwelling type.
'''

layout = html.Div([
    dbc.Container([
        html.H1("Electricity Consumption Heatmap", className="text-center my-4"),

        dbc.Row([
            dbc.Col([
                html.Label("Select Dwelling Type"),
                dcc.Dropdown(options=[each for each in df["dwelling_type"].unique()], value = df['dwelling_type'].iloc[1], id='dwelling-dropdown')
            ], width=4)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="heatmap")
            ])
        ])
    ])
])

# Callback
@callback(
    Output("heatmap", "figure"),
    [Input("dwelling-dropdown", "value")]
)

# Update the map
def update_map(selected_dwelling):

    # Filter data based on selection
    df_filtered = df_agg[df_agg["dwelling_type"] == selected_dwelling]

    # Create the figure
    fig = px.scatter_mapbox(
        df_filtered,
        lat="lat",
        lon="lon",
        size="kwh_per_acc",
        color="kwh_per_acc",
        hover_name="Area",
        hover_data={"kwh_per_acc": ":.2f", "lat": False, "lon": False},
        center={"lat": 1.3521, "lon": 103.8198},
        zoom=10,
        mapbox_style="carto-positron",
        title=f"Electricity Consumption by Area - {selected_dwelling}"
    )

    # Update graph layout
    fig.update_layout(
        title={"font":{"size":16},"x":0.5},
        xaxis={"title":{"font":{"size":14}},"tickfont":{"size":12}},
        yaxis={"title":{"font":{"size":14}},"tickfont":{"size":12}},
        font={"color":"black"},
        height=700
        )

    return fig