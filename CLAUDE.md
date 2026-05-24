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
├── main.tex              entry point — compile this
├── references.bib        BibTeX bibliography
├── readme.md             usage guide (how to compile / upload)
├── sections/
│   ├── 01-introduction.tex
│   ├── 02-database.tex
│   ├── 03-methodology.tex
│   └── 04-website-and-outputs.tex
├── figures/              place .pdf/.png figures here
├── data/
│   ├── raw/              Dallas Fed downloads (hp2504.xlsx, hpta2504.xlsx)
│   └── processed/        cleaned outputs for tables
└── references/           downloaded PDFs of key papers
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

## Team

- Konstantin Vasilopoulos — `ihpdr`/`exuber` R packages, dashboard code
- Enrique Martínez-García — Dallas Fed, leads International Research Group
- Themis Pavlidis — Lancaster University
- Ivan Paya — University of Alicante

## Dashboard code

`/c/Users/User/Documents/02-housing-observatory/02-dashboard/idash`

## Data source

https://www.dallasfed.org/research/international/houseprice
