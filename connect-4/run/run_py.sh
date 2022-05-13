#!/bin/sh

script_path=$(readlink -f "$0")
script_directory_path=$(dirname "$script_path")
script_parent_directory=$(dirname "$script_directory_path")

python_script_path="$script_parent_directory/src_py/main.py"
python_path="$script_parent_directory/venv/bin/python3"

export PYTHONUNBUFFERED=1

. "$script_parent_directory/venv/bin/activate"

$python_path $python_script_path --x "$1" --y "$2" --board "$3"
