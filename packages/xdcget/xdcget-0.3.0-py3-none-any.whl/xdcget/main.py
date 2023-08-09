"""
Command line options and xdcget subcommand wrapper.
"""
import argparse
from pathlib import Path

from termcolor import colored

from . import __version__
from .config import read_config, write_initial_config
from .errors import EmptyOrUnsetEnvVar, MissingOrEmptyField
from .storage import perform_export, perform_update


class Out:
    def red(self, msg):
        print(colored(msg, "red"))

    def green(self, msg):
        print(colored(msg, "green"))

    def __call__(self, msg, red=False, green=False):
        color = "red" if red else ("green" if green else None)
        print(colored(msg, color))


description = """\
Collect webxdc apps from releases in public repositories,
perform consistency checks and export them with normalized filenames
with full metadata in a toml file.  The tool is configured via a `xdcget.ini` file
that can be created using 'xdcget init'.
"""


def get_parser():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--config",
        type=Path,
        dest="xdcget_ini",
        default=Path("xdcget.ini"),
        help="path to xdcget.ini file (defaults to look in current directory)",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help=f"only output version ({__version__})",
    )
    subparsers = parser.add_subparsers(
        title="subcommands",
    )

    def add(func):
        name = func.__name__
        assert name.endswith("_cmd")
        name = name[:-4]
        doc = func.__doc__.strip()
        p = subparsers.add_parser(name, description=doc, help=doc)
        p.set_defaults(func=func)
        return p

    add(init_cmd)
    subparser = add(update_cmd)
    subparser.add_argument(
        "--offline",
        action="store_true",
        help="don't perform any network requests",
    )
    subparser.add_argument(
        "app_filter",
        metavar="filter",
        nargs="?",
        help="Only update sources whose app-id contains the specified filter string",
    )
    return parser


def init_cmd(args, out):
    """Initialize config template file if it doesn't exist."""
    if args.xdcget_ini.exists():
        out.red(f"Path exists, not modifying: {args.xdcget_ini}")
        raise SystemExit(1)
    write_initial_config(args.xdcget_ini, out)


def update_cmd(args, out):
    """Update released webxdc app files by checking remote repositories."""
    try:
        config = read_config(args.xdcget_ini)
    except (EmptyOrUnsetEnvVar, MissingOrEmptyField) as ex:
        out.red(ex)
        raise SystemExit(1)
    else:
        perform_update(config, args.app_filter, out, offline=args.offline)
        perform_export(config, out, offline=args.offline)


def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args=args)
    if not hasattr(args, "func"):
        if args.version:
            print(__version__)
            parser.exit(0)
        return parser.parse_args(["-h"])
    out = Out()
    args.func(args, out)


if __name__ == "__main__":
    main()
