# Monograph Expansion: Shared Context for Writing Agents

## Framework Summary

This paper develops **consent-holding theory** — an axiomatic framework for measuring political legitimacy across governance domains. The core idea: in any domain where collective decisions produce shared consequences, someone must hold authority to decide. This consent-holder mapping H_t(d) is a structural necessity.

### Key Notation
- **alpha(d,t)** = consent alignment = stakes-weighted share of decision power held by affected parties
- **F(d,t)** = friction = stakes-weighted deviation between outcomes and stakeholder preferences
- **L(d,t)** = legitimacy = w1*alpha + w2*P (consent-performance trade-off)
- **H_t(d)** = consent-holder mapping (who decides in domain d at time t)
- **s_i(d)** = stakes of agent i in domain d
- **C_{i,d}** = consent power of agent i in domain d
- **eff_voice_i** = effective voice (formal authority + capacity)
- **S_d** = affected set = {i | s_i(d) > 0}

### Core Results
- **T1 (Consent-Holding Necessity)**: Wherever decisions occur, some H_t(d) must exist
- **T2 (Inevitable Friction)**: Plural preferences guarantee friction unless perfect alignment
- **D1 (Legitimacy as Alignment)**: alpha(d,t) operationalizes legitimacy empirically
- **P1 (Competence-Consent Trade-Off)**: L = w1*alpha + w2*P
- **T3 (Minimal Absolutism)**: Value relativism doesn't extend to structural necessities

### Hypotheses (H1-H5)
- H1: Higher alpha predicts lower future F
- H2: Increasing Cov(s_i, C_i) reduces friction
- H3: Threshold effects — alpha < tau produces discontinuous instability
- H4: Persistent F predicts future alpha increases (reform pressure)
- H5: Performance interactions — high P partially compensates for low alpha

### Monte Carlo Results
- Stakes-weighted DoCS: final alpha=0.872, F reduction 94.9%, converges in 18 periods
- DoCS ranks first across ALL 4 dynamic modes (static, learning, social, stakes)
- 1000 runs x 50 timesteps x 5 mechanisms

## Equations (for reference in text)

Consent alignment:
```latex
\alpha(d,t) = \frac{\sum_{i \in S_d} s_i(d) \cdot \text{eff\_voice}_i(d,t)}{\sum_{i \in S_d} s_i(d)}
```

Friction:
```latex
F(d,t) = \sum_i s_i(d) \cdot \delta(x_d(t), x^*_{i,d})
```

Legitimacy:
```latex
L(d,t) = w_1 \cdot \alpha(d,t) + w_2 \cdot P(d,t)
```

Panel regression:
```latex
F_{d,t} = \beta_0 + \beta_1 \cdot \alpha_{d,t} + \beta_2 \cdot P_{d,t} + \gamma \cdot X_{d,t} + \mu_d + \lambda_t + \varepsilon_{d,t}
```

## Monograph Structure (v2.0.0)

### Part I: Foundations (Sections 1-4)
Mostly exists. Sec 2 gets expanded lit review. Sec 4 gets new subsections.

### Part II: Normative Architecture (Section 5)
Promoted from current Appendices F+G + expanded current Section 5.

### Part III: Historical Validation (Sections 6-15) — PRIMARY NEW CONTENT
Each historical section MUST have:
1. **Domain Definition** — what governance domain, who are stakeholders
2. **Alpha Proxy Construction** — how to measure consent alignment (quantitative where possible: enfranchised/total population, union density, board composition, voter registration, legal recognition indices)
3. **Friction Proxy Construction** — how to measure friction (protest events, petition counts, litigation rates, strike days, boycotts)
4. **Time Series Narrative** — trace alpha(d,t) and F(d,t) over time with specific dates/events
5. **Framework Testing** — which hypotheses (H1-H5) does this case illuminate?
6. **Cross-Case Connections** — how does this case relate to others?

### Part IV: Computational Validation (Sections 16-17)
Exists. Section 17 gets promoted Appendix D claims.

### Part V: Implications & Extensions (Sections 18-21)
Objections (add 2 new), Weight Determination, Research Agenda, Conclusion.

### Appendices (reduced)
A: Robustness Tables, B: Mathematical Proofs, C: Data Sources & Coding Protocols [NEW], D: Formal Model Specification

## Writing Guidelines

1. **LaTeX format** — write as raw LaTeX section content. No preamble, no \begin{document}. Just \section{}, \subsection{}, content.
2. **Citation style** — use \citet{key} for textual and \citep{key} for parenthetical. Use \citeyearpar{key} for year-only.
3. **Cross-references** — use \label{sec:section-name} and \ref{sec:section-name}
4. **Equations** — use equation environment with \label{eq:name}
5. **Tone** — rigorous academic prose, clear and precise. Not corporate. This is a monograph for political scientists, economists, and governance researchers.
6. **Framework integration** — always connect back to alpha, F, H_t(d). Historical cases aren't just narratives — they're framework demonstrations.
7. **Figures** — reference alpha/F time series figures that will be created in Phase 3. Use \ref{fig:alpha-suffrage} style references.
8. **Tables** — use booktabs style (toprule, midrule, bottomrule)
9. **Self-citation** — cite farzulla2025stakes (Stakes Without Voice), farzulla2025rom (ROM), farzulla2025aoc (Axiom of Consent) where relevant
10. **Length** — each page is ~40 lines of LaTeX or ~350 words. Hit your page targets.

