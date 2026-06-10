# SafariFX — AI Treasury Advisor for Frontier Market FX Optimization

> **A multi-step reasoning agent that eliminates hidden costs in cross-border foreign exchange transactions across frontier and emerging markets. Powered by Microsoft Foundry IQ.**

**Track**: 🧠 Reasoning Agents | **IQ Layer**: Foundry IQ | **Event**: Agents League Hackathon 2026

---

## 🌍 The Problem: A $3 Trillion Blind Spot

Businesses in frontier and emerging markets lose **1.5% to 3%** on every foreign exchange transaction — not because they chose the wrong bank, but because they had no way to know which bank was the right one.

In markets like **Kenya, Nigeria, Egypt, Pakistan, Argentina, and Ghana**, finance managers:
- Manually call 3–5 banks to compare rates — there is no consolidated dashboard
- Face hidden fees buried across SWIFT charges, correspondent commissions, and opaque spread markups
- Have zero visibility into central bank auction schedules that historically shift currency values
- Leave no audit trail — decisions happen over phone calls and WhatsApp

These markets collectively process over **$3 trillion annually** in commercial FX. Even a 1% efficiency improvement translates to **$30 billion** in recovered value for businesses globally.

---

## 💡 The Solution: SafariFX

SafariFX is an **AI-powered interbank treasury advisor** built as a **configurable, market-agnostic platform**. The reasoning engine, scoring model, and UI work identically across any frontier market — only the central bank policy documents and bank rate feeds change.

**For this hackathon, we built a complete working implementation targeting Kenya** — the world's most active mobile-money market and a textbook example of frontier FX friction.

### The 6-Step Reasoning Engine

| Step | Name | What It Does |
|---|---|---|
| 1 | **Invoice Analysis** | Parses pending USD invoices, scores urgency by deadline (CRITICAL ≤ 2d, HIGH ≤ 5d) |
| 2 | **Market Intelligence** | Aggregates real-time rates across 5 banks, computes true all-in cost (rate + SWIFT + commission) |
| 3 | **Policy Grounding** | Queries **Foundry IQ** for central bank monetary policy, bank tariffs, and regulatory codes — with citations |
| 4 | **Bank Selection** | Weighted multi-criteria scoring (Spread 35%, Fees 20%, Liquidity 20%, Trend 15%, Compliance 10%) |
| 5 | **Timing Optimization** | Analyzes 7-day trends + central bank auction calendar → BUY_NOW / WAIT / SPLIT_PURCHASE |
| 6 | **Recommendation Synthesis** | Final cited report with exact savings in local currency vs. worst-case execution |

### Global Configurability

To deploy SafariFX in a new country:
1. **Swap the Foundry IQ knowledge base** — replace CBK circulars with CBN (Nigeria), SBP (Pakistan), or CBE (Egypt) documents
2. **Configure bank rate feeds** — plug in the local commercial banks
3. **Adjust scoring weights** — if regulatory environment differs
4. **Everything else stays unchanged** — the reasoning engine, frontend, and API are market-agnostic

| Ready Market | Central Bank | Potential Banks |
|---|---|---|
| 🇰🇪 Kenya (Demo) | CBK | Equity, KCB, Stanbic, NCBA, Co-op |
| 🇳🇬 Nigeria | CBN | GTBank, Zenith, First Bank, Access, UBA |
| 🇵🇰 Pakistan | SBP | HBL, MCB, UBL, Allied, Meezan |
| 🇪🇬 Egypt | CBE | CIB, NBE, Banque Misr, QNB, HSBC Egypt |
| 🇦🇷 Argentina | BCRA | Galicia, Macro, BBVA, Santander, ICBC |

---

## 🧠 Microsoft Foundry IQ Integration

SafariFX uses **Foundry IQ** for **agentic retrieval** — ensuring zero-hallucination financial advice.

During **Step 3** of the reasoning engine, the system sends 3 parallel queries to the Foundry IQ knowledge base:
1. Central bank monetary policy stance and interest rate decisions
2. Commercial bank FX tariff schedule comparisons
3. Regulatory FX codes governing bank operations

Every recommendation includes **citation tags** linking to the specific policy or tariff that justified the decision (e.g., `CBK/MPC/2026/06 — Monetary Policy Committee Press Release`).

**Mock Fallback**: If Azure credentials are not configured, the client seamlessly switches to a realistic mock mode with 5 topic-specific response templates — ensuring the demo always works during judging.

---

## 🏗️ Architecture

