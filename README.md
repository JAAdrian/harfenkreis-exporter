# Harfenkreis Exporter

This repository provides a Python script which reads in a large WAV file and a
corresponding Audacity label file in order to extract and write the audio segments to
file using the MP3 format.

# Usage

For detailed information use the file's CLI help:

```bash
python export_from_audacity_labels.py -h
```

This will result in something like

```
usage: export_from_audacity_labels.py [-h] [-i INPUT_PATH] [-o OUTPUT_PATH]

options:
  -h, --help            show this help message and exit
  -i INPUT_PATH, --input-path INPUT_PATH
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
```

For smooth operations, just provide an input and output directory.

The **input directory** is implicitly supposed to contain a WAV and a TXT file. Both are
usually exports from Audacity. The TXT file is an export of the label track in Audacity
which was used to label the song segments.

```
input_directory
|
|-- source_audio.wav
|-- label_export.txt
```

The resulting MP3 files of the individual song segments will be exported to the output
directory. If it does not yet exist, it will be created.
