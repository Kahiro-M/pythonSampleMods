#!/bin/bash
pyinstaller \
    --onefile \
    --noconsole \
    --add-data "external_define.py:." \
    --add-data "mkdir_datetime.py:." \
    --add-data "file_size.py:." \
    --add-data "sample.py:." \
    --icon=icon.ico \
    sample_gui.py \
    -n sample