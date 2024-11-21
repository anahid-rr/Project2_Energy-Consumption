import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Energy Consumption Dashboard",
    layout="wide"
)

st.title("Energy Consumption Dashboard")
color_palette = sns.color_palette("Set2", 10)

df = pd.read_csv('df_countries_10years.csv')
df_continent = pd.read_csv('df_continents_10years.csv')

df_continent['energy_source'] = df_continent['energy_source'].str.capitalize()
st.sidebar.subheader("Please Filter:")

continents = df_continent['country'].unique()
country_filter = []
for continent in continents:
    if st.sidebar.checkbox(continent, value=True): 
        country_filter.append(continent)

years = df_continent['year'].unique()
year_filter = st.sidebar.multiselect('Select Year(s)', years, default=years)

filtered_data = df[(df['year'].isin(year_filter))]
filtered_continent = df_continent[(df_continent['year'].isin(year_filter)) & (df_continent['country'].isin(country_filter))]

renewable_sources = ['Solar', 'Wind', 'Hydro', 'Biofuel', 'Low_carbon']
non_renewable_sources = ['Coal', 'Gas', 'Oil', 'Fossil', 'Fossil Fuel', 'Nuclear']

energy_type = st.sidebar.radio("Select Energy Type", ['All', 'Renewable', 'Non-Renewable'])

if energy_type == 'Renewable':
    selected_sources = renewable_sources
elif energy_type == 'Non-Renewable':
    selected_sources = non_renewable_sources
else:
    selected_sources = renewable_sources + non_renewable_sources  

filtered_data = filtered_data[filtered_data['energy_source'].isin(selected_sources)]
filtered_continent = filtered_continent[filtered_continent['energy_source'].isin(selected_sources)]
st.sidebar.markdown("### Created by: Anahid Raisrohani")
# ********************************** Primary Energy Consumption Trends Over Time By Source *************************
data_Cons = filtered_continent[filtered_continent['type'] == 'consumption']
st.subheader("Primary Energy Consumption Trends Over Time By Source")
plt.figure(figsize=(14, 8))
sns.lineplot(x='year', y='value', hue='energy_source', data=data_Cons, ci=None, palette=color_palette)
plt.xticks(ticks=data_Cons['year'].unique(), rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.title('Energy Consumption Trends Over Time', fontsize=18)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Energy Consumption (TWh)', fontsize=16)
plt.legend(title='Energy Source', loc='upper right', bbox_to_anchor=(1.2, 1), fontsize=16)
plt.tight_layout()
st.pyplot(plt)
plt.close()

# ********************************** Primary Energy Consumption Trends Over Time By Energy Type*************************
data_Cons['energy_type'] = data_Cons['energy_source'].apply(
    lambda x: 'Renewable' if x in renewable_sources else 'Non-Renewable' if x in non_renewable_sources else 'Other'
)

pivot_data = data_Cons.groupby(['year', 'energy_type'])['value'].sum().unstack(fill_value=0)
st.subheader("Energy Consumption by Energy Type Over Years")
plt.figure(figsize=(14, 10))
pivot_data.plot(kind='area', stacked=True, colormap='Set2', ax=plt.gca())
plt.title('Energy Consumption by Energy Type Over Years', fontsize=18)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Energy Consumption (TWh)', fontsize=16)
plt.xticks(rotation=45, ha="right", fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.legend(title='Energy Type', loc='upper right', bbox_to_anchor=(1.2, 1), fontsize=16)
st.pyplot(plt)
plt.close()

# ***************************************** Energy Source Consumption Distribution ********************************
st.subheader("Energy Source Consumption Distribution")
energy_distribution = data_Cons.groupby('energy_source')['value'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='value', y='energy_source', data=energy_distribution, palette='Set2')

total_value = energy_distribution['value'].sum()

for index, value in enumerate(energy_distribution['value']):
    percentage = (value / total_value) * 100
    plt.text(value + 0.1, index, f'{percentage:.1f}%', va='center', fontsize=12)

plt.title('Energy Source Consumption Distribution', fontsize=16)
plt.xlabel('Energy Consumption (TWh)', fontsize=14)
plt.ylabel('Energy Source', fontsize=14)

plt.tight_layout()
st.pyplot(plt)
plt.close()

# *********************************** Primary Energy Consumption Trends Over Time Per Capita (By Continent) ***********************
data_2 = filtered_continent[(filtered_continent['type'] == 'cons') | (df_continent['type']=='energy')]
st.subheader("Primary Energy Consumption Trends Over Time Per Capita")
plt.figure(figsize=(14, 8))
sns.lineplot(x='year', y='value', hue='country', data=data_2, ci=None, palette=color_palette)
plt.xticks(ticks=data_2['year'].unique(), rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.title('Energy Consumption Trends Over Time Per Capita By Continent', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Energy Consumption (KWh)', fontsize=14)
plt.legend(title='Country', loc='upper right', bbox_to_anchor=(1.2, 1), fontsize=12)
plt.tight_layout()
st.pyplot(plt)
plt.close()

# ***************************************** Energy Consumption by Source and Continent ***********************
st.subheader("Energy Consumption by Source and Continent")

energy_consumption_by_source = data_2.groupby(['country', 'energy_source'])['value'].sum().unstack(fill_value=0)

plt.figure(figsize=(20, 12))
energy_consumption_by_source.plot(kind='bar', colormap='Set2', ax=plt.gca(), width=0.8)
plt.title('Energy Consumption by Source', fontsize=18)
plt.xlabel('Continent', fontsize=18)
plt.ylabel('Energy Consumption (TWh)', fontsize=18)
plt.xticks(rotation=45, ha="right", fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.legend(title='Energy Source', loc='upper left', fontsize=18)
st.pyplot(plt)
plt.close()

# ********************************************* CO2 Emissions by Country ********************************
st.subheader("CO2 Emissions (Metric Million Tons)")
df_map = df[(df['year'].isin(year_filter)) & (df['type'] == 'emissions')]
fig = px.choropleth(df_map,
                    locations="country",
                    locationmode="country names",
                    color="value",
                    color_continuous_scale="Viridis",
                   
                    labels={'value': 'CO2 Emissions (Metric Million Tons)'},
                    title=f"CO2 Emissions by Country")

fig.update_layout(
    title_font_size=16,
    geo=dict(
        showland=True,
        landcolor="white",
        showlakes=True,
        lakecolor="white",
        showcoastlines=True,
        coastlinecolor="grey",
        projection_type="natural earth",
        visible=True
    ),
    geo_bgcolor='rgba(0,0,0,0)',
    coloraxis_colorbar_title="CO2 Emissions (Metric Million Tons)",
    margin={"r":0,"t":0,"l":0,"b":0},
    showlegend=False
)

st.plotly_chart(fig)
