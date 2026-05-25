# Project: International House Price Database — Technical Report

## What this is

LaTeX technical report for the International Housing Observatory
(https://int.housing-observatory.com/). Documents the Dallas Fed
International House Price Database (IHPD), GSADF/PSY-IVX methodology,
and the Observatory's web platform.

Hosted on Overleaf. Compile entry point: `main.tex`.

## Folder layout

```
04-technical-report/
├── main.tex                        entry point — compile this
├── references.bib                  BibTeX bibliography
├── readme.md                       usage guide (how to compile / upload)
├── sections/
│   ├── 01-introduction.tex
│   ├── notation.tex                abbreviations table (unnumbered section)
│   ├── 02-database.tex             IHPD construction, variables, sources
│   ├── 03-data-access.tex          data retrieval, ihpdr, update workflow
│   ├── 03-methodology.tex          GSADF + PSY-IVX
│   ├── 04-website-and-outputs.tex  dashboard, reports, software
│   ├── appendix-a-countries.tex    country source table
│   ├── appendix-b-changelog.tex    version history
│   └── bibliography.tex            wraps \bibliographystyle + \bibliography
├── figures/                        place .pdf/.png figures here
├── data/
│   ├── raw/                        Dallas Fed downloads (hp2504.xlsx, hpta2504.xlsx)
│   └── processed/                  cleaned outputs for tables
└── references/                     downloaded PDFs of key papers
```

## Key domain facts

- **Data:** 25 countries, 1975 Q1 – present, quarterly
- **Variables:** HPI, RHPI, PDI, RPDI — all rebased 2005 = 100; PCE deflated
- **Methods:** GSADF test (Phillips, Shi & Yu 2015 IER) + PSY-IVX (Shi & Phillips 2021 JES)
- **R packages:** `ihpdr` (data access), `exuber` (GSADF estimation) — both maintained by Konstantin
- **Latest data:** `data/raw/hp2504.xlsx` = Q4 2025; `hpta2504.xlsx` = BSADF sequences

## References policy

**Always use the published journal version**, not working paper, where one exists:

| Working paper | Published as |
|---|---|
| GMI WP 165 (Pavlidis et al. 2013) | JMCB 2016, 48(8):1541–1578 — key `pavlidis2016` |
| Phillips, Shi & Yu — | IER 2015, 56(4) — keys `phillips2015a`, `phillips2015b` |
| Shi & Phillips — | JES 2021, 35(5) — key `shi2021` |
| GMI WP 99 (Mack & MG 2011) | **No journal version** — working paper only, key `mack2011` |
| GMI WP 325 (Pavlidis et al. 2017/2018) | **No journal version** — working paper only, key `pavlidis2018` |
| `exuber` `@manual` | JSS 2022, 103(10):1–26 — key `vasilopoulos2022` (use this for methodology citations) |

## Team

| Name | Role | Affiliation |
|---|---|---|
| Enrique Martínez-García | Director | Federal Reserve Bank of Dallas |
| Themis Pavlidis | Director | Lancaster University Management School |
| Ivan Paya | Director | University of Alicante |
| Kostas Vasilopoulos | Web Administrator | — (`ihpdr`/`exuber` R packages, dashboard) |
| Erik Andres Escayola | Researcher | — |

## Dashboard code

`/c/Users/User/Documents/02-housing-observatory/02-dashboard/idash`

## Data source

https://www.dallasfed.org/research/international/houseprice

---

## Report format and versioning

### Document type

Methodological note / data descriptor — NOT a journal article. Living document
updated quarterly alongside the website and data releases.

Genre precedent: Dallas Fed WP99 ("A Cross-Country Quarterly Database of Real
House Prices: A Methodological Note", Mack & Martínez-García 2011).

### Versioning scheme: semantic versioning

Format: `vMAJOR.MINOR.PATCH`

| Increment | When |
|---|---|
| MAJOR | Structural change: new section, new method, breaking change to data schema |
| MINOR | Data update (quarterly release) or methodology refinement |
| PATCH | Correction, typo fix, clarification |

Starting version: `v1.0.0` — first complete release.

Version appears in: title page, PDF filename (`ihpd-technical-report-v1.0.0.pdf`),
and the version history table (Section — Changelog).

### Citability

Publish each release to Zenodo → DOI per version. Cite as:
> Vasilopoulos et al. (2025). *International Housing Observatory: Data and
> Methods*. Technical Report v1.0.0. doi:10.5281/zenodo.XXXXXXX

### Report structure (canonical sections)

```
1. Introduction
   1.1 Background
   1.2 The International Housing Observatory
   1.3 Purpose of This Report
   1.4 Scope

2. The International House Price Database
   2.1 Country Coverage and Time Span
   2.2 Variable Definitions (HPI, RHPI, PDI, RPDI)
   2.3 Seasonal Adjustment
   2.4 Real Series Construction
   2.5 Programmatic Access — ihpdr R package

3. Econometric Methodology
   3.1 Exuberance Detection: GSADF Test (PSY 2015)
   3.2 Fundamental Decomposition: PSY-IVX (Shi & Phillips 2021)
   3.3 Rolling Window and Critical Values
   3.4 Estimation — exuber R package

4. Web Platform and Outputs
   4.1 Dashboard
   4.2 Quarterly PDF Reports
   4.3 Update Cadence

Appendix A. Country Sources
Appendix B. Changelog / Version History
```

### Key exemplars for reference

| Document | Why relevant |
|---|---|
| [BIS WP1149](https://www.bis.org/publ/work1149.pdf) | Best narrative model for describing a new dataset |
| [Eurostat ESMS HPI](https://ec.europa.eu/eurostat/cache/metadata/en/prc_hpi_inx_esmshpi_se.htm) | Best operational model: structured fields, dated, versioned |
| [OECD RPPI FAQ](https://www.oecd.org/en/data/insights/data-explainers/2024/07/Residential-Property-Price-Indices-and-related-housing-indicators-Frequently-Asked-Questions.html) | Living reference doc with persistent URL |
| [Handbook on RPPIs 2013](https://economics.ubc.ca/wp-content/uploads/sites/38/2013/06/pdf_paper_erwin-diewert-eurostat-handbook-residential.pdf) | Gold standard for HPI methodology depth (ILO/IMF/OECD/Eurostat/WB) |
| [StatCan Quality Guidelines 12-539-X](https://unstats.un.org/unsd/dnss/docs-nqaf/Canada-12-539-x2009001-eng.pdf) | Minimum documentation requirements |
| [Dallas Fed Appendix A](https://www.dallasfed.org/~/media/documents/research/international/houseprice/appendixA.pdf) | Country-source reference — already covers our Appendix A |
