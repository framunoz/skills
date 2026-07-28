# Manuscripts

Quarto Manuscripts (introduced in v1.4) provide a workflow for creating scholarly publications with integrated notebooks, JATS export, and manuscript-specific metadata.

## Table of Contents

* [Basic Manuscript Configuration](#basic-manuscript-configuration)
* [Manuscript Metadata](#manuscript-metadata)
* [Embedding Notebooks](#embedding-notebooks)
* [JATS and Journal Formats](#jats-and-journal-formats)
  * [JATS Export](#jats-export)
  * [Quarto Journals](#quarto-journals)
* [Manuscript Features](#manuscript-features)
* [Workflow Examples](#workflow-examples)
  * [Rendering the Manuscript](#rendering-the-manuscript)
  * [Linking Data to Analysis](#linking-data-to-analysis)
* [Resources](#resources)

## Basic Manuscript Configuration

In `_quarto.yml`:

```yaml
project:
  type: manuscript

manuscript:
  article: index.qmd
  notebooks:
    - analysis.ipynb
    - data-prep.py

format:
  html:
    toc: true
  pdf:
    documentclass: article
  jats: default
```

## Manuscript Metadata

Manuscritpts use extended metadata for authors and scholarly context:

```yaml
---
title: "Title of the Manuscript"
author:
  - name: "First Author"
    affiliations:
      - id: 1
        name: "University A"
    orcid: 0000-0000-0000-0000
    email: author@example.com
    corresponding: true
abstract: |
  A concise abstract summarizing the manuscript.
keywords: [quarto, scholarship, Reproducibility]
citation:
  type: article-journal
  container-title: "Journal of Open Science"
  doi: "10.1234/example.123"
---
```

## Embedding Notebooks

Manuscripts can embed output directly from related notebooks:

```markdown
{{< embed analysis.ipynb#fig-plot >}}
```

This shortcode pulls the output (e.g., a figure) and its associated metadata into the main manuscript.

## JATS and Journal Formats

### JATS Export

Quarto generates JATS (Journal Article Tag Suite) XML for archival and submission:

```bash
quarto render --to jats
```

### Quarto Journals

Use journal-specific extensions:

```bash
quarto add quarto-journals/nature
```

```yaml
format:
  nature-pdf: default
  nature-html: default
```

## Manuscript Features

| Feature | Description |
| --- | --- |
| `project: manuscript` | Enables manuscript project type |
| `jats` format | Generates Journal Article Tag Suite XML |
| `notebooks` | Declares supporting notebooks/scripts |
| `embed` | Embeds output from notebooks into text |
| Scholarly Metadata | Detailed author, affiliation, and citation info |
| Manuscript Website | HTML output with notebook links and downloads |

## Workflow Examples

### Rendering the Manuscript

```bash
quarto render    # Renders all formats and the manuscript website
```

### Linking Data to Analysis

```yaml
manuscript:
  article: manuscript.qmd
  notebooks:
    - data_analysis.ipynb
```

In `manuscript.qmd`:

```markdown
See @fig-analysis for the main result.

{{< embed data_analysis.ipynb#fig-analysis >}}
```

## Resources

- [Quarto Manuscripts](https://quarto.org/docs/manuscripts/)
- [JATS XML](https://quarto.org/docs/manuscripts/jats.html)
- [Quarto Journals](https://quarto.org/docs/journals/index.html)
- [Embedding Notebooks](https://quarto.org/docs/authoring/includes.html#embedding)
