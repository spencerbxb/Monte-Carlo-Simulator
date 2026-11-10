# 0 = English, 1 = French
PORTFOLIOPARAMETER = ('Portfolio parameters', 'Paramètres du portefeuille')
SYMBOL = ('Symbol', 'Symbole')
WEIGHT = ('Weight (%)', 'Pondération (%)')
ADD_ASSET = ('+ Add stock', '+ Ajouter une action')
SIMULATION = ('Simulation', 'Simulation')
INITIAL_CAPITAL = ('Initial capital ($)', 'Capital initial ($)')
SIMULATION_COUNT = ('Number of simulations', 'Nombre de simulations')
TIME_HORIZON = ('Horizon (trading days)', 'Horizon (jours de bourse)')
HISTORY = ('History (calendar days)', 'Historique (jours civils)')
APPLY = ('Apply — Simulate', 'Appliquer — Simuler')
READY = ('Ready.', 'Prêt.')
RUNNING = ('Downloading data and simulating…', 'Téléchargement et simulation en cours…')
RESULTS = ('Results', 'Résultats')
NO_RESULTS = ('Run a simulation to display statistics.', 'Lancez une simulation pour afficher les statistiques.')
CHART_TITLE = ('Simulated portfolio trajectories', 'Trajectoires simulées du portefeuille')
CHART_X = ('Trading days', 'Jours de bourse')
CHART_Y = ('Portfolio value ($)', 'Valeur du portefeuille ($)')
MEDIAN = ('Median', 'Médiane')
PORTFOLIO = ('Portfolio', 'Portefeuille')
KEEP_ASSET = ('Keep at least one stock.', 'Conservez au moins une action.')
INVALID_INPUT = ('Invalid input', 'Entrée invalide')
CHECK_NUMBERS = ('Check the entered numbers.', 'Vérifiez les nombres saisis.')
ERROR = ('Error', 'Erreur')
SIMULATION_FAILED = ('Simulation failed.', 'Échec de la simulation.')
SIMULATIONS_COMPLETED = ('{} simulations completed.', '{} simulations terminées.')
LANGUAGE = ('Language', 'Langue')
MEAN_FINAL = ('Mean final value', 'Valeur finale moyenne')
MEDIAN_FINAL = ('Median final value', 'Valeur finale médiane')
PERCENTILE_5 = ('5th percentile', '5e percentile')
PERCENTILE_95 = ('95th percentile', '95e percentile')
LOSS_PROBABILITY = ('Probability of loss', 'Probabilité de perte')


# Portfolio validation errors
EMPTY_SYMBOL = (
    "Every stock must have a non-empty ticker symbol.",
    "Chaque action doit avoir un symbole boursier non vide."
)

DUPLICATE_SYMBOL = (
    "Stock ticker symbols must be unique.",
    "Les symboles boursiers doivent être uniques."
)

INVALID_WEIGHTS = (
    "Portfolio weights must be finite, non-negative numbers.",
    "Les pondérations doivent être des nombres finis, positifs ou nuls."
)

WEIGHTS_SUM = (
    "Portfolio weights must add up to 100%.",
    "La somme des pondérations doit être égale à 100 %."
)

INVALID_CAPITAL = (
    "Initial capital must be greater than zero.",
    "Le capital initial doit être strictement positif."
)

INVALID_SIMULATION_PARAMS = (
    "Simulations: 1 to 10,000; horizon: 1 to 2,520 days.",
    "Simulations : 1 à 10 000 ; horizon : 1 à 2 520 jours."
)

INVALID_HISTORY = (
    "Historical data must cover at least 60 calendar days.",
    "L'historique doit couvrir au moins 60 jours civils."
)

# Market data errors
NO_DATA = (
    "No data could be downloaded from Yahoo Finance.",
    "Aucune donnée n'a pu être téléchargée depuis Yahoo Finance."
)

MISSING_DATA = (
    "No market data available for: {}",
    "Aucune donnée boursière disponible pour : {}"
)

INSUFFICIENT_HISTORY = (
    "Insufficient historical data: fewer than 20 common daily returns.",
    "Historique insuffisant : moins de 20 rendements quotidiens communs."
)

DOWNLOAD_FAILED = (
    "Failed to download market data: {}",
    "Échec du téléchargement des données boursières : {}"
)

# Mathematical errors
INVALID_COVARIANCE = (
    "The covariance matrix is not positive semidefinite.",
    "La matrice de covariance n'est pas semi-définie positive."
)

# Simulation summary
MEAN_FINAL = ("Mean final value", "Valeur finale moyenne")
MEDIAN_FINAL = ("Median final value", "Valeur finale médiane")
PERCENTILE_5 = ("5th percentile", "5e percentile")
PERCENTILE_95 = ("95th percentile", "95e percentile")
LOSS_PROBABILITY = ("Probability of loss", "Probabilité de perte")