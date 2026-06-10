# SafariFX — Official 3-Minute Demo Video Script

> **Project**: SafariFX — AI Treasury Advisor for Frontier Market FX Optimization
> **Target Video Duration**: 3 to 4 minutes
> **Track**: 🧠 Reasoning Agents | **IQ Layer**: Foundry IQ (Microsoft Azure AI Foundry)

---

## 🎬 Act I: The Hook & The Problem

| Visual / Action (SHOW) | Narration (TELL) |
| :--- | :--- |
| **SHOW**: Cold open close-up on a USD invoice stamped **"DUE IN 48 HOURS."** Swiftly pan to a chaotic mock WhatsApp chat window showing multiple bank treasury desks sending conflicting spot quotes. Flash to a volatile daily KES/USD morning rate chart with wide spreads. | **TELL**: "At 8:30 AM in Nairobi, a CFO gets a fifty-thousand-dollar invoice due in 48 hours. The current industry standard is chaos: calling three to five banks manually, comparing headline rates, and guessing execution timing—all while getting hit by hidden commission percentages, SWIFT transfer fees, and opaque spreads. SafariFX turns this chaos into a single, timing-optimized, fully cited FX execution plan so businesses stop leaking 1.5% to 3% on every cross-border payment." |
| **SHOW**: Simple, high-contrast title card: **"SafariFX — AI Treasury Advisor for Frontier Market FX."** Then show a clean "Before vs After" split-screen: left side lists manual calls, messy spreadsheets, and zero audit trails; right side highlights the SafariFX advice report with citations and direct cost savings. | **TELL**: "We built SafariFX to eliminate hidden costs in frontier-market foreign exchange. By combining multi-bank rates, true all-in fee stacking, and regulatory grounding, every treasury decision becomes explainable, auditable, and ready for internal sign-off." |

---

## 🎬 Act II: The Team, Story, & Audience

| Visual / Action (SHOW) | Narration (TELL) |
| :--- | :--- |
| **SHOW**: Quick team profile slides showing experience: "Frontier-market operations experience," "Reasoning & grounding engineering," and "Enterprise delivery mindset." | **TELL**: "We are the right team to build this because we have witnessed the friction in these workflows up close, we know how to engineer reasoning agents with strict anti-hallucination guardrails, and we build with an enterprise delivery mindset—ensuring clean architecture and modular separation of concerns." |
| **SHOW**: Brief personal story B-roll/slides: someone toggling between bank rates, circling "commission %" on a printed bank tariff PDF, and pointing out the 1.5%–3% leakage. | **TELL**: "The inspiration for this project came from watching finance teams make high-stakes decisions with incomplete data—focusing only on headline spot rates that look cheap, while ignoring backend fees and timing factors that quietly worsen execution. We wanted an advisor that doesn't just output a rate, but shows its entire work and its sources." |
| **SHOW**: Target audience slide featuring icons for: Corporate Treasurers, SME Finance Managers, Importers & Manufacturers, and Logistics operators. Highlight a metric panel on the right side. | **TELL**: "Our primary audience consists of corporate treasurers and SME finance managers in frontier and emerging markets who regularly pay international suppliers in USD. Quantitatively, this segment faces typical FX leakage of 1.5% to 3% per transaction alongside hours of daily operational overhead." |

---

## 🎬 Act III: Live Walkthrough & Demo

| Visual / Action (SHOW) | Narration (TELL) |
| :--- | :--- |
| **SHOW**: Live screen recording of the SafariFX dark-mode React interface. <br>1. Show the bank rate cards with sparklines.<br>2. Upload/Select the raw invoices.<br>3. Click **"Run Treasury Audit"**.<br>4. Show the async progress status displaying the **"6-step reasoning engine"** loading card. | **TELL**: "Here is the workflow from a user's perspective. After importing your pending invoices, you simply trigger the treasury analysis. SafariFX automatically analyzes invoice urgency, aggregates current bank rates, fetches regulatory rules, scores the best banks, optimizes timing, and synthesizes a full execution report." |
| **SHOW**: Scroll to the **"Reasoning Trace Viewer"**. Highlight the step timeline (Parse → Aggregate → Ground → Score → Optimize → Report) lighting up green, with confidence scores and source citations. Next, scroll down to the finalized **"Advisory Report"** highlighting the split-payment recommendations and the comparison table. | **TELL**: "Under the hood, SafariFX executes a deterministic six-step pipeline. It aggregates rates from multiple commercial banks, stacks all SWIFT and commission fees to compute true all-in cost, grounds assumptions in Central Bank circulars using Microsoft Foundry IQ, applies a weighted scoring model, and coordinates timing around treasury auctions. For large invoices, it even recommends splitting purchases across the top two banks to reduce concentration risk." |
| **SHOW**: Display the clean architecture system diagram (React Frontend ➔ FastAPI Backend ➔ Foundry IQ Agentic Retrieval Layer). Point to the `.env` settings and show the mock fallback capability. | **TELL**: "On the technical side, the architecture is clean and robust. We use a FastAPI backend to run the async reasoning pipeline, grounded by a retrieval-augmented knowledge base in Azure AI Search. We also built a mock fallback mode so that judges can experience the full grounding and citation workflow even without live Azure credentials." |

---

## 🎬 Act IV: Impact & Roadmap

| Visual / Action (SHOW) | Narration (TELL) |
| :--- | :--- |
| **SHOW**: Graphics highlighting key benefits: "Measurable Margin Recovery," "Auditable Decision Logs," and "Operational Time Saved" (dropping from hours to seconds). | **TELL**: "The business impact is immediate: measurable savings on every transaction, automated rate verification, and a clear audit trail. Decisions are backed by verified policy references, ensuring easy governance and quick internal approvals." |
| **SHOW**: Highlight the project roadmap timeline:<br>• **Phase 1: Hackathon MVP** *(Complete)*<br>• **Phase 2: Live Rate Feeds & Pilot Readiness** *(In Progress)*<br>• **Phase 3: Multi-Market Corridor Expansion** *(Upcoming)*<br>• **Phase 4: Enterprise Integrations & Audit Export** *(Scale)* | **TELL**: "We have a fully working Kenya corridor demo today. Moving forward, our roadmap takes us from this initial proof-of-concept into live integration trials, expanding to new frontier corridors by simply swapping out the Foundry IQ knowledge base, and building production integrations for major ERPs." |
| **SHOW**: Final call-to-action slide showing: "Contact & Collaborations," QR code to repository, and GitHub URL: `https://github.com/ChrisDamian/SafariFX`. | **TELL**: "We are actively looking for pilot partners, treasury collaborators, and data partnerships. If you want to optimize your cross-border payments with a grounded, auditable agent, connect with us at our GitHub repository. Thank you!" |
