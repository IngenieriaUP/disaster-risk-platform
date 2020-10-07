# -*- coding: utf-8 -*-
import dash
import json
import pandas as pd
import geopandas as gpd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

df_eqs = gpd.read_file("data_geoserver_uni/sismos.geojson")
df_eqs["date"] = pd.to_datetime(df_eqs["fecha"])
df_eqs["year"] = df_eqs["date"].dt.year
df_eqs = df_eqs.sort_values(by="date")

with open("data_geoserver_uni/tsunamis_crs4326.geojson", "rb") as f:
    tsunamis = json.load(f)

df_tsu = gpd.read_file("data_geoserver_uni/tsunamis_crs4326.geojson")

with open("data_geoserver_uni/tsunamis.geojson", "rb") as f:
    tsunamis = json.load(f)

px.set_mapbox_access_token(open(".mapbox_token").read())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children="Disaster Risk Platform"),
    html.Div(children="""
        DRP: A interactive data analytics platform for Disaster Risk Topics
    """),
    dcc.Graph(
        id="earthquake-scattermap",
        figure=px.scatter_mapbox(
            df_eqs,
            lat="lati",
            lon="long",
            color="mag",
            size="mag",
            animation_frame="year",
            title="Earthquake location and magnitude by year")
    ),
    dcc.Graph(
        id="earthquake-densitymap",
        figure=go.Figure(
            data=go.Densitymapbox(
                lat=df_eqs.lati,
                lon=df_eqs.long,
                z=df_eqs.mag,
                radius=10
            ),
            layout=go.Layout(
                title=go.layout.Title(text="Earthquake density map"),
                mapbox_style="stamen-terrain"
            )
        )
    ),
    dcc.Graph(
        id="tsunami-map",
        figure=go.Figure(
            data=go.Choroplethmapbox(
                geojson=tsunamis,
                locations=df_tsu.id,
                z=df_tsu.shape_area),
            layout=go.Layout(
                title=go.layout.Title(text="Tsunamis inundation risk in Lima"),
                mapbox_style="carto-positron")
        )
    )
], style={'columnCount': 2})

if __name__ == '__main__':
    app.run_server(debug=True)
