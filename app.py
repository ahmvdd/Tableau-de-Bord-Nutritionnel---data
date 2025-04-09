import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Nutri-diab | Dashboard Nutritionnel",
    page_icon="🍎",
    layout="wide"
)

# Chargement des données
@st.cache_data
def load_data():
    return pd.read_csv("nutridiab_filtré.csv")

df = load_data()

# ----------- EN-TÊTE DU TABLEAU DE BORD -----------
st.title("🍎 Nutri-diab - Tableau de Bord Nutritionnel")
st.markdown("""
Bienvenue sur **Nutri-diab**, une application de visualisation dédiée à l’analyse de données nutritionnelles pour les **personnes atteintes de diabète**.

Ce tableau de bord a pour objectif de :
- Visualiser les valeurs nutritionnelles des produits alimentaires
- Identifier les produits potentiellement risqués (fortement sucrés, gras saturés, etc.)
- Fournir un outil d'aide à la décision pour les professionnels de santé ou projets en nutrition préventive

Les données analysées proviennent d’un échantillon filtré de produits disponibles dans le commerce.
""")

st.markdown("---")

# ----------- APERÇU DES DONNÉES -----------
st.subheader("🔍 Aperçu des données")
st.dataframe(df.head(), use_container_width=True)

# ----------- STATISTIQUES DESCRIPTIVES -----------
st.subheader("📊 Statistiques descriptives globales")
st.write(df.describe())

# ----------- SIDEBAR - CONTRÔLES -----------
st.sidebar.header("⚙️ Options d'analyse")

# Filtres par marque si dispo
if "brands" in df.columns:
    brands = ["Toutes"] + sorted(df["brands"].dropna().unique().tolist())
    selected_brand = st.sidebar.selectbox("Filtrer par marque :", brands)
    if selected_brand != "Toutes":
        df = df[df["brands"] == selected_brand]

# Sélections de variables numériques
columns = df.select_dtypes(include='number').columns.tolist()
selected_col = st.sidebar.selectbox("Variable pour histogramme", columns)
x_col = st.sidebar.selectbox("Variable X (scatter)", columns, index=0)
y_col = st.sidebar.selectbox("Variable Y (scatter)", columns, index=1)

# ----------- VISUALISATION : HISTOGRAMME -----------
st.subheader(f"📈 Distribution de la variable : {selected_col}")
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    sns.histplot(df[selected_col], kde=True, ax=ax, color="teal")
    ax.set_title(f"Distribution de {selected_col}")
    st.pyplot(fig)

with col2:
    st.markdown(f"""
    **Informations :**
    - Moyenne : `{df[selected_col].mean():.2f}`
    - Médiane : `{df[selected_col].median():.2f}`
    - Écart-type : `{df[selected_col].std():.2f}`
    """)

# ----------- MATRICE DE CORRÉLATION -----------
st.subheader("🔗 Corrélation entre variables nutritionnelles")
fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
sns.heatmap(df[columns].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax_corr)
ax_corr.set_title("Matrice de corrélation")
st.pyplot(fig_corr)

# ----------- SCATTER INTERACTIF (PLOTLY) -----------
st.subheader(f"📍 Visualisation interactive : {x_col} vs {y_col}")
fig_plotly = px.scatter(
    df, 
    x=x_col, 
    y=y_col, 
    color="nutriscore_grade" if "nutriscore_grade" in df.columns else df.columns[0],
    hover_name="product_name" if "product_name" in df.columns else None,
    size="sugars_100g" if "sugars_100g" in df.columns else None,
    title=f"{y_col} en fonction de {x_col}",
    opacity=0.7
)
st.plotly_chart(fig_plotly, use_container_width=True)

# ----------- FUTURS AJOUTS (suggestions) -----------
# st.markdown("🔧 Prochaine étape : filtrage intelligent selon seuils glycémiques, recommandations produit, scoring santé...")

