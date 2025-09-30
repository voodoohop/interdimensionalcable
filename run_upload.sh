#!/bin/bash
set -a
source .env
set +a
python3 upload_to_stream.py
