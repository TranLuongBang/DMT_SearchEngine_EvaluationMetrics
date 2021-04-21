from bs4 import BeautifulSoup
import regex as re
import csv
from whoosh.analysis import *
import os


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def parse_html_files(path, output='html_content.tsv'):
    """
    Given a path with a set of html files, parse them and store results as a tsv table

    :param path: Path in which html files are located
    :param output: Name of the tsv that will be created (will be stored in the path folder)
    :return: Generate tsv file
    """
    general_list = [['ID', 'Title', 'Content']]
    for html_file in os.listdir(path):
        print(html_file)
        with open(path + '/' + html_file, encoding='utf8') as infile:
            print('...parsing...')
            soup = BeautifulSoup(infile, features='lxml')
            ID = int(re.findall(r'\d+', html_file)[0])
            Title = remove_html_tags(str(soup.find('title'))).replace('\n', ' ')
            Content = remove_html_tags(str(soup.find('body'))).replace('\n', ' ')
            temp_list = [ID, Title, Content]
            general_list.append(temp_list)

    with open(path + '/' + output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(general_list)


def main():
    path = '..\..\..\data\DOCUMENTS_CRAN'
    parse_html_files(path, output='html_content_cran.tsv')


if __name__ == "__main__":
    main()
