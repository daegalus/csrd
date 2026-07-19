# Cypher System Reference Document

The goal of this project is to make a nice, readable way to view the cypher system reference document.

The primary work is formatting and styling the text, with no changes in the words in the document.

## Goals

* Clean and Simple
* No changes to original wording.
* Markdown for readability and portability.

## Translations

There are no official translations to my knowledge, but if there ever are, this projects is prepared to handle it.

A new folder with the language code needs to be made, and a similar structure and set of files need to be created, but with the translated text.

As there are no official translations, I won't be accepting PRs with translations for the time being.

## Building locally

Dependencies:

* Git
* Hugo Extended Version (theme requires it)

When you pull the git repo, make sure you run `git submodule init` to pull the theme.

From there, you just need to run `hugo` to build, it will output to the `/public` folder, it will be created if it is nor present.

You can also use `hugo server --minify` to run a live-updating development server.

## Licenses

### Cypher System

The cypher system and it's contents are under the `Cypher System Open License`, which is included as `CYPHER_LICENSE` in this repository. The original SRD is in the `srds` folder.

### Hugo

Hugo is under the Apache License 2.0
Hugo's output to my knowledge falls under the licenses of the repo and the theme.

### The Rest

Theme is `hugo_book` and can be [found here](https://github.com/alex-shpak/hugo-book) and is under the `MIT License`.

Everything else that isn't covered by other licenses, I license under the `ISC license` and can be read in the `LICENSE` file.