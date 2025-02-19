import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json

dash.register_page(__name__, path='/map')

# Load the electricity data
df = pd.read_csv("final.csv")

# Calculate average consumption by area for each dwelling type
df_agg = df.groupby(['Area', 'dwelling_type'])['kwh_per_acc'].mean().reset_index()

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

# Simple GeoJSON for Singapore regions (you should replace this with actual detailed GeoJSON)
singapore_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": area},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [singapore_coordinates[area]['lon'] - 0.02, singapore_coordinates[area]['lat'] - 0.02],
                    [singapore_coordinates[area]['lon'] + 0.02, singapore_coordinates[area]['lat'] - 0.02],
                    [singapore_coordinates[area]['lon'] + 0.02, singapore_coordinates[area]['lat'] + 0.02],
                    [singapore_coordinates[area]['lon'] - 0.02, singapore_coordinates[area]['lat'] + 0.02],
                    [singapore_coordinates[area]['lon'] - 0.02, singapore_coordinates[area]['lat'] - 0.02]
                ]]
            }
        } for area in singapore_coordinates
    ]
}

# Update the layout (remains the same)
layout = html.Div([
    dbc.Container([
        html.H1("Electricity Consumption Heatmap", className="text-center my-4"),

        dbc.Row([
            dbc.Col([
                html.Label("Select Dwelling Type"),
                dcc.Dropdown(options=[each for each in df["dwelling_type"].unique()],
                           value=df['dwelling_type'].iloc[1],
                           id='dwelling-dropdown')
            ], width=4)
        ], className="mb-4", justify="center"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id="heatmap")
            ], width=12)
        ])
    ])
])

@callback(
    Output('heatmap', 'figure'),
    [Input('dwelling-dropdown', 'value')]
)
def update_heatmap(selected_dwelling):
    # Filter data based on selection
    filtered_df = df_agg[df_agg['dwelling_type'] == selected_dwelling]

    # Create the choropleth map
    fig = px.choropleth_mapbox(
        filtered_df,
        geojson=singapore_geojson,
        locations='Area',
        featureidkey='properties.name',
        color='kwh_per_acc',
        center={"lat": 1.3521, "lon": 103.8198},
        zoom=10.5,
        mapbox_style="carto-positron",
        color_continuous_scale="Viridis",
        opacity=0.7,
        labels={'kwh_per_acc': 'kWh per Account'},
        title=f"Electricity Consumption by Area - {selected_dwelling}"
    )

    # Customize layout
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        height=700,
        coloraxis_colorbar=dict(
            title="kWh per Account",
            titleside="right",
            thickness=20,
            len=0.9,
            outlinewidth=1
        )
    )

    return fig