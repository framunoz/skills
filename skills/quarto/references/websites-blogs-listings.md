# Quarto Websites, Blogs, and Listings

Use Quarto website configuration for navigable sites, blogs, and content listings.

## Table of Contents

- [Website Root](#website-root)
- [Blogs and Listings](#blogs-and-listings)
- [Safe Workflow](#safe-workflow)
- [Related References](#related-references)

## Website Root

Set `project: type: website` and keep navigation, site metadata, output, and
shared format options in `_quarto.yml`. Use the existing project structure and
do not move pages or alter output directories without a stated need. Consult
[project configuration](project-configuration.md) and [YAML front matter](yaml-front-matter.md).

## Blogs and Listings

Treat posts as normal Quarto documents governed by the site's conventions.
Configure listings from the project's established pages and fields; keep dates,
titles, categories, draft status, and image paths consistent. Verify that a
listing's source glob does not unintentionally publish drafts or generated files.
Listings and website navigation are HTML-oriented; confirm expectations before
adding non-HTML formats.

## Safe Workflow

Inspect existing navigation, listing pages, metadata, and generated-site rules.
Make the smallest configuration or page change. Ask before previewing or fully
rendering a site because it may execute cells and rewrite output. Use
[publishing and deployment](publishing-deployment.md) before any remote publish.

## Related References

- [Project configuration](project-configuration.md)
- [Profiles and directory metadata](profiles-directory-metadata.md)
- [Publishing and deployment](publishing-deployment.md)
- [Figures](figures.md) and [shortcodes](shortcodes.md)
