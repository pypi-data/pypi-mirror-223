#!/usr/bin/env python

import os, glob, shutil
import json
import re

from newexercises.enums import Language


def remove_trailing_commas(json_like):
    """Removes trailing commas from json_like."""

    trailing_object_commas_re = re.compile(
        r'(,)\s*}(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
    trailing_array_commas_re = re.compile(
        r'(,)\s*\](?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
    # Fix objects {} first
    objects_fixed = trailing_object_commas_re.sub("}", json_like)
    # Now fix arrays/lists [] and return the result
    return trailing_array_commas_re.sub("]", objects_fixed)


def fix_json(file):
    """Removes trailing coma from json file."""

    _file = open(file)
    # read whole file to a string
    data = _file.read()
    proper_json = remove_trailing_commas(data)  # Remove trailing commas
    validated = json.loads(proper_json)
    with open(file, 'w') as processed_file:
        processed_file.write(json.dumps(validated, indent=4))


def get_separator(lang):
    return Language.map_to_separator(lang)


def move_files(sourceDir, destinationDir):
    """Move files from source directory to destination (solutions folder)"""
    if not os.path.isdir(destinationDir):
        os.mkdir(destinationDir)
    [shutil.move(f, destinationDir) for f in glob.glob(sourceDir) if 'input' not in f]


def replace_last(source_string, element, replace_with):
    file_path, separator, tail = source_string.rpartition(element)
    return f'{file_path}{replace_with}{tail}'
