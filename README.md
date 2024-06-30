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
usage: export_from_audacity_labels.py [-h] -i INPUT_FILE -o OUTPUT_PATH -l LABEL_FILE
                                      [-d CREATION_DATE]

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Point to the very WAV file for which the labels have been created. Audio
                        from here will be segmented and exported to MP3.
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        State the output path to where the MP3 artifacts should be exported to. If
                        the directory does not exist it will be created.
  -l LABEL_FILE, --label-file LABEL_FILE
                        Point to the corresponding label file from Audacity. This will be used to
                        segment the audio from INPUT_FILE.
  -d CREATION_DATE, --creation-date CREATION_DATE
                        Choose a date like '2024-06-09'. It will be affixed in the MP3 filestem if
                        available.
```

The resulting MP3 files of the individual song segments will be exported to the output
directory. If it does not yet exist, it will be created.
