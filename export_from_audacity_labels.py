"""Script which cuts audio from a WAV recording based on labels and exports MP3.

Author: Jens-Alrik Adrian
Year: 2024
"""

import argparse
import pathlib

import pandas
import soundfile
from tqdm import tqdm


def _get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-path", type=pathlib.Path)
    parser.add_argument("-o", "--output-path", type=pathlib.Path)

    return parser


def _read_label_file(filepath: pathlib.Path) -> pandas.DataFrame:
    labels = pandas.read_csv(filepath, delimiter="\t", header=None)
    labels.columns = ("start", "end", "name")
    return labels


def _export_mp3(
    wav_file: pathlib.Path, labels: pandas.DataFrame, destination_path: pathlib.Path
):
    audio, sample_rate = soundfile.read(wav_file)

    for index, row in tqdm(labels.iterrows(), total=labels.shape[0]):
        start, stop, name = row

        start_sample = round(start * sample_rate)
        stop_sample = round(stop * sample_rate)

        filestem = f"{index}_{name}.mp3"
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

    input_path = arguments.input_path
    output_path = arguments.output_path

    wav_files = tuple(input_path.glob("*.wav"))
    label_files = tuple(input_path.glob("labels.txt"))

    if len(wav_files) > 1 or len(label_files) > 1:
        raise ValueError(
            "More than one WAV or label file have been found. "
            "Only provide one of each in a single direcotry."
        )

    wav_file = wav_files[0]
    label_file = label_files[0]

    destination = pathlib.Path("mp3")
    if not destination.is_dir():
        destination.mkdir()

    labels = _read_label_file(label_file)
    _export_mp3(wav_file, labels, destination_path=destination)
