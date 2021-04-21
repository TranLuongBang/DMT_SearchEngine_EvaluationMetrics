import pandas as pd
from collections import defaultdict
import utils
import csv
import string
import numpy as np
import matplotlib.pyplot as plt


def preprocess_data(input_path):
    data = pd.read_csv(input_path, usecols=['ID', 'song'])
    data['song'] = data['song'].apply(
        lambda x: str(x).replace('-', ' ').translate(str.maketrans('', '', string.punctuation)).lower())
    return data


def generate_shingle(data, output_path, w=3):
    shingles_dict = dict()
    shingles_identifier = defaultdict(set)
    count = 0

    for index, row in data.iterrows():
        id = row['ID']
        song = row['song'].split(' ')

        if len(song) < w:
            shingle = tuple(song)
            shingles_identifier[id].add(shingle)
            if shingle not in shingles_dict:
                shingles_dict[shingle] = count
                count += 1
        else:
            for i in range(len(song) - w + 1):
                shingle = tuple(song[i:i + w])
                if shingle not in shingles_dict:
                    shingles_dict[shingle] = count
                    count += 1
                shingles_identifier[id].add(shingle)

    shinglees_results = defaultdict(list)

    for id, shingles in shingles_identifier.items():
        shinglees_results['id_' + str(id)] = [shingles_dict[shingle] for shingle in shingles]

    final_data = pd.DataFrame(shinglees_results.items(), columns=['ID', 'ELEMENTS_IDS'])

    final_data.to_csv(output_path, sep="\t", index=False)


def prob(j, r, b):
    value = 1 - (1 - j ** r) ** b
    return value


def b_vs_r(r, t = 0.97):
    """
    Given a value of r, based on the second constraint, what is the minimum value b can take?
    :param t:
    :param r:
    :return:
    """
    min_b = (np.log(1 - t)) / (np.log(1 - .95 ** r))
    return min_b


def view_plot(r, b='default', jacc=.95, t=.97):
    if b == 'default':
        b_value = b_vs_r(r, t)
        print(b_value)
    else:
        b_value = b
    x = np.arange(0, 1, .001)
    y = prob(x, r, b_value)
    # plot the prob
    plt.plot(x, y, 'b-')
    plt.xlabel('Jaccard Similarity value')
    plt.ylabel('Probability of two pairs with that Jaccard value \n of being provided by the LSH algorithm')
    plt.axvline(x=jacc, ymin=0, ymax=1, color='r', linestyle='--')
    plt.title('S-Curve')
    plt.show()


def main():
    input_path = './data/250K_lyrics_from_MetroLyrics.csv'
    output_path = './data/Shingles_Results.tsv'
    data = preprocess_data(input_path)
    generate_shingle(data, output_path)
    r = 10
    view_plot(r, b='default', jacc=1, t=0.7)



if __name__ == "__main__":
    main()
