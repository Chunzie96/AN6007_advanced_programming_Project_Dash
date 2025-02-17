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

# Initialize the app with a Bootstrap theme
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])

# Navbar
navbar = dbc.NavbarSimple(
    brand="Electricity Data Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink("Regional Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Trend Analysis", href="/trend"))
    ]
)

# App layout
app.layout = html.Div([
    navbar,  # Add the navbar
    html.Div(dash.page_container, className="p-4")  # Add padding around the page content
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)