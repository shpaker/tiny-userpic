# Changelog

All notable changes to this project are documented in this file.

Entries from 1.0.0 onwards are generated from [conventional commits](https://www.conventionalcommits.org/)
by [commitizen](https://commitizen-tools.github.io/commitizen/); earlier releases predate that
convention and are summarised by hand.

## 1.0.0 (2026-08-22)

### BREAKING CHANGE

- the padding default changed from (0, 0) to (20, 20) in
make_userpic_svg and in both *_from_string functions, make_userpic was removed,
and degenerate size/image_size/padding values now raise ValueError instead of
hanging or returning a broken image. The rendered pixels and the SVG markup
differ from 0.4.0, although the pattern for a given seed or string is unchanged.

### Feat

- declare the api stable and automate releases

### Fix

- pattern rendering, input validation and svg output

## 0.4.0 (2025-03-24)

### Feat

- add `make_userpic_image_from_string` and `make_userpic_svg_from_string`, deriving the pattern from
  a SHA-256 digest of the input text
- add the `seed` parameter to the image and SVG generators for reproducible output
- add a test suite and the example images used by the readme

## 0.3.0 (2024-12-12)

### Refactor

- rewrite the library as a single `userpic.py` module
- drop the command line interface, leaving a library-only package
- make Pillow the only runtime dependency
- move the tooling to uv and just

Patch releases 0.3.1, 0.3.2 and 0.3.3 only touched the readme and the packaging metadata.

## 0.2.0 (2022-07-22)

### Refactor

- make CairoSVG an optional dependency instead of a required one
- replace typer with click in the command line interface

## 0.1.1 (2021-07-03)

Initial release: a `userpic` package with an SVG generator, a Cairo-backed PNG renderer and a
typer-based command line interface.
