import streamlit as st
import pandas as pd
from bienici import search_ads

st.set_page_config(
    page_title="House Finder",
    page_icon='🔎',
    layout="wide"
)

st.title("House Finder")  
articles = []

st.sidebar.write("# Antoine Lecoffre - Web Scraping 2023")

st.sidebar.write("### Rechercher votre logement facilement via bienici.fr")

st.sidebar.write("Le but de l'application est de vous permettre d'identifier rapidement les logements mis en vente sur le site bienici dans la ville de votre choix")
st.sidebar.write("Le framwork Selenium est utilisé pour récupérer les données du site bienici.fr parce que le site utilise du JavaScript pour afficher les données et que j'ai une meilleure apétence à utiliser Selenium plutôt que Scrapy ou BS4")
# lien cliquable
st.sidebar.markdown("### https://www.bienici.com/")


with st.form('FormSearchArticle'):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pattern = st.text_input('Ville de recherche')
    with col2:
        page = st.text_input('Nombre de page à parcourir')
    with col3:
        min_price = st.text_input('Budget minimum')
    with col4:
        max_price = st.text_input('Budget maximum')
        


    if st.form_submit_button('Lancer la recherche'):
        articles = search_ads(pattern,min_price, max_price, int(page))
        # pass
        st.write(articles)

if articles != []:
    if 'articles' not in st.session_state:
        st.session_state.key = 'articles'
        st.session_state['articles'] = articles

    st.session_state['pattern'] = pattern

    st.write("### Résultats de la recherche visible dans la page ResultViewer")