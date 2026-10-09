# Dashboards

> Stub — core syntax only. Expand this file when dashboards become a regular deliverable; until
> then fetch the official pages listed at the bottom for anything beyond the basics.

`format: dashboard`. Headings define the layout instead of document sections; every code cell
becomes a **card**.

````markdown
---
title: "Operations"
format:
  dashboard:
    orientation: rows          # rows (default) | columns
    scrolling: false           # true = page scrolls instead of filling the viewport
    nav-buttons: [github]
---

# Overview                     <!-- level 1 = page (adds a navbar tab) -->

## Row {height=30%}            <!-- level 2 = row (or column with orientation: columns) -->

```{python}
#| content: valuebox
#| title: "Orders today"
#| icon: cart                  # any Bootstrap icon
#| color: primary
dict(value = 1284)
```

## Row {height=70%}

```{python}
#| title: "Orders by hour"     # card title
fig
```

# Details

## {.sidebar}                  <!-- inputs / notes; `# {.sidebar}` = global sidebar -->
````

- `{.tabset}` on a row/column turns its cards into tabs; `{.fill}` / `{.flow}` controls card height.
- Value boxes: R uses `list(value = ..., icon = ..., color = ...)`; Python uses `dict(...)`.
- Static by default (htmlwidgets, plotly, itables, ojs still interactive client-side). Real
  inputs need **Shiny** (`server: shiny`, R or Python) or **Observable JS**; static
  dashboards can be parameterised (`dashboards/parameters`).
- Theming: `theme:` / `_brand.yml` as in HTML; `logo:` in the navbar.
- `axe: {output: document}` (1.9+) adds an accessibility sidebar report.

## More detail

`dashboards/index`, `dashboards/layout`, `dashboards/data-display`, `dashboards/inputs`,
`dashboards/theming`, `dashboards/parameters`, `dashboards/deployment`,
`dashboards/interactivity/index`, `dashboards/interactivity/shiny-r`,
`dashboards/interactivity/shiny-python/index`, `dashboards/interactivity/observable`,
`reference/formats/dashboard`.
