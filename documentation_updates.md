# SafariFX — Project Status, Updates, & Ontology Integration Guide

This document provides a comprehensive summary of the recent updates made to the SafariFX codebase, its verification status, and step-by-step instructions on running and deploying the **Microsoft Ontology Playground** to visualize the project's ontology layer.

---

## 🚀 Part 1: SafariFX Updates & Verification

### Key Updates
1. **Pydantic v2 Type Alignment**: Updated schema structures in `test_reasoning_engine.py` to match the strict validation constraints in `models.py` (UPPERCASE indicators, `swift_fee` naming convention, and `^[A-Z]{3,5}$` regex pattern for bank codes).
2. **Import Discrepancy Fixes**: Resolved Python package resolution issues by aligning imports across the test suite and engine. Both now load models consistently from the parent `models` module, preventing class-mismatch errors in Pydantic.
3. **Rates Cache Injection**: Integrated custom-rates loading in `ReasoningEngine` to override the static JSON feed files during execution. This allows robust testing against custom scenarios.
4. **Global Market Positioning**: Fully reframed the project documentation (`README.md`, presentation scripts, and devpost guides) to present SafariFX as a configurable, global frontier-market FX optimizer with Kenya serving as the reference corridor.

### Verification Status
*   The test suite was run inside the Python 3.11 environment.
*   **Result**: `1 passed in 0.84s`. The 6-step reasoning engine (parsing, aggregating, grounding, scoring, optimizing, and report synthesis) runs deterministically and produces exact savings calculations as expected.

---

## 🎨 Part 2: Microsoft Ontology Playground Guide

We have cloned the official **Microsoft Ontology Playground** into a separate folder on your system:
`c:\Users\user\Desktop\BISF1\Project 26\Ontology-Playground`

Inside this folder, we have created the community contribution for **SafariFX** containing:
1. `catalogue/community/safarifx/metadata.json` — Catalogue info & metadata tags.
2. `catalogue/community/safarifx/safarifx.rdf` — Full entity definition language (RDF/XML) representing the classes (`Invoice`, `BankRate`, `ReasoningStep`, `Recommendation`, `GroundingSource`, `AnalysisReport`) and their domain relationships.

### How to Run Locally

To run the Ontology Playground app locally and explore the SafariFX graph:

1. **Open a Command Terminal (CMD / PowerShell)**.
2. **Navigate to the Ontology-Playground directory**:
   ```bash
   cd "c:\Users\user\Desktop\BISF1\Project 26\Ontology-Playground"
   ```
3. **Install Dependencies**:
   ```bash
   npm install
   ```
4. **Run the Development Server**:
   ```bash
   npm run dev
   ```
5. **Open in Browser**:
   Navigate to **`http://localhost:5173/`**.
6. **Load SafariFX**:
   * Go to the **Catalogue** tab.
   * Search for **"SafariFX"** under community contributions, or directly go to the hash route:
     **`http://localhost:5173/#/catalogue/community/safarifx`**

---

### Deployment Solutions

If you want to host the Ontology Playground online so judges or collaborators can view your ontology diagram interactively, here are the deployment options:

#### Option A: GitHub Pages (Recommended for Forks / Personal Repos)
The playground includes a GitHub Action workflow (`.github/workflows/deploy-ghpages.yml`) designed to build and deploy to GitHub Pages automatically upon pushes to the main branch:
1. Create a repository on GitHub (e.g. `Ontology-Playground`).
2. Go to **Settings ➔ Pages ➔ Source** and select **GitHub Actions**.
3. Add your remote origin and push the cloned code:
   ```bash
   git remote add origin https://github.com/ChrisDamian/Ontology-Playground.git
   git branch -M main
   git push -u origin main
   ```
4. The GitHub Action will compile the RDF models and host the interactive site at `https://ChrisDamian.github.io/Ontology-Playground/`.

#### Option B: Azure Static Web Apps
The repository includes configuration settings (`staticwebapp.config.json`) for zero-configuration deployments to Azure:
1. Log in to the **Azure Portal** and search for **Static Web Apps**.
2. Click **Create**, choose your GitHub account, and select the repository.
3. For build presets, select **Vite** or choose custom config:
   * **App location**: `/`
   * **Output location**: `build` (the project builds static pages into `build/` via `npm run build`).
4. Save and deploy. Azure will host your live ontology diagram dashboard.
