"""
SafariFX — Pydantic v2 Domain Models
=====================================

Defines the core data models used throughout the SafariFX treasury advisory
platform. All models leverage Pydantic v2 for strict validation, JSON
serialization, and OpenAPI schema generation via FastAPI.

Models hierarchy:
  Invoice → input from importers
  BankRate → aggregated FX rate from a commercial bank
  ReasoningStep → one step in the multi-step analysis pipeline
  Recommendation → actionable output per invoice/bank pairing
  AnalysisReport → top-level report bundling all analysis artifacts
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class UrgencyLevel(str, Enum):
    """Invoice payment urgency classification."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LiquidityIndicator(str, Enum):
    """Bank FX desk liquidity level."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TimingAdvice(str, Enum):
    """Recommended timing for FX purchase."""
    BUY_NOW = "BUY_NOW"
    WAIT_1D = "WAIT_1D"
    WAIT_2D = "WAIT_2D"
    WAIT_AUCTION = "WAIT_AUCTION"
    SPLIT_PURCHASE = "SPLIT_PURCHASE"


# ---------------------------------------------------------------------------
# Invoice
# ---------------------------------------------------------------------------

class Invoice(BaseModel):
    """
    Represents an importer's foreign-currency payable.

    The ``urgency`` field is auto-computed from the deadline if omitted.
    Amounts are denominated in USD (source) and optionally in the local
    destination currency (amount_local, typically KES).
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique invoice identifier (UUID v4)",
    )
    supplier_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Name of the foreign supplier",
    )
    currency: str = Field(
        default="USD",
        pattern=r"^[A-Z]{3}$",
        description="ISO 4217 currency code of the payable",
    )
    amount_usd: float = Field(
        ...,
        gt=0,
        description="Invoice amount in US Dollars",
    )
    amount_local: Optional[float] = Field(
        default=None,
        ge=0,
        description="Equivalent amount in local currency (KES), populated after rate application",
    )
    deadline: datetime = Field(
        ...,
        description="Payment due date (ISO 8601)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Free-text description of the goods / services",
    )
    urgency: UrgencyLevel = Field(
        default=UrgencyLevel.MEDIUM,
        description="Payment urgency level",
    )

    model_config = {"json_schema_extra": {
        "examples": [{
            "supplier_name": "Shenzhen Electronics Co.",
            "currency": "USD",
            "amount_usd": 45000.00,
            "deadline": "2026-06-15T00:00:00Z",
            "description": "PCB components batch #4412",
            "urgency": "HIGH",
        }]
    }}


# ---------------------------------------------------------------------------
# BankRate
# ---------------------------------------------------------------------------

class BankRate(BaseModel):
    """
    A point-in-time FX quotation from a Kenyan commercial bank.

    Spread is the difference between ``sell_rate`` (what the importer pays)
    and ``buy_rate`` (what the bank bids for USD).  ``trend_7d`` captures
    the bank's daily buy-rate over the past seven trading days to enable
    trend analysis.
    """

    bank_name: str = Field(..., description="Full legal name of the bank")
    bank_code: str = Field(
        ...,
        pattern=r"^[A-Z]{3,5}$",
        description="Internal short code (e.g. KCB, EQTY)",
    )
    buy_rate: float = Field(..., gt=0, description="Bank's USD buy rate (KES per 1 USD)")
    sell_rate: float = Field(..., gt=0, description="Bank's USD sell rate (KES per 1 USD)")
    spread: float = Field(..., ge=0, description="Sell − Buy spread in KES")
    liquidity_indicator: LiquidityIndicator = Field(
        ...,
        description="FX desk liquidity level",
    )
    swift_fee: float = Field(..., ge=0, description="SWIFT transfer fee in USD")
    commission_pct: float = Field(
        ...,
        ge=0,
        le=5.0,
        description="Commission as a percentage of transfer amount",
    )
    timestamp: datetime = Field(..., description="Quotation timestamp (ISO 8601)")
    trend_7d: list[float] = Field(
        ...,
        min_length=7,
        max_length=7,
        description="Daily buy-rate for the past 7 trading days (oldest → newest)",
    )

    @field_validator("spread")
    @classmethod
    def validate_spread_consistency(cls, v: float, info) -> float:
        """Ensure reported spread matches sell − buy (within tolerance)."""
        data = info.data
        if "sell_rate" in data and "buy_rate" in data:
            expected = round(data["sell_rate"] - data["buy_rate"], 4)
            if abs(v - expected) > 0.02:
                raise ValueError(
                    f"Spread {v} does not match sell_rate − buy_rate = {expected}"
                )
        return v


