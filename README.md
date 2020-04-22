# Azure DevOps WIKI export script

Export Azure DevOps WIKI to:

* Markdown
* HTML
* PDF

Supports:

* customization via CSS

## Get Started

Assuming Debian-based linux distribution (or WSL on WIndows 10) is in use :)

Init python virtual environment, assuming it will be located in `.venv` folder: `python3 -m venv .venv`

Activate it: `. .venv/bin/activate`

Optional, **pip** update: `python -m pip install -U pip` or `pip install -U pip`

Install requirements: `pip install -r requirements.txt`

Make executable: `chmod +x azuredevops-export-wiki.py`

See usage and help info `./azuredevops-export-wiki.py -h`

```text
Usage:
    azuredevops-export-wiki.py [options] WIKI-ROOT

Options:
    -h --help               # Show this screen
    --to <str>              # Target format: md, html, pdf [default=pdf]
    --img-root <str>        # Path to images folder, if not passed CWD will be in used
    --css-file <FILE>       # Path to CSS file
    -o --out <FILE>         # For "md" and "html", path to file
```

Where `WIKI-ROOT` is a path to WIKI root folder or any WIKI child folder you want to use as an entry point.

## CSS

All images are wrapped with with class `img-parent`, it can be used for image positioning, for example.

## Road Map

* add support for `--max-depth` option
* add support for `.env` file via `--env-file` option
* add [Wheels](https://pythonwheels.com) package setup
* add support for a sequence of CSS files in `--css-file` option