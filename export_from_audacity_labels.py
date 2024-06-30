"""Script which cuts audio from a WAV recording based on labels and exports MP3.

Author: Jens-Alrik Adrian
Year: 2024
"""

import argparse
import pathlib
import sys

import pandas
import soundfile
from tqdm import tqdm

__version__ = "1.0.0"


def _get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", type=pathlib.Path, required=True)
    parser.add_argument("-o", "--output-path", type=pathlib.Path, required=True)
    parser.add_argument("-l", "--label-file", type=pathlib.Path, required=True)

    return parser


def _read_label_file(filepath: pathlib.Path) -> pandas.DataFrame:
    """Read the Audactity label export file into a pandas DataFrame.

    Args:
        filepath: Filepath to the TXT label file.

    Returns:
        DataFrame containing the TXT-file's tabular content
    """
    labels = pandas.read_csv(filepath, delimiter="\t", header=None)
    labels.columns = ("start", "end", "name")
    return labels


def _export_mp3(
    wav_file: pathlib.Path, labels: pandas.DataFrame, destination_path: pathlib.Path
):
    """Export the individual audio segments to MP3.

    Args:
        wav_file: Filepath to the source WAV file.
        labels: DataFrame containing the Audacity labels.
        destination_path: Destination filepath to which the MP3 files are being
                          exported.
    """
    audio, sample_rate = soundfile.read(wav_file)

    # Iterate over each DataFrame's row and export the corresponding audio segment.
    for index, row in tqdm(labels.iterrows(), total=labels.shape[0]):
        start, stop, name = row

        start_sample = round(start * sample_rate)
        stop_sample = round(stop * sample_rate)

        filestem = f"{index+1}_{name}.mp3"
        filestem = filestem.replace(" ", "_").strip()
        mp3_filename = destination_path / filestem

        soundfile.write(
            file=mp3_filename,
            data=audio[start_sample:stop_sample],
            samplerate=sample_rate,
        )


if __name__ == "__main__":
    parser = _get_argparser()
    arguments = parser.parse_args()

    # Shortcircuit if no arguments had been given.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    input_file: pathlib.Path = arguments.input_file
    output_path: pathlib.Path = arguments.output_path
    label_file: pathlib.Path = arguments.label_file

    if not input_file.is_file():
        raise ValueError()
    if not label_file.is_file():
        raise ValueError()

    if not output_path.is_dir():
        output_path.mkdir()

    labels = _read_label_file(label_file)
    _export_mp3(wav_file=input_file, labels=labels, destination_path=output_path)
