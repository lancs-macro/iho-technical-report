# How to Use This Report

Technical report on the International House Price Database (IHPD) and the
International Housing Observatory. Written in LaTeX; hosted on Overleaf.

---

## Compile locally

Requires a LaTeX distribution (TeX Live, MiKTeX, or MacTeX).

```bash
# Full build (run twice to resolve cross-references)
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or use `latexmk` for automatic dependency resolution:

```bash
latexmk -pdf main.tex
latexmk -pdf -pvc main.tex   # continuous preview mode
```

Output: `main.pdf`

---

## Upload to Overleaf

1. Zip the entire folder: `zip -r report.zip . --exclude '*.xlsx' --exclude '*.pdf' --exclude 'data/*'`
2. Overleaf → New Project → Upload Project → select `report.zip`
3. Set compiler to **pdfLaTeX** and main document to `main.tex`
4. Overleaf compiles automatically on save

> **Note:** Do not upload the `data/` folder or large PDFs in `references/` — Overleaf has a 50 MB project limit.

---

## Update data

New Dallas Fed quarterly releases appear at:
https://www.dallasfed.org/research/international/houseprice

Download pattern: `hp{YY}{Q}.xlsx` (e.g., `hp2504.xlsx` = 2025 Q4)

**Via R:**
```r
library(ihpdr)
raw   <- hpdr_raw()    # latest HPI, RHPI, PDI, RPDI
bsadf <- hpdr_bsadf()  # latest BSADF sequences
```

Save new files to `data/raw/`.

---

## Edit the report

| What to change | File |
|---|---|
| Title, authors, abstract | `main.tex` |
| Introduction | `sections/01-introduction.tex` |
| Database description | `sections/02-database.tex` |
| GSADF / PSY-IVX methodology | `sections/03-methodology.tex` |
| Website and outputs | `sections/04-website-and-outputs.tex` |
| Bibliography | `references.bib` |
| Figures | `figures/` (use `.pdf` or `.png`) |

---

## Add a figure

1. Place file in `figures/` (e.g., `figures/bsadf_us.pdf`)
2. In the relevant `.tex` section:

```latex
\begin{figure}[ht]
  \centering
  \includegraphics[width=0.85\textwidth]{bsadf_us}
  \caption{BSADF sequence for the United States.}
  \label{fig:bsadf_us}
\end{figure}
```

---

## Add a citation

Add the entry to `references.bib`, then cite in text:

```latex
\citet{key}    % Jones (2020) showed that ...
\citep{key}    % ... (Jones, 2020)
```

**Policy:** Always use the published journal version. See `CLAUDE.md` for the
working-paper → journal mapping.

---

## Key links

| Resource | URL |
|---|---|
| Observatory | https://int.housing-observatory.com/ |
| Data page | https://www.dallasfed.org/research/international/houseprice |
| `ihpdr` CRAN | https://cran.r-project.org/web/packages/ihpdr/ |
| `exuber` CRAN | https://cran.r-project.org/web/packages/exuber/ |
| Housing Fever (PSY-IVX) | https://housing-fever.com/ |
