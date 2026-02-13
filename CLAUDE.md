# Consent-Theoretic Framework for Quantifying Legitimacy

**WP Number:** DAI-2501
**Status:** Preprint (Zenodo + SSRN) — monograph v2.0.0 complete
**DOI:** 10.5281/zenodo.17684676
**Canonical:** `paper/Farzulla_2025_Consent_Holding_v2.0.0.tex`
**Previous version:** `paper/Farzulla_2025_Consent_Holding_v1.0.2.tex`
**Bib:** `references.bib` (at root, 185 entries, 84/85 orphans cited)

## Structure
- `paper/` — LaTeX source, compiled PDF, figures/, Makefile
- `paper/sections_*.tex` — agent-written section files (5 files, used during integration)
- `code/` — implementation code
- `consent-theory-models/` — theoretical models + `generate_phase3_figures.py`
- `data/` — datasets (V-Dem v15 + Monte Carlo CSVs)
- `figures/` — root-level figures (8 total: 3 historical, 2 simulation, 1 frontier, 2 Phase 3)
- `tables/` — generated tables
- `archive/` — old versions (note: NOT `_archive/`)
- `references.bib` — bibliography at root level
- `MONOGRAPH_EXPANSION.md` — shared context for writing agents

## Monograph v2.0.0 (February 2026)
- **140 pages**, ~2960 lines, 5 Parts, 21 main sections + 4 appendices
- **Clean compile:** 0 errors, 0 warnings, 0 undefined refs
- Part I: Foundations (Intro, Lit Review x11, Framework, Operationalization)
- Part II: Normative Architecture (Social Contract expanded with 7 subsections)
- Part III: Historical Validation (9 case studies with quantified alpha/F)
- Part IV: Computational Validation (Monte Carlo + Dynamic Validation)
- Part V: Implications (9 Objections, Weight Determination, Research Agenda, Conclusion)
- 1 uncited bib entry: `maloy2012divine` (flagged as possible drop)

## Data Assets
- `data/V-Dem-CY-Core-v15.csv` — Full V-Dem v15 dataset (204MB, 1789-2024)
- `data/vdem_consent_subset.csv` — Extracted subset: GBR/USA/FRA/CHE/NZL, 1119 rows
  - Variables: v2x_suffr, v2x_polyarchy, v2x_libdem, v2x_clphy, v2x_clpriv, v2x_clpol, v2xcl_dmove, v2xcl_slave, v2xcl_disc
- `data/dynamics_results_*.csv` — 20 Monte Carlo simulation files (~67MB total)
- `vdem-data.zip` — Original V-Dem download (keep for provenance)

## Phase 3 Figures — Complete
- `figures/alpha_suffrage.pdf` — V-Dem v15 annual suffrage data, 5 nations (1789-1980)
- `figures/alpha_abolition.pdf` — Ordinal trajectories, 4 polities (1760-1975)
- Script: `consent-theory-models/generate_phase3_figures.py`

## Future Data Directions
Additional figures could be built from existing + new data:

| Case Study | Data Available | Data Needed | Priority |
|------------|---------------|-------------|----------|
| Civil Rights (§10) | V-Dem v2x_clphy, v2x_clpriv, v2xcl_disc | — (sufficient) | Medium |
| Labor (§9) | — | OECD TUD / ILOSTAT / ICTWSS v6.1 (union density, CB coverage, strikes) | Medium |
| LGBT (§11) | — | Pew Global Attitudes, ILGA legal index | Low |
| Corporate (§12) | — | Ordinal coding from text (no dataset needed) | Low |
| Platform (§13) | — | Ordinal coding from text (no dataset needed) | Low |
| Climate (§14) | — | Ordinal coding from text (no dataset needed) | Low |
| Cross-case (§15) | V-Dem v2x_polyarchy, v2x_libdem | — (sufficient) | Medium |

V-Dem subset already has enough for civil rights and cross-case comparative figures.
OECD trade union data (ILOSTAT or ICTWSS v6.1) would complete the labor case.
Pew LGBT acceptance data would enhance §11 but ordinal coding is sufficient.

## Notes
- Title: "Consent-Theoretic Framework for Quantifying Legitimacy: Stakes, Voice, and Friction in Adversarial Governance"
- This is NOT consent-misalignment-paper (that's a different, deprecated paper)
- SSRN: 5918222
- Has code/, data/, and models — a full research package
- V3 template applied
