from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import yfinance as yf

import textcontent as tx

def tr(message, language=0):
    return message[language]

@dataclass
class SimulationResult:
    paths: np.ndarray
    final_values: np.ndarray
    mean_returns: pd.Series
    covariance: pd.DataFrame
    tickers: list[str]
    weights: np.ndarray
    initial_capital: float


    def summary(self, language=0) -> dict:
        v = self.final_values

        return {
            tr(tx.MEAN_FINAL, language): float(np.mean(v)),
            tr(tx.MEDIAN_FINAL, language): float(np.median(v)),
            tr(tx.PERCENTILE_5, language): float(np.percentile(v, 5)),
            tr(tx.PERCENTILE_95, language): float(np.percentile(v, 95)),
            tr(tx.LOSS_PROBABILITY, language): float(
                np.mean(v < self.initial_capital)
            ),
        }


def validate_portfolio(
    tickers: list[str],
    weights: list[float],
    language: int = 0
) -> tuple[list[str], np.ndarray]:

    symbols = [s.strip().upper() for s in tickers]

    if not symbols or any(not s for s in symbols):
        raise ValueError(tr(tx.EMPTY_SYMBOL, language))

    if len(set(symbols)) != len(symbols):
        raise ValueError(tr(tx.DUPLICATE_SYMBOL, language))

    try:
        w = np.asarray(weights, dtype=float)
    except (TypeError, ValueError):
        raise ValueError(tr(tx.INVALID_WEIGHTS, language)) from None

    if (
        len(w) != len(symbols)
        or not np.all(np.isfinite(w))
        or np.any(w < 0)
    ):
        raise ValueError(tr(tx.INVALID_WEIGHTS, language))

    if not np.isclose(w.sum(), 100, atol=0.01):
        raise ValueError(tr(tx.WEIGHTS_SUM, language))

    return symbols, w / 100.0

def get_data(
    tickers: list[str],
    lookback_days: int = 300,
    language: int = 0
) -> tuple[pd.Series, pd.DataFrame]:

    end = datetime.now()
    start = end - timedelta(days=lookback_days)

    try:
        raw = yf.download(
            tickers,
            start=start,
            end=end,
            auto_adjust=True,
            progress=False,
            threads=False
        )
    except Exception as exc:
        raise ValueError(
            tr(tx.DOWNLOAD_FAILED, language).format(str(exc))
        ) from exc

    if raw.empty or 'Close' not in raw:
        raise ValueError(tr(tx.NO_DATA, language))

    prices = raw['Close']

    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    missing = [
        t for t in tickers
        if t not in prices.columns or prices[t].dropna().empty
    ]

    if missing:
        raise ValueError(
            tr(tx.MISSING_DATA, language).format(', '.join(missing))
        )

    prices = prices.loc[:, tickers].dropna()

    returns = prices.pct_change(fill_method=None).dropna()

    if len(returns) < 20:
        raise ValueError(tr(tx.INSUFFICIENT_HISTORY, language))

    return returns.mean(), returns.cov()



def simulate(
    tickers: list[str],
    percentages: list[float],
    initial_capital: float,
    simulations: int,
    days: int,
    lookback_days: int = 300,
    seed: int | None = None,
    language: int = 0
) -> SimulationResult:

    tickers, weights = validate_portfolio(
        tickers, percentages, language
    )

    if not np.isfinite(initial_capital) or initial_capital <= 0:
        raise ValueError(tr(tx.INVALID_CAPITAL, language))

    if not (1 <= simulations <= 10000 and 1 <= days <= 2520):
        raise ValueError(tr(tx.INVALID_SIMULATION_PARAMS, language))

    if lookback_days < 60:
        raise ValueError(tr(tx.INVALID_HISTORY, language))

    mu, cov = get_data(tickers, lookback_days, language)

    matrix = cov.to_numpy()

    eigvals, eigvecs = np.linalg.eigh(matrix)

    if eigvals.min() < -1e-9:
        raise ValueError(tr(tx.INVALID_COVARIANCE, language))

    factor = eigvecs @ np.diag(
        np.sqrt(np.maximum(eigvals, 0))
    )

    rng = np.random.default_rng(seed)

    paths = np.empty(
        (days + 1, simulations),
        dtype=float
    )

    paths[0] = initial_capital

    for j in range(simulations):
        z = rng.standard_normal((len(tickers), days))

        daily = mu.to_numpy()[:, None] + factor @ z

        portfolio_daily = weights @ daily

        paths[1:, j] = (
            initial_capital
            * np.cumprod(1 + portfolio_daily)
        )

    return SimulationResult(
        paths,
        paths[-1].copy(),
        mu,
        cov,
        tickers,
        weights,
        initial_capital
    )

