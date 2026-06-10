"""
SafariFX — FX Rate Aggregation Service
========================================

Aggregates and analyses foreign-exchange rates from multiple Kenyan
commercial banks.  In production this service would poll live bank APIs
and the CBK indicative rate feed; for development it loads data from
``../data/mock_rates.json``.

Key capabilities:
  • Current rate retrieval across all configured banks
  • Historical rate series for trend analysis
  • Cross-bank spread comparison and ranking
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from models import BankRate

logger = logging.getLogger("safarifx.rate_service")

# Path to mock data file (relative to this module)
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_MOCK_RATES_PATH = _DATA_DIR / "mock_rates.json"


class RateService:
    """
    FX rate aggregation and analysis service.

    Loads bank rate data from ``mock_rates.json`` on first access and
    caches it in memory.  Provides methods for current-rate retrieval,
    historical trend access, and spread analytics.
    """

    def __init__(self) -> None:
        self._raw_data: dict[str, Any] | None = None
        self._rates_cache: list[BankRate] | None = None

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def _load_data(self) -> dict[str, Any]:
        """Load and cache the raw JSON rate data from disk."""
        if self._raw_data is not None:
            return self._raw_data

        if not _MOCK_RATES_PATH.exists():
            logger.error("Mock rates file not found at %s", _MOCK_RATES_PATH)
            raise FileNotFoundError(
                f"Rate data file not found: {_MOCK_RATES_PATH}"
            )

        with open(_MOCK_RATES_PATH, encoding="utf-8") as fh:
            self._raw_data = json.load(fh)
            logger.info(
                "Loaded rates for %d banks from %s",
                len(self._raw_data.get("banks", [])),
                _MOCK_RATES_PATH,
            )
        return self._raw_data

    def _parse_bank_rates(self) -> list[BankRate]:
        """Parse raw JSON bank entries into validated ``BankRate`` models."""
        if self._rates_cache is not None:
            return self._rates_cache

        data = self._load_data()
        rates: list[BankRate] = []

        for entry in data.get("banks", []):
            try:
                rate = BankRate(
                    bank_name=entry["bank_name"],
                    bank_code=entry["bank_code"],
                    buy_rate=entry["buy_rate"],
                    sell_rate=entry["sell_rate"],
                    spread=entry["spread"],
                    liquidity_indicator=entry["liquidity_indicator"],
                    swift_fee=entry["swift_fee"],
                    commission_pct=entry["commission_pct"],
                    timestamp=datetime.fromisoformat(entry["timestamp"]),
                    trend_7d=entry["trend_7d"],
                )
                rates.append(rate)
            except Exception as exc:
                logger.warning(
                    "Skipping malformed bank entry '%s': %s",
                    entry.get("bank_name", "?"),
                    exc,
                )

        self._rates_cache = rates
        return rates

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_current_rates(self) -> list[BankRate]:
        """
        Return the latest FX rates for all configured banks.

        Returns:
            A list of ``BankRate`` objects sorted by spread (tightest first).
        """
        rates = self._parse_bank_rates()
        return sorted(rates, key=lambda r: r.spread)

    def get_historical_rates(self, days: int = 7) -> dict[str, Any]:
        """
        Return historical rate series for all banks.

        Parameters:
            days: Number of historical days to include (7 or 14).

        Returns:
            A dictionary keyed by bank code, each value a list of daily
            buy rates (oldest → newest).
        """
        data = self._load_data()
        historical = data.get("historical", {})

        # Pick the correct series based on requested window
        if days <= 7:
            series_key = "7d"
        else:
            series_key = "14d"

        series = historical.get(series_key, {})

        return {
            "period": series_key,
            "days": days,
            "banks": series,
            "cbk_indicative_rate": data.get("cbk_indicative_rate"),
            "interbank_rate": data.get("interbank_rate"),
            "next_cbk_auction": data.get("next_cbk_auction"),
        }

    def compute_spread_analysis(self) -> dict[str, Any]:
        """
        Compute a comprehensive spread comparison across all banks.

        Returns:
            A dictionary containing:
              - ``rankings``:  Banks ranked by effective cost (spread + fees).
              - ``best_bank``:  Bank with lowest total effective cost.
              - ``worst_bank``:  Bank with highest total effective cost.
              - ``spread_range``: Min and max spreads in KES.
              - ``average_spread``:  Mean spread across banks.
              - ``cbk_indicative_rate``:  CBK's published midrate.
              - ``interbank_rate``:  Current interbank midrate.
        """
        rates = self.get_current_rates()
        data = self._load_data()

        if not rates:
            return {"error": "No rate data available"}

        # Compute effective cost per USD 10,000 transfer for apples-to-apples
        # comparison: (sell_rate × amount) + swift_fee + (amount × commission%)
        reference_amount = 10_000.0
        rankings: list[dict[str, Any]] = []

        for rate in rates:
            fx_cost = rate.sell_rate * reference_amount
            swift_cost = rate.swift_fee
            commission_cost = reference_amount * (rate.commission_pct / 100.0)
            total_cost_kes = fx_cost + (swift_cost * rate.sell_rate) + commission_cost

            # 7-day trend direction
            trend = rate.trend_7d
            trend_delta = trend[-1] - trend[0]
            trend_direction = (
                "appreciating" if trend_delta < 0
                else "depreciating" if trend_delta > 0
                else "stable"
            )

            rankings.append({
                "bank_name": rate.bank_name,
                "bank_code": rate.bank_code,
                "sell_rate": rate.sell_rate,
                "spread": rate.spread,
                "swift_fee_usd": rate.swift_fee,
                "commission_pct": rate.commission_pct,
                "total_cost_kes_per_10k": round(total_cost_kes, 2),
                "liquidity": rate.liquidity_indicator.value,
                "trend_7d_direction": trend_direction,
                "trend_7d_delta_kes": round(trend_delta, 2),
            })

        # Sort by total effective cost (ascending = cheapest first)
        rankings.sort(key=lambda r: r["total_cost_kes_per_10k"])

        spreads = [r.spread for r in rates]

        return {
            "reference_amount_usd": reference_amount,
            "rankings": rankings,
            "best_bank": rankings[0]["bank_name"] if rankings else None,
            "worst_bank": rankings[-1]["bank_name"] if rankings else None,
            "spread_range": {
                "min_kes": min(spreads),
                "max_kes": max(spreads),
            },
            "average_spread_kes": round(sum(spreads) / len(spreads), 4),
            "cbk_indicative_rate": data.get("cbk_indicative_rate"),
            "interbank_rate": data.get("interbank_rate"),
            "next_cbk_auction": data.get("next_cbk_auction"),
        }
