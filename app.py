"""
app.py — Interface Streamlit de l'application de simulation d'investissement.

Lancer avec : streamlit run app.py

Ce fichier ne contient QUE de la logique d'affichage et d'orchestration.
Tous les calculs vivent dans calculs.py, toutes les données de référence dans
data.py, et toute la persistance dans persistence.py.
"""

import streamlit as st
import pandas as pd

from data import ACTIONS, ETFS, AVERTISSEMENT_RENDEMENTS
from calculs import (
    projeter_trois_scenarios,
    calculer_portefeuille_cumule,
    taux_rendement_annualise_approx,
)
from persistence import charger_portefeuille, ajouter_position, supprimer_position


# ---------------------------------------------------------------------------
# Configuration générale de la page
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulateur d'Investissement",
    page_icon="📈",
    layout="wide",
)

# --- Thème noir & orange ---
COULEUR_FOND = "#0E0E0E"
COULEUR_FOND_CARTE = "#1A1A1A"
COULEUR_ACCENT = "#F27A00"       # orange
COULEUR_ACCENT_HOVER = "#FF9533"
COULEUR_TEXTE = "#FFFFFF"
COULEUR_PESSIMISTE = "#FF5C4D"
COULEUR_CENTRAL = "#F27A00"
COULEUR_OPTIMISTE = "#4DD68A"

