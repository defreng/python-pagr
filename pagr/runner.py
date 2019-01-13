import importlib
import logging
import os
import re
from argparse import ArgumentParser

import sys
import yaml

from pagr.mbook import MBook


def run(args=None):
    parser = ArgumentParser(description='pagr - the Python Aggregator')
    parser.add_argument('mbooks', metavar='my_mbook.yaml', type=str, nargs='+',
                        help='a metricbook configuration file to execute')

    args = parser.parse_args(args)
    for mbook_filename in args.mbooks:
        mbook = MBook(mbook_filename)
        mbook.run()
