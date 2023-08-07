#!/usr/bin/env python

# SPDX-FileCopyrightText: 2023 Xavier Bordoy <somenxavier@posteo.net>
#
# SPDX-License-Identifier: GPL-2.0-only

import cagen.libcagen as libcagen
import argparse
import os.path, pathlib
import shutil
from mako.template import Template
import importlib.resources

def cagen_cli():
    """Defines the `cagen` command line script function to call from pyproject.toml"""

    parser = argparse.ArgumentParser(prog = "cagen", description="static site generator for cmpalgorithms project", epilog="For better processing, please put the options at the end of the call of the program.")
    parser.add_argument("--source", type=str, help="the source markdown file. It could be None. In this case, it renders Template with --metadata fields to `to` path")
    parser.add_argument("to", type=str, help="destination file")
    parser.add_argument("template", type=str, help="Mako template file path")
    parser.add_argument("--syntax", type=str, default='html5', help="syntax of destination file. By default 'html5'")
    parser.add_argument("--metadata", type=str, nargs='*', help="extra metadata provided to template. In the form variable=value variable2=value2 ... . If you want to use cagen.libcagen.Collection invoke as Collection not full name")
    parser.add_argument("--evals", type=str, nargs='*', help="evals with `eval()` python function the specified metadata variables. Eg. if `--metadata foo=2.0` and `--eval foo`, then the foo variable is the float 2.0, not the string '2.0'.")
    args = parser.parse_args()

    # Conversion
    entry = libcagen.Entry(args.source)
    if os.path.exists(args.template):
        with open(args.to, "w") as f:
            assignments=libcagen.extract_assignments(args.metadata)
            evals=args.evals
            eassignments=libcagen.evaluate_assignments(assignments, evals)
            f.write(entry.to(mytemplatepath=args.template, additionalsearchlist=eassignments, destsyntax=args.syntax))
            print("{} -> {} ({}) using {}".format(args.source, args.to, args.syntax, args.template))
    else:
        print("Template {} not found".format(args.template))

def cagen_make():
    """Defines the `cagen-make` command line script function to call from pyproject.toml"""

    maketemplate = """
# Default template
TMPHTML5 = templates/schema.tmpl
TMPLIST = templates/list.md.tmpl

# Select all markdowns file except index.md
MARKDOWNS = $(shell find . -type f -name "*.md" ! -name "index.md" ! -name "README.md")
## List them as comma-separated and quotating list
LISTMD = "$(shell echo $(MARKDOWNS) | sed 's/ /", "/g')"

# Replace the extension.
# By default HTML5
MARKDOWNS_HTML5 = $(MARKDOWNS:.md=.html)

# Extra metadata. Use if you want and edit freely
REPOSITORY = "https://repo.or.cz/cagen.git"
REVISIONNUMBER = $(shell git log --format=oneline $<  | wc -l)

# Commands

SSG = cagen

# Processing

.PHONY: all clean

all: $(MARKDOWNS_HTML5)

# .MD.HTML -> .HTML
%.html: %.md
\t$(SSG) $@ $(TMPHTML5) --source $< --metadata sourcefile="$(shell echo $<)" revisionnumber=$(REVISIONNUMBER) repository=$(REPOSITORY)

# List files
## index.md
index.md: $(MARKDOWNS)
\t$(SSG) $@ $(TMPLIST) --metadata title='Index' collection='Collection([$(LISTMD)])' --evals collection

## keywords.md aka glossary of keywords
#keywords.md: $(MARKDOWNS)
#\t$(SSGLIST) --title Glossary --group_by keywords $(TMPLIST) $(MARKDOWNS)

clean:
\trm $(MARKDOWNS_HTML5)
"""

    parser = argparse.ArgumentParser(prog = "cagen-make", description="creates a Makefile file for using GNU Make to generate HTML5 files using cagen")
    parser.add_argument("directory", type=str, help="creates the Makefile in the DIRECTORY")
    parser.add_argument("--templates", action='store_true', help="creates the directory 'templates' in the current directory with the copy of basic cagen templates")
    args = parser.parse_args()

    if args.directory:
        # If args.directory exists, then create the Makefile
        if os.path.exists(args.directory):
            with open(args.directory + "/" + "Makefile", "w") as f:
                f.write(maketemplate)

            # Create templates directory if user wants
            if args.templates:
                destination = args.directory + "/" + "templates"
                if not os.path.exists(destination):
                    os.makedirs(destination)
                    for f in importlib.resources.files('cagen.templates').iterdir():
                        shutil.copy(f, destination + "/" + f.name)
        else:
            print("The directory {} does not exist. Please create it".format(args.directory))
    else:
        print("See --help for hints")
