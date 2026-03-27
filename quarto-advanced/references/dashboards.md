# Dashboards

Quarto Dashboards (introduced in v1.4) provide a flexible, responsive layout system for creating interactive dashboards with R, Python, Julia, or Observable JS.

## Table of Contents

* [Basic Dashboard Structure](#basic-dashboard-structure)
* [Layout Configuration](#layout-configuration)
  * [Orientation](#orientation)
  * [Scrolling and Filling](#scrolling-and-filling)
  * [Card Layout](#card-layout)
* [Tabsets](#tabsets)
* [Value Boxes](#value-boxes)
* [Toolbars](#toolbars)
* [Interactive Components](#interactive-components)
  * [Shiny](#shiny)
  * [Observable JS (OJS)](#observable-js-ojs)
* [Dashboard Components](#dashboard-components)
* [Navigation and Styling](#navigation-and-styling)
  * [Navigation Bar](#navigation-bar)
  * [Logo and Favicon](#logo-and-favicon)
* [Resources](#resources)

## Basic Dashboard Structure

```yaml
---
title: "Sales Dashboard"
format: dashboard
---

## Row {height=60%}

### Column {width=40%}

```{r}
# Value box 1
```

```{r}
# Value box 2
```

### Column {width=60%}

```{r}
# Main plot
```

## Row {height=40%}

```{r}
# Secondary plot
```
```

Dashboards are organized into pages (Level 1 `#`), rows or columns (Level 2 `##`), and cards (Level 3 `###`).

## Layout Configuration

### Orientation

Control the default orientation in YAML:

```yaml
format:
  dashboard:
    orientation: rows    # Default: rows
    orientation: columns
```

### Scrolling and Filling

By default, cards fill the height of the dashboard. Enable scrolling for long content:

```yaml
format:
  dashboard:
    scrolling: true    # Enable vertical scrolling
```

Per-row/column override:

```markdown
## Row {.scrolling}
```

### Card Layout

Use `.fill` or `.flow` classes:

```markdown
### Card 1 {.fill}
### Card 2 {.flow}
```

## Tabsets

Group multiple cards into tabs:

```markdown
## Row {.tabset}

### Chart A
### Chart B
```

## Value Boxes

Display key metrics:

```markdown
```{r}
#| content: valuebox
#| title: "Total Sales"
#| icon: cart
#| color: primary

list(
  value = 1234,
  caption = "Growth: +10%"
)
```
```

Common icons from [Bootstrap Icons](https://icons.getbootstrap.com/).

## Toolbars

Add global or sidebar toolbars:

```markdown
## {.toolbar}

This toolbar appears at the top.

## Sidebar {.sidebar}

This sidebar appears on the left.
```

## Interactive Components

### Shiny

```yaml
server: shiny
```

### Observable JS (OJS)

```markdown
```{ojs}
// Reactive OJS code
```
```

## Dashboard Components

| Component | Description |
| --- | --- |
| `## Row` | Defines a horizontal row |
| `## Column` | Defines a vertical column |
| `### Card` | Defines an individual card (header + content) |
| `.tabset` | Groups elements into tabs |
| `valuebox` | Displays metric with icon and color |
| `.sidebar` | Fixed sidebar for inputs |
| `.toolbar` | Top-level bar for global controls |

## Navigation and Styling

### Navigation Bar

```yaml
website:
  navbar:
    logo: logo.png
    nav-buttons:
      - icon: github
        href: https://github.com
```

### Logo and Favicon

```yaml
format:
  dashboard:
    logo: logo.png
    favicon: favicon.ico
```

## Resources

- [Quarto Dashboards](https://quarto.org/docs/dashboards/)
- [Dashboard Layout](https://quarto.org/docs/dashboards/layout.html)
- [Value Boxes](https://quarto.org/docs/dashboards/value-boxes.html)
- [Interactive Dashboards](https://quarto.org/docs/dashboards/interactivity/shiny-python/index.html)
