"""
data.py — Base de données statique des actifs (Actions & ETF)

⚠️ IMPORTANT — LIS CECI AVANT DE MODIFIER :
Les rendements ci-dessous sont des moyennes ANNUALISÉES HISTORIQUES (approximatives,
sur ~20 à 30 ans selon les données disponibles, ou depuis la création de l'actif s'il
est plus récent). Ce ne sont PAS des garanties et PAS des prévisions.

"rendement_central" = exactement la moyenne historique annualisée sur la période
(≈30 ans quand l'historique existe). "rendement_pessimiste" / "rendement_optimiste"
= bornes basse/haute pour montrer la variance réelle vécue par l'actif (ex: pire et
meilleure décennie), pas des scénarios futurs différents.

Pour les ACTIONS individuelles en particulier : un rendement passé élevé sur 30 ans
reflète souvent un "survivant" (l'entreprise a eu un parcours exceptionnel et rare).
Une entreprise qui a fait +20%/an pendant 30 ans est une exception statistique, pas
une norme reproductible. Ne traite jamais ces chiffres comme des prévisions fiables.

Pour les ETF (indices larges diversifiés), l'historique est plus représentatif car
il lisse les échecs individuels d'entreprises, mais reste un historique, pas une
promesse sur les 30 prochaines années.

➕ POUR AJOUTER TES PROPRES ACTIFS :
Ajoute simplement une entrée dans le dictionnaire correspondant, au format :
    "Nom affiché": {
        "rendement_central": 0.XX,   # moyenne historique annualisée (décimal, ex: 0.08 = 8%)
        "rendement_pessimiste": 0.XX,
        "rendement_optimiste": 0.XX,
        "type": "Action" ou "ETF",
        "note": "courte note de contexte (optionnel)"
    }
"""

