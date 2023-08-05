#!/usr/bin/python3
# coding=utf-8

import sys

from xarg import argp

from .xgit_filter import add_cmd_filter_author
from .xgit_filter import add_cmd_filter_branch
from .xgit_filter import add_cmd_filter_path
from .xgit_filter import add_cmd_filter_repo
from .xgit_util import author
from .xgit_util import committed_datetime
from .xgit_util import committer
from .xgit_util import xgit_object


def add_cmd_summary(_arg: argp):
    _arg.add_opt_on('-d', '--debug', help="show debug information")
    add_cmd_filter_repo(_arg)
    add_cmd_filter_branch(_arg)
    add_cmd_filter_author(_arg)
    add_cmd_filter_path(_arg)
    # TODO: author option and datetime option
    _arg.add_opt_on('--short', help="show prefix, default full 40-byte SHA256")
    _arg.add_opt_on('--datetime', help="show datetime, default show date")
    _arg.add_opt_on('--author-email', help="show author email")
    _arg.add_opt_on('--committer', help="show committer name")
    _arg.add_opt_on('--committer-email', help="show committer name and email")


def run_cmd_summary(args) -> int:
    _idx = 0
    _obj = xgit_object(args.repo)
    kwargs = {"author": args.author, "no_merges": True}
    for commit in _obj.filter_commits(args.branch, args.path, **kwargs):
        _idx += 1
        _hexsha = _obj.short_hexsha(commit) if args.short else commit.hexsha
        _datetime = committed_datetime(commit, not args.datetime)
        _author = author(commit, not args.author_email)
        info_list = [_idx, _hexsha, _datetime, _author]
        if args.committer or args.committer_email:
            _committer = committer(commit, not args.committer_email)
            info_list.append(_committer)
        info_list.append(commit.summary)
        # _commit_info.append(commit.message)
        _commit_info = ",".join([str(i) for i in info_list])
        sys.stdout.write(f"{_commit_info}\n")
        sys.stdout.flush()
    return 0


def main():
    try:
        _arg = argp(prog="xgit-summary", description="list commit summary")
        add_cmd_summary(_arg)
        args = _arg.parse_args()
        if hasattr(args, "debug") and args.debug:
            sys.stderr.write(f"{args}\n")
            sys.stderr.flush()
        run_cmd_summary(args)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.stderr.flush()
