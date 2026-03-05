from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
#from services.bigquery_client import run_query

st.set_page_config(layout="wide")

DEPARTEMENTS_OCCITANIE = [
    "09","11","12","30","31","32","34",
    "46","48","65","66","81","82"
]

DEPARTEMENTS_NOMS = {
    "971": "Guadeloupe",
    "972": "Martinique",
    "973": "Guyane",
    "974": "La Réunion",
    "976": "Mayotte",
    "31": "Haute-Garonne",
    "34": "Hérault",
    "30": "Gard",
    "11": "Aude",
    "12": "Aveyron",
    "09": "Ariège",
    "32": "Gers",
    "48": "Lozère",
    "65": "Hautes-Pyrénées",
    "66": "Pyrénées-Orientales",
    "46": "Lot",
    "81": "Tarn",
    "82": "Tarn-et-Garonne"
}

# ========================
# PALETTE COULEURS
# ========================

BLEU_NUIT = "#1F2A44"
PRUNE = "#6C3B8E"
TERRACOTTA = "#C05A2B"
SABLE = "#D8A47F"
FRAMBOISE = "#A13D63"

@st.cache_data
def get_intensite_globale():

    # ---------------------------
    # Chargement local
    # ---------------------------

    BASE_DIR = Path(__file__).resolve().parents[1]
    DATA_PROCESSED = BASE_DIR / "data"

    path = DATA_PROCESSED / "mortalite_2023_standardise_all.csv"

    if not path.exists():
        st.error(f"Fichier manquant : {path.name}")
        st.stop()

    df = pd.read_csv(path)

    df = (
        df[df["annee"] == 2023]
        .query("sexe == 'Tous sexes'")
        .groupby("departement", as_index=False)["valeur"]
        .sum()
        .rename(columns={"valeur": "taux_total"})
    )

    df["ecart_a_moyenne"] = (
        df["taux_total"] - df["taux_total"].mean()
    ).round(2)

    return df

# ===============================
# 2. Rendu Streamlit
# ===============================
def render_diagnostic():

    df = get_intensite_globale()

        # Remplacement des codes départements par les noms
    df["departement_nom"] = (
        df["departement"]
        .astype(str)
        .map(DEPARTEMENTS_NOMS)
        .fillna(df["departement"])
    )

    if df.empty:
        st.warning("Aucune donnée trouvée.")
        return

    # ======================
    # TITRE
    # ======================
    st.title("📊 Diagnostic territorial 2023")

    st.markdown("""
    Cet axe vise à situer l’Occitanie par rapport au niveau national 
    et à identifier les éventuelles disparités internes entre départements.
    """)

    st.divider()

    # ======================
    # 1️⃣ POSITION DE L’OCCITANIE
    # ======================

    st.header("1️⃣ Position de l’Occitanie")

    # ---- Calcul des moyennes ----
    moyenne_france = df["taux_total"].mean()

    df_occitanie = df[df["departement"].isin(DEPARTEMENTS_OCCITANIE)]
    moyenne_occitanie = df_occitanie["taux_total"].mean()

    ecart_reg = moyenne_occitanie - moyenne_france

    # ---- Affichage KPI ----
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Moyenne France",
            value=f"{round(moyenne_france,1)} décès / 100 000"
        )

    with col2:
        st.metric(
            label="Moyenne Occitanie",
            value=f"{round(moyenne_occitanie,1)} décès / 100 000",
            delta=round(ecart_reg,1)
        )

    # ---- Interprétation ----
    if ecart_reg < 0:
        st.info(
            f"L’Occitanie présente un niveau de mortalité inférieur à la moyenne nationale "
            f"({abs(round(ecart_reg,1))} points d’écart). "
            "La région se situe donc dans une position globalement favorable."
        )
    else:
        st.warning(
            f"L’Occitanie présente un niveau de mortalité supérieur à la moyenne nationale "
            f"({round(ecart_reg,1)} points d’écart). "
            "Ce différentiel interroge l’organisation territoriale de l’offre de soins."
        )

    st.divider()

    # ======================
    # 2️⃣ CLASSEMENT REGIONAL
    # ======================

    st.header("2️⃣ Les écarts territoriaux sont-ils significatifs ?")

    df_occitanie = df[df["departement"].isin(DEPARTEMENTS_OCCITANIE)]
    df_occitanie_sorted = df_occitanie.sort_values("taux_total")

    # ----------------------
    # Sélection dynamique d’un département
    # ----------------------
    departement_selectionne = st.selectbox(
        "Choisir un département à analyser",
        options=df_occitanie_sorted["departement_nom"].unique()
    )

    dept_row = df_occitanie_sorted[
    df_occitanie_sorted["departement_nom"] == departement_selectionne
]

    val_dept = dept_row["taux_total"].values[0]


    fig_occ = px.bar(
        df_occitanie_sorted,
        x="taux_total",
        y="departement_nom",
        orientation="h",
        template="plotly_white",
        color_discrete_sequence=[PRUNE],
        labels={
            "taux_total": "Décès pour 100 000 habitants",
            "departement_nom": "Département"
        },
        title="Taux standardisé de mortalité – Occitanie 2023"
    )

    # Ligne moyenne régionale
    fig_occ.add_vline(
        x=moyenne_occitanie,
        line_color=BLEU_NUIT,
        line_width=3
    )

    # Ligne département sélectionné
    fig_occ.add_vline(
    x=val_dept,
    line_color=FRAMBOISE,
    line_width=3,
    line_dash="dash"
)

    fig_occ.add_annotation(
    x=moyenne_occitanie,
    y=1.05,
    yref="paper",
    text="Moyenne régionale",
    showarrow=False,
    font=dict(size=12, color=TERRACOTTA),
    xanchor="center"
    )

    fig_occ.update_layout(
    font=dict(family="Inter, sans-serif", size=14),
    margin=dict(l=20, r=20, t=50, b=20)
)

    ecart_fr = val_dept - moyenne_france
    ecart_occ = val_dept - moyenne_occitanie

    st.markdown(f"""
    ### 📍 Analyse du département sélectionné

    **{round(val_dept,0)} décès / 100 000 habitants**

    {'+' if ecart_fr > 0 else '–'}{abs(round(ecart_fr,0))} points vs France  
    {'+' if ecart_occ > 0 else '–'}{abs(round(ecart_occ,0))} points vs Occitanie
    """)

    st.plotly_chart(fig_occ, use_container_width=True)

    st.info(
    "Les écarts restent modérés, mais certains départements se distinguent durablement de la moyenne régionale."
    ) 

    st.divider()

    