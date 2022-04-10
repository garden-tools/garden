import argparse
import logging
import os

from travel.cli import python_wrapper, packer, planner
from travel.cli.cleaner import Cleaner
from travel.cli.setupper import Setupper

logger = logging.getLogger(__name__)


def main():

    # Travel
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Print a stacktrace of errors", action="store_true")
    parser.add_argument("--context", default=os.getcwd(), help="Path to the folder containing the bag.yml file")
    parser.set_defaults(action=lambda args: parser.parse_args(["-h"]))
    subparsers = parser.add_subparsers()

    # Clean
    clean = subparsers.add_parser("clean")
    clean.set_defaults(action=lambda args, rest: Cleaner().manage(args.context))

    # Plan
    plan = subparsers.add_parser("plan")
    plan.add_argument("name", help="Main bag name (name of the project)")
    plan.set_defaults(action=lambda args, rest: planner.run(args.context, args.name))

    # Setup
    setup = subparsers.add_parser("setup")
    setup.set_defaults(action=lambda args, rest: Setupper().manage(args.context))

    # Pack
    pack = subparsers.add_parser("pack")
    pack.add_argument("--target", help="Name of the bag to run setup.py commands", required=False)
    pack.add_argument("--no-setup", help="Do not update the venvs", required=False, action="store_true")
    pack.set_defaults(action=lambda args, rest: packer.pack(args.context, rest, target=args.target, setup=not args.no_setup))

    # Release

    # # Python
    # python = subparsers.add_parser("python")
    # python.add_argument("package", help="Name of the bag (it will be used to activate its venv)")
    # python.set_defaults(action=lambda args, rest: python_wrapper.run(args.context, args.package, rest))

    # Parse args
    arguments, remainder = parser.parse_known_args()

    try:

        # Invoke the corresponding functions
        arguments.action(arguments, remainder)
        logger.info("All done.")

    except Exception as e:

        if arguments.debug:
            logger.exception("")
        else:
            logger.error(e if str(e) else f"Error: {type(e)}")
        exit(1)


if __name__ == '__main__':
    main()
