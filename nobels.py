#Importamos los paquetes que utilizaremos
import streamlit as st
from streamlit.components.v1 import html as ht
import leafmap.foliumap as leafmap
import folium
import pandas as pd
import numpy as np
import geopandas as gpd
import altair as alt
import matplotlib.pyplot as plt

# CARGAMOS LOS DATOS
laureates = pd.read_csv('laureates_clean.csv')

#Vamos a crear una app que tendrá 4 pestañas con diferentes insights que se llamará 'NOBEL AWARDS'
st.title("NOBEL AWARDS")

#En la primera pestaña se mostrará un mapa mundial donde se colorearán los países según el número de premios nobel que se hayan otrogado. 
#Existirá una leyenda y se podrá consultar el número de premios exacto pulsando sobre el icono de info de cada país
#Vamos a calcular latitud media, longitud media y numero de premios por país

map_data = laureates.groupby(by = 'Country')[['name','Latitude','Longitude']].agg({
    'Latitude': 'mean',
    'Longitude': 'mean',
    'name':'count'
}).reset_index()

#Guardamos los países que aparecen en nuestros datos
my_data_countries = map_data['Country'].unique()

#Creamos el mapa
m = leafmap.Map()

# Descargamos el archivo GeoJSON del mundo
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world_df = pd.DataFrame(world)
#Guardamos los países del GeoJSON
json_countries = world_df['name'].unique()

#PARA AVERIGUAR A QUE PAÍSES DEBEMOS RENOMBRAR HAREMOS EL SIGUIENTE MATCH:

#print(list(set(my_data_countries)-set(json_countries)))
#print(list(set(json_countries)-set(my_data_countries)))

# de esa manera encontramos en primer lugar los países que debemos renombrar y en segundo lugar, el nombre por el que los debemos cambiar

#Los renombramos:
map_data.loc[map_data['Country'] == 'Schleswig', 'Country'] = 'Germany'
map_data.loc[map_data['Country'] == 'Persia', 'Country'] = 'Iran'
map_data.loc[map_data['Country'] == 'British Mandate of Palestine', 'Country'] = 'Palestine'
map_data.loc[map_data['Country'] == 'Prussia', 'Country'] = 'Germany'
map_data.loc[map_data['Country'] == 'Gold Coast', 'Country'] = 'Ghana'
map_data.loc[map_data['Country'] == 'Hesse-Kassel', 'Country'] = 'Germany'
map_data.loc[map_data['Country'] == 'French Algeria', 'Country'] = 'Algeria'
map_data.loc[map_data['Country'] == 'East Friesland', 'Country'] = 'Germany'
map_data.loc[map_data['Country'] == 'the Netherlands', 'Country'] = 'Netherlands'
map_data.loc[map_data['Country'] == 'Guadeloupe Island', 'Country'] = 'Mexico'
map_data.loc[map_data['Country'] == 'Russian Empire', 'Country'] = 'Russia'
map_data.loc[map_data['Country'] == 'Northern Ireland', 'Country'] = 'Ireland'
map_data.loc[map_data['Country'] == 'Austrian Empire', 'Country'] = 'Austria'
map_data.loc[map_data['Country'] == 'Java, Dutch East Indies', 'Country'] = 'Indonesia'
map_data.loc[map_data['Country'] == 'Southern Rhodesia', 'Country'] = 'Zimbabwe'
map_data.loc[map_data['Country'] == 'Crete', 'Country'] = 'Greece'
map_data.loc[map_data['Country'] == 'Czechoslovakia', 'Country'] = 'Czechia'
map_data.loc[map_data['Country'] == 'Mecklenburg', 'Country'] = 'Germany'
map_data.loc[map_data['Country'] == 'British India', 'Country'] = 'India'
map_data.loc[map_data['Country'] == 'Belgian Congo', 'Country'] = 'Congo'
map_data.loc[map_data['Country'] == 'USSR', 'Country'] = 'Russia'
map_data.loc[map_data['Country'] == 'Württemberg', 'Country'] = 'Germany'
map_data.loc[map_data['Country'] == 'East Timor', 'Country'] = 'Timor-Leste'
map_data.loc[map_data['Country'] == 'Tuscany', 'Country'] = 'Italy'
map_data.loc[map_data['Country'] == 'Austria-Hungary', 'Country'] = 'Austria'
map_data.loc[map_data['Country'] == 'Bosnia', 'Country'] = 'Bosnia and Herz.'
map_data.loc[map_data['Country'] == 'Ottoman Empire', 'Country'] = 'Turkey'
map_data.loc[map_data['Country'] == 'Burma', 'Country'] = 'Myanmar'
map_data.loc[map_data['Country'] == 'Faroe Islands (Denmark)', 'Country'] = 'Denmark'
map_data.loc[map_data['Country'] == 'Tibet', 'Country'] = 'China'
map_data.loc[map_data['Country'] == 'Korea', 'Country'] = 'South Korea'
map_data.loc[map_data['Country'] == 'USA', 'Country'] = 'United States of America'
map_data.loc[map_data['Country'] == 'French protectorate of Tunisia', 'Country'] = 'Tunisia'
map_data.loc[map_data['Country'] == 'Free City of Danzig', 'Country'] = 'Poland'
map_data.loc[map_data['Country'] == 'West Germany', 'Country'] = 'Germany'
map_data.loc[map_data['Country'] == 'Bavaria', 'Country'] = 'Germany'
map_data.loc[map_data['Country'] == 'German-occupied Poland', 'Country'] = 'Poland'

