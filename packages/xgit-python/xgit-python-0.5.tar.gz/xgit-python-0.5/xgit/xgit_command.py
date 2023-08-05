#!/usr/bin/python3
# coding=utf-8

from errno import ENOENT
import sys
from typing import List
from typing import Optional

from xarg import argp

from . import __version__
from .xgit_modify_author import add_cmd_modify_author
from .xgit_modify_author import run_cmd_modify_author
from .xgit_modify_committer import add_cmd_modify_committer
from .xgit_modify_committer import run_cmd_modify_committer
from .xgit_summary import add_cmd_summary
from .xgit_summary import run_cmd_summary
from .xgit_util import URL_PROG


def run_sub_command(args) -> int:
    cmds = {
        "summary": run_cmd_summary,
        "modify-author": run_cmd_modify_author,
        "modify-committer": run_cmd_modify_committer,
    }
    if not hasattr(args, "sub") or args.sub not in cmds:
        return ENOENT
    return cmds[args.sub](args)


def main(argv: Optional[List[str]] = None) -> int:
    try:
        _arg = argp("xgit",
                    description="Git tool based on GitPython",
                    epilog=f"For more, please visit {URL_PROG}")
        _arg.add_opt_on('-d', '--debug', help="show debug information")
        _arg.add_opt_on('-v', '--version', help="show version information")
        _sub = _arg.add_subparsers(dest="sub")
        add_cmd_modify_author(_sub.add_parser("modify-author"))
        add_cmd_modify_committer(_sub.add_parser("modify-committer"))
        add_cmd_summary(_sub.add_parser("summary"))

        args = _arg.parse_args()
        if hasattr(args, "debug") and args.debug:
            sys.stderr.write(f"{args}\n")
            sys.stderr.flush()

        if hasattr(args, "version") and args.version:
            sys.stderr.write(f"{__version__}\n")
            sys.stderr.flush()
            return 0

        return run_sub_command(args)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.stderr.flush()
        return 10000
