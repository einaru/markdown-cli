"""
    Markdown to HTML generator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Copyright: (c) 2014 Einar Uvsløkk
"""
import os
import sys
import logging
import argparse

import markdown
from bs4 import BeautifulSoup

from mdcli import __version__
# Future features:
# TODO:2014-10-18:einar: implement file watch functionality
# TODO:2014-10-18:einar: implement 'view in browser' functionality

log = logging.getLogger(__name__)

DOC_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
</head>
<body>
{content}
</body>
</html>
"""

DOC_STYLE = """
body { padding: 1em; margin: 0; color #222; }
a { color: #3498db; }
a:hover, a:visited { color: #2980b9; }
.table-wrapper { width: 100%; overflow-x: auto; margin: 1em 0; }
table { width: 900px; border-collapse: collapse; }
table th { text-align: left; border-bottom: 0.125em solid #888; }
table td { border-bottom: 0.063em solid #888; }
table th, table td { padding: 0.4em; }
tbody tr:nth-child(odd) { background-color: #efefef; }
"""

MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra'  # Includes table support
]


def create_html5_document(content, args, template=DOC_TEMPLATE, style=DOC_STYLE):
    """Creates the complete html5 document."""
    def create_title(filename):
        return os.path.splitext(os.path.basename(filename))[0]

    if args.vanilla:
        soup = BeautifulSoup(content)
    else:
        soup = BeautifulSoup(template.format(content=content))

        # Add document title
        title = args.title or create_title(args.infile.name)
        title_tag = soup.new_tag('title')
        title_tag.append(title)
        log.info('adding title: {}'.format(title))
        soup.html.head.append(title_tag)

        # Add viewport meta
        meta_tag = soup.new_tag('meta')
        meta_tag['name'] = 'viewport'
        meta_tag['content'] = 'width=device-width,initial-scale=1.0'
        log.info('adding meta: viewport')
        soup.html.head.append(meta_tag)

        if not args.no_css:
            # Add stylesheet
            style_tag = soup.new_tag('style')
            style_tag['type'] = 'text/css'
            style_tag.append(style)
            log.info('adding stylesheet: inline')
            soup.html.head.append(style_tag)

        if not args.no_wrap_table:
            # Wrap tables
            for table in soup.find_all('table'):
                wrapper = soup.new_tag('div')
                wrapper['class'] = 'table-wrapper'
                log.info('adding .table-wrapper to table')
                table.wrap(wrapper)

    if args.prettify:
        log.info('prettifying the html')
        soup = soup.prettify()

    return soup


def generate_content(md_file):
    html = markdown.markdown(md_file, extensions=MARKDOWN_EXTENSIONS,
                             ouput_format='html5')
    return html


def parse_command_line(argv):
    """Parses the command line arguments, and setup log level."""

    parser = argparse.ArgumentParser(prog='markdown-cli',
        description='Markdown to HTML command-line utility.')

    parser.add_argument('infile', type=argparse.FileType('r'),
                        help='markdown document')
    parser.add_argument('-o', '--output', metavar='FILE', dest='outfile',
                        type=argparse.FileType('w'), default=sys.stdout,
                        help='write output to a file')
    parser.add_argument('-t', '--title',
                        help='set the html document title')
    parser.add_argument('--no-css', action='store_true',
                        help='do not include stylesheets')
    parser.add_argument('--no-wrap-table', action='store_true',
                        help='do not wrap tables in \'table-wrapper\' divs')
    parser.add_argument('--vanilla', action='store_true',
                        help='output vanilla html, i.e. do not wrap tables, '
                        'add stylesheets, or wrap in <html> tags')
    parser.add_argument('--prettify', action='store_true',
                        help='output prettyfied html, e.g. with indentation')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__),
                        help='show the application version and exit')
    parser.add_argument('-v', '--verbose', dest='verbose_count',
                        action='count', default=0,
                        help='increase log verbosity')

    args = parser.parse_args(argv[1:])

    # Set the log level to WARN going more verbose for each -v
    log.setLevel(max(3 - args.verbose_count, 0) * 10)

    return args


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.WARN,
                        format='%(name)s (%(levelname)s): %(message)s')
    try:
        args = parse_command_line(sys.argv)
        content = generate_content(args.infile.read())
        doc = create_html5_document(content, args)

        print(doc, file=args.outfile)
    finally:
        logging.shutdown()

