"""
persistence.py — Lecture/écriture du portefeuille sur Google Sheets.

Architecture : chaque position est stockée comme UNE ligne dans la feuille,
avec deux colonnes : "id" (entier) et "donnees_json" (le dict complet de la
position, sérialisé en JSON). On ne découpe pas chaque champ en colonne
séparée car certains champs sont des listes (ex: historique_central), ce
qui serait pénible à représenter proprement en colonnes Sheets — stocker le
JSON brut est plus robuste si le format de données évolue plus tard.

CONFIGURATION REQUISE (voir GUIDE_CONFIGURATION.md pour le détail pas à pas) :
1. Un compte de service Google Cloud avec l'API Google Sheets activée.
2. Un fichier de credentials JSON (ou ses champs collés dans les secrets
   Streamlit), partagé en écriture avec la feuille Google Sheets cible.
3. Dans .streamlit/secrets.toml (en local) ou les "Secrets" de l'app sur
   Streamlit Cloud (en ligne), une section [gcp_service_account] avec les
   champs du compte de service, + une clé "sheet_id" avec l'ID de la feuille.

REPLI AUTOMATIQUE : si ces secrets ne sont pas configurés (ex: pendant que
tu développes encore en local sans les avoir mis en place), l'app retombe
automatiquement sur un fichier portefeuille.json local, pour ne jamais être
bloquée. Un message d'avertissement s'affiche dans ce cas.
"""

import json
import os
from typing import List, Dict
from datetime import datetime

NOM_FEUILLE = "Portefeuille"  # nom de l'onglet dans le Google Sheet
CHEMIN_FICHIER_LOCAL = os.path.join(os.path.dirname(__file__), "portefeuille.json")


def _mode_google_sheets_disponible() -> bool:
    """Vérifie si les secrets Streamlit pour Google Sheets sont configurés."""
    try:
        import streamlit as st
        return "gcp_service_account" in st.secrets and "sheet_id" in st.secrets
    except Exception:
        return False


def _obtenir_feuille():
    """Retourne l'objet worksheet gspread, en le créant si besoin."""
    import streamlit as st
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]), scopes=scopes
    )
    client = gspread.authorize(credentials)
    classeur = client.open_by_key(st.secrets["sheet_id"])

    try:
        feuille = classeur.worksheet(NOM_FEUILLE)
    except gspread.WorksheetNotFound:
        feuille = classeur.add_worksheet(title=NOM_FEUILLE, rows=1000, cols=2)
        feuille.update([["id", "donnees_json"]])  # en-têtes

    return feuille


# ---------------------------------------------------------------------------
# API publique — identique à l'ancienne version basée sur JSON local, pour
# qu'app.py n'ait pas besoin de changer.
# ---------------------------------------------------------------------------

def charger_portefeuille() -> List[Dict]:
    """Charge la liste des positions depuis Google Sheets (ou le JSON local en repli)."""
    if _mode_google_sheets_disponible():
        try:
            feuille = _obtenir_feuille()
            lignes = feuille.get_all_values()
            positions = []
            for ligne in lignes[1:]:  # on saute l'en-tête
                if len(ligne) >= 2 and ligne[1].strip():
                    try:
                        positions.append(json.loads(ligne[1]))
                    except json.JSONDecodeError:
                        continue
            return positions
        except Exception:
            # En cas de problème réseau/config, on ne plante pas l'app :
            # on retombe sur le fichier local s'il existe.
            return _charger_local()
    return _charger_local()


def ajouter_position(positions: List[Dict], nouvelle_position: Dict) -> List[Dict]:
    """Ajoute une position avec un identifiant unique et un horodatage, sauvegarde, et retourne la liste mise à jour."""
    nouvelle_position = dict(nouvelle_position)  # copie défensive
    nouvelle_position["id"] = _generer_id(positions)
    nouvelle_position["date_ajout"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    positions = positions + [nouvelle_position]

    if _mode_google_sheets_disponible():
        try:
            feuille = _obtenir_feuille()
            feuille.append_row([
                str(nouvelle_position["id"]),
                json.dumps(nouvelle_position, ensure_ascii=False),
            ])
            return positions
        except Exception:
            pass  # on retombe sur le local ci-dessous si Sheets échoue

    _sauvegarder_local(positions)
    return positions


def supprimer_position(positions: List[Dict], position_id: int) -> List[Dict]:
    """Retire une position par son id, sauvegarde, et retourne la liste mise à jour."""
    positions = [p for p in positions if p.get("id") != position_id]

    if _mode_google_sheets_disponible():
        try:
            feuille = _obtenir_feuille()
            lignes = feuille.get_all_values()
            for idx, ligne in enumerate(lignes[1:], start=2):  # ligne 1 = en-tête
                if len(ligne) >= 1 and ligne[0] == str(position_id):
                    feuille.delete_rows(idx)
                    break
            return positions
        except Exception:
            pass

    _sauvegarder_local(positions)
    return positions


def _generer_id(positions: List[Dict]) -> int:
    """Génère un id entier croissant simple (max existant + 1)."""
    if not positions:
        return 1
    return max(p.get("id", 0) for p in positions) + 1


# ---------------------------------------------------------------------------
# Repli local (fichier JSON) — utilisé si Google Sheets n'est pas configuré
# ou momentanément indisponible.
# ---------------------------------------------------------------------------

def _charger_local() -> List[Dict]:
    if not os.path.exists(CHEMIN_FICHIER_LOCAL):
        return []
    try:
        with open(CHEMIN_FICHIER_LOCAL, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _sauvegarder_local(positions: List[Dict]) -> None:
    with open(CHEMIN_FICHIER_LOCAL, "w", encoding="utf-8") as f:
        json.dump(positions, f, ensure_ascii=False, indent=2)
