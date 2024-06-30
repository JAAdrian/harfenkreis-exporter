"""Script which cuts audio from a WAV recording based on labels and exports MP3.

Author: Jens-Alrik Adrian
Year: 2024
"""

import argparse
import pathlib
import sys
from datetime import datetime

import pandas
import soundfile
from tqdm import tqdm

__version__ = "1.0.0"


def _get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-file",
        help=(
            "Point to the very WAV file for which the labels have been created. "
            "Audio from here will be segmented and exported to MP3."
        ),
        type=pathlib.Path,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output-path",
        help=(
            "State the output path to where the MP3 artifacts should be exported to. "
            "If the directory does not exist it will be created."
        ),
        type=pathlib.Path,
        required=True,
    )
    parser.add_argument(
        "-l",
        "--label-file",
        help=(
            "Point to the corresponding label file from Audacity. This will be used "
            "to segment the audio from INPUT_FILE."
        ),
        type=pathlib.Path,
        required=True,
    )
    parser.add_argument(
        "-d",
        "--creation-date",
        help=(
            "Choose a date like '2024-06-09'. It will be affixed in the MP3 filestem "
            "if available."
        ),
        required=False,
    )

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
    wav_file: pathlib.Path,
    labels: pandas.DataFrame,
    destination_path: pathlib.Path,
    creation_date: datetime = None,
):
    """Export the individual audio segments to MP3.

    Args:
        wav_file: Filepath to the source WAV file.
        labels: DataFrame containing the Audacity labels.
        destination_path: Destination filepath to which the MP3 files are being
                          exported.
        creation_date: Optional date which is affixed in the MP3 filestem. If `None`, no
                       date will be affixed.
    """
    audio, sample_rate = soundfile.read(wav_file)

    # Iterate over each DataFrame's row and export the corresponding audio segment.
    for index, row in tqdm(labels.iterrows(), total=labels.shape[0]):
        start, stop, name_raw = row

        name = name_raw.replace(" ", "-").replace("'", "")

        start_sample = round(start * sample_rate)
        stop_sample = round(stop * sample_rate)

        if creation_date:
            filestem = f"{index+1}_{creation_date.strftime('%Y%m%d')}_{name}.mp3"
        else:
            filestem = f"{index+1}_{name}.mp3"
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

    creation_date = None
    if arguments.creation_date:
        creation_date = datetime.fromisoformat(arguments.creation_date)

    if not input_file.is_file():
        raise ValueError()
    if not label_file.is_file():
        raise ValueError()

    if not output_path.is_dir():
        output_path.mkdir()

    labels = _read_label_file(label_file)
    _export_mp3(
        wav_file=input_file,
        labels=labels,
        destination_path=output_path,
        creation_date=creation_date,
    )
