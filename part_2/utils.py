import os
import json
from collections import defaultdict
import pandas as pd
import csv


def write_json(file_name, content):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as outfile:
        json.dump(content, outfile, sort_keys=True, indent=4)


def read_json(file_name):
    with open(file_name) as json_file:
        data_dict = json.load(json_file, object_hook=jsonKeys2int)
        return data_dict


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(k): v for k, v in x.items()}
    return x


def read_ground_truth(path):
    """
    Function to read ground truth into dictionary

    :param path: Path and file name to be converted
    :return: Dictionary
    """
    ground_truth_dict = defaultdict(list)
    df = pd.read_csv(path, sep='\t')
    for index, row in df.iterrows():
        ground_truth_dict[str(row['Query_id'])].append(row['Relevant_Doc_id'])
    return dict(ground_truth_dict)


def write_csv(filename, content):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wt", newline='', encoding='utf-8') as out_file:
        tsv_writer = csv.writer(out_file, delimiter=',')
        tsv_writer.writerow(content)

def read_result_se(path):
    """
    Function to read ground truth into dictionary

    :param path: Path and file name to be converted
    :return: Dictionary
    """
    result_se_dict = defaultdict(list)
    df = pd.read_csv(path, sep='\t')
    count = 0
    for index, row in df.iterrows():
        if row['Rank'] <= 4:
            result_se_dict[row['Query_ID']].append(row['Doc_ID'])
            count += 1
    return dict(result_se_dict)



def write_tsv(filename, content):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wt", newline='', encoding='utf-8' ) as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(content)

