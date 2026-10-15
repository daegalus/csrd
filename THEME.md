# Hugo Book

Vendored from https://github.com/alex-shpak/hugo-book at
`79af35c876870c6c9f9edede15ef093f4a7bbf8a` (2026-10-15).
Build with Hugo **0.168.0 extended**, also pinned in the deploy workflow.

This upstream version uses plain CSS. The former `_custom.scss` and custom
palette are ported to the project's `assets/styles/custom.css`, including
light, dark and automatic color modes. The two custom theme screenshots
remain in `themes/hugo-book/images/`.

The project overrides `layouts/_shortcodes/{details,columns,columns2,hint}.html`
to render Markdown in existing shortcode calls, preserving SRD content.
`assets/search.js` follows this upstream version with a guard that waits for
the asynchronous search index before searching. Review that override on
future updates; remove it once the equivalent upstream fix is present.
