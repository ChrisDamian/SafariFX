# SafariFX — Domain Ontology, Extensibility, & Lessons Learned

This document explains how developers, financial analysts, and corporate users can leverage the **SafariFX Domain Ontology** to understand, expand, and scale the platform, alongside a detailed breakdown of the engineering lessons learned from building this solution.

---

## 🌍 Part 1: How to Use and Improve SafariFX via the Ontology

The SafariFX ontology acts as the semantic blueprint for the entire application. It bridges the gap between raw data (invoices and exchange rates) and cognitive reasoning (grounded recommendations).

### The Semantic Flow

Every user action and system process directly maps to a class or relationship in our ontology:

```
[Invoice] ──(Analyzed By)──> [ReasoningStep] ──(Grounded In)──> [GroundingSource] (Foundry IQ)
    │                               │
(Resolved By)                  (Generates)
    │                               │
    ▼                               ▼
[Recommendation] ──(Allocated To)──> [BankRate]
```

1. **User Action (Upload)**: A corporate treasurer uploads an `Invoice`. The system instantiates an `Invoice` entity, parsing its core data properties (`amountUsd`, `deadline`, and auto-calculating `urgency`).
2. **Agent Execution (Audit)**: The orchestrator triggers six sequential `ReasoningStep` instances. 
3. **Regulatory Verification (Grounding)**: During Step 3, the engine queries the Foundry IQ knowledge base, connecting the `ReasoningStep` to one or more `GroundingSource` entities (such as Central Bank policy circulars and bank tariff schedules) via the `groundsIn` relationship.
4. **Optimization (Analysis)**: The engine aggregates current `BankRate` quotes, weights them based on compliance parameters, and generates specific `Recommendation` entities indicating which bank to use (`allocatesToBank`) and when to execute (`timingAdvice`).
5. **Synthesis (Output)**: All entities are bundled into a final `AnalysisReport` for audit and governance exports.

---

### How Developers & Analysts Can Improve and Extend the Model

Because SafariFX is built around this structured ontology rather than hardcoded logic, individuals can easily expand the platform in three ways:

#### 1. Corridor Expansion (New Emerging Markets)
To deploy SafariFX in Nigeria (NGN), Egypt (EGP), or Pakistan (PKR), you don't need to rewrite the codebase. Using the ontology:
*   **Swap Grounding Sources**: In the Foundry IQ knowledge base, swap out the Central Bank of Kenya (CBK) documents for Central Bank of Nigeria (CBN) or Central Bank of Egypt (CBE) circulars.
*   **Map Local Bank Feeds**: Standardize local commercial bank API outputs to populate the `BankRate` fields (`buy_rate`, `sell_rate`, `swift_fee`, `commission_pct`). The weighted scoring model and timing optimization logic will automatically parse them correctly.

#### 2. Introducing Hedging Instruments (Ontology Growth)
Currently, SafariFX focuses on spot currency conversion and timing optimization. Analysts can introduce hedging options by defining new classes in the RDF file:
*   Add a **`ForwardContract`** or **`FXOption`** class.
*   Define relationships: `Recommendation` ➔ `suggestsHedging` ➔ `ForwardContract`.
*   Add data properties: `maturityDate`, `strikeRate`, `premiumFee`.
*   The reasoning engine can then ingest forward-market curves alongside spot rates and recommend locking in forward rates for high-urgency, long-deadline invoices.

#### 3. Advanced Liquidity and Settlement Routing
Introduce intermediary entities like **`CorrespondentBank`** or **`PaymentRail`** (e.g. SWIFT vs. regional clearing networks like RTGS or PAPSS in Africa). This allows the scoring model to calculate multi-hop transfer costs dynamically if direct routing is unavailable.

---

## 🧠 Part 2: Lessons Learned from Building SafariFX

Building an AI Treasury Advisor for highly volatile frontier markets taught us several critical lessons about designing reasoning agents for enterprise financial workflows:

### 1. RAG Grounding is a Hard Requirement for Financial Compliance
*   **The Problem**: Generative LLMs are prone to hallucinating numbers, dates, and regulatory rules. In corporate treasury, a single hallucinated commission percentage or misquoted base rate can result in massive financial leakage or compliance fines.
*   **The Lesson**: We used **Microsoft Foundry IQ** to enforce strict retrieval-augmented grounding. By forcing the agent to attach verifiable citations (`GroundingSource`) to every timing decision and bank recommendation, we created a transparent audit trail. If the LLM makes an assertion (e.g., *"The Central Bank auction on Wednesday is expected to increase KES liquidity"*), it must point directly to the source circular.

### 2. Orchestration Must Be Deterministic, Not Purely Generative
*   **The Problem**: Free-form agentic planning (asking an LLM to decide how to analyze the data) is unstable and unpredictable.
*   **The Lesson**: We structured the agent as a **deterministic 6-step pipeline**. Each step has defined input requirements, a bounded reasoning process, and typed output schemas (enforced via Pydantic v2). The AI's job is restricted to extraction, evaluation, and semantic synthesis within each step. This hybrid approach—combining deterministic flow control with LLM-powered cognitive grounding—is the only way to build reliable financial agents.

### 3. All-In Cost Stacking Exposes the "Headline Rate" Illusion
*   **The Problem**: Banks frequently attract corporate clients by offering competitive-looking "headline" spot rates, only to recoup margins via hidden conversion commissions, SWIFT transfer fees, and correspondent bank fees.
*   **The Lesson**: The ontology model forces the aggregation of *all* fee structures. When the engine ranked bank options, we discovered that a bank with a slightly worse spot rate but zero commission frequently outperformed a bank with a "cheap" spot rate but a 0.15% commission on large transfers. Structured data aggregation is essential to expose these hidden costs.

### 4. Mock Mode is Essential for Resilient Hackathon Deliverables
*   **The Problem**: Cloud credential rotations, API rate limits, and network outages frequently break live integrations during hackathon evaluations.
*   **The Lesson**: Designing a dual-mode client (`FoundryIQClient`) that seamlessly switches to a high-fidelity local Mock Mode when Azure endpoints are not set ensures that the application is always demo-ready. The mock templates return realistic, citation-rich JSON structures that match live Azure AI search responses exactly, ensuring zero friction for judges.
