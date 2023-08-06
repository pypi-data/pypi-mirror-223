
import itertools
import json
import logging
import os
import pandas as pd
from pathlib import Path



LOGGER = logging.getLogger(__name__)


def _get_dataset_subset(data, metadata_dict, max_rows=1000, max_columns=10):

    columns = metadata_dict['columns']
    if len(columns) > max_columns:
        columns = dict(itertools.islice(columns.items(), max_columns))
        metadata_dict['columns'] = columns
        data = data[columns.keys()]

    data = data.head(max_rows)

    return data, metadata_dict


def load_original_dataset(dataset_path, limit_dataset_size=None):

    with open(dataset_path) as data_csv:
        data = pd.read_csv(data_csv)

    stem=Path(dataset_path).stem
    base_path=Path(dataset_path).parent
    metadata_filename = stem+'_metadata.json'
    if not os.path.exists(f'{base_path}/{metadata_filename}'):
        raise Exception('Metadata file absent')

    with open(base_path / metadata_filename) as metadata_file:
        metadata_dict = json.load(metadata_file)

    if limit_dataset_size:
        data, metadata_dict = _get_dataset_subset(data, metadata_dict)

    return data, metadata_dict


def load_synthetic_dataset(dataset_path):

    with open(dataset_path) as data_csv:
        data = pd.read_csv(data_csv)

    stem=Path(dataset_path).stem
    output_filename = stem+'_output.json'
    base_path=Path(dataset_path).parent
    if not os.path.exists(f'{base_path}/{output_filename}'):
        raise Exception('Output file absent')

    with open(base_path / output_filename) as metadata_file:
        output_dict = json.load(metadata_file)


    return data, output_dict