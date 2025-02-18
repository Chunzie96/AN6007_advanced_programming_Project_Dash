#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 20:07:20 2025

@author: chunhan
"""
import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable

dash.register_page(__name__, path="/map")  # Register the map page

# Load the electricity data
df = pd.read_csv("final.csv")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define Singapore area coordinates
singapore_coordinates = {
    'Ang Mo Kio': {'lat': 1.3691, 'lon': 103.8454},
    'Bedok': {'lat': 1.3236, 'lon': 103.9273},
    'Bishan': {'lat': 1.3526, 'lon': 103.8352},
    'Bukit Batok': {'lat': 1.3590, 'lon': 103.7637},
    'Bukit Merah': {'lat': 1.2819, 'lon': 103.8239},
    'Bukit Panjang': {'lat': 1.3774, 'lon': 103.7719},
    'Bukit Timah': {'lat': 1.3294, 'lon': 103.8021},
    'Central Area': {'lat': 1.2789, 'lon': 103.8536},
    'Choa Chu Kang': {'lat': 1.3840, 'lon': 103.7470},
    'Clementi': {'lat': 1.3162, 'lon': 103.7649},
    'Geylang': {'lat': 1.3201, 'lon': 103.8918},
    'Hougang': {'lat': 1.3612, 'lon': 103.8863},
    'Jurong East': {'lat': 1.3329, 'lon': 103.7436},
    'Jurong West': {'lat': 1.3404, 'lon': 103.7090},
    'Kallang': {'lat': 1.3100, 'lon': 103.8651},
    'Marine Parade': {'lat': 1.3020, 'lon': 103.8971},
    'Pasir Ris': {'lat': 1.3721, 'lon': 103.9474},
    'Punggol': {'lat': 1.3984, 'lon': 103.9072},
    'Queenstown': {'lat': 1.2942, 'lon': 103.7861},
    'Sembawang': {'lat': 1.4491, 'lon': 103.8185},
    'Sengkang': {'lat': 1.3868, 'lon': 103.8914},
    'Serangoon': {'lat': 1.3554, 'lon': 103.8679},
    'Tampines': {'lat': 1.3496, 'lon': 103.9568},
    'Toa Payoh': {'lat': 1.3343, 'lon': 103.8563},
    'Woodlands': {'lat': 1.4382, 'lon': 103.7890},
    'Yishun': {'lat': 1.4304, 'lon': 103.8354}
}

# Process the dataframe to add coordinates
def add_coordinates(df):
    # Create new columns for latitude and longitude
    df['latitude'] = df['Area'].map(lambda x: singapore_coordinates.get(x, {}).get('lat'))
    df['longitude'] = df['Area'].map(lambda x: singapore_coordinates.get(x, {}).get('lon'))
    return df

# Assuming df is your original dataframe
# df = pd.read_csv('your_data.csv')
df = add_coordinates(df)

layout = html.Div([
    dbc.Container([
        html.H1("Singapore Electricity Consumption Heatmap",
                className="text-center my-4"),

        # Dropdown for dwelling type
        dbc.Row([
            dbc.Col([
                html.Label("Select Dwelling Type"),
                dcc.Dropdown(
                    id='dwelling-dropdown',
                    options=[{'label': i, 'value': i}
                            for i in df['dwelling_type'].unique()],
                    value=df['dwelling_type'].iloc[0],
                    className="mb-4"
                )
            ], width=6)
        ], justify="center"),

        # Heatmap
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='singapore-heatmap')
            ], width=12)
        ])
    ])
])

@callback(
    Output('singapore-heatmap', 'figure'),
    [Input('dwelling-dropdown', 'value')]
)
def update_heatmap(selected_dwelling):
    # Filter data based on dwelling type
    filtered_df = df[df['dwelling_type'] == selected_dwelling]

    # Create the heatmap
    fig = px.density_mapbox(
        filtered_df,
        lat='latitude',
        lon='longitude',
        z='kwh_per_acc',
        radius=10,
        center=dict(lat=1.3521, lon=103.8198),  # Singapore's center
        zoom=11,
        mapbox_style="carto-positron",
        title=f"Electricity Consumption Heatmap - {selected_dwelling}",
        opacity=0.7,
        color_continuous_scale="Thermal",
        range_color=[100, 200],
        hover_data=['Area', 'kwh_per_acc']  # Show area name and value in hover
    )

    # Update layout
    fig.update_layout(
        mapbox=dict(
            bounds=dict(
                west=103.6,
                east=104.0,
                south=1.2,
                north=1.5
            )
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=700,
        coloraxis_colorbar=dict(
            title="kWh per Account",
            titleside="right",
            thickness=20,
            len=0.9,
            outlinewidth=1
        )
    )

    fig.update_traces(
        colorbar=dict(
            tickmode='linear',
            tick0=filtered_df['kwh_per_acc'].min(),
            dtick=(filtered_df['kwh_per_acc'].max() - filtered_df['kwh_per_acc'].min()) / 10
        )
    )

    return fig