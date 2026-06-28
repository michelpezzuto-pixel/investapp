"""
calculs.py — Logique financière pure (aucune dépendance Streamlit ici).

Toutes les fonctions sont testables indépendamment de l'interface.
Convention : les rendements sont des décimaux (0.08 = 8%), les durées en années,
les montants en euros.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ResultatProjection:
    """Résultat d'une simulation pour un seul scénario (ex: 'central')."""
    valeur_finale: float
    total_investi: float
    gains: float
    historique_annuel: List[float] = field(default_factory=list)  # valeur du portefeuille année par année


def projeter_investissement(
    investissement_initial: float,
    apport_mensuel: float,
    duree_annees: int,
    rendement_annuel: float,
) -> ResultatProjection:
    """
    Calcule la projection d'un investissement avec intérêts composés et apports
    mensuels réguliers.

    Méthode : on simule mois par mois (plus précis que d'appliquer le rendement
    une seule fois par an sur un apport annuel forfaitaire), avec un rendement
    mensuel équivalent dérivé du rendement annuel composé.

    Args:
        investissement_initial: capital de départ (€)
        apport_mensuel: versement mensuel constant (€)
        duree_annees: durée de la simulation (années)
        rendement_annuel: rendement annuel attendu (décimal, ex 0.08)

    Returns:
        ResultatProjection avec valeur finale, total investi, gains, et
        l'historique de la valeur du portefeuille à la fin de chaque année.
    """
    if duree_annees <= 0:
        return ResultatProjection(
            valeur_finale=investissement_initial,
            total_investi=investissement_initial,
            gains=0.0,
            historique_annuel=[investissement_initial],
        )

    rendement_mensuel = (1 + rendement_annuel) ** (1 / 12) - 1

    capital = investissement_initial
    total_investi = investissement_initial
    historique_annuel = []

    nb_mois = duree_annees * 12
    for mois in range(1, nb_mois + 1):
        capital = capital * (1 + rendement_mensuel) + apport_mensuel
        total_investi += apport_mensuel
        if mois % 12 == 0:
            historique_annuel.append(round(capital, 2))

    gains = capital - total_investi

    return ResultatProjection(
        valeur_finale=round(capital, 2),
        total_investi=round(total_investi, 2),
        gains=round(gains, 2),
        historique_annuel=historique_annuel,
    )


def projeter_trois_scenarios(
    investissement_initial: float,
    apport_mensuel: float,
    duree_annees: int,
    rendement_pessimiste: float,
    rendement_central: float,
    rendement_optimiste: float,
) -> Dict[str, ResultatProjection]:
    """
    Calcule les trois scénarios (pessimiste / central / optimiste) en une fois.
    C'est la fonction principale à appeler depuis l'interface du simulateur.
    """
    return {
        "pessimiste": projeter_investissement(
            investissement_initial, apport_mensuel, duree_annees, rendement_pessimiste
        ),
        "central": projeter_investissement(
            investissement_initial, apport_mensuel, duree_annees, rendement_central
        ),
        "optimiste": projeter_investissement(
            investissement_initial, apport_mensuel, duree_annees, rendement_optimiste
        ),
    }


def calculer_portefeuille_cumule(positions: List[dict]) -> List[float]:
    """
    Additionne les projections (scénario central) de toutes les positions
    validées du portefeuille, année par année, pour le graphique global.

    Chaque position est un dict tel que stocké dans portefeuille.json, avec
    une clé 'historique_central' (liste de valeurs annuelles).

    Si les positions ont des durées différentes, on aligne sur la durée max :
    une position terminée garde sa valeur finale constante (capital qui ne
    bouge plus une fois la durée simulée écoulée — hypothèse simplificatrice
    à signaler à l'utilisateur).
    """
    if not positions:
        return []

    duree_max = max(len(p.get("historique_central", [])) for p in positions)
    cumul = [0.0] * duree_max

    for p in positions:
        historique = p.get("historique_central", [])
        if not historique:
            continue
        derniere_valeur = historique[-1]
        for annee in range(duree_max):
            if annee < len(historique):
                cumul[annee] += historique[annee]
            else:
                # Position déjà arrivée à terme : on garde sa valeur finale (simplification)
                cumul[annee] += derniere_valeur

    return [round(v, 2) for v in cumul]


def taux_rendement_annualise_approx(valeur_finale: float, total_investi: float, duree_annees: int) -> float:
    """
    Calcule un TRI (taux de rendement interne) APPROXIMATIF, en supposant que
    tout le capital avait été investi dès le départ (approximation grossière,
    car en réalité les apports sont étalés dans le temps — un vrai TRI exigerait
    un calcul XIRR sur les flux datés). Utile comme indicateur comparatif simple,
    pas comme métrique précise.
    """
    if total_investi <= 0 or duree_annees <= 0:
        return 0.0
    ratio = valeur_finale / total_investi
    if ratio <= 0:
        return -1.0
    return ratio ** (1 / duree_annees) - 1
