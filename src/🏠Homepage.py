import streamlit as st
from PIL import Image

# ---------------------------------------------------------
# CONFIGURATION DE LA PAGE
# ---------------------------------------------------------
st.set_page_config(
    page_title="Projet Data Analytics – Homepage",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("📊 Projet de fin de bootcamp – Data Analytics.")

st.subheader("Comment aider les acteurs locaux à réaliser un diagnostic de santé publique sur leur territoire en Occitanie?")

st.markdown(
    """
Cette application présente l’ensemble des analyses, visualisations et outils développés autour des jeux de données sélectionnés.

---
"""
)

# ---------------------------------------------------------
# OBJECTIFS DU PROJET
# ---------------------------------------------------------
st.header("🎯 Objectifs du projet")

st.markdown(
    """
- **Explorer et préparer les données** pour garantir leur qualité et leur cohérence.  
- **Construire un pipeline automatisé** pour l’ingestion, le nettoyage et la transformation des données.  
- **Analyser les tendances clés** grâce à des visualisations interactives.  
- **Fournir des insights actionnables** pour les décideurs.  
- **Déployer une application Streamlit** claire, robuste et professionnelle.
"""
)

# ---------------------------------------------------------
# STRUCTURE DU TABLEAU DE BORD
# ---------------------------------------------------------
st.header("🗂️ Navigation dans l'application")

st.markdown(
    """
L'application est organisée en plusieurs sections accessibles via le menu latéral :

- **🏠 Accueil** : Présentation générale du projet. 
- **🩺 Offre de soins** : Analyse des indicateurs de vulnérabilité
- **🏢 Etablissements** : Localisation des établissements de santé.  
- **🤒 Pathologies** : Analyse des pathologies sur le territoire  
- **☠️ Mortalite** : Analyse des indicateurs de mortalité
- **📖 Lexique** : Définition des acronymes
"""
)

# ---------------------------------------------------------
# METHODOLOGIE
# ---------------------------------------------------------
st.header("🧭 Méthodologie")

st.markdown(
    """
La démarche suivie repose sur les étapes classiques d’un projet data :

1. **Compréhension du besoin métier**  
2. **Collecte et exploration des données**  
3. **Nettoyage et préparation (ELT)**  
4. **Analyses statistiques et visualisations**  
5. **Modélisation (si applicable)**  
6. **Synthèse et recommandations**  
7. **Déploiement Streamlit**


"""
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.caption("Projet réalisé dans le cadre du bootcamp Data Analytics – Artefact School of Data")