# Antibody Data Harmonizer

A small, reproducible Python project for harmonizing antibody identifiers across
tables, auditing failed matches, locating sequence features, and preparing
developability analyses.

> **Portfolio-safe demo:** all data and sequences in this repository are
> synthetic. Do not upload confidential company data, internal identifiers,
> proprietary schemas, or unpublished results.

## Why this project exists

Antibody assay results and sequence annotations often arrive in separate Excel
worksheets with inconsistent headers and identifier formats. Manual copying,
dragging, and visual checking are slow and difficult to audit.

This project turns that workflow into a reusable pipeline:

1. Standardize column names.
2. Normalize antibody identifiers using explicit, conservative rules.
3. Merge tables with relationship validation.
4. Export matched, unmatched, and duplicate-ID audit tables.
5. Locate and mark a motif or regular-expression feature in sequences.
6. Join feature results back to antibody IDs.
7. Analyze CDR3 length against expression, HIC, Tm, or other variables.

## Demonstrated skills

- Python and pandas data wrangling
- Excel/CSV ingestion
- Identifier harmonization
- Data-quality checks and audit trails
- Sequence feature search and annotation
- Statistical correlation analysis
- Reproducible project organization
- Unit testing with pytest
- Technical documentation

## Project structure

```text
antibody-data-harmonizer/
├── data/
│   ├── sample/            # Synthetic public demo data
│   ├── raw/               # Local confidential data; ignored by Git
│   └── processed/         # Generated local outputs; ignored by Git
├── notebooks/
│   └── 01_demo_pipeline.ipynb
├── outputs/               # Generated reports; ignored by Git
├── src/
│   ├── analysis.py
│   ├── feature_locator.py
│   └── id_harmonization.py
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Quick start

### 1. Create and activate a virtual environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Launch JupyterLab

```bash
jupyter lab
```

Open `notebooks/01_demo_pipeline.ipynb` and run the cells from top to bottom.

### 4. Run tests

From the repository root:

```bash
python -m pytest
```

## Core safety principle

The pipeline separates **exact automated matching** from **human-reviewed
candidate suggestions**. Approximate matches are never silently accepted.

## Example portfolio description

> Built a reusable Python/pandas pipeline to harmonize inconsistent antibody
> identifiers across assay and sequence-annotation tables, generate auditable
> unmatched/duplicate reports, annotate sequence motifs, and prepare CDR3
> developability analyses using synthetic demonstration data.

## Possible next steps

- Read multiple Excel sheets from a configuration file.
- Export a multi-sheet quality-control workbook.
- Add interactive column mapping.
- Support Kabat insertion labels such as `100A` and `100B`.
- Add plots and HTML reports.
- Build a lightweight Streamlit interface.
