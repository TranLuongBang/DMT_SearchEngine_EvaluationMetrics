import csv
import re
import pandas as pd
import string
import dask.dataframe as ddf
import time



def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(set(list1)) + len(set(list2))) - intersection
    return float(intersection) / union


def get_JS(df1, df2, not_near_duplicate):

    for index, row in df1.iterrows():

        shingle1_id = row['name_set_1']
        shingle2_id = row['name_set_2']
        print(index,shingle1_id, shingle2_id)

        shingle1 = df2.loc[df2['ID'] == shingle1_id, 'ELEMENTS_IDS'].iloc[0]
        shingle2 = df2.loc[df2['ID'] == shingle2_id, 'ELEMENTS_IDS'].iloc[0]

        if sorted(shingle1) != sorted(shingle2):
            jac_sim = jaccard_similarity(shingle1, shingle2)
            print(jac_sim, shingle1_id, shingle2_id)
            not_near_duplicate[str(jac_sim)] = (shingle1_id, shingle2_id)

    return not_near_duplicate


def reduce_false_positive(input_path, output_path, shingle_path):
    result = pd.read_csv(input_path, sep='\t')
    shingles_results = pd.read_csv(shingle_path, sep='\t')

    dask_dataframe = ddf.from_pandas(result, npartitions=20)
    start = time.process_time()
    print(start)
    not_near_duplicate = dict()
    a = dask_dataframe.map_partitions(get_JS, df2=shingles_results, not_near_duplicate=not_near_duplicate, meta=dict).compute()
    end = time.process_time()
    print(end, end-start)
    print(a)


def main():
    input_path = './data/approximated_duplicated1.tsv'
    shingle_path = './data/Shingles_Results.tsv'
    reduce_false_positive(input_path, '', shingle_path)


if __name__ == "__main__":
    main()