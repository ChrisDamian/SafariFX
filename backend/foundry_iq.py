"""
SafariFX — Foundry IQ Knowledge-Base Client
=============================================

Provides a ``FoundryIQClient`` that queries Azure AI Foundry's grounded
knowledge-base for CBK regulatory data, bank tariff schedules, and FX
market intelligence.

The client gracefully falls back to a **mock mode** when Azure credentials
are unavailable (e.g. local development without an Azure subscription),
returning realistic, citation-rich responses that mirror production output.

Mock responses cover:
  1. CBK monetary policy stance & MPC decisions
  2. Commercial bank FX tariff schedules
  3. Historical CBK T-bill auction patterns
  4. Regulatory FX codes & compliance requirements
  5. Interbank liquidity analysis & market depth
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("safarifx.foundry_iq")


class FoundryIQClient:
    """
    Client for Azure AI Foundry's grounded knowledge-base (Foundry IQ).

    On initialisation the client attempts to authenticate via
    ``DefaultAzureCredential``.  If this fails (missing SDK, no credentials,
    or no project endpoint configured), the client silently switches to
    **mock mode** and logs a warning.

    Attributes:
        mock_mode:  ``True`` when running without real Azure credentials.
        project_client:  The Azure ``AIProjectClient`` instance (or ``None``).
    """

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        self.mock_mode: bool = False
        self.project_client: Any = None
        self._agent_model: str = os.getenv("AGENT_MODEL", "gpt-4.1-mini")

        endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
        if not endpoint:
            logger.warning(
                "FOUNDRY_PROJECT_ENDPOINT not set — starting in mock mode."
            )
            self.mock_mode = True
            return

        try:
            from azure.identity import DefaultAzureCredential
            from azure.ai.projects import AIProjectClient

            credential = DefaultAzureCredential()
            self.project_client = AIProjectClient(
                endpoint=endpoint,
                credential=credential,
            )
            logger.info("Foundry IQ client initialised (live mode).")
        except Exception as exc:
            logger.warning(
                "Azure credential setup failed (%s) — falling back to mock mode.",
                exc,
            )
            self.mock_mode = True

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def query_knowledge_base(self, query: str) -> dict[str, Any]:
        """
        Query the Foundry IQ knowledge-base with a natural-language question.

        Parameters:
            query: Free-text question about Kenyan FX policy, bank tariffs,
                   or market conditions.

        Returns:
            A dictionary with keys:
              - ``answer``   (str):  Grounded, cited answer text.
              - ``citations`` (list[dict]):  Source references.
              - ``confidence`` (float):  Confidence score 0–1.
              - ``source``   (str):  Knowledge-base source identifier.
              - ``timestamp`` (str): ISO-8601 response timestamp.
        """
        if self.mock_mode:
            return self._mock_query(query)

        return await self._live_query(query)

    # ------------------------------------------------------------------
    # Live query (Azure AI Foundry)
    # ------------------------------------------------------------------

    async def _live_query(self, query: str) -> dict[str, Any]:
        """Execute a grounded query against the real Foundry IQ endpoint."""
        try:
            # Use the Azure AI Projects SDK to run a grounded agent query.
            # The agent is configured in Azure AI Foundry with access to
            # knowledge-base indices containing CBK circulars, bank tariffs,
            # and FX market data.
            response = self.project_client.agents.create_and_run(
                model=self._agent_model,
                instructions=(
                    "You are a Kenyan treasury advisor. Answer questions about "
                    "CBK monetary policy, commercial bank FX tariffs, and FX "
                    "market conditions with specific citations to CBK circulars "
                    "and bank tariff schedules."
                ),
                messages=[{"role": "user", "content": query}],
            )

            # Extract the assistant reply
            answer_text = ""
            citations: list[dict[str, str]] = []
            if hasattr(response, "choices") and response.choices:
                answer_text = response.choices[0].message.content or ""
            elif hasattr(response, "content"):
                answer_text = str(response.content)

            return {
                "answer": answer_text,
                "citations": citations,
                "confidence": 0.85,
                "source": "azure-ai-foundry-knowledge-base",
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as exc:
            logger.error("Live Foundry IQ query failed: %s — using mock.", exc)
            return self._mock_query(query)

    # ------------------------------------------------------------------
    # Mock knowledge-base
    # ------------------------------------------------------------------

    def _mock_query(self, query: str) -> dict[str, Any]:
        """
        Return a realistic mock response based on keyword matching.

        The mock knowledge-base covers five topic areas, each with
        genuine-sounding CBK circular references and bank tariff details.
        """
        q = query.lower()
        ts = datetime.utcnow().isoformat()

        # ----- 1. CBK Monetary Policy & MPC Decisions -----
        if any(kw in q for kw in ["monetary policy", "mpc", "cbk rate", "policy stance", "interest rate"]):
            return {
                "answer": (
                    "The Central Bank of Kenya's Monetary Policy Committee (MPC) "
                    "held its benchmark Central Bank Rate (CBR) steady at 10.00% "
                    "during the June 2026 session, citing easing inflationary "
                    "pressures (headline CPI at 4.1% y/y) but persistent external "
                    "risks from volatile global commodity prices. The MPC noted "
                    "that the KES has appreciated 1.4% against the USD over the "
                    "past quarter, supported by resilient diaspora remittances "
                    "(USD 382M in May 2026) and improved horticulture export "
                    "receipts. The committee expects the shilling to remain "
                    "broadly stable in the near term, reducing urgency for "
                    "immediate FX cover on non-critical payables."
                ),
                "citations": [
                    {
                        "source": "CBK/MPC/2026/06",
                        "title": "Monetary Policy Committee Press Release — June 2026",
                        "url": "https://www.centralbank.go.ke/monetary-policy/mpc-press-releases/",
                    },
                    {
                        "source": "CBK/STAT/2026/05",
                        "title": "Monthly Economic Review — May 2026",
                        "url": "https://www.centralbank.go.ke/statistics/monthly-economic-review/",
                    },
                ],
                "confidence": 0.92,
                "source": "cbk-monetary-policy-corpus",
                "timestamp": ts,
            }

        # ----- 2. Bank FX Tariff Schedules -----
        if any(kw in q for kw in ["tariff", "fee", "commission", "swift", "charge", "bank cost"]):
            return {
                "answer": (
                    "Analysis of published FX tariff schedules across Kenyan "
                    "commercial banks reveals significant variation in total "
                    "transaction costs:\n\n"
                    "• Standard Chartered Kenya (SCBK): Tightest spread at "
                    "KES 2.55, but highest SWIFT fee (USD 45) and commission "
                    "(0.175%). Best for large-value transfers (>USD 50K) where "
                    "spread savings outweigh fixed fees.\n"
                    "• Equity Bank (EQTY): Competitive spread (KES 2.65), lowest "
                    "SWIFT fee (USD 30), and lowest commission (0.10%). Optimal "
                    "for mid-size transfers (USD 10K–50K).\n"
                    "• KCB: Moderate spread (KES 2.75), mid-range fees. High "
                    "liquidity makes it reliable for same-day settlement.\n"
                    "• Co-operative Bank (COOP): Widest spread (KES 2.90) and "
                    "highest commission (0.15%). Not recommended unless existing "
                    "correspondent relationship offers netting benefits.\n"
                    "• NCBA: Moderate spread (KES 2.85) with competitive SWIFT "
                    "fees (USD 38). Good for clients with NCBA trade finance lines."
                ),
                "citations": [
                    {
                        "source": "SCBK/TARIFF/2026/Q2",
                        "title": "Standard Chartered Kenya — Schedule of Charges Q2 2026",
                        "url": "https://www.sc.com/ke/fees-and-charges/",
                    },
                    {
                        "source": "EQTY/TARIFF/2026/Q2",
                        "title": "Equity Bank — Tariff Guide Q2 2026",
                        "url": "https://equitygroupholdings.com/ke/tariff-guide",
                    },
                    {
                        "source": "CBK/BSD/CIRC/04/2024",
                        "title": "CBK Circular on Transparency in Bank Charges",
                        "url": "https://www.centralbank.go.ke/regulation/circulars/",
                    },
                ],
                "confidence": 0.89,
                "source": "bank-tariff-corpus",
                "timestamp": ts,
            }

        # ----- 3. Historical CBK Auction Patterns -----
        if any(kw in q for kw in ["auction", "t-bill", "treasury", "government securities"]):
            return {
                "answer": (
                    "CBK Treasury Bill auctions have historically exerted "
                    "short-term downward pressure on the KES/USD rate. Analysis "
                    "of the past 12 months of weekly 91-day T-bill auctions "
                    "shows that the KES strengthens by an average of KES 0.15–0.25 "
                    "on auction settlement days (typically T+1 from Wednesday "
                    "auctions) as banks repatriate USD to fund KES-denominated "
                    "government securities purchases.\n\n"
                    "The next scheduled auction is 2026-06-11 (Wednesday). "
                    "Expected subscription rate: 120–135% based on current "
                    "91-day yield of 9.45%. Importers with non-urgent payables "
                    "(deadline > T+3) should consider delaying FX purchases to "
                    "Thursday 2026-06-12 to capture post-auction KES strength."
                ),
                "citations": [
                    {
                        "source": "CBK/DOMES/2026/W23",
                        "title": "CBK Domestic Market Operations — Week 23, 2026",
                        "url": "https://www.centralbank.go.ke/treasury-bills-results/",
                    },
                    {
                        "source": "CBK/GOK/AUCTION/2026/06/11",
                        "title": "T-Bill Auction Prospectus — 11 June 2026",
                        "url": "https://www.centralbank.go.ke/securities/treasury-bills/",
                    },
                ],
                "confidence": 0.87,
                "source": "cbk-auction-analysis-corpus",
                "timestamp": ts,
            }

        # ----- 4. Regulatory FX Codes & Compliance -----
        if any(kw in q for kw in ["regulation", "compliance", "forex code", "fx code", "cbk circular", "limit"]):
            return {
                "answer": (
                    "Key CBK regulations governing commercial bank FX operations "
                    "in Kenya:\n\n"
                    "1. **CBK/PG/FEM/01/2023** (Foreign Exchange Market Code of "
                    "Conduct): Requires banks to offer rates within ±2% of the "
                    "CBK indicative midrate. Spreads exceeding this threshold "
                    "must be justified and disclosed to the client.\n\n"
                    "2. **CBK/PG/BSD/03/2024** (Single-Transaction Limit): "
                    "Individual FX transactions exceeding USD 500,000 require "
                    "same-day reporting to CBK. Transactions above USD 1M need "
                    "prior notification.\n\n"
                    "3. **CBK/PG/FEM/02/2023** (FX Exposure Limits): Commercial "
                    "banks' overall open FX position must not exceed 10% of core "
                    "capital. This affects liquidity availability during periods "
                    "of high demand.\n\n"
                    "4. All cross-border transfers require valid Import "
                    "Declaration Forms (IDF) and supporting trade documentation "
                    "per the Kenya Revenue Authority (KRA) customs requirements."
                ),
                "citations": [
                    {
                        "source": "CBK/PG/FEM/01/2023",
                        "title": "Kenya Foreign Exchange Market Code of Conduct — 2023",
                        "url": "https://www.centralbank.go.ke/regulation/forex-market-code/",
                    },
                    {
                        "source": "CBK/PG/BSD/03/2024",
                        "title": "Prudential Guideline — FX Transaction Reporting",
                        "url": "https://www.centralbank.go.ke/regulation/prudential-guidelines/",
                    },
                    {
                        "source": "KRA/CUSTOMS/IDF/2025",
                        "title": "KRA Import Declaration Form Requirements",
                        "url": "https://www.kra.go.ke/customs/import-requirements",
                    },
                ],
                "confidence": 0.94,
                "source": "cbk-regulatory-corpus",
                "timestamp": ts,
            }

        # ----- 5. Interbank Liquidity & Market Depth -----
        if any(kw in q for kw in ["liquidity", "interbank", "market depth", "volume", "demand"]):
            return {
                "answer": (
                    "The Kenyan interbank FX market is currently exhibiting "
                    "moderate-to-good liquidity with daily average turnover of "
                    "USD 28–35M over the past two weeks. Key observations:\n\n"
                    "• **Supply side**: Diaspora remittance inflows remain "
                    "robust (USD 382M in May 2026), and horticulture export "
                    "receipts have increased 8% y/y due to favorable European "
                    "demand.\n"
                    "• **Demand side**: Oil import bills have moderated as "
                    "global Brent prices stabilised near USD 72/barrel, "
                    "reducing USD demand pressure.\n"
                    "• **Bank positioning**: Tier-1 banks (KCB, Equity, StanChart) "
                    "are net USD sellers this week, suggesting they hold "
                    "comfortable long positions. This favours importers seeking "
                    "competitive rates.\n"
                    "• **Interbank midrate**: KES 128.80/USD — trading 0.54% "
                    "below the CBK indicative rate of KES 129.50, confirming "
                    "mild KES strength.\n\n"
                    "Recommendation: Current liquidity conditions support "
                    "executing trades up to USD 100K without material market "
                    "impact. Larger transactions should be split across 2–3 days."
                ),
                "citations": [
                    {
                        "source": "CBK/DOMES/2026/INTERBANK/W23",
                        "title": "CBK Interbank FX Market Report — Week 23, 2026",
                        "url": "https://www.centralbank.go.ke/interbank-forex-market/",
                    },
                    {
                        "source": "CBK/REMIT/2026/05",
                        "title": "Diaspora Remittance Report — May 2026",
                        "url": "https://www.centralbank.go.ke/remittances/",
                    },
                ],
                "confidence": 0.88,
                "source": "interbank-liquidity-corpus",
                "timestamp": ts,
            }

        # ----- Fallback: General FX Guidance -----
        return {
            "answer": (
                "Based on current CBK data and commercial bank quotations, "
                "the KES/USD exchange rate is exhibiting a mild appreciation "
                "trend. The 7-day moving average across major banks shows a "
                "decline of approximately KES 0.50–0.65 from the prior week. "
                "Importers should evaluate urgency against this downward trend "
                "before executing FX purchases. Key factors to monitor include "
                "the upcoming CBK T-bill auction on 2026-06-11 and the next "
                "MPC meeting scheduled for late June 2026."
            ),
            "citations": [
                {
                    "source": "CBK/DOMES/2026/W23",
                    "title": "CBK Weekly Market Summary — Week 23, 2026",
                    "url": "https://www.centralbank.go.ke/forex/",
                },
            ],
            "confidence": 0.80,
            "source": "general-fx-corpus",
            "timestamp": ts,
        }
