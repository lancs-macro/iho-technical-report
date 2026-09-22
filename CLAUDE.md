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
│   ├── 02-database.tex             IHPD coverage, variables, construction, limitations
│   ├── 03-data-access.tex          release files, ihpdr, data API, update workflow
│   ├── 04-methodology.tex          GSADF + PSY-IVX + nowcast
│   ├── 05-website-and-outputs.tex  dashboard, reports, software
│   ├── 06-roadmap.tex              planned extensions (database + toolkit)
│   ├── acknowledgements.tex
│   ├── appendix-a-countries.tex    coverage table + pointer to WP99 / Dallas Fed Appendix A
│   ├── appendix-b-changelog.tex    version history
│   └── bibliography.tex            wraps \bibliographystyle + \bibliography
├── figures/                        place .pdf/.png figures here
├── data/
│   ├── raw/                        Dallas Fed downloads (hp2504.xlsx, hpta2504.xlsx)
│   └── processed/                  cleaned outputs for tables
└── references/
    ├── *.pdf                       downloaded PDFs of key papers
    └── extracted/                  pdftotext -layout output, for grep/reuse
```

Regenerate extracted text after adding a PDF:
`cd references && for f in *.pdf; do pdftotext -layout "$f" "extracted/${f%.pdf}.txt"; done`

## Key domain facts

**Verified against `data/raw/hp2504.xlsx` — do not "correct" these from memory.**

- **Coverage:** 26 economies + 2 aggregate series, 1975 Q1 – 2025 Q4, quarterly (204 obs)
- **Economies:** Australia, Belgium, Canada, Colombia, Croatia, Denmark, Finland,
  France, Germany, Ireland, Israel, Italy, Japan, Luxembourg, Netherlands,
  New Zealand, Norway, Portugal, Slovenia, South Africa, South Korea, Spain,
  Sweden, Switzerland, UK, US
- **Aggregates:** `Aggregate - 2005 Fixed Weights` and `Aggregate - Dynamic Weights`
  (dashboard headline charts use the dynamic one)
- **Panel is balanced** — no interior gaps. That is a product of splicing /
  interpolation / backcasting, NOT of uniform national reporting since 1975.
- **Variables:** HPI, RHPI, PDI, RPDI — rebased 2005 = 100; real series PCE deflated;
  income per *working-age* capita
- **File naming:** `hp{YY}{Q}.xlsx` — YY = year, Q = last quarter included.
  `hp2504.xlsx` = data through 2025 Q4 (released first full week of Jan 2026).
  Not a release-month code.
- **Sheet layout:** one sheet per *variable* (`Note`, `HPI`, `RHPI`, `PDI`, `RPDI`),
  quarters in rows, economies in columns. NOT one sheet per country.
- **`hpta{YY}{Q}.xlsx`:** sheets `Note`, `LAG=1`, `LAG=4`; GSADF/SADF stats + 95% CVs
  per country, and BSADF sequences for RHPI and RHPI/RPDI (start 1988 Q2)
- **Release schedule:** first full week of Jan / Apr / Jul / Oct, 3-month lag
- **Methods:** GSADF (Phillips, Shi & Yu 2015 IER) + PSY-IVX (Shi & Phillips 2021 JES)
  + mixed-frequency DFM nowcast
- **Seasonal adjustment:** BSTS model (Harvey 1989), ML + Kalman filter — also
  supplies the Dallas Fed's own backcasts/nowcasts that complete each release

## Actual API surface (verified in `03-data/api/int/01-download.R`)

`ihpdr`: `ihpd_get(version = )`, `ihpd_versions()`, `ihpd_countries()`,
`ihpd_get_local(path)`. Output cols: `Date, country, hpi, rhpi, pdi, rpdi`.
There is no `hpdr_raw()` / `hpdr_sadf()` / `hpdr_bsadf()` — an early draft of
this report invented those.

`exuber`: `radf(x, lag = 1)`; critical values from the stored table
`radf_crit[[NROW(x)]]` (not simulated per run); `tidy_join()`, `augment_join()`,
`datestamp(est, cv, min_duration = 2)`.

Dashboard reports 90% / 95% / 99% critical values. Reporting convention:
≥95% = evidence of exuberance; 90–95% = caution; <90% = none.

Observatory JSON API: `https://api.housing-observatory.com/datasets/int/index.json`

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
1. Introduction — background, the Observatory, purpose, scope
2. The International House Price Database
   2.1 Overview and relationship to WP99   <- we summarise, WP99 is authoritative
   2.2 Coverage (26 economies + 2 aggregates)
   2.3 Variables
   2.4 Construction methodology (benchmark, frequency conversion, splicing,
       backcast/nowcast, BSTS seasonal adjustment, rebasing)
   2.5 Release schedule and vintages
   2.6 Data quality and known limitations
3. Data Access — release files, ihpdr, Observatory JSON API, update workflow
4. Econometric Methodology
   4.1 The toolkit (three tools, three questions)
   4.2 GSADF / BSADF date-stamping
   4.3 Reporting conventions
   4.4 PSY-IVX
   4.5 Nowcasting (mixed-frequency DFM)     <- Erik owns this subsection
5. Platform and Outputs — dashboard, quarterly reports, nowcast reports,
   Housing Fever, software
6. Planned Extensions — database, toolkit, real-time evaluation
Appendix A. Coverage and country documentation
Appendix B. Changelog / Version History
```

### Editorial stance

The report is a **companion to WP99, not a replacement**. Where WP99 already
documents something in depth — above all the country-by-country sources — point
there rather than restating it. Do not reconstruct per-country source tables
from memory; that is how the previous draft acquired invented sources.

### Key exemplars for reference

| Document | Why relevant |
|---|---|
| [BIS WP1149](https://www.bis.org/publ/work1149.pdf) | Best narrative model for describing a new dataset |
| [Eurostat ESMS HPI](https://ec.europa.eu/eurostat/cache/metadata/en/prc_hpi_inx_esmshpi_se.htm) | Best operational model: structured fields, dated, versioned |
| [OECD RPPI FAQ](https://www.oecd.org/en/data/insights/data-explainers/2024/07/Residential-Property-Price-Indices-and-related-housing-indicators-Frequently-Asked-Questions.html) | Living reference doc with persistent URL |
| [Handbook on RPPIs 2013](https://economics.ubc.ca/wp-content/uploads/sites/38/2013/06/pdf_paper_erwin-diewert-eurostat-handbook-residential.pdf) | Gold standard for HPI methodology depth (ILO/IMF/OECD/Eurostat/WB) |
| [StatCan Quality Guidelines 12-539-X](https://unstats.un.org/unsd/dnss/docs-nqaf/Canada-12-539-x2009001-eng.pdf) | Minimum documentation requirements |
| [Dallas Fed Appendix A](https://www.dallasfed.org/~/media/documents/research/international/houseprice/appendixA.pdf) | Country-source reference — already covers our Appendix A |
