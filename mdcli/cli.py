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
# Future features:
# TODO:2014-10-18:einar: implement file watch functionality
# TODO:2014-10-18:einar: implement 'view in browser' functionality

__version__ = '0.1.0'
__author__ = 'Einar Uvsløkk'
__description__ = 'Markdown to HTML command-line utility.'

log = logging.getLogger(__name__)

DOC_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/></head>
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
    soup = BeautifulSoup(template.format(content=content))

    # Add document title
    log.debug('using filename to create title')
    title = os.path.splitext(args.infile.name)[0]
    log.info('adding title to document')
    title_tag = soup.new_tag('title')
    soup.html.head.append(title_tag)

    if not args.vanilla:
        # Add viewport meta
        meta_tag = soup.new_tag('meta')
        meta_tag['name'] = 'viewport'
        meta_tag['content'] = 'width=device-width,initial-scale=1.0'
        soup.html.head.append(meta_tag)

        # Add document style
        style_tag = soup.new_tag('style')
        style_tag['type'] = 'text/css'
        log.info('adding default stylesheet to document')
        style_tag.append(style)
        soup.html.head.append(style_tag)

        # Wrap tables
        log.info('wrapping tables')
        for table in soup.find_all('table'):
            wrapper = soup.new_tag('div')
            wrapper['class'] = 'table-wrapper'
            table.wrap(wrapper)

    return soup


def generate_content(md_file):
    html = markdown.markdown(md_file, extensions=MARKDOWN_EXTENSIONS,
                             ouput_format='html5')
    return html


def parse_command_line(argv):
    """Parses the command line arguments, and setup log level."""
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('infile', type=argparse.FileType('r'),
                        help='markdown document')
    parser.add_argument('-o', '--output', metavar='FILE', dest='outfile',
                        type=argparse.FileType('w'), default=sys.stdout,
                        help='write output to a file')
    parser.add_argument('--vanilla', action='store_true',
                        help='output vanilla html, i.e. do not wrap tables, '
                        'or add stylesheets')
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

