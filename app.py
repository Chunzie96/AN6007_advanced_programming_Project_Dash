# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 14:31:04 2024

@author: Controls and Callbacks
https://dash.plotly.com/tutorial
"""

# Import packages

import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

# Initialize app with use_pages and a Bootstrap theme
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY])

# Navigation bar setup
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Regional Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Trend Analysis", href="/trend"))
    ],
    brand="Electricity Dashboard",
    brand_href="/",
    color="light",
    dark=False
)

# App layout
app.layout = html.Div([
    navbar, 
    html.Div(dash.page_container, className="p-4")  
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)