```
┌────────────────────────┐     ┌─────────────────────────────────┐
│  Frontend (Vite/React) │────▶│  Backend (Python FastAPI)       │
│  • Dark-mode dashboard │     │  • POST /api/invoices           │
│  • Rate cards + sparks │     │  • GET  /api/rates              │
│  • Reasoning trace     │     │  • POST /api/analyze            │
│  • Cited report view   │     │  • GET  /api/reports/{id}       │
│  Port: 5173            │     │  Port: 8000                     │
└────────────────────────┘     │                                 │
                               │  ┌─────────────────────────────┐│
                               │  │ 6-Step Reasoning Engine     ││
                               │  │ (870 lines, async pipeline) ││
                               │  └──────────┬──────────────────┘│
                               │             │                   │
                               │  ┌──────────▼──────────────────┐│
                               │  │ Foundry IQ Client           ││
                               │  │ (Live mode / Mock fallback) ││
                               │  └──────────┬──────────────────┘│
                               └─────────────┼───────────────────┘
                                             │
                               ┌─────────────▼───────────────────┐
                               │  Microsoft Azure AI Foundry     │
                               │  • Knowledge Base (CBK docs)    │
                               │  • Azure AI Search (retrieval)  │
                               └─────────────────────────────────┘
```

### Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React + Vite + Vanilla CSS | Premium glassmorphic dashboard with animated reasoning traces |
| Backend | Python 3.11 + FastAPI + Pydantic v2 | Async API, strict type validation, reasoning orchestration |
| Intelligence | Azure AI Projects SDK + Foundry IQ | Agentic retrieval with citation-backed grounding |
| Data | JSON/Markdown mock datasets | Simulates live bank feeds and central bank circulars |

---

## 💻 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- *(Optional)* Azure AI Foundry project with Foundry IQ enabled

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

> No Azure credentials? The backend automatically starts in **Mock Mode** with realistic Foundry IQ simulation.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** → Click **"Load Sample Kenyan Import Invoices"** → **"Proceed to FX Analysis"** → **"Run SafariFX Analysis"**

---

## 📁 Project Structure

```
SafariFX/
├── README.md
├── .env.example
├── .gitignore
├── backend/
│   ├── main.py                 # FastAPI app — 4 endpoints + CORS + lifespan
│   ├── models.py               # Pydantic v2 — Invoice, BankRate, ReasoningStep, Recommendation, AnalysisReport
│   ├── reasoning_engine.py     # 6-step reasoning pipeline (870 lines)
│   ├── foundry_iq.py           # Foundry IQ client — Azure live + mock fallback
│   ├── rate_service.py         # FX rate aggregation + spread analysis
│   ├── requirements.txt
│   └── tests/
│       └── test_reasoning_engine.py
├── data/
│   ├── mock_rates.json         # 14-day rates for 5 Kenyan banks
│   ├── mock_invoices.json      # 10 sample USD invoices
│   ├── cbk_circulars.md        # Simulated CBK monetary policy
│   └── bank_tariffs.md         # Simulated bank fee schedules
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css           # Design system — HSL tokens, glassmorphism, animations
        └── components/
            ├── Navbar.jsx
            ├── Dashboard.jsx
            ├── InvoiceUpload.jsx
            ├── RateDashboard.jsx
            ├── AnalysisView.jsx
            ├── ReasoningTrace.jsx
            ├── RecommendationReport.jsx
            ├── SavingsTracker.jsx
            └── ReportsView.jsx
```

---

## 🏆 Hackathon Rubric Alignment

| Criteria | Weight | How SafariFX Scores |
|---|---|---|
| **Accuracy & Relevance** | 20% | Foundry IQ grounding ensures zero-hallucination, citation-backed advice |
| **Reasoning & Multi-step** | 20% | 6-step deterministic pipeline with visual trace — the deepest reasoning chain in the competition |
| **Creativity & Originality** | 15% | Zero competing projects address frontier-market FX optimization |
| **User Experience** | 15% | Premium glassmorphic UI with animated reasoning traces that build trust |
| **Reliability & Safety** | 20% | Mock fallback ensures demo resilience; Pydantic v2 prevents data corruption |
| **Community Vote** | 10% | Relatable, real-world problem with a visually compelling demo |

## 👤 Author

**Christopher Munene** — Full Stack Developer & AI Engineer

- [GitHub](https://github.com/ChrisDamian)
- [LinkedIn](https://linkedin.com/in/christopher-munene)

---

*Built for the 2026 Microsoft Agents League Hackathon.*
