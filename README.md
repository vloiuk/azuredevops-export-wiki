# Azure DevOps WIKI export script

Export Azure DevOps WIKI to:

* Markdown
* HTML
* PDF

Supports:

* customization via CSS

## Get Started

Script forged with Python 3, so make sure you have it installed.

### Init python virtual environment

Assuming it will be located in `.venv` folder.

#### On Linux:

Create: `python3 -m venv .venv`

Activate: `. .venv/bin/activate`

#### On Windows:

##### Using windows command prompt

Create: `python -m venv .venv`

Activate: `.venv\scripts\activate`

### Install updates and requirements

Optional, but recommended, **pip** update: `python -m pip install -U pip` or `pip install -U pip`

Install requirements: `pip install -r requirements.txt`

Grab [wkhtmltopdf with patched qt Qt](https://wkhtmltopdf.org/downloads.html) and install it.

### Run script

#### On Linux

First, mark script as executable: `chmod +x azuredevops-export-wiki.py`

See usage and help info `./azuredevops-export-wiki.py -h`

#### On windows

See usage and help info `python azuredevops-export-wiki.py -h`

### How to use

```text
Usage:
    azuredevops-export-wiki.py [options] WIKI-ROOT

Options:
    -h --help               # Show this screen
    --to <str>              # Target format: md, html, pdf [default=pdf]
    --img-root <str>        # Path to images folder, if not passed CWD will be in used
    --no-code-styles        # Do not inject default code CSS styles
    --css-file <FILE>       # Path to CSS file
    --toc                   # Add "table of content" to the beginning of the file
    --adjust-heading        # When export a part of WIKI, set H1 as initial heading
    --title <str>           # Add H1 title to the beginning of the file
    -o --out <FILE>         # For "md" and "html", path to file 
```

Where `WIKI-ROOT` is a path to WIKI root folder or any WIKI child folder you want to use as an entry point.

## Layout customization

All images are wrapped with class `img-parent`, it can be used for image positioning, for example.

"Table of content" is wrapped with class `toc`

Custom theme for code block can be included into css file (see: `--css-file` option). There are some popular options [here](http://jwarby.github.io/jekyll-pygments-themes/languages/javascript.html). If you do so, use `--no-code-styles` option to avoid "double theme" issue.

## Road Map

* add support for `--max-depth` option
* add support for `.env` file via `--env-file` option
* add [Wheels](https://pythonwheels.com) package setup
* add support for a sequence of CSS files in `--css-file` option
* add support for [mermaid](https://mermaid-js.github.io/mermaid/) diagrams