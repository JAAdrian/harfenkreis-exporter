"""Script which cuts audio from a WAV recording based on labels and exports MP3."""

import argparse
import pathlib

import numpy


def _get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=pathlib.Path)

    return parser


if __name__ == "__main__":
    parser = _get_argparser()
    arguments = parser.parse_args()

    path = arguments.path