# ---------------------------------------------------------------------------
# ACTIONS INDIVIDUELLES
# Rendements indicatifs. Le scénario pessimiste pour une action individuelle
# inclut volontairement la possibilité de perte (rendement négatif ou proche
# de zéro) car le risque idiosyncratique (faillite, déclin sectoriel) est réel.
# ---------------------------------------------------------------------------
ACTIONS = {
    # --- Technologie US ---
    "Apple (AAPL)": {
        "rendement_central": 0.20, "rendement_pessimiste": 0.04, "rendement_optimiste": 0.28,
        "type": "Action", "note": "Croissance exceptionnelle historique (2000-2024). Non garantie pour le futur.",
    },
    "Microsoft (MSFT)": {
        "rendement_central": 0.18, "rendement_pessimiste": 0.05, "rendement_optimiste": 0.25,
        "type": "Action", "note": "Forte régularité historique, concentration sectorielle (tech/cloud).",
    },
    "Amazon (AMZN)": {
        "rendement_central": 0.22, "rendement_pessimiste": 0.00, "rendement_optimiste": 0.32,
        "type": "Action", "note": "Très volatile. Croissance historique exceptionnelle, marges faibles.",
    },
    "Alphabet / Google (GOOGL)": {
        "rendement_central": 0.17, "rendement_pessimiste": 0.03, "rendement_optimiste": 0.24,
        "type": "Action", "note": "Historique depuis 2004 (IPO). Dépendance forte à la publicité.",
    },
    "Meta / Facebook (META)": {
        "rendement_central": 0.16, "rendement_pessimiste": -0.30, "rendement_optimiste": 0.30,
        "type": "Action", "note": "Historique court (depuis 2012), a perdu ~70% en 2022 avant de remonter.",
    },
    "Nvidia (NVDA)": {
        "rendement_central": 0.35, "rendement_pessimiste": -0.15, "rendement_optimiste": 0.55,
        "type": "Action", "note": "Croissance extrême récente (IA), très haute volatilité, pas représentatif d'une norme.",
    },
    "Tesla (TSLA)": {
        "rendement_central": 0.25, "rendement_pessimiste": -0.10, "rendement_optimiste": 0.40,
        "type": "Action", "note": "Extrême volatilité. Le pessimiste inclut un scénario de perte réelle.",
    },
    "Netflix (NFLX)": {
        "rendement_central": 0.24, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.35,
        "type": "Action", "note": "A perdu ~75% en 2022, forte cyclicité.",
    },
    "IBM": {
        "rendement_central": 0.06, "rendement_pessimiste": -0.02, "rendement_optimiste": 0.10,
        "type": "Action", "note": "Croissance lente, sous-performance prolongée 2013-2020.",
    },
    "Intel (INTC)": {
        "rendement_central": 0.03, "rendement_pessimiste": -0.15, "rendement_optimiste": 0.10,
        "type": "Action", "note": "Forte perte de parts de marché récente, exemple de déclin sectoriel.",
    },

    # --- Finance ---
    "JPMorgan Chase (JPM)": {
        "rendement_central": 0.12, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.18,
        "type": "Action", "note": "Grande banque US, cyclique avec les taux d'intérêt.",
    },
    "Visa (V)": {
        "rendement_central": 0.19, "rendement_pessimiste": 0.05, "rendement_optimiste": 0.25,
        "type": "Action", "note": "Historique depuis IPO 2008, croissance régulière des paiements électroniques.",
    },
    "Berkshire Hathaway (BRK.B)": {
        "rendement_central": 0.10, "rendement_pessimiste": 0.02, "rendement_optimiste": 0.15,
        "type": "Action", "note": "Holding diversifié de Warren Buffett, volatilité plus faible que la moyenne.",
    },

    # --- Santé ---
    "Johnson & Johnson (JNJ)": {
        "rendement_central": 0.08, "rendement_pessimiste": 0.02, "rendement_optimiste": 0.12,
        "type": "Action", "note": "Très stable, dividendes réguliers depuis +60 ans.",
    },
    "Novo Nordisk (NVO)": {
        "rendement_central": 0.21, "rendement_pessimiste": -0.10, "rendement_optimiste": 0.32,
        "type": "Action", "note": "Forte croissance récente liée aux traitements anti-obésité (Ozempic).",
    },

    # --- Consommation ---
    "Coca-Cola (KO)": {
        "rendement_central": 0.09, "rendement_pessimiste": 0.03, "rendement_optimiste": 0.13,
        "type": "Action", "note": "Croissance lente mais historiquement stable, dividendes réguliers.",
    },
    "McDonald's (MCD)": {
        "rendement_central": 0.13, "rendement_pessimiste": 0.03, "rendement_optimiste": 0.18,
        "type": "Action", "note": "Croissance régulière, franchise mondiale.",
    },
    "Nike (NKE)": {
        "rendement_central": 0.11, "rendement_pessimiste": -0.10, "rendement_optimiste": 0.20,
        "type": "Action", "note": "Cyclique, sensible aux tendances de consommation.",
    },
    "Walmart (WMT)": {
        "rendement_central": 0.10, "rendement_pessimiste": 0.02, "rendement_optimiste": 0.15,
        "type": "Action", "note": "Distribution, croissance modérée mais résiliente en récession.",
    },

    # --- Europe ---
    "LVMH (MC.PA)": {
        "rendement_central": 0.13, "rendement_pessimiste": 0.02, "rendement_optimiste": 0.18,
        "type": "Action", "note": "Luxe européen, cyclique selon la conjoncture chinoise/mondiale.",
    },
    "L'Oréal (OR.PA)": {
        "rendement_central": 0.11, "rendement_pessimiste": 0.03, "rendement_optimiste": 0.16,
        "type": "Action", "note": "Cosmétiques, croissance régulière internationale.",
    },
    "ASML (ASML)": {
        "rendement_central": 0.24, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.35,
        "type": "Action", "note": "Quasi-monopole sur les machines de lithographie EUV (semi-conducteurs).",
    },
    "SAP (SAP.DE)": {
        "rendement_central": 0.10, "rendement_pessimiste": 0.01, "rendement_optimiste": 0.16,
        "type": "Action", "note": "Logiciel d'entreprise européen, croissance stable.",
    },
    "Total Energies (TTE.PA)": {
        "rendement_central": 0.07, "rendement_pessimiste": -0.10, "rendement_optimiste": 0.15,
        "type": "Action", "note": "Pétrole/gaz, très cyclique avec les prix de l'énergie.",
    },
    "Unilever (ULVR.L)": {
        "rendement_central": 0.07, "rendement_pessimiste": 0.01, "rendement_optimiste": 0.11,
        "type": "Action", "note": "Biens de consommation, croissance lente et stable.",
    },

    # --- Belgique ---
    "AB InBev (ABI.BR)": {
        "rendement_central": 0.04, "rendement_pessimiste": -0.10, "rendement_optimiste": 0.12,
        "type": "Action", "note": "Sous-performance prolongée depuis le rachat de SABMiller (2016), forte dette.",
    },
    "KBC Groupe (KBC.BR)": {
        "rendement_central": 0.11, "rendement_pessimiste": -0.15, "rendement_optimiste": 0.20,
        "type": "Action", "note": "Banque belge, cyclique, a connu la crise 2008 (quasi-faillite évitée par l'État).",
    },
    "UCB (UCB.BR)": {
        "rendement_central": 0.10, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.18,
        "type": "Action", "note": "Pharma belge, dépendante du succès de quelques molécules.",
    },

    # --- Asie ---
    "Toyota (7203.T)": {
        "rendement_central": 0.08, "rendement_pessimiste": -0.02, "rendement_optimiste": 0.14,
        "type": "Action", "note": "Constructeur auto japonais, croissance lente et stable.",
    },
    "Samsung Electronics (005930.KS)": {
        "rendement_central": 0.09, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.16,
        "type": "Action", "note": "Conglomérat tech coréen, cyclique avec les semi-conducteurs.",
    },
    "Alibaba (BABA)": {
        "rendement_central": 0.05, "rendement_pessimiste": -0.30, "rendement_optimiste": 0.20,
        "type": "Action", "note": "A perdu plus de 70% depuis son pic 2020, risque réglementaire chinois élevé.",
    },
    "TSMC (TSM)": {
        "rendement_central": 0.18, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.28,
        "type": "Action", "note": "Leader mondial de la fabrication de semi-conducteurs, risque géopolitique (Taïwan).",
    },
}

