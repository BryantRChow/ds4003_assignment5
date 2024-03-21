#!/usr/bin/env python
# coding: utf-8

# # Assignment 5: Callbacks
# Objective: Practice adding callbacks to Dash apps.
#  
# 
# Task:
# (1) Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. 
# TASK 1 is the same as ASSIGNMENT 4. You are welcome to update your code. 
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# - The dropdown should allow the user to select multiple countries
# - The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# - The slider should allow the user to select a range of years
# - The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# - The graph should display the gdpPercap for each country as a line
# - Each country should have a unique color
# - The graph should have a title and axis labels in reader friendly format
#  
# 
# (2) Write Callback functions for the slider and dropdown to interact with the graph
# 
# This means that when a user updates a widget the graph should update accordingly.
# The widgets should be independent of each other. 
# Layout:
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# Submission:
# - Deploy your app on Render. 
# - In Canvas, submit the URL to your public Github Repo (made specifically for this assignment)
# - The readme in your GitHub repo should contain the URL to your Render page. 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# In[1]:


# import libraries
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback


# In[2]:


gdp = pd.read_csv('gdp_pcap.csv')
gdp.head()


# In[3]:


# melt data so year becomes a variable
gdp = gdp.melt(id_vars='country', var_name='year', value_name='gdp per capita')
gdp.head()


# In[4]:


# convert year from str to int
gdp['year'] = gdp['year'].astype(int)


# In[5]:


# convert gdp per capita to int
gdp['gdp per capita'] = gdp['gdp per capita'].str.replace('k', '').astype(float)
gdp.loc[gdp['gdp per capita'] < 500, 'gdp per capita'] *= 1000
gdp.dtypes


# In[6]:


# load stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

# initialize app
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server


# In[7]:


app.layout = html.Div([

    # title row
    html.Div(
        html.H1(
            "Gdp Per Capita of Different Countries",
            style={"color": "white", "font-family": "serif"}),
    className="row"
    ),

    # description row
    html.Div(
        html.P(
            "Gdp per capita over time. Includes projected gdp per capita up to the year 2100. Data available per country varies.",
            style={"color": "white", "font-family": "serif"}),
    className="row"
    ),

    # dropdown and slider row
    html.Div([
        # country multiselect dropdown
        html.Div(children=[
            html.Label(
                'Select Countries',
                style={"color": "white"}),
            dcc.Dropdown(
                id = 'countries',
                options=[

                {"label": x, "value": x}

                for x in sorted(gdp["country"].unique())

                ],
                multi = True,
                value=['USA', 'Belgium', 'Argentina', 'Egypt', 'Russia','China']
                )
        ], 
        className="six columns"),

        # timeframe slider
        html.Div(children=[
            html.Label(
                'Select Timeframe',
                style={"color": "white"}),
            dcc.RangeSlider(
                min = gdp['year'].min(), 
                max = gdp['year'].max(), 
                step = 1.0, 
                value = [1950,2020], #default, note array notation
                marks = None,
                id = 'timeframe',
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ],
        className="six columns"),
    ],
    className="row"
    ),
    
    # graph row
    html.Div(
        dcc.Graph(
            id = 'gdp_graph'
        ),
    className="row"
    )
])

# define callbacks
@app.callback(
    Output('gdp_graph', 'figure'),
    Input('timeframe', 'value'),
    Input('countries', 'value'))
def update_figure(selected_years, selected_countries):
    # create a filtered dataset
    filtered_df = gdp.loc[(gdp['year'] >= selected_years[0]) & (gdp['year'] <= selected_years[1]) & 
                          (gdp['country'].isin(selected_countries))]

    # build a line chart
    fig = px.line(filtered_df, 
        x = 'year', 
        y = 'gdp per capita',
        color = 'country',
        markers = True,
        symbol = 'country',
        title = 'GDP per Capita by Country')
    fig.update_layout(xaxis_title = "Year", yaxis_title = "GDP per Capita", transition_duration=500)

    return fig


# In[8]:


if __name__ == '__main__':
    app.run_server(debug=True)

