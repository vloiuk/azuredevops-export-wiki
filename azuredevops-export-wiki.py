#!/usr/bin/env python3

"""
Usage:
    azuredevops-export-wiki.py [options] WIKI-ROOT

Options:
    -h --help               # Show this screen
    --to <str>              # Target format [default=pdf]
    --img-root <str>        # Path to images folder, if not passed CWD will be in used
    --css-file <FILE>       # Path to exyternal CSS file
    -o --out <FILE>         # For "md" and "html", frite to file
"""

import base64
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
import re
from bs4 import BeautifulSoup
import pdfkit
from markdown import markdown
from os import path
from docopt import docopt
import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


def get_md_for_order_file_record(_path):
    _result = "\n"
    _file_path = "{0}.md".format(_path)
    if path.exists(_file_path):
        with open(_file_path, "r") as _file:
            _result += _file.read().strip()
    if path.exists(_path):
        _result += generate_for_path(_path)
    return _result


def generate_for_path(_path):
    _order_file_path = path.join(_path, ".order")
    if not path.exists(_order_file_path):
        return ""

    _order_file_records = []
    with open(_order_file_path, "r") as _order_file:
        _line = _order_file.readline()
        while _line:
            _order_file_records.append(_line.strip())
            _line = _order_file.readline()

    result = ""

    for _record in _order_file_records:
        result += get_md_for_order_file_record(path.join(_path, _record))
        result += "\n"

    return result


def load_css(_file_path):
    if not _file_path or not path.exists(_file_path):
        return ""
    with open(_file_path, "r") as _file:
        return _file.read().strip()


def handle_html_soup(_soup):
    # code blocks
    for tag in _soup.find_all("code"):
        if not "\n" in tag.string:
            continue
        _code_content = tag.string
        _lexer = None
        try:
            _lang_name = re.match(r"^[a-z]+$", _code_content, re.M)[0]
            if _lang_name == "cs":
                _lang_name = "csharp"
            _lexer = get_lexer_by_name(_lang_name)
            _code_content = re.sub(
                r"^[a-z]+$", "", _code_content, flags=re.M)
        except:
            pass
        if not _lexer:
            _lexer = guess_lexer(_code_content)
        _code_content = highlight(_code_content, _lexer, _code_formatter)
        _code = _soup.new_tag("div")
        _code_dom = BeautifulSoup(_code_content, features="html.parser")
        _code.append(_code_dom)
        tag.replace_with(_code)

    # images
    for tag in _soup.find_all("img"):
        _src = ""
        try:
            _src = tag["src"]
        except KeyError:
            continue
        if not _src:
            continue
        if _src.startswith("http"):
            continue
        _src = re.sub(r"\.\.\/?", "", _src)
        _src = path.join(_img_root, _src)
        if path.exists(_src):
            _data_src = base64.b64encode(open(_src, "rb").read()).decode()
            tag["src"] = "data:image/png;base64,{0}".format(_data_src)
        else:
            _img_err = _soup.new_tag("div")
            _img_err["class"] = "error"
            _img_err.append("Image '{0}' not found.".format(_src))
            tag.replace_with(_img_err)

    # collect css
    _css = _code_formatter.get_style_defs('.highlight')
    _style = _soup.new_tag("style", {type: "text/css"})
    _style.string = _css
    _soup.head.append(_style)


_base_html = "<!DOCTYPE html>" \
    "<html lang='en'>" \
    "<head>" \
    "    <meta charset='UTF-8'>" \
    "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>" \
    "    <title>{0}</title>" \
    "    <style type='text/css'>{1}</style>" \
    "</head>" \
    "<body>" \
    "{2}" \
    "</body>" \
    "</html>"


def main():
    try:
        _md = generate_for_path(_doc_root)
        # TBD: fix image urls, this is done for HTML and PDF, but not for MD format
        if _to == "md":
            if _out:
                with open(_out, "w") as f:
                    f.write(_md)
            else:
                print(_md)
            exit(0)

        #_html = markdown(_md, extensions=["tables", "codehilite"])
        _html = markdown(_md, extensions=["tables"])
        _css = load_css(_css_file_path)
        _html = _base_html.format("WIKI", _css, _html)
        _soup = BeautifulSoup(_html, features="html.parser")
        handle_html_soup(_soup)
        _prod_html = _soup.prettify()
        if _to == "html":
            if _out:
                with open(_out, "w") as f:
                    f.write(_prod_html)
            else:
                print(_prod_html)
            exit(0)

        _pdf_path = path.join(_cwd, "output.pdf")
        if _out:
            _pdf_path = _out
        pdfkit.from_string(_prod_html, _pdf_path)

        print("\nFile path: {0}".format(_pdf_path))

    except Exception as ex:
        print(ex)
        exit(1)


if __name__ == "__main__":
    _cwd = path.dirname(__file__)
    _doc_root = _cwd
    _img_root = _doc_root
    _to = "pdf"
    _code_formatter = HtmlFormatter()
    _css_file_path = None
    _out = None

    _args = docopt(__doc__)
    if _args["WIKI-ROOT"]:
        _doc_root = _args["WIKI-ROOT"]
    if _args["--to"]:
        _to = _args["--to"]
    if _args["--css-file"]:
        _css_file_path = _args["--css-file"]
    if _args["--img-root"]:
        _img_root = _args["--img-root"]
    if _args["--out"]:
        _out = _args["--out"]

    main()