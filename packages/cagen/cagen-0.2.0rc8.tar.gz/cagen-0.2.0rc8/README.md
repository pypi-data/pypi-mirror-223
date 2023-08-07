<!--
SPDX-FileCopyrightText: 2023 Xavier Bordoy <somenxavier@posteo.net>

SPDX-License-Identifier: GPL-2.0-only
-->

# cagen

## About

cagen is a static site generator. Originally, it was intented for [cmpalgorithms project](https://sr.ht/~somenxavierb/cmpalgorithms/) but now it's an independent project.

## License

The software is distributed under [GPL 2-only license](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt).

## How it runs

It assumes your documents are written with markdown syntax. It is capable of convert those documents to any other format, using [pandoc](https://pandoc.org/) (specifically [pypandoc](https://github.com/JessicaTegner/pypandoc) wrapper) and [Mako templating system](https://www.makotemplates.org/).

The reason to use "external" templating system instead of built-in pandoc template system is because pandoc templates [are not capable of make conditions with values](https://pandoc.org/MANUAL.html#conditionals) (something like `$if(author=='me') Print full name here $endif$`).

The program just converts markdown files to HTML ones by default in the same directory. Unlike many other static site generators, there is no predefined structure by default: no `assets` directory neither `site` directory. By default, all generated files are in the same directory than the source files. Obviously, you can modify it if you want.

We provide:

- a [library](https://repo.or.cz/cagen.git/blob/HEAD:/src/cagen/libcagen.py)
- a [command line program](https://repo.or.cz/cagen.git/blob/HEAD:/src/cagen/cmd.py) (called `cagen`) for convert documents
- a script called `cagen-make` to generate a Makefile to convert automatically all markdown files to HTML ones.

The software is implemented in [python](https://www.python.org/) because it's easy to program (I'm very language-neutral). If you want some really fast static site generator, be free to fork the project and program with any compiled language.

## Installation

You can install via [pip](https://pypi.org/project/cagen/):
```
pip install cagen
```

If you are running ArchLinux or any Arch derivative distribution, you can use this [PKGBUILD](https://repo.or.cz/cagen.git/blob/HEAD:/extras/PKGBUILD) to make a pacman package.

## Usage

Basic use is:
```
cagen generatedfile.html template.tmpl --source sourcefile.md
```
where 

- `sourcefile.md` is Markdown file
- `generatedfile.html` is the HTML5 file
- `template.tmpl` is Mako template file

The `source` argument is optional. In the case it is omitted, `cagen` just renders the template to `generatedfile.html`

See `cagen --help` for more options.

This tool is some kind of low-level tool. If you want some more higher-level one to automatically converts all markdown files to corresponding HTML5 files, we provide the `cagen-make` script (see above). The steps are:
```
cagen-make --init
```

It creates `Makefile`

```
make
```

It automatically convert all markdown files to HTML5 ones using `templates/schema.tmpl` Mako template. You can modify it editing `Makefile`.

## Other resources

- You can see the [list of tasks](https://repo.or.cz/cagen.git/tree/HEAD:/tasks) (completed and pending).
- The [API documentation](https://repo.or.cz/cagen.git/tree/HEAD:/src/cagen/docs) is available (automatically generated with [pdoc](https://pdoc.dev/)).

## Contribute

If you want to make a suggestion, a question, reporting a bug, or even send patches, then you can send me an email to the concatenation, in some order, of the words in the set {"@", "posteo.net", "somenxavier"}. Sorry for the riddle, spam is strong in the web nowadays.

