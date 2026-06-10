"""
SafariFX — FastAPI Application Entry Point
============================================

The main FastAPI application for the SafariFX AI Treasury Advisor platform.
Provides four REST endpoints for invoice management, FX rate retrieval,
multi-step reasoning analysis, and report retrieval.

Endpoints:
  POST /api/invoices            — Parse and store uploaded invoices
  GET  /api/rates               — Return current multi-bank FX rates
  POST /api/analyze             — Trigger full multi-step reasoning analysis
  GET  /api/reports/{report_id} — Retrieve a specific analysis report

Run with:
  uvicorn main:app --reload --port 8000
"""

from __future__ import annotations

import logging
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from models import (
    AnalysisReport,
    BankRate,
    Invoice,
    UrgencyLevel,
)
from foundry_iq import FoundryIQClient
from rate_service import RateService
from reasoning_engine import ReasoningEngine

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-28s  %(levelname)-7s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("safarifx.main")


# ---------------------------------------------------------------------------
# Application state (in-memory stores)
# ---------------------------------------------------------------------------

class AppState:
    """Centralised in-memory application state."""

    def __init__(self) -> None:
        self.invoices: dict[str, Invoice] = {}
        self.reports: dict[str, AnalysisReport] = {}
        self.iq_client: FoundryIQClient | None = None
        self.rate_service: RateService | None = None


