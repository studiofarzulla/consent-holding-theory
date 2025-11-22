# LaTeX Compilation Checklist

**Paper**: `Farzulla_2025_Consent_Holding_v1.0.0.tex`
**Status**: Ready for compilation

---

## Compilation Commands (4-pass required)

```bash
cd ~/Resurrexi/projects/need-work/consent-theory/paper/

# Pass 1: Generate .aux file
pdflatex -interaction=nonstopmode Farzulla_2025_Consent_Holding_v1.0.0.tex

# Pass 2: Generate bibliography
bibtex Farzulla_2025_Consent_Holding_v1.0.0

# Pass 3: Incorporate citations
pdflatex -interaction=nonstopmode Farzulla_2025_Consent_Holding_v1.0.0.tex

# Pass 4: Resolve cross-references
pdflatex -interaction=nonstopmode Farzulla_2025_Consent_Holding_v1.0.0.tex
```

---

## Post-Compilation Verification

### Critical Checks (MUST PASS)

- [ ] **PDF generated successfully** (`Farzulla_2025_Consent_Holding_v1.0.0.pdf` exists)
- [ ] **No compilation errors** (warnings OK, errors = STOP)
- [ ] **All citations resolved** (no "(?)" in references)
- [ ] **All equations render** (check eq:bayesian-update in Section 6.3.2)
- [ ] **All figures appear**:
  - [ ] Figure 6.1: `alpha_convergence_learning.pdf` (learning trajectories with CI bands)
  - [ ] Figure 6.2: `friction_reduction_learning.pdf` (friction collapse)
  - [ ] Figure 6.3: `convergence_speed_learning.pdf` (bar chart)
  - [ ] Other existing figures still render
- [ ] **Section numbering correct** (Section 7 = Dynamic Validation, Section 8 = Objections)

### Content Verification

- [ ] **Abstract mentions learning dynamics** ("Bayesian learning dynamics across 1000 Monte Carlo runs...")
- [ ] **Section 6.3.2 exists** ("Bayesian Preference Learning Dynamics")
- [ ] **Equation 6.1 present** (Bayesian update formula)
- [ ] **Results split into 6.3.3.1 (static) and 6.3.3.2 (learning)**
- [ ] **Section 7 present** ("Dynamic Validation and Robustness")
- [ ] **Plutocracy convergence discussion present** (co-option vs. legitimacy)
- [ ] **Figure captions updated** (mention learning dynamics, 95% CI, final α values)

### Formatting Checks

- [ ] **Two-column layout** maintained throughout main body
- [ ] **Single-column frontmatter** (abstract, metadata, TOC)
- [ ] **Single-column references** at end
- [ ] **Line spacing consistent** (1.5x in two-column sections)
- [ ] **Headers/footers on all pages** (farzulla.org, DOI, version, page numbers)
- [ ] **No overfull hbox errors** that break layout (warnings OK)

### Statistical Reporting Accuracy

Check these exact numbers appear in text:

- [ ] DoCS final α = **0.872** (or 0.8722)
- [ ] DoCS improvement = **+39%** (0.627 → 0.872)
- [ ] DoCS friction reduction = **98.5%** (105.5 → 1.6)
- [ ] DoCS convergence time = **18 periods**
- [ ] Monotonic runs = **87.1%** (DoCS)
- [ ] Ljung-Box Q = **1847.3**
- [ ] Friedman χ² = **3842.7**

---

## Common LaTeX Issues & Fixes

### Issue: Citations show as (?)
**Fix**: Run full 4-pass sequence. Check `references.bib` exists in paper directory.

### Issue: Figures not found
**Fix**: Verify `\graphicspath{{figures/}}` in preamble. Check PDF files exist:
```bash
ls -lh paper/figures/*.pdf
```

### Issue: Equation breaks two-column layout
**Fix**: Use `\begin{equation}...\end{equation}` (NOT `equation*` for numbered)

### Issue: Overfull \hbox warnings
**Fix**: Acceptable in two-column mode if < 10pt overfull. Reword if > 10pt.

### Issue: Figure placement weird
**Fix**: LaTeX auto-places floats. Use `[htbp]` for flexibility. Don't force `[H]`.

---

## Expected Output Size

- **PDF file size**: ~2-4 MB (with figures)
- **Page count**: ~35-40 pages (two-column, 1.5 spacing)
- **Compile time**: ~20-30 seconds per pass

---

## Troubleshooting Commands

### Check for errors in log
```bash
grep "^!" Farzulla_2025_Consent_Holding_v1.0.0.log
```

### Check for missing references
```bash
grep "Warning.*Citation" Farzulla_2025_Consent_Holding_v1.0.0.log
```

### Check for missing figures
```bash
grep "Warning.*File.*not found" Farzulla_2025_Consent_Holding_v1.0.0.log
```

### View last 50 lines of log
```bash
tail -50 Farzulla_2025_Consent_Holding_v1.0.0.log
```

---

## Success Criteria

✅ **Compilation succeeds** (PDF generated)
✅ **All new content appears** (Section 7, new figures, Bayesian learning)
✅ **Statistics accurate** (numbers match data)
✅ **No broken references** (citations resolve)
✅ **Professional appearance** (two-column, proper spacing)

If all checkboxes pass → **Ready for review/submission**

---

## Quick Visual Test

Open PDF and verify:
1. **Page 1**: Abstract mentions "Bayesian learning dynamics" and quantified results
2. **Section 6.3**: Has subsection 6.3.2 "Bayesian Preference Learning Dynamics"
3. **Figures**: Figure 6.1 shows **curved lines**, not flat (learning trajectories)
4. **Section 7**: Titled "Dynamic Validation and Robustness" (not "Limitations")
5. **References**: Render at end in single column

---

## If Compilation Fails

1. **Check error message** in terminal output
2. **Read .log file** (search for "^!" lines)
3. **Common culprits**:
   - Missing `references.bib`
   - Figures not in `figures/` directory
   - Typo in `\includegraphics` filename
   - Unescaped special characters (%, &, $, _, {, })
4. **Nuclear option**: Delete auxiliary files and retry
   ```bash
   rm *.aux *.bbl *.blg *.log *.out *.toc
   # Then re-run 4-pass sequence
   ```

---

## After Successful Compilation

1. **Review PDF thoroughly** (read revised sections)
2. **Check figure quality** (resolution, labels, colors)
3. **Verify statistics** (compare to `PAPER_REVISION_SUMMARY.md`)
4. **Run spell check** (if available)
5. **Share with collaborators** (if applicable)

Then you're good to submit, publish, or archive!
