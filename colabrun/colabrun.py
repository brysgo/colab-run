# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Usage:
#
# python -m libcst.tool --help
# python -m libcst.tool print python_file.py

import argparse
import os
import os.path
import sys
from abc import abstractmethod
from typing import Any, Dict, List
from colabrun.colab_metadata_transform import (
    ConvertColabMetadataCommand,
)


from libcst import (
    parse_module,
)
from libcst._nodes.deep_equals import deep_equals
from libcst.codemod import (
    CodemodCommand,
    CodemodContext,
    diff_code,
    exec_transform_with_prettyprint,
    gather_files,
    parallel_exec_transform_with_prettyprint,
)


def _default_config() -> Dict[str, Any]:
    current_dir = os.path.abspath(os.getcwd())

    return {
        "generated_code_marker": f"@gen{''}erated",
        "formatter": ["black", "-"],
        "blacklist_patterns": [],
        "modules": [
            os.path.abspath(
                os.path.join(current_dir, "colab_metadata_transform"),
            )
        ],
        "repo_root": ".",
    }


def _codemod_impl(proc_name: str, command_args: List[str]) -> int:  # noqa: C901
    # Grab the configuration for running this, if it exsts.
    config = _default_config()

    # First, try to grab the command with a first pass. We aren't going to react
    # to user input here, so refuse to add help. Help will be parsed in the
    # full parser below once we know the command and have added its arguments.
    parser = argparse.ArgumentParser(add_help=False, fromfile_prefix_chars="@")
    parser.add_argument(
        "path",
        metavar="PATH",
        nargs="+",
        help=(
            "Path to codemod. Can be a directory, file, or multiple of either. To "
            + 'instead read from stdin and write to stdout, use "-"'
        ),
    )
    args, _ = parser.parse_known_args(command_args)
    command_class = ConvertColabMetadataCommand

    codemod_args = {"gather": True}
    command_instance = command_class(CodemodContext(), **codemod_args)

    # Now, construct the full parser, parse the args and run the class.
    full_parser = argparse.ArgumentParser(
        description=ConvertColabMetadataCommand.DESCRIPTION,
        fromfile_prefix_chars="@",
    )
    command_class.add_args(full_parser)
    args, _ = parser.parse_known_args(command_args)

    f = open(args.path[0], "r")
    oldcode = f.read()

    # Let's run it!
    exec_transform_with_prettyprint(
        command_instance,
        oldcode,
        include_generated=None,
        generated_code_marker=config["generated_code_marker"],
        format_code=False,
        formatter_args=config["formatter"],
        python_version=None,
    )

    full_parser.add_argument(
        "path",
        metavar="PATH",
        type=str,
        help="Path to initialize with a default LibCST codemod configuration",
    )
    args = full_parser.parse_args(command_args)
    codemod_args = {
        k: v
        for k, v in vars(args).items()
        if k
        not in [
            "command",
            "path",
            "unified_diff",
            "jobs",
            "python_version",
            "include_generated",
            "include_stubs",
            "no_format",
            "show_successes",
            "hide_generated_warnings",
            "hide_blacklisted_warnings",
            "hide_progress",
        ]
    }
    command_instance = command_class(CodemodContext(), **codemod_args)

    newcode = exec_transform_with_prettyprint(
        command_instance,
        oldcode,
        include_generated=None,
        generated_code_marker=config["generated_code_marker"],
        format_code=False,
        formatter_args=config["formatter"],
        python_version=None,
    )
    if not newcode:
        print("Failed to codemod from stdin", file=sys.stderr)
        return 1

    print(newcode)
    return 0


def cli():
    main(sys.argv[0], sys.argv[1:])


def main(proc_name: str, cli_args: List[str]) -> int:
    # Hack to allow "--help" to print out generic help, but also allow subcommands
    # to customize their parsing and help messages.
    first_arg = cli_args[0] if cli_args else "--help"
    add_help = first_arg in {"--help", "-h"}

    # Create general parser to determine which command we are invoking.
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Utility to help run colab exports from the CLI",
        add_help=add_help,
        prog=proc_name,
        fromfile_prefix_chars="@",
    )
    args, command_args = parser.parse_known_args(cli_args)

    return _codemod_impl(proc_name, command_args)


if __name__ == "__main__":
    sys.exit()