state = AppState()


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise services on startup and clean up on shutdown."""
    logger.info("SafariFX backend starting up...")

    # Initialise Foundry IQ client (auto-falls back to mock mode)
    state.iq_client = FoundryIQClient()
    mode = "MOCK" if state.iq_client.mock_mode else "LIVE"
    logger.info("Foundry IQ client ready (%s mode).", mode)

    # Initialise rate service
    state.rate_service = RateService()
    rates = state.rate_service.get_current_rates()
    logger.info("Rate service ready — %d banks loaded.", len(rates))

    # Seed sample invoices for demo purposes
    _seed_sample_invoices()

    logger.info("SafariFX backend ready. Listening for requests.")
    yield
    logger.info("SafariFX backend shutting down.")


def _seed_sample_invoices() -> None:
    """Pre-load realistic sample invoices for demo / testing."""
    samples = [
        Invoice(
            id=str(uuid.uuid4()),
            supplier_name="Shenzhen Electronics Co. Ltd",
            currency="USD",
            amount_usd=45_000.00,
            deadline=datetime(2026, 6, 12, 0, 0, 0),
            description="PCB components and SMD resistors — Batch #4412",
            urgency=UrgencyLevel.HIGH,
        ),
        Invoice(
            id=str(uuid.uuid4()),
            supplier_name="Mumbai Textiles International",
            currency="USD",
            amount_usd=28_500.00,
            deadline=datetime(2026, 6, 18, 0, 0, 0),
            description="Cotton fabric rolls — PO #TXT-2026-089",
            urgency=UrgencyLevel.MEDIUM,
        ),
        Invoice(
            id=str(uuid.uuid4()),
            supplier_name="Deutsche Maschinenbau GmbH",
            currency="USD",
            amount_usd=112_000.00,
            deadline=datetime(2026, 6, 25, 0, 0, 0),
            description="CNC milling machine — Model DM-X500 with installation",
            urgency=UrgencyLevel.MEDIUM,
        ),
    ]
    for inv in samples:
        state.invoices[inv.id] = inv

    logger.info("Seeded %d sample invoices.", len(samples))


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="SafariFX — AI Treasury Advisor",
    description=(
        "An AI-powered treasury advisory platform that helps Kenyan importers "
        "optimise foreign exchange purchases across multiple commercial banks. "
        "Powered by Azure AI Foundry's grounded knowledge-base for CBK policy "
        "analysis and multi-step reasoning."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class InvoiceCreateRequest(BaseModel):
    """Schema for creating a new invoice via POST /api/invoices."""
    supplier_name: str = Field(..., min_length=1, max_length=200)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    amount_usd: float = Field(..., gt=0)
    deadline: datetime
    description: str | None = Field(default=None, max_length=500)
    urgency: UrgencyLevel = Field(default=UrgencyLevel.MEDIUM)


class InvoiceListResponse(BaseModel):
    """Response for invoice listing / creation."""
    invoices: list[Invoice]
    count: int


class RatesResponse(BaseModel):
    """Response for the /api/rates endpoint."""
    rates: list[BankRate]
    cbk_indicative_rate: float | None = None
    interbank_rate: float | None = None
    next_cbk_auction: str | None = None
    last_updated: str | None = None
    spread_analysis: dict[str, Any] | None = None


class AnalyzeRequest(BaseModel):
    """Optional request body for /api/analyze. If empty, uses stored invoices."""
    invoice_ids: list[str] | None = Field(
        default=None,
        description="Specific invoice IDs to analyse. If omitted, all stored invoices are used.",
    )


class AnalyzeResponse(BaseModel):
    """Response for the /api/analyze endpoint."""
    report_id: str
    status: str
    report: AnalysisReport


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post(
    "/api/invoices",
    response_model=InvoiceListResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Invoices"],
    summary="Create or upload invoices",
)
async def create_invoices(
    invoices: list[InvoiceCreateRequest],
) -> InvoiceListResponse:
    """
    Parse and store one or more invoices for later analysis.

    Accepts a JSON array of invoice objects.  Each invoice is validated,
    assigned a unique ID, and stored in the in-memory invoice store.
    """
    created: list[Invoice] = []

    for req in invoices:
        invoice = Invoice(
            id=str(uuid.uuid4()),
            supplier_name=req.supplier_name,
            currency=req.currency,
            amount_usd=req.amount_usd,
            deadline=req.deadline,
            description=req.description,
            urgency=req.urgency,
        )
        state.invoices[invoice.id] = invoice
        created.append(invoice)
        logger.info(
            "Stored invoice %s: %s — USD %.2f",
            invoice.id,
            invoice.supplier_name,
            invoice.amount_usd,
        )

    return InvoiceListResponse(invoices=created, count=len(created))


@app.get(
    "/api/invoices",
    response_model=InvoiceListResponse,
    tags=["Invoices"],
    summary="List all stored invoices",
)
async def list_invoices() -> InvoiceListResponse:
    """Return all invoices currently in the store."""
    all_invoices = list(state.invoices.values())
    return InvoiceListResponse(invoices=all_invoices, count=len(all_invoices))


@app.get(
    "/api/rates",
    response_model=RatesResponse,
    tags=["FX Rates"],
    summary="Get current multi-bank FX rates",
)
async def get_rates() -> RatesResponse:
    """
    Return current FX rates across all configured Kenyan commercial banks.

    Rates are sorted by spread (tightest first) and include 7-day trend
    data, SWIFT fees, and commission percentages.  Also returns the CBK
    indicative rate, interbank midrate, and the next scheduled T-bill
    auction date.
    """
    if not state.rate_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Rate service not initialised.",
        )

    rates = state.rate_service.get_current_rates()
    spread_analysis = state.rate_service.compute_spread_analysis()
    historical = state.rate_service.get_historical_rates(days=7)

    return RatesResponse(
        rates=rates,
        cbk_indicative_rate=historical.get("cbk_indicative_rate"),
        interbank_rate=historical.get("interbank_rate"),
        next_cbk_auction=historical.get("next_cbk_auction"),
        last_updated=rates[0].timestamp.isoformat() if rates else None,
        spread_analysis=spread_analysis,
    )


@app.post(
    "/api/analyze",
    response_model=AnalyzeResponse,
    tags=["Analysis"],
    summary="Run multi-step reasoning analysis",
)
async def analyze(request: AnalyzeRequest | None = None) -> AnalyzeResponse:
    """
    Trigger a full multi-step reasoning analysis on stored invoices.

    The reasoning engine executes six sequential analytical steps:
      1. **Invoice Analysis** — urgency scoring and currency grouping
      2. **Market Intelligence** — bank ranking by effective cost
      3. **Policy Grounding** — CBK policy and regulatory context via Foundry IQ
      4. **Bank Selection** — weighted multi-criteria scoring model
      5. **Timing Optimisation** — trend analysis and auction calendar
      6. **Report Generation** — final recommendations with savings computation

    Optionally pass ``invoice_ids`` to analyse a subset of invoices.
    If omitted, all stored invoices are analysed.
    """
    if not state.rate_service or not state.iq_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Backend services not fully initialised.",
        )

    # Determine which invoices to analyse
    if request and request.invoice_ids:
        invoices = []
        for iid in request.invoice_ids:
            if iid not in state.invoices:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Invoice '{iid}' not found.",
                )
            invoices.append(state.invoices[iid])
    else:
        invoices = list(state.invoices.values())

    if not invoices:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No invoices available. Upload invoices first via POST /api/invoices.",
        )

    # Get current rates
    rates = state.rate_service.get_current_rates()
    if not rates:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No FX rate data available.",
        )

    # Run the reasoning engine
    engine = ReasoningEngine(
        invoices=invoices,
        rates=rates,
        iq_client=state.iq_client,
    )
    report = await engine.run()

    # Store the report
    state.reports[report.id] = report
    logger.info(
        "Analysis complete — report %s: %d recommendations, "
        "savings KES %.2f (%.2f%%).",
        report.id,
        len(report.recommendations),
        report.total_savings_kes,
        report.total_savings_pct,
    )

    return AnalyzeResponse(
        report_id=report.id,
        status="completed",
        report=report,
    )


@app.get(
    "/api/reports/{report_id}",
    response_model=AnalysisReport,
    tags=["Reports"],
    summary="Retrieve a specific analysis report",
)
async def get_report(report_id: str) -> AnalysisReport:
    """
    Retrieve a previously generated analysis report by its unique ID.

    Returns the full ``AnalysisReport`` including all reasoning steps,
    recommendations, rate snapshots, and savings computations.
    """
    if report_id not in state.reports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report '{report_id}' not found. Run POST /api/analyze first.",
        )

    return state.reports[report_id]


@app.get(
    "/api/reports",
    tags=["Reports"],
    summary="List all report IDs",
)
async def list_reports() -> dict[str, Any]:
    """Return a list of all generated report IDs with timestamps."""
    return {
        "reports": [
            {
                "id": r.id,
                "timestamp": r.timestamp.isoformat(),
                "invoice_count": len(r.invoices),
                "recommendation_count": len(r.recommendations),
                "total_savings_kes": r.total_savings_kes,
            }
            for r in state.reports.values()
        ],
        "count": len(state.reports),
    }


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["System"], summary="Health check")
async def health_check() -> dict[str, str]:
    """Return service health status."""
    return {
        "status": "healthy",
        "service": "SafariFX AI Treasury Advisor",
        "version": "1.0.0",
        "foundry_iq_mode": "mock" if (state.iq_client and state.iq_client.mock_mode) else "live",
        "invoices_loaded": str(len(state.invoices)),
        "reports_generated": str(len(state.reports)),
    }
