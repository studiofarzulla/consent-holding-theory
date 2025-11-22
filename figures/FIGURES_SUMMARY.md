# Consent-Holding Theory: Figure Summary

**Generated:** November 15, 2025
**Output Directory:** `/home/kawaiikali/Resurrexi/projects/need-work/consent-theory/figures/`

---

## Figure 1: α-P Frontier (Competence-Consent Trade-off)
**File:** `alpha_p_frontier.png` (311 KB)

**Visual Content:**
- Scatter plot comparing governance systems on consent alignment (α) vs performance (P)
- 5 governance systems plotted: Technocracy, Democracy, Authoritarianism, Weighted Democracy, Citizens' Assembly
- 3 iso-legitimacy curves showing different legitimacy functions (L = w₁α + w₂P) with varying weight ratios
- Demonstrates trade-offs between competence and consent in governance design

**Use Case:** Introduce the theoretical framework showing that different governance systems optimize different legitimacy functions.

---

## Figure 2: Historical Friction Trajectories
**File:** `friction_trajectories.png` (285 KB)

**Visual Content:**
- Line plot showing friction F(d) over time (1800-2025) across 4 domains
- **Women's Suffrage:** Sharp spike during suffragette movement (1890-1920), resolution at voting rights
- **Abolition:** Exponential rise to Civil War, partial resolution followed by Jim Crow plateau
- **LGBT Rights:** Stonewall spike, AIDS crisis activism, gradual decline with marriage equality
- **Platform Governance:** Recent exponential rise (2010-2025) still ongoing
- Vertical markers for key historical events

**Use Case:** Demonstrate friction dynamics and how consent deficits manifest as social instability across different historical contexts.

---

## Figure 3: Consent Alignment Over Time (α(d) Trajectories)
**File:** `alpha_historical_trajectories.png` (280 KB)

**Visual Content:**
- Line plot showing α(d) evolution (1800-2050) across 5 domains
- **Suffrage:** Steady expansion from 0.05 to 0.9 (near-universal adult suffrage)
- **Labor:** Rise to peak 0.65 (1975), decline to 0.35 (union decline, gig economy)
- **LGBT Rights:** Rapid rise 2000-2015, slight backlash
- **Platform Governance:** Flat at 0.15 (ongoing low consent)
- **Climate Policy:** Projection showing potential rise with guardian mechanisms
- Shaded "legitimacy threshold" region (α > 0.6)

**Use Case:** Show historical expansion of consent-holding and identify contemporary domains with consent deficits.

---

## Figure 4: Monte Carlo Mechanism Comparison
**File:** `monte_carlo_mechanisms.png` (167 KB)

**Visual Content:**
- Grouped bar chart comparing 4 mechanisms: Dictator, Simple Majority, Stakes-Weighted, Technocracy
- Three metrics per mechanism:
  - **Friction E[F]:** Expected friction (red bars)
  - **Alignment E[α]:** Expected consent alignment (blue bars)
  - **Instability P(Y=1):** Probability of instability (gray bars)
- Error bars showing 95% confidence intervals
- Stakes-weighted mechanism clearly minimizes friction and instability while maximizing alignment

**Use Case:** Provide empirical validation (via simulation) that stakes-weighted mechanisms outperform alternatives.

---

## Figure 5: Corporate Governance Consent Matrix
**File:** `corporate_consent_matrix.png` (307 KB)

**Visual Content:**
- Side-by-side heatmaps comparing current vs proposed corporate governance
- **Left (Current):** Shareholder primacy model showing concentrated power (α values: 0.20-0.40)
- **Right (Proposed):** Stakes-weighted model redistributing consent power (α values: 0.70-0.85)
- 4 stakeholders (rows): Shareholders, Workers, Customers, Community
- 5 domains (columns): Strategy, Executive Pay, Wages, Product Safety, Environmental Impact
- Cell values: sᵢ(d) × Cᵢ (stakes × consent power)
- Color intensity represents consent power magnitude

**Use Case:** Concrete application showing how stakes-weighted consent could transform corporate governance to reduce stakeholder friction.

---

## Technical Specifications

**All figures:**
- **Resolution:** 300 DPI (publication quality)
- **Format:** PNG with tight bounding box
- **Dimensions:** 10×6 inches (landscape) or 8×10 inches (portrait)
- **Font:** DejaVu Sans (clear sans-serif)
- **Color scheme:** Professional grayscale + navy blue accent (#1f77b4)
- **Grid:** Light gray, subtle
- **Spines:** Only left and bottom (clean academic style)

**Total size:** 1.4 MB for all 5 figures

---

## Regeneration

To regenerate all figures:

```bash
cd /home/kawaiikali/Resurrexi/projects/need-work/consent-theory
python generate_figures.py
```

All visualization code is self-contained in `generate_figures.py`.
