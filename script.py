"""
Based on : https://towardsdatascience.com/visualizing-the-coronavirus-pandemic-with-choropleth-maps-7f30fccaecf5
Data source : https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset/data#covid_19_data.csv
"""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot

# Read data
df = pd.read_csv("novel-corona-virus-2019-dataset/covid_19_data.csv")

# Rename columns
df = df.rename(columns={'Country/Region':'Country'})
df = df.rename(columns={'ObservationDate':'Date'})

# Get date of last update
last_update = np.max(df['Date'])

# Manipulate Dataframe
df_countries = df.groupby(['Country', 'Date']).sum().reset_index().sort_values('Date', ascending=False)
df_countries = df_countries[df_countries['Confirmed']>0]
df_countries = df_countries.drop_duplicates(subset = ['Country'])

# Create choropleth map for last update
choroplethmap = go.Figure(data=go.Choropleth(locations=df_countries['Country'], locationmode='country names',
                                   z=df_countries['Confirmed'], colorscale='Reds', marker_line_color='black',
                                   marker_line_width=0.5))

choroplethmap.update_layout(title_text='Confirmed Cases as of '+last_update, title_x=0.5,
                  geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))

plot(choroplethmap, filename='choroplethmap.html')

# Manipulate Dataframe
df_countrydate = df[df['Confirmed'] > 0]
df_countrydate = df_countrydate.groupby(['Date', 'Country']).sum().reset_index()

# Create visualization over time
vis = px.choropleth(df_countrydate, locations="Country", locationmode="country names", color="Confirmed",
                    hover_name="Country", animation_frame="Date", color_continuous_scale='Reds')

vis.update_layout(title_text='Global Spread of Coronavirus', title_x=0.5,
                  geo=dict(showframe=False, showcoastlines=False))

plot(vis, filename='visualization.html')