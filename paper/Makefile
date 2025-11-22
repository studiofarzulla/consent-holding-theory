# Makefile for Consent-Holding Theory Paper
# Based on tensor-defi arxiv-submission Makefile

# Main document
TARGET = Farzulla_2025_Consent_Holding
BIBFILE = references

# LaTeX compiler
LATEX = pdflatex
BIBTEX = bibtex

# Flags
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

# Default target - full build
.PHONY: all
all: pdf

# Full 4-pass build (pdflatex -> bibtex -> pdflatex -> pdflatex)
.PHONY: pdf
pdf: $(TARGET).pdf

$(TARGET).pdf: $(TARGET).tex $(BIBFILE).bib figures/*.png
	@echo "=== Pass 1: First pdflatex (generate .aux) ==="
	$(LATEX) $(LATEX_FLAGS) $(TARGET)
	@echo ""
	@echo "=== Pass 2: BibTeX (process citations) ==="
	$(BIBTEX) $(TARGET)
	@echo ""
	@echo "=== Pass 3: Second pdflatex (incorporate bibliography) ==="
	$(LATEX) $(LATEX_FLAGS) $(TARGET)
	@echo ""
	@echo "=== Pass 4: Third pdflatex (resolve cross-references) ==="
	$(LATEX) $(LATEX_FLAGS) $(TARGET)
	@echo ""
	@echo "=== Build complete! ==="
	@echo "Output: $(TARGET).pdf"

# Quick single-pass compile (for debugging LaTeX errors)
.PHONY: quick
quick:
	@echo "=== Quick compile (single pass) ==="
	$(LATEX) $(LATEX_FLAGS) $(TARGET)

# Clean auxiliary files (keep PDF)
.PHONY: clean
clean:
	@echo "=== Cleaning auxiliary files ==="
	rm -f $(TARGET).aux $(TARGET).log $(TARGET).out $(TARGET).toc $(TARGET).bbl $(TARGET).blg
	@echo "Cleaned. PDF preserved."

# Clean everything including PDF
.PHONY: distclean
distclean: clean
	@echo "=== Removing PDF ==="
	rm -f $(TARGET).pdf
	@echo "All generated files removed."

# Watch mode (requires inotify-tools)
.PHONY: watch
watch:
	@echo "=== Watch mode: auto-rebuild on file changes ==="
	@echo "Press Ctrl+C to stop"
	@while true; do \
		inotifywait -e modify $(TARGET).tex $(BIBFILE).bib; \
		make pdf; \
	done

# Word count estimate
.PHONY: wordcount
wordcount:
	@echo "=== Estimated word count ==="
	@pdftotext $(TARGET).pdf - | wc -w

# Spell check (requires aspell)
.PHONY: spell
spell:
	@echo "=== Interactive spell check ==="
	aspell -c $(TARGET).tex

# Help message
.PHONY: help
help:
	@echo "Makefile targets for $(TARGET)"
	@echo ""
	@echo "  make          - Full 4-pass build (default)"
	@echo "  make pdf      - Same as 'make'"
	@echo "  make quick    - Single-pass compile (fast, for debugging)"
	@echo "  make clean    - Remove auxiliary files (keep PDF)"
	@echo "  make distclean - Remove all generated files including PDF"
	@echo "  make watch    - Auto-rebuild on file changes (requires inotify-tools)"
	@echo "  make wordcount - Estimate word count from PDF"
	@echo "  make spell    - Interactive spell check (requires aspell)"
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "Build system: 4-pass LaTeX compilation"
	@echo "  Pass 1: pdflatex - Generate .aux file"
	@echo "  Pass 2: bibtex   - Process citations"
	@echo "  Pass 3: pdflatex - Incorporate bibliography"
	@echo "  Pass 4: pdflatex - Resolve cross-references"