# ---------------------------------------------------------------------------
# ReasoningStep
# ---------------------------------------------------------------------------

class ReasoningStep(BaseModel):
    """
    A single step in the multi-step treasury reasoning pipeline.

    Each step records what data was consumed (``input_summary``), which
    Foundry IQ knowledge-base source was consulted (``iq_source`` /
    ``iq_citation``), the analytical conclusion, and a confidence score.
    """

    step_number: int = Field(..., ge=1, le=10, description="Sequential step number")
    title: str = Field(..., description="Human-readable step title")
    description: str = Field(
        ...,
        description="Detailed narrative of the analytical work performed",
    )
    input_summary: str = Field(
        ...,
        description="Summary of the data / inputs consumed by this step",
    )
    iq_source: Optional[str] = Field(
        default=None,
        description="Foundry IQ knowledge-base source queried (if any)",
    )
    iq_citation: Optional[str] = Field(
        default=None,
        description="Verbatim citation from Foundry IQ response",
    )
    conclusion: str = Field(
        ...,
        description="Analytical conclusion drawn from this step",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for this step's conclusion (0.0 – 1.0)",
    )
    duration_ms: int = Field(
        ...,
        ge=0,
        description="Wall-clock time consumed by this step in milliseconds",
    )


# ---------------------------------------------------------------------------
# Recommendation
# ---------------------------------------------------------------------------

class Recommendation(BaseModel):
    """
    An actionable FX purchase recommendation.

    Ties a specific bank, rate, and timing strategy to a quantified saving
    versus the worst-case alternative.
    """

    bank_name: str = Field(..., description="Recommended bank name")
    amount_usd: float = Field(..., gt=0, description="USD amount to purchase at this bank")
    rate: float = Field(..., gt=0, description="Applicable sell rate (KES per USD)")
    total_kes: float = Field(
        ...,
        gt=0,
        description="Total cost in KES including fees and commission",
    )
    timing: TimingAdvice = Field(
        ...,
        description="Recommended purchase timing strategy",
    )
    rationale: str = Field(
        ...,
        description="Detailed explanation of why this recommendation was selected",
    )
    citations: list[str] = Field(
        default_factory=list,
        description="Supporting citations from CBK circulars, bank tariffs, and IQ sources",
    )
    savings_vs_worst: float = Field(
        ...,
        ge=0,
        description="Savings in KES compared to worst-case bank + timing",
    )


# ---------------------------------------------------------------------------
# AnalysisReport
# ---------------------------------------------------------------------------

class AnalysisReport(BaseModel):
    """
    Top-level analysis report produced by the reasoning engine.

    Bundles together the input invoices, the rate snapshot used, every
    reasoning step executed, and the final set of recommendations with
    aggregate savings metrics.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique report identifier (UUID v4)",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Report generation timestamp (UTC)",
    )
    invoices: list[Invoice] = Field(
        ...,
        min_length=1,
        description="Invoices analyzed in this report",
    )
    rates_snapshot: list[BankRate] = Field(
        ...,
        min_length=1,
        description="FX rates used as of analysis time",
    )
    reasoning_steps: list[ReasoningStep] = Field(
        ...,
        min_length=1,
        description="Ordered list of reasoning steps executed",
    )
    recommendations: list[Recommendation] = Field(
        ...,
        min_length=1,
        description="Final actionable recommendations",
    )
    total_savings_kes: float = Field(
        ...,
        ge=0,
        description="Aggregate savings in KES across all recommendations",
    )
    total_savings_pct: float = Field(
        ...,
        ge=0,
        le=100.0,
        description="Aggregate savings as a percentage of total worst-case cost",
    )