#Agrupamos otra vez para incorporar la corrección
map_data_corr = map_data.groupby(by = 'Country')[['name','Latitude','Longitude']].agg({
    'Latitude': 'mean',
    'Longitude': 'mean',
    'name':'sum'}).reset_index()

#Agregamos el mapa
folium.Choropleth(
    geo_data=world,
    name='choropleth',
    data=map_data_corr,
    columns=['Country', 'name'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    nan_fill_color='white',  # Color para países sin datos
    nan_fill_opacity=0.7,
    legend_name='Prizes per country'
).add_to(m)


#Agregamos los marcadores al mapa
for index, row in map_data_corr.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Country:{row['Country']} Prizes: {row['name']}",
        icon=folium.Icon(icon = 'info-sign', color='grey', icon_size=(15,15))
    ).add_to(m)

#Mostramos el mapa
mapa_html = m._repr_html_()

#Creamos el índice de selección en Streamlit. El mapa aparecerá al cargar la app por defecto.
selected_tab = st.sidebar.radio("Select an option", ["Nobel Awards World Map", "Laureates by Year", "Awards by Category", "Prize Amount Over the Years"])

#Creamos las opciones
if selected_tab == "Nobel Awards World Map":
    st.title("Nobel Awards World Map")
    #Mostramos el mapa en streamlit
    ht(mapa_html, height=600, width=800, scrolling=True)
    
#En la segunda pestaña se mostrarán los premiados por cada año, su país y la categoría, con un slider donde se podrá seleccionar el año.
elif selected_tab == "Laureates by Year":
    # Sección 2: Slider para seleccionar un año y mostrar ganadores
    slider_data = laureates[['name','Country', 'awardYear', 'category']]
    st.title('Select Laureates by Year:')
    selected_year = st.slider('Select year', min_value=slider_data['awardYear'].min(), max_value=slider_data['awardYear'].max(), value=1957)
    winners_for_year = slider_data.loc[laureates['awardYear'] == selected_year]
    st.write(f'Laureates in {selected_year}:')
    st.table(winners_for_year[['name', 'Country','category']].reset_index(drop=True))
    
#En la tercera pestaña se podrá consultar los premios por categoría otorgados a cada país, seleccionando de un desplegable
elif selected_tab == "Awards by Category":
    st.title('Awards by Category')
    selected_country = st.selectbox('Select a country', laureates['Country'].unique())
    #Filtramos datos por país seleccionado
    data_selected_country = laureates[laureates['Country'] == selected_country]
    #Contamos el número de premios por categoría
    category_counts_by_country = data_selected_country['category'].value_counts().astype(int)
    #Creamos el gráfico con Matplotlib
    fig, ax = plt.subplots()
    category_counts_by_country.plot(kind='bar', ax=ax)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Configurar el eje y para mostrar solo enteros
    ax.set_ylabel('Count')
    ax.set_xlabel('Category')
    #Mostramos el gráfico en Streamlit
    st.pyplot(fig)
    
#Finalmente mostraremos la evolución del premio en euros con los años en una gráfica en la que se podrá colocar el ratón encima para 
#consultar el año concreto y la cantidad en euros concreta en cualquier punto de la gráfica
elif selected_tab == "Prize Amount Over the Years":
    st.title('Prize Amount Over the Years')
    #Creamos gráfico de línea interactivo con Altair
    chart_data = laureates.loc[:,['awardYear', 'prizeAmount']]
    chart = alt.Chart(chart_data).mark_line().encode(
        x=alt.X('awardYear', title='Year'), 
        y=alt.Y('prizeAmount', title='Prize Amount (eur)'),
        tooltip=['awardYear','prizeAmount']).properties(
            width=800,
            height=500)
    st.altair_chart(chart, use_container_width=True)