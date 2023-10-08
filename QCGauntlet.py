import os, sys, shutil, subprocess
import pandas as pd
import numpy as np

from modules import *


class CommandLine:
    def __init__(self):
        import argparse

        # init parser
        self.parser = argparse.ArgumentParser(
            description="A CLI program that processes datasets and analyzes the quality of it.",
            prog="QCGauntlet.py",
            usage="python %(prog)s [command] [arg] [subparser] ...",
            add_help=True,
            prefix_chars="-",
        )

        # add subparser
        self.parser.add_subparsers(title="Gauntlet Analysis", dest="subcommands")


def main(inOpts=None):
    return


if __name__ == "__main__":
    main()
