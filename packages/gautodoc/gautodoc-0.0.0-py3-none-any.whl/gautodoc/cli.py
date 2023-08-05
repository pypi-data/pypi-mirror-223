#!/usr/bin/env python

import os
import argparse
import gautodoc.registry
from gautodoc.config import Config
from gautodoc.build import build

def gautodoc_init(args):
    build_dir = os.path.relpath(args.build_dir, start=args.project_dir)

    Config(
        modules=args.modules,
        build_dir=build_dir,
    ).write(dir_relpath=args.project_dir)

def gautodoc_build(args):
    cfg = Config.load(args.project_dir)
    build(cfg, args.project_dir)

def gautodoc_cli():
    """does all of the argparsing and dispatches to subcommands"""

    # main parser
    gautodoc_parser = argparse.ArgumentParser(
        prog="gautodoc",
        description="a stupid simple autodoc for python",
    )
    subparsers = gautodoc_parser.add_subparsers(
        required=True,
        help="gautodoc subcommands",
    )

    # gautodoc init
    init_parser = subparsers.add_parser(
        'init',
        help="initialize or reconfigure a gautodoc project",
    )
    init_parser.set_defaults(dispatch=gautodoc_init)

    init_parser.add_argument(
        'modules',
        type=str,
        nargs='+',
        help="paths to root modules to be documented",
    )
    init_parser.add_argument(
        '-d',
        '--project-dir',
        type=str,
        default='.',
        help="project directory to configure",
    )
    init_parser.add_argument(
        '-b',
        '--build-dir',
        type=str,
        default='./doc',
        help="build output directory",
    )

    # gautodoc build
    build_parser = subparsers.add_parser(
        'build',
        help="build a gautodoc project",
    )
    build_parser.set_defaults(dispatch=gautodoc_build)

    build_parser.add_argument(
        '-d',
        '--project-dir',
        type=str,
        default='.',
        help="project directory to build",
    )

    # parse args and dispatch
    args = gautodoc_parser.parse_args()
    args.dispatch(args)