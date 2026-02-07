# Consent-Theoretic Framework for Quantifying Legitimacy

**Stakes, Voice, and Friction in Adversarial Governance**

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17684676-blue.svg)](https://doi.org/10.5281/zenodo.17684676)
[![SSRN](https://img.shields.io/badge/SSRN-5918222-blue.svg)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5918222)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status](https://img.shields.io/badge/Status-Preprint-green.svg)](https://doi.org/10.5281/zenodo.17684676)

**Working Paper DAI-2501** | [Dissensus AI](https://dissensus.ai)

## Abstract

This paper develops a unified analytical framework for measuring political legitimacy across heterogeneous governance domains. Building on insights from constitutional political economy, social choice theory, and institutional analysis, the framework establishes consent-holding -- the mapping from decision domains to those with authority over them -- as a structural necessity of collective action. We formalize this intuition through five axioms and five theorems, demonstrating that legitimacy can be operationalized as stakes-weighted consent alignment alpha(d,t), while friction F(d,t) measures the deviation between outcomes and stakeholder preferences. The framework bridges normative democratic theory and empirical prediction, generating testable hypotheses about institutional stability. Historical validation examines suffrage expansion, abolition movements, labor rights, and contemporary platform governance, demonstrating how misalignment between stakes and voice generates observable instability. Unlike existing approaches that prescribe ideal institutions, this framework provides analytical tools for measuring legitimacy within any governance structure, enabling systematic comparison across democratic, technocratic, and algorithmic systems. Computational mechanism comparison via Bayesian learning dynamics across 1000 Monte Carlo runs demonstrates relative performance under adaptive agents: when preferences update based on observed policy outcomes, stakes-weighted DoCS achieves highest final alignment (alpha = 0.872) with lowest terminal friction (F = 1.5, 94.9% reduction from initial F = 30.3). This comparative advantage holds across static baseline (alpha = 0.627), learning dynamics (alpha = 0.872), and alternative temporal mechanisms, suggesting stakes-weighting produces superior initial matches that persist even when agents adapt to institutional performance. The framework's domain-specific approach resolves the apparent tension between consent and competence, showing both as complementary dimensions of institutional legitimacy.

## Key Findings

| Finding | Result |
|---------|--------|
| Stakes-weighted DoCS final alignment | alpha = 0.872, F = 1.5 (94.9% friction reduction) |
| Equal Voice comparison | alpha = 0.870, F = 1.8 (94.2% reduction) |
| Plutocracy comparison | alpha = 0.860, F = 2.1 (93.5% reduction) |
| Monotonic alpha increase | 87.1% of DoCS runs |
| Time regression | Mean beta_1 = 0.0048 (p < 0.001) |
| Simulation scale | 1000 Monte Carlo runs, 50 periods, 4 dynamic modes |

## Repository Structure

```
consent-holding-theory/
├── paper/                      # LaTeX source and compiled PDF
│   ├── Farzulla_2025_Consent_Holding_v1.0.2.tex
│   └── figures/                # Paper figures
├── code/                       # Simulation code
│   ├── dynamics_examples.py    # Example usage of dynamic models
│   └── generate_learning_figures.py  # Figure generation
├── data/                       # Monte Carlo simulation results
│   ├── dynamics_results_learning_*.csv
│   ├── dynamics_results_social_*.csv
│   ├── dynamics_results_stakes_*.csv
│   └── dynamics_results_static_*.csv
├── consent-theory-models/      # Model implementations
├── dashboard/                  # Interactive visualization
├── figures/                    # Standalone figures
├── tables/                     # Data tables
└── references.bib              # Bibliography (89 entries)
```

## Replication

```bash
cd code/
python generate_learning_figures.py
```

## Keywords

Legitimacy, Consent, Political Stability, Social Choice, Institutional Design, Friction, Stakes-Weighting

## Citation

```bibtex
@article{farzulla2025consent,
  author    = {Farzulla, Murad},
  title     = {Consent-Theoretic Framework for Quantifying Legitimacy: Stakes, Voice, and Friction in Adversarial Governance},
  year      = {2025},
  doi       = {10.5281/zenodo.17684676},
  url       = {https://doi.org/10.5281/zenodo.17684676}
}
```

## Authors

- **Murad Farzulla** -- [Dissensus AI](https://dissensus.ai) & King's College London
  - ORCID: [0009-0002-7164-8704](https://orcid.org/0009-0002-7164-8704)
  - Email: murad@dissensus.ai

## License

Paper content: [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)
Code: [MIT License](LICENSE)
