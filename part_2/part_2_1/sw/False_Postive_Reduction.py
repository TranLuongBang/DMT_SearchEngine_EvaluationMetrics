import csv
import re
import pandas as pd
import string


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(set(list1)) + len(set(list2))) - intersection
    return float(intersection) / union


def reduce_false_positive(input, output, file_path):
    df = pd.read_csv(file_path)
    j=0
    w = 3
    final_near_duplicates = []
    with open(input, 'r') as read_obj:
        csv_reader = csv.reader(read_obj, delimiter='\t')
        header = next(csv_reader)
        # Check file as empty
        if header is not None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:
                j += 1
                if j % 100 == 0:
                    print(j)
                # Extract information
                ID1 = re.findall("\d+", row[2])[0]
                ID2 = re.findall("\d+", row[4])[0]
                song1 = df[df.ID == int(ID1)].lyrics.values[0]
                song2 = df[df.ID == int(ID2)].lyrics.values[0]
                song1_words = song1.translate(str.maketrans('', '', string.punctuation)).lower().split()
                song2_words = song2.translate(str.maketrans('', '', string.punctuation)).lower().split()
                shingle1 = [' '.join(song1_words[i:i + w]) for i in range(len(song1_words) - w + 1)]
                shingle2 = [' '.join(song2_words[i:i + w]) for i in range(len(song2_words) - w + 1)]
                jaccard_sim = jaccard_similarity(shingle1, shingle2)
                if jaccard_sim > .95:
                    final_near_duplicates.append([ID1, ID2, jaccard_sim])

    print('...writing tsv file...')
    with open(output, 'w', newline='') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['ID1', 'ID2', 'Jaccard Value (w=3)'])
        for i in final_near_duplicates:
            tsv_writer.writerow(i)


def main():
    input_path = '../output_data/Results.tsv'
    output_path = '../output_data/Final_Results.tsv'
    file_path = '../../dataset/250K_lyrics_from_MetroLyrics.csv'

    reduce_false_positive(input=input_path, output=output_path, file_path=file_path)

    file = pd.read_csv(input_path, delimiter='\t')
    print('Potential Near Duplicates:', len(file))

    file = pd.read_csv(output_path, delimiter='\t')
    print('Final Near Duplicates:', len(file))


if __name__ == "__main__":
    main()


