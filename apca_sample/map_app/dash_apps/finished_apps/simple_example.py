import pandas as pd
import geopandas as gpd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample')

# DATA WRANGLING STARTS

# Import geojson file with california counties
ca_counties = json.load(open('/Users/hillarykhan/Desktop/apca-api-sample/apca_sample/map_app/data/ca-county-boundaries.geojson', 'r'))

for feature in ca_counties['features']:
    feature['id'] = feature['properties']['geoid']
# Confirm id key added
print("After: ", ca_counties['features'][0].keys())

# Import unemployment data
df = pd.read_csv('/Users/hillarykhan/Desktop/apca-api-sample/apca_sample/map_app/data/fips-unemp-16.csv')
# Confirm csv read in correctly
print("csv loaded: ", df.head())

df['fips'] = df['fips'].apply(lambda x: str(x).zfill(5))
print("df with adjusted fips: ", df.head())

df['year'] = 2016
print("year added to df: ", df.head())

# Create dataframe from geojson file
geo_df = gpd.GeoDataFrame.from_features(
    ca_counties["features"])
print("geo_df: ", geo_df.head())

# Inner join our tables to retain data on California counties only
df = pd.merge(df, geo_df, left_on='fips', right_on='geoid')
# DATA WRANGLING ENDS

# APP LAYOUT STARTS
app.layout = html.Div([
    html.H1("Interactive Choropleth by Hillary Khan", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
    options=[
        {"label": "2001", "value": 2001},
        {"label": "2002", "value": 2002},
        {"label": "2003", "value": 2003},
        {"label": "2004", "value": 2004},
        {"label": "2005", "value": 2005},
        {"label": "2006", "value": 2006},
        {"label": "2007", "value": 2007},
        {"label": "2008", "value": 2008},
        {"label": "2009", "value": 2009},
        {"label": "2010", "value": 2010},
        {"label": "2011", "value": 2011},
        {"label": "2012", "value": 2012},
        {"label": "2013", "value": 2013},
        {"label": "2014", "value": 2014},
        {"label": "2015", "value": 2015},
        {"label": "2016", "value": 2016},
        {"label": "2017", "value": 2017},
        {"label": "2018", "value": 2018},
        {"label": "2019", "value": 2019},
        {"label": "2020", "value": 2020}],
    multi=False,
    value=2016,
    style={'width': "30%"}
    ),

html.Div(id='output_container', children=[]),
html.Br(),

dcc.Graph(id='my_unemp_map', figure={})

])
# APP LAYOUT ENDS


# CALLBACK STARTS

@app.callback(
    Output(component_id='my_unemp_map', component_property='figure'),
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = df.copy()
    dff = dff[dff['year'] == option_slctd]

    fig = px.choropleth(
        dff,
        locations='geoid',
        geojson=ca_counties,
        color='unemp',
        labels={'unemp':'unemployment rate'},
        hover_name='name',
        hover_data=['unemp'])
    fig.update_geos(fitbounds='locations', visible=False)
    return fig
# CALLBACK ENDS
