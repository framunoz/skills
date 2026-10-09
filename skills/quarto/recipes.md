# Recipes

Proven end-to-end patterns. Each lists the files involved and the command that proves it works.

## 1. Python HTML report with uv

```bash
uv init --bare && uv add pandas plotly && uv add --dev jupyter
cp <skill>/assets/report.qmd report.qmd        # set engine-specific cells to {python}
uv run quarto preview report.qmd               # live reload while writing
uv run quarto render report.qmd                # final
```

Every `quarto` invocation goes through `uv run` (or set `QUARTO_PYTHON`) so the venv is used.

## 2. R HTML report with renv

```bash
Rscript -e 'renv::init(bare = TRUE)'
Rscript -e 'renv::install(c("rmarkdown", "knitr", "ggplot2")); renv::snapshot()'
printf 'project:\n  type: default\n' > _quarto.yml   # makes R always start at the root
quarto render report.qmd
```

knitr needs `rmarkdown` and `knitr` inside the renv library; `quarto check knitr` confirms.

## 3. R and Python in one document

- Engine is knitr (because of the `{r}` cells); Python runs through `reticulate`
  (install it in renv).
- Point reticulate at the uv venv: `RETICULATE_PYTHON=.venv/bin/python` in `.Renviron`.
- Exchange objects: `r.df` in Python, `py$obj` in R.
- Use when one language has the better library for one step; otherwise keep one language per document.

## 4. One HTML file to email

```yaml
format:
  html:
    embed-resources: true
    self-contained-math: true      # only if the document has equations
```

Check the size afterwards; heavy widgets (leaflet with many points, big DT tables) can make
it tens of MB.

## 5. Parameterised reports in batch

```bash
for region in north south east; do
  quarto render report.qmd -P region:$region --output report-$region.html
done
```

- knitr: `params: {region: north}` in front matter → `params$region`.
- jupyter: first cell `#| tags: [parameters]` with `region = "north"`.
- Inside R, `quarto::quarto_render("report.qmd", execute_params = list(region = r), output_file = ...)`.
- Put shared options in `_quarto.yml` so each variant only differs by parameter.

## 6. Report and slides from the same analysis

Keep the computation in one place and **embed** its outputs:

```
analysis.qmd           # all code, labelled cells: fig-sales, tbl-summary
report.qmd             # {{< embed analysis.qmd#fig-sales >}}
slides.qmd             # {{< embed analysis.qmd#fig-sales >}}
```

Each deliverable keeps its own structure; numbers never drift between them. Alternative for
text reuse: `{{< include _shared-intro.qmd >}}` (included content executes in the host document).

## 7. Slides that walk through code

````markdown
## Fitting the model

```{r}
#| echo: true
#| output-location: column-fragment
#| code-line-numbers: "|1|2-3"
fit <- lm(y ~ x, data = df)
summary(fit)$r.squared
plot(fit, which = 1)
```
````

Each `|` step highlights lines; output appears beside the code on the next click.

## 8. Draft vs production via profiles

`_quarto.yml` (fast, local):

```yaml
execute:
  freeze: auto
format:
  html:
    embed-resources: false
```

`_quarto-production.yml`:

```yaml
format:
  html:
    embed-resources: true
```

`quarto render --profile production` for the deliverable.

## 9. Plots that follow light/dark

```{r}
#| renderings: [light, dark]
p + theme_minimal()
p + theme_minimal() + theme_dark_custom()
```

The theme needs both modes (`theme: {light: flatly, dark: darkly}`). For captions/crossrefs,
wrap in a `::: {#fig-x}` div (see `gotchas.md`).

## 10. Publish a site to GitHub Pages with frozen results

1. `_quarto.yml`: `execute: freeze: auto`; render locally (`quarto render`) and commit `_freeze/`.
2. `quarto publish gh-pages` once locally (creates the branch and `_publish.yml`).
3. Add `.github/workflows/publish.yml` using `quarto-dev/quarto-actions/setup@v2` and
   `quarto-dev/quarto-actions/publish@v2` with `target: gh-pages`
   (exact file in `publishing/github-pages`). Give Actions write permission.

CI then renders without R/Python, using `_freeze/`.

## 11. Consistent identity across many reports

A `default` project holding all reports + one `_brand.yml` + shared `format:` options in
`_quarto.yml`. New report = new `.qmd`; branding is inherited. Slides pick up the same brand.

## 12. Reports in Spanish

`lang: es` translates generated labels (Figura, Tabla, Índice). Date formatting:
`date: today` + `date-format: "D [de] MMMM, YYYY"`. Override any label under `language:`
(e.g. `language: {crossref-fig-title: "Gráfico"}`).
