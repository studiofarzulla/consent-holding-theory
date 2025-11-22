# Doctrine of Consensual Sovereignty (DoCS)

**Version**: 1.0.0
**Date**: November 2025
**Author**: Murad Farzulla
**DOI**: 10.5281/zenodo.17626763
**Website**: https://farzulla.org

## Overview

This repository contains the research materials, computational validation, and publication files for "The Doctrine of Consensual Sovereignty: Quantifying Legitimacy in Adversarial Environments."

The framework operationalizes political legitimacy through stakes-weighted consent alignment (α), friction (F), and legitimacy (L = w₁·α + w₂·P), enabling systematic comparison across democratic, technocratic, and algorithmic governance systems.

## Repository Structure

```
consent-theory/
├── paper/                          # LaTeX source and compiled PDF
│   ├── Farzulla_2025_Consent_Holding_v1.0.0.tex
│   ├── Farzulla_2025_Consent_Holding_v1.0.0.pdf
│   └── figures/                    # Paper figures (learning dynamics, etc.)
├── code/                           # Simulation code
│   ├── dynamics_examples.py        # Example usage of dynamic models
│   └── generate_learning_figures.py # Figure generation from data
├── data/                           # Monte Carlo simulation results
│   ├── dynamics_results_learning_*.csv  # Bayesian learning mode (50k rows each)
│   ├── dynamics_results_social_*.csv    # Social learning mode
│   ├── dynamics_results_stakes_*.csv    # Stakes evolution mode
│   └── dynamics_results_static_*.csv    # Static baseline
├── docs/                           # Documentation and reports
│   ├── DYNAMICS_INTEGRATION_SUMMARY.md
│   ├── dynamics_comparison_report.md
│   ├── CRITICISM_RESPONSE_WITH_DYNAMICS.md
│   ├── PAPER_REVISION_SUMMARY.md
│   ├── suggested_citations_consent_holding_paper.csv
│   └── QUICK_STATS.txt
├── figures/                        # Standalone figures
│   ├── alpha_historical_trajectories.png
│   ├── friction_trajectories.png
│   ├── legitimacy_frontier.png
│   └── robustness_parameter_heatmap.pdf
├── tables/                         # Data tables
├── consent-theory-models/          # Model implementations
├── dashboard/                      # Interactive visualization (if deployed)
├── references.bib                  # Complete bibliography (64 entries)
└── README.md                       # This file
```

## Key Results

**Computational Mechanism Comparison** (1000 Monte Carlo runs, 50 periods):
- **Stakes-Weighted DoCS**: α = 0.872 (final), F = 1.6 (98.5% friction reduction)
- **Equal Voice**: α = 0.870 (final), F = 1.8 (98.4% reduction)
- **Plutocracy**: α = 0.860 (final), F = 2.1 (98.2% reduction)

**Convergence Properties**:
- Monotonic α increase in 87.1% of DoCS runs
- Mean β₁ = 0.0048 (p < 0.001) for time regression
- Robust across 4 dynamic modes (static, learning, social, stakes)

## Theoretical Framework

**Five Axioms** (minimal assumptions):
- A1: Collective decision necessity
- A2: Outcome constraints (scarcity)
- A3: Shared reality
- A4: Preference heterogeneity
- A5: Stakes heterogeneity

**Five Core Results**:
- Theorem 1: Consent-holding necessity
- Theorem 2: Inevitable friction
- Definition 3: Legitimacy as consent alignment
- Postulate 4: Competence-consent trade-off
- Theorem 5: Minimal absolutism from relativism

## Computational Methods

**Bayesian Learning Dynamics**:
- Agents update preferences via Bayesian inference: `x*ᵢ(t+1) = (τ₀·x*ᵢ(t) + τ_obs,i·y(t)) / (τ₀ + τ_obs,i)`
- Stakes-weighted observation precision: `τ_obs,i = s*ᵢ`
- Noise: `y(t) = d(t) + ε`, `ε ~ N(0, 0.1)`

**Alternative Dynamics Implemented**:
1. **Static**: Cross-sectional baseline (no learning)
2. **Learning**: Bayesian updating with stakes-weighted attention
3. **Social**: DeGroot opinion dynamics via network diffusion
4. **Stakes**: Endogenous stakes evolution (winners accumulate power)

## Citation

```bibtex
@article{farzulla2025docs,
  author    = {Murad Farzulla},
  title     = {The Doctrine of Consensual Sovereignty: Quantifying Legitimacy in Adversarial Environments},
  year      = {2025},
  journal   = {Zenodo Preprint},
  doi       = {10.5281/zenodo.17626763},
  url       = {https://doi.org/10.5281/zenodo.17626763}
}
```

## Reproducibility

All simulation code, data, and LaTeX source are included. To regenerate figures:

```bash
cd code/
python generate_learning_figures.py
```

To compile the paper:

```bash
cd paper/
pdflatex Farzulla_2025_Consent_Holding_v1.0.0.tex
bibtex Farzulla_2025_Consent_Holding_v1.0.0
pdflatex Farzulla_2025_Consent_Holding_v1.0.0.tex
pdflatex Farzulla_2025_Consent_Holding_v1.0.0.tex
```

## Research Context

This work forms part of the **Adversarial Systems Research** program, investigating stability, alignment, and friction dynamics in complex systems where competing interests generate structural conflict. Related research:

- Cryptocurrency volatility and regulatory responses (TARCH-X event study)
- Trauma as maladaptive learning from adversarial training environments
- Multi-agent AI alignment with competing objectives

## License

This repository uses dual licensing:

- **Code** (`code/`, `consent-theory-models/`, scripts): [MIT License](LICENSE) - Permissive open-source
- **Paper** (`paper/` directory): [CC-BY-4.0](paper/LICENSE) - Attribution required for reuse
- **Data** (`data/` directory): CC0 Public Domain - No restrictions

See respective LICENSE files in root and `paper/` subdirectory for full terms.

## Contact

**Murad Farzulla**
Email: murad@farzulla.org
Website: https://farzulla.org
ORCID: 0009-0002-7164-8704

---

**Methodologies**: Research methodologies and reproducibility practices documented at https://farzulla.org/methodologies
