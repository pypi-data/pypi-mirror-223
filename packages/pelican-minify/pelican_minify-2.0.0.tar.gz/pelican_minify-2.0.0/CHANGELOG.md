CHANGELOG
=========

2.0.0 - 2023-08-03
------------------

- Rename plugin and move under Pelican Plugins organization
- Restructure according to latest plugin best practices
- Add `JS_MIN` setting and ability to minify JavaScript files
- Replace all minifiers with [`minify-html`](https://github.com/wilsonzlin/minify-html)

1.0.0 - 2022-02-19
------------------

- Add configuration options: `CSS_MIN`, `HTML_MIN`, `INLINE_CSS_MIN`, `INLINE_JS_MIN`
- Add ability to minify inline JS & CSS
- Refactor for Pelican 4.x
- Drop Python 2.7 support
- Fix CSS minification failure on embedded SVG in CSS rules (`url()` function)

0.1.1 - 2015-01-19
------------------

Disable stripping of HTML attribute quotes

0.1.0 - 2014-07-06
------------------

Initial release
