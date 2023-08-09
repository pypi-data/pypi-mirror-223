"""tool.py -- contains the command line interface to use this package."""
import argparse
import json
import sys

from tabulate import tabulate


def bq_tabulate(bq_results, fmt='simple'):
    """
    Format results from BQ into pretty-printed text.

    Format results produced by BigQuery into a text that is pretty-printed in
    the requested tabulate format `fmt`.
    """
    headers = list(bq_results[0].keys())
    rows = [list(row.values()) for row in bq_results]
    table = [headers] + rows
    return tabulate(table, headers="firstrow", tablefmt=fmt)


def run():
    """Run the bqtabulate tool."""
    args = _parse_cli()
    bq_json = json.load(args.infile)
    tabulated = bq_tabulate(bq_json, args.fmt)
    args.outfile.write(tabulated + '\n')
    sys.exit(0)


def _parse_cli():
    parser = argparse.ArgumentParser(prog='bqtabulate')
    parser.add_argument('-i', '--infile', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o', '--outfile', nargs='?',
                        type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('-f', '--fmt', default='simple', help="Table format")
    return parser.parse_args()