## Orphan Bib Entries — Section Assignments

### Section 2.4 (CPR Expansion) — 7 entries
agrawal1999enchantment, dietz2003drama, gibson2005local, baland1996halting, berkes2006globalization, weeratunge2014smallscale, ostrom2010

### Section 2.5 (Deliberative Expansion) — 8 entries
bouricius2013democracy, fishkin2009when, participatory2023, smith2009democratic, wampler2007participatory, schneiderhan2008realizing, niemeyer2011emancipatory, hendriks2014emergent

### Section 2.9 (Political Anthropology) — 3 entries
graeber2021, boehm1999, scott2017

### Section 2.10 (Social Movements) — 7 entries
olson1965logic, tarrow1998power, tilly2007, tilly2008contentious, schussman2005process, singh2020globalization, stekelenburg2010social

### Section 2.11 (Institutional Theory) — 8 entries
acemoglu2012why, acemoglu2019narrow, linz1996problems, sartori1994comparative, nolan2015international, gerring2015institutional, soifer2012causal, evans1995embedded, slater2010informative

### Section 5 (Social Contract expanded) — 7 entries
rawls1993, habermas1987, weber1978economy, raz1986morality, calhoun1994habermas, condorcet1785essay, campos2008implementing

### Section 7 (Suffrage) — 5 entries
acemoglu2000why, chapman2020extension, batinti2022voting, berlinski2010extension, mason1912, miller2021, pankhurst1914, higginson1859

### Section 8 (Abolition) — 1 entry
abolitionsociety1787

### Section 9 (Labor) — 3 entries
bosch2013activating, cole1923, hinton1973

### Section 10 (Civil Rights) — 4 entries
branch1988, king1963, levy1998, parks1992

### Section 11 (LGBT) — 1 entry (+ stekelenburg2010social from 2.10)
(stekelenburg2010social referenced here too)

### Section 12 (Corporate Governance) — 6 entries
doyle2020nordic, ferrarini2012corporate, jackson2010corporate, aguilera2015connecting, goranova2014shareholder, edmans2017equity

### Section 13 (Platform Governance) — 4 entries
gorwa2020algorithmic, resseguier2020ai, costanza2020design, mittelstadt2017individual

### Section 14 (Climate) — 4 entries
ukclimate2022, ukclimate2020, lorenzoni2025review, lorenzoni2007barriers, wells2021citizen

### Section 18 (New Objections) — 3 entries
anderson2006, gerver2024, thaler2008

### Section 19 (Weight Determination) — 3 entries
shapley1953value, binmore1989outside, compte2010coalitional

### Section 20 (Research Agenda) — 3 entries
lalley2018quadratic, posner2017quadratic, bovens2014oxford

### Section 1 (Introduction) — 1 entry
farzulla2025stakes

### Possible drop
maloy2012divine (uncertain relevance — "history of genius"), borda1781memoire, mclean1994condorcet

## Agent Assignments

### lit-expander
**Sections:** 2.4 (expand), 2.5 (expand), 2.9 (NEW), 2.10 (NEW), 2.11 (NEW)
**Output:** paper/sections_lit_expander.tex
**Orphans:** See sections 2.4, 2.5, 2.9, 2.10, 2.11 above (~33 entries)
**Pages:** ~8

### historian-1
**Sections:** 6 (NEW methodology), 7 (REWRITE suffrage), 8 (REWRITE abolition)
**Output:** paper/sections_historian_1.tex
**Orphans:** See sections 7, 8 above (~9 entries)
**Pages:** ~14

### historian-2
**Sections:** 9 (REWRITE labor), 10 (NEW civil rights), 12 (NEW corporate governance)
**Output:** paper/sections_historian_2.tex
**Orphans:** See sections 9, 10, 12 above (~13 entries)
**Pages:** ~16

### historian-3
**Sections:** 11 (NEW LGBT), 13 (EXPAND platform), 14 (NEW climate), 15 (EXPAND scope conditions)
**Output:** paper/sections_historian_3.tex
**Orphans:** See sections 11, 13, 14 above (~9 entries + comparative table)
**Pages:** ~16

### normative-writer
**Sections:** 5 (consolidate + expand social contract), 18 (new objections 8-9), 19 (weight determination), 20 (research agenda), Appendix C (data sources)
**Output:** paper/sections_normative.tex
**Orphans:** See sections 5, 18, 19, 20 above (~16 entries)
**Pages:** ~14
