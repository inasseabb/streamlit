import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt 
import datetime
import folium
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import ipywidgets as widgets
from IPython.display import display
import rasterio
from rasterio.plot import show
import ipyleaflet as leaflet

st.title("Application de Visualisation Géospatiale")
st.subheader("Affichage de données à partir d'un GeoParquet")
#load data
donnees_geospatiales = gpd.read_parquet('C:/Users/Admin/Desktop/mapdashboard/data.parquet')
# Afficher la carte avec la fonction st.map()
print(donnees_geospatiales.head())

# Sélection du jour (i) et de l'attribut (j)
jour_i = st.selectbox("Choisissez le jour (i)", ["0", "-1", "-2", "-3", "-4", "-5", "-6"])
attribut_j = st.selectbox("Choisissez l'attribut (j)", ["1", "2", "3"])

# Nom de la colonne à cartographier
colonne_a_cartographier = f"Attibut{attribut_j}Jour{jour_i}"
# Création de la carte Folium
m = folium.Map(location=[donnees_geospatiales.geometry.y.mean(), donnees_geospatiales.geometry.x.mean()], zoom_start=6)

# Ajout des points sur la carte
for index, row in donnees_geospatiales.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], tooltip=row[colonne_a_cartographier]).add_to(m)

# Afficher la carte avec la fonction folium_static
folium_static(m)



# Slider pour naviguer entre les jours
jours_disponibles = ["0", "-1", "-2", "-3", "-4", "-5", "-6"]
jour_selectionne = st.select_slider("Sélectionnez le jour à afficher", options=jours_disponibles, value=jour_i)

# Mise à jour de la carte en fonction du jour sélectionné avec le slider
colonne_a_cartographier_slider = f"Attibut{attribut_j}Jour{jour_selectionne}"
fig, ax = plt.subplots()
cax = ax.matshow(data, cmap='viridis')
fig.colorbar(cax)
plt.close(fig)  # Fermer la figure pour éviter l'affichage direct dans Streamlit

# Convertir la figure en image et l'afficher dans Streamlit
image_stream = BytesIO()
fig.savefig(image_stream, format='png')
image_stream.seek(0)

# Créer une carte Folium
m = folium.Map(location=[0, 0], zoom_start=1)

# Ajouter l'image à la carte
img = folium.raster_layers.ImageOverlay(
    image=image_stream,
    bounds=[[0, 0], [10, 10]],  # Ajustez les limites en fonction de vos données
    colormap=lambda x: (0, x, 0, 1),  # Exemple de colormap (vert pour les valeurs plus élevées)
).add_to(m)

# Afficher la carte dans Streamlit
folium_static(m)

# Sélection du jour (i) et de l'attribut (j)
jour_i2 = st.selectbox("Chkhtarou)", ["0", "-1", "-2", "-3", "-4", "-5", "-6"])
attribut_j2 = st.selectbox("Ckhtarou(j)", ["1", "2", "3"])

# Nom de la colonne à cartographier
colonne_a_comparer = f"Attibut{attribut_j2}Jour{jour_i2}"

m = leaflet.Map()
m.split_map(
    left_layer='colonne_a_cartographier', right_layer='colonne_a_comparer'
)
m.add_legend(title='colonne_a_cartographier', builtin_legend='colonne_a_comparer')


def creer_couche_par_jour(jour, donnees_geospatiales, attribut_j):
    """Crée une couche à partir des données spatiales d'un jour donné"""

    # Sélectionne les données correspondant au jour spécifié
    donnees_du_jour = donnees_geospatiales[donnees_geospatiales[attribut_j] == jour]

    # Convertit les données en geojson
    geojson = donnees_du_jour.to_json()

    # Crée la couche à partir du geojson
    couche = folium.GeoJson(geojson, name=jour, style_function=style_function)

    return couche
def mettre_a_jour_couche(couche, jour, donnees_geospatiales, attribut_j):
    colonne_a_cartographier = f"Attibut{attribut_j}Jour{jour}"
    geojson = gpd.io.json.dumps(donnees_geospatiales)
    couche.data = geojson
    couche.style = {"color": "#ff7800", "fillColor": "#ffffb2", "opacity": 0.5, "fillOpacity": 0.5}
    couche.name = f"Jour {jour}"
    return couche
# Création de la carte ipyleaflet
m = leaflet.Map(location=[donnees_geospatiales.geometry.y.mean(), donnees_geospatiales.geometry.x.mean()], zoom_start=6)

# Ajout des couches pour chaque jour
couches = {}
for jour in jours_disponibles:
    couches[jour] = creer_couche_par_jour(jour, donnees_geospatiales, attribut_j)
    couches[jour].add_to(m)

# Mise à jour de la carte en fonction du jour sélectionné avec le slider
couche_selectionnee = couches[jour_selectionne]
couche_selectionnee.style = {"color": "#008000", "fillColor": "#00ff00", "opacity": 1, "fillOpacity": 1}

# Afficher la carte avec la fonction leaflet.show
m
