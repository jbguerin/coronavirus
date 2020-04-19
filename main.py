import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot

# Read data
# Data source: https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset/data#covid_19_data.csv
df = pd.read_csv("novel-corona-virus-2019-dataset/covid_19_data.csv")

# Rename columns
df = df.rename(columns={'Country/Region':'Country'})
df = df.rename(columns={'ObservationDate':'Date'})

# Get date of last entry in the dataset
last_date = np.max(df['Date'])
last_date = last_date[3:6] + last_date[:2] + last_date[5:]

# Manipulate Dataframe
df_countries = df.groupby(['Country', 'Date']).sum().reset_index().sort_values('Date', ascending=False)
df_countries = df_countries[df_countries['Confirmed']>0]
df_countries = df_countries.drop_duplicates(subset = ['Country'])

# Create choropleth map for last update
choroplethmap = go.Figure(data=go.Choropleth(locations=df_countries['Country'], locationmode='country names',
                                   z=df_countries['Confirmed'], colorscale='Reds', marker_line_color='black',
                                   marker_line_width=0.5))

choroplethmap.update_layout(title_text='Cas confirmés : ' + last_date, title_x=0.5,
                            geo=dict(showframe=False, showcoastlines=False, projection_type='orthographic'))

plot(choroplethmap, filename='choroplethmap.html')


# Plot confirmed cases by date

# Manipulate Dataframe
df_confirmed_cases = df[df['Confirmed'] > 0]
df_confirmed_cases = df_confirmed_cases.groupby(['Date', 'Country']).sum().reset_index()

# Create visualization over time
confirmed_cases = px.choropleth(df_confirmed_cases, locations="Country", locationmode="country names", color="Confirmed",
                                hover_name="Country", animation_frame="Date", color_continuous_scale='Reds')

confirmed_cases.update_layout(title_text='Évolution du nombre de cas confirmés par pays', title_x=0.5,
                              geo=dict(showframe=False, showcoastlines=False))

plot(confirmed_cases, filename='confirmedcases.html')

# Plot deaths by date

df_deaths = df[df['Deaths'] > 0]
df_deaths = df_deaths.groupby(['Date', 'Country']).sum().reset_index()

deaths = px.choropleth(df_deaths, locations="Country", locationmode="country names", color="Deaths",
                       hover_name="Country", animation_frame="Date", color_continuous_scale='Reds')

deaths.update_layout(title_text='Évolution du nombre de décès par pays', title_x=0.5,
                              geo=dict(showframe=False, showcoastlines=False))

plot(deaths, filename='deaths.html')