st.markdown(
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
    /* Bloque le zoom tactile/pinch sur mobile, garde une mise en page fixe */
    html {{ touch-action: pan-x pan-y; }}

    .stApp {{
        background-color: {COULEUR_FOND};
        color: {COULEUR_TEXTE};
    }}

    h1, h2, h3, h4, h5, label, p, span, div, .stMarkdown {{
        color: {COULEUR_TEXTE} !important;
    }}

    h1, h2, h3 {{ color: {COULEUR_ACCENT} !important; }}

    /* Boutons : gros, contrastés, faciles à viser au doigt */
    .stButton>button {{
        background-color: {COULEUR_ACCENT};
        color: {COULEUR_TEXTE} !important;
        border-radius: 10px;
        border: none;
        font-weight: 700;
        font-size: 1.25rem;
        padding: 1.1rem 1.5rem;
        min-height: 60px;
        width: 100%;
    }}
    .stButton>button:hover {{
        background-color: {COULEUR_ACCENT_HOVER};
        color: {COULEUR_TEXTE} !important;
    }}
    .stButton>button p {{
        font-size: 1.25rem !important;
        font-weight: 700 !important;
    }}

    /* Cartes / conteneurs (inputs, expanders) */
    .stNumberInput, .stSelectbox, .stSlider, .stRadio {{
        background-color: {COULEUR_FOND_CARTE};
        border-radius: 8px;
        padding: 0.3rem;
    }}

    /* Le champ de saisie lui-même garde un fond clair (comportement natif) :
       on force donc son texte en noir pour rester lisible, sans toucher
       au reste de la page qui est en texte blanc sur fond noir. */
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] *,
    .stSelectbox input {{
        color: #111111 !important;
    }}
    .stNumberInput input {{
        background-color: #FFFFFF !important;
    }}
    .stSelectbox div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
    }}
    /* Liste déroulante ouverte (les options) */
    ul[data-testid="stSelectboxVirtualDropdown"] li,
    ul[data-testid="stSelectboxVirtualDropdown"] li * {{
        color: #111111 !important;
    }}

    div[data-testid="stExpander"] {{
        background-color: {COULEUR_FOND_CARTE};
        border-radius: 8px;
        border: 1px solid #333;
    }}

    div[data-testid="stMetric"] {{
        background-color: {COULEUR_FOND_CARTE};
        border-radius: 8px;
        padding: 0.8rem;
        border: 1px solid #333;
    }}
    div[data-testid="stMetricLabel"] {{ color: {COULEUR_TEXTE} !important; }}
    div[data-testid="stMetricValue"] {{ color: {COULEUR_ACCENT} !important; }}

    .bloc-avertissement {{
        background-color: {COULEUR_FOND_CARTE};
        border-left: 4px solid {COULEUR_ACCENT};
        padding: 0.6rem 1rem;
        border-radius: 4px;
        font-size: 0.85rem;
        color: {COULEUR_TEXTE} !important;
    }}

    /* Tabs */
    button[data-baseweb="tab"] {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {COULEUR_TEXTE} !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {COULEUR_ACCENT} !important;
        border-bottom-color: {COULEUR_ACCENT} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Initialisation du session_state
# ---------------------------------------------------------------------------
if "portefeuille" not in st.session_state:
    st.session_state.portefeuille = charger_portefeuille()

if "actif_selectionne_nom" not in st.session_state:
    st.session_state.actif_selectionne_nom = None

if "position_detail_id" not in st.session_state:
    st.session_state.position_detail_id = None


def _formater_euros(valeur: float) -> str:
    return f"{valeur:,.0f} €".replace(",", " ")


# ---------------------------------------------------------------------------
# En-tête
# ---------------------------------------------------------------------------
st.title("📈 Simulateur d'investissement")
st.caption("Outil pédagogique de simulation — ne constitue pas un conseil en investissement personnalisé.")

onglet_simulateur, onglet_portefeuille = st.tabs(["🧮 Simulateur", "💼 Mon portefeuille"])


# ===========================================================================
# ONGLET 1 — SIMULATEUR
# ===========================================================================
with onglet_simulateur:

    with st.expander("⚠️ Remarque importante (à lire une fois)", expanded=False):
        st.markdown(AVERTISSEMENT_RENDEMENTS)

    col_param, col_resultat = st.columns([1, 1.4], gap="large")

    with col_param:
        st.subheader("1. Choisir un actif")

        categorie = st.radio(
            "Catégorie",
            options=["Actions", "ETF"],
            horizontal=True,
            label_visibility="collapsed",
        )

        catalogue = ACTIONS if categorie == "Actions" else ETFS
        noms_actifs = ["— Aucun (saisie manuelle) —"] + list(catalogue.keys())

        nom_choisi = st.selectbox(f"{categorie} disponibles", options=noms_actifs)

        if nom_choisi != "— Aucun (saisie manuelle) —":
            infos_actif = catalogue[nom_choisi]
            st.session_state.actif_selectionne_nom = nom_choisi
            st.caption(f"ℹ️ {infos_actif['note']}")
        else:
            infos_actif = {
                "rendement_central": 0.07,
                "rendement_pessimiste": 0.02,
                "rendement_optimiste": 0.11,
                "type": categorie,
            }
            st.session_state.actif_selectionne_nom = None

        st.subheader("2. Ajuster les rendements (modifiable)")
        st.caption("Pré-rempli depuis l'historique de l'actif choisi. Modifie librement si tu veux tester d'autres hypothèses.")

        c1, c2, c3 = st.columns(3)
        with c1:
            rendement_pessimiste = st.number_input(
                "Pessimiste (%)",
                value=round(infos_actif["rendement_pessimiste"] * 100, 1),
                step=0.5,
                key=f"pess_{nom_choisi}",
            ) / 100
        with c2:
            rendement_central = st.number_input(
                "Central (%)",
                value=round(infos_actif["rendement_central"] * 100, 1),
                step=0.5,
                key=f"cent_{nom_choisi}",
            ) / 100
        with c3:
            rendement_optimiste = st.number_input(
                "Optimiste (%)",
                value=round(infos_actif["rendement_optimiste"] * 100, 1),
                step=0.5,
                key=f"opti_{nom_choisi}",
            ) / 100

        if rendement_pessimiste > rendement_central or rendement_central > rendement_optimiste:
            st.warning("⚠️ Logiquement : pessimiste ≤ central ≤ optimiste. Vérifie tes valeurs.")

        st.subheader("3. Paramètres de versement")

        investissement_initial = st.number_input(
            "Investissement initial (€)", min_value=0.0, value=1000.0, step=100.0
        )
        apport_mensuel = st.number_input(
            "Apport mensuel (€)", min_value=0.0, value=100.0, step=10.0
        )
        duree_annees = st.slider("Durée (années)", min_value=1, max_value=40, value=20)

        col_btn1, col_btn2 = st.columns(2)
        bouton_valider = col_btn1.button("💰 Investir", use_container_width=True)
        bouton_reset = col_btn2.button("🔄 Réinitialiser", use_container_width=True)

        if bouton_reset:
            st.rerun()

    # -----------------------------------------------------------------
    # Calcul (recalculé à chaque interaction — c'est volontaire et léger)
    # -----------------------------------------------------------------
    resultats = projeter_trois_scenarios(
        investissement_initial,
        apport_mensuel,
        duree_annees,
        rendement_pessimiste,
        rendement_central,
        rendement_optimiste,
    )

    with col_resultat:
        st.subheader("Projection")

        nom_affiche = st.session_state.actif_selectionne_nom or "Actif personnalisé"
        st.markdown(f"**{nom_affiche}** — sur {duree_annees} ans")

        m1, m2, m3 = st.columns(3)
        m1.metric(
            "Pessimiste",
            _formater_euros(resultats["pessimiste"].valeur_finale),
            delta=f"{rendement_pessimiste*100:.1f} %/an",
        )
        m2.metric(
            "Central",
            _formater_euros(resultats["central"].valeur_finale),
            delta=f"{rendement_central*100:.1f} %/an",
        )
        m3.metric(
            "Optimiste",
            _formater_euros(resultats["optimiste"].valeur_finale),
            delta=f"{rendement_optimiste*100:.1f} %/an",
        )

        st.markdown("")

        # Graphique des 3 scénarios superposés
        df_scenarios = pd.DataFrame({
            "Année": list(range(1, duree_annees + 1)),
            "Pessimiste": resultats["pessimiste"].historique_annuel,
            "Central": resultats["central"].historique_annuel,
            "Optimiste": resultats["optimiste"].historique_annuel,
        }).set_index("Année")

        st.line_chart(
            df_scenarios,
            color=[COULEUR_PESSIMISTE, COULEUR_CENTRAL, COULEUR_OPTIMISTE],
        )

        total_investi = resultats["central"].total_investi
        gains_central = resultats["central"].gains
        st.markdown(
            f"**Total versé : {_formater_euros(total_investi)}** · "
            f"**Gains estimés (scénario central) : {_formater_euros(gains_central)}**"
        )

        if rendement_pessimiste < 0 or (categorie == "Actions" and nom_choisi != "— Aucun (saisie manuelle) —" and infos_actif["rendement_pessimiste"] < 0.02):
            st.error(
                "🔴 Le scénario pessimiste de cet actif est proche de zéro ou négatif. "
                "Une action individuelle peut sous-performer fortement, voire faire faillite. "
                "Ne mets pas dans une seule action plus que ce que tu es prêt à perdre."
            )

        st.divider()

        if bouton_valider:
            nouvelle_position = {
                "nom": nom_affiche,
                "type": infos_actif.get("type", categorie),
                "investissement_initial": investissement_initial,
                "apport_mensuel": apport_mensuel,
                "duree_annees": duree_annees,
                "rendement_pessimiste": rendement_pessimiste,
                "rendement_central": rendement_central,
                "rendement_optimiste": rendement_optimiste,
                "valeur_finale_pessimiste": resultats["pessimiste"].valeur_finale,
                "valeur_finale_centrale": resultats["central"].valeur_finale,
                "valeur_finale_optimiste": resultats["optimiste"].valeur_finale,
                "total_investi": resultats["central"].total_investi,
                "historique_central": resultats["central"].historique_annuel,
            }
            st.session_state.portefeuille = ajouter_position(
                st.session_state.portefeuille, nouvelle_position
            )
            st.success(f"💰 « {nom_affiche} » ajouté à tes investissements.")


# ===========================================================================
# ONGLET 2 — MON PORTEFEUILLE
# ===========================================================================
with onglet_portefeuille:

    positions = st.session_state.portefeuille

    from persistence import _mode_google_sheets_disponible
    if _mode_google_sheets_disponible():
        st.caption("☁️ Stockage : Google Sheets (synchronisé entre tous tes appareils)")
    else:
        st.caption("💻 Stockage : fichier local (visible uniquement sur cette machine)")

    if not positions:
        st.info(
            "Ton portefeuille est vide. Va dans l'onglet **Simulateur**, configure une "
            "simulation, puis clique sur **Investir** pour l'ajouter ici."
        )
    else:
        st.subheader("Vue d'ensemble")

        total_investi_global = sum(p["total_investi"] for p in positions)
        total_central_global = sum(p["valeur_finale_centrale"] for p in positions)
        total_pessimiste_global = sum(p["valeur_finale_pessimiste"] for p in positions)
        total_optimiste_global = sum(p["valeur_finale_optimiste"] for p in positions)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total versé", _formater_euros(total_investi_global))
        k2.metric("Projection pessimiste", _formater_euros(total_pessimiste_global))
        k3.metric("Projection centrale", _formater_euros(total_central_global))
        k4.metric("Projection optimiste", _formater_euros(total_optimiste_global))

        st.caption(
            "Ces totaux additionnent les projections individuelles de chaque position, "
            "à leurs durées respectives — voir détail de chaque position ci-dessous."
        )

        st.markdown("#### Progression cumulée du portefeuille (scénario central)")
        cumul = calculer_portefeuille_cumule(positions)
        if cumul:
            df_cumul = pd.DataFrame({
                "Année": list(range(1, len(cumul) + 1)),
                "Valeur cumulée (€)": cumul,
            }).set_index("Année")
            st.area_chart(df_cumul, color=COULEUR_PRINCIPALE)
            st.caption(
                "⚠️ Pour les positions dont la durée simulée est dépassée, la valeur est "
                "supposée rester constante (simplification) — elles ne génèrent plus de "
                "rendement dans ce graphique au-delà de leur durée initiale."
            )

        st.divider()
        st.subheader("Mes positions")

        for position in positions:
            with st.expander(
                f"**{position['nom']}** — {position['type']} · "
                f"{_formater_euros(position['valeur_finale_centrale'])} projeté "
                f"sur {position['duree_annees']} ans"
            ):
                col_a, col_b = st.columns([2, 1])

                with col_a:
                    st.write(f"**Type :** {position['type']}")
                    st.write(f"**Investissement initial :** {_formater_euros(position['investissement_initial'])}")
                    st.write(f"**Apport mensuel :** {_formater_euros(position['apport_mensuel'])}")
                    st.write(f"**Durée simulée :** {position['duree_annees']} ans")
                    st.write(f"**Date d'ajout :** {position.get('date_ajout', 'inconnue')}")

                    tri_approx = taux_rendement_annualise_approx(
                        position["valeur_finale_centrale"],
                        position["total_investi"],
                        position["duree_annees"],
                    )
                    st.write(f"**TRI approximatif (scénario central) :** {tri_approx*100:.1f} %/an")
                    st.caption("TRI approximatif et simplifié — ne tient pas compte précisément de l'étalement réel des apports.")

                with col_b:
                    st.metric("Total versé", _formater_euros(position["total_investi"]))
                    gains = position["valeur_finale_centrale"] - position["total_investi"]
                    st.metric(
                        "Gains estimés (central)",
                        _formater_euros(gains),
                        delta=f"{(gains/position['total_investi']*100) if position['total_investi'] else 0:.1f} %",
                    )

                if position.get("historique_central"):
                    df_pos = pd.DataFrame({
                        "Année": list(range(1, len(position["historique_central"]) + 1)),
                        "Valeur (€)": position["historique_central"],
                    }).set_index("Année")
                    st.line_chart(df_pos, color=COULEUR_PRINCIPALE)

                if st.button("🗑️ Supprimer cette position", key=f"suppr_{position['id']}"):
                    st.session_state.portefeuille = supprimer_position(
                        st.session_state.portefeuille, position["id"]
                    )
                    st.rerun()