# ---------------------------------------------------------------------------
# ETF (FONDS INDICIELS DIVERSIFIÉS)
# Plus représentatifs sur longue durée car diversifiés, mais toujours soumis
# au risque de marché global (krach, stagnation prolongée type Japon 1990-2010).
# ---------------------------------------------------------------------------
ETFS = {
    # --- Indices larges US ---
    "S&P 500 (ex: IVV, VOO)": {
        "rendement_central": 0.10, "rendement_pessimiste": 0.04, "rendement_optimiste": 0.13,
        "type": "ETF", "note": "≈10%/an nominal historique depuis 1957 (dividendes réinvestis).",
    },
    "Nasdaq 100 (ex: QQQ)": {
        "rendement_central": 0.13, "rendement_pessimiste": 0.02, "rendement_optimiste": 0.18,
        "type": "ETF", "note": "Concentré tech/croissance. Plus volatil qu'un indice large.",
    },
    "Dow Jones (ex: DIA)": {
        "rendement_central": 0.09, "rendement_pessimiste": 0.03, "rendement_optimiste": 0.12,
        "type": "ETF", "note": "30 grandes capitalisations US historiques, moins de tech que le S&P 500.",
    },
    "Russell 2000 (ex: IWM)": {
        "rendement_central": 0.08, "rendement_pessimiste": -0.02, "rendement_optimiste": 0.13,
        "type": "ETF", "note": "Petites capitalisations US, plus volatil, plus sensible aux récessions.",
    },

    # --- Indices mondiaux ---
    "MSCI World (ex: IWDA)": {
        "rendement_central": 0.08, "rendement_pessimiste": 0.03, "rendement_optimiste": 0.11,
        "type": "ETF", "note": "Diversification mondiale (US, Europe, Japon...). Référence pour débutants.",
    },
    "MSCI ACWI (Monde + émergents)": {
        "rendement_central": 0.07, "rendement_pessimiste": 0.02, "rendement_optimiste": 0.11,
        "type": "ETF", "note": "MSCI World + marchés émergents inclus, diversification maximale.",
    },
    "MSCI Emerging Markets": {
        "rendement_central": 0.07, "rendement_pessimiste": -0.02, "rendement_optimiste": 0.12,
        "type": "ETF", "note": "Marchés émergents : potentiel plus élevé, risque devise/politique plus élevé.",
    },

    # --- Europe ---
    "Euro Stoxx 50": {
        "rendement_central": 0.06, "rendement_pessimiste": 0.01, "rendement_optimiste": 0.09,
        "type": "ETF", "note": "Grandes capitalisations européennes. Croissance historiquement plus lente que le S&P 500.",
    },
    "MSCI Europe": {
        "rendement_central": 0.06, "rendement_pessimiste": 0.00, "rendement_optimiste": 0.10,
        "type": "ETF", "note": "Europe élargie (hors zone euro uniquement), diversification sectorielle.",
    },
    "BEL 20 (Belgique)": {
        "rendement_central": 0.05, "rendement_pessimiste": -0.03, "rendement_optimiste": 0.09,
        "type": "ETF", "note": "Indice belge, faible diversification (20 valeurs), sous-performance vs indices mondiaux.",
    },
    "CAC 40 (France)": {
        "rendement_central": 0.06, "rendement_pessimiste": -0.01, "rendement_optimiste": 0.10,
        "type": "ETF", "note": "40 grandes capitalisations françaises.",
    },
    "DAX (Allemagne)": {
        "rendement_central": 0.08, "rendement_pessimiste": 0.00, "rendement_optimiste": 0.13,
        "type": "ETF", "note": "Indice allemand, fort poids industriel/automobile.",
    },

    # --- Asie ---
    "Nikkei 225 (Japon)": {
        "rendement_central": 0.04, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.10,
        "type": "ETF", "note": "A stagné ~20 ans après 1990 — exemple réel de marché qui ne monte pas toujours.",
    },
    "MSCI China": {
        "rendement_central": 0.04, "rendement_pessimiste": -0.15, "rendement_optimiste": 0.15,
        "type": "ETF", "note": "Risque réglementaire et géopolitique élevé, forte volatilité récente.",
    },

    # --- Sectoriels / thématiques ---
    "Technologie mondiale (ex: IXN)": {
        "rendement_central": 0.14, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.20,
        "type": "ETF", "note": "Concentré sur le secteur tech mondial, plus volatil qu'un indice large.",
    },
    "Énergie propre (ex: ICLN)": {
        "rendement_central": 0.02, "rendement_pessimiste": -0.20, "rendement_optimiste": 0.20,
        "type": "ETF", "note": "Très récent et volatil, a fortement chuté après son pic 2020-2021.",
    },
    "Immobilier mondial (REIT)": {
        "rendement_central": 0.07, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.12,
        "type": "ETF", "note": "Sensible aux taux d'intérêt, diversification hors actions classiques.",
    },

    # --- Obligataire / défensif ---
    "Obligations d'État monde (ex: AGGH)": {
        "rendement_central": 0.03, "rendement_pessimiste": 0.00, "rendement_optimiste": 0.05,
        "type": "ETF", "note": "Faible risque, faible rendement. Utile pour comparer/diversifier.",
    },
    "Obligations d'entreprises (Corporate Bonds)": {
        "rendement_central": 0.04, "rendement_pessimiste": 0.00, "rendement_optimiste": 0.06,
        "type": "ETF", "note": "Rendement légèrement supérieur aux obligations d'État, risque de défaut un peu plus élevé.",
    },
    "Or (ex: GLD)": {
        "rendement_central": 0.07, "rendement_pessimiste": -0.05, "rendement_optimiste": 0.15,
        "type": "ETF", "note": "Pas une action ni un ETF d'entreprises — valeur refuge, ne produit pas de dividende.",
    },
}

# Texte d'avertissement réutilisé partout dans l'app — ne pas retirer.
AVERTISSEMENT_RENDEMENTS = (
    "Les rendements affichés sont des **moyennes historiques approximatives**, "
    "pas des garanties. Les performances passées ne préjugent pas des performances "
    "futures. Pour une action individuelle, un historique flatteur reflète souvent "
    "un parcours exceptionnel et rare (biais du survivant), pas une norme. "
    "Cette application est un outil pédagogique de simulation, pas un conseil "
    "en investissement personnalisé."
)


def get_tous_les_actifs():
    """Retourne un dictionnaire fusionné {nom: infos} pour les deux catégories."""
    fusion = {}
    fusion.update(ACTIONS)
    fusion.update(ETFS)
    return fusion
