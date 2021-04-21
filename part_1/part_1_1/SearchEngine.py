# Import libraries
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import *
import pandas as pd
from whoosh import index as abc
from whoosh.qparser import *
from whoosh import scoring
import utils
from collections import defaultdict
import os


STOP_WORDS = frozenset(("i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                        "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                        "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom",
                        "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
                        "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but",
                        "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
                        "against", "between", "into", "through", "during", "before", "after", "above", "below", "to",
                        "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
                        "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few",
                        "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
                        "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"))


def SearchEngineCran(queries, text_analyzer, scoring_function, data_path, directory_containing_the_index, top_k):

    # Create a Schema
    schema = Schema(id=ID(stored=True), title=TEXT(stored=False, analyzer=text_analyzer),
                    content=TEXT(stored=False, analyzer=text_analyzer))

    if not os.path.exists(directory_containing_the_index):
        os.mkdir(directory_containing_the_index)

    # Create an empty-Index
    create_in(directory_containing_the_index, schema)

    # Open the Index
    ix = abc.open_dir(directory_containing_the_index)

    # Fill the Index
    writer = ix.writer()

    data = pd.read_csv(data_path, sep=',', header=0)

    for index, row in data.iterrows():
        id = row['ID']
        title = row['Title']
        content = row['Content']

        writer.add_document(id=str(id), title=title, content=content)

    writer.commit()

    ix = abc.open_dir(directory_containing_the_index)

    # Create a MultifieldParser for parsing the input_query
    qp = MultifieldParser(['title', 'content'], ix.schema)

    query_results = dict()
    for index, query in queries.iterrows():
        query_id = query['Query_ID']
        # print(query_id)
        parsed_query = qp.parse(query['Query'])

        # print('Input Query: ' + query['Query'])
        # print('Parsed Query:' + str(parsed_query))

        # Create a Searcher for the Index with the selected Scoring- Function
        docIDs = []

        with ix.searcher(weighting=scoring_function) as searcher:

            # perform a Search
            results = searcher.search(parsed_query, limit=top_k, terms=True, scored=True)
            # if results.has_matched_terms():
            #     # What terms matched in each hit?
            #     for hit in results:
            #         print('ID:', hit['id'])
            #         print(hit.score)
            #         print('Terms Matched:', hit.matched_terms())
            #         print('================')
            # print the ID of the best document
            for relev in results:
                docIDs.append(relev['id'])
        query_results[str(query_id)] = list(map(int, docIDs))

    # write query results
    utils.write_json('../../../data/query_results_cran.json', query_results)

    return query_results


def SearchEngineTime(queries, text_analyzer, scoring_function, data_path, directory_containing_the_index, top_k):

    # Create a Schema
    schema = Schema(id=ID(stored=True), content=TEXT(stored=False, analyzer=text_analyzer))

    if not os.path.exists(directory_containing_the_index):
        os.mkdir(directory_containing_the_index)

    # Create an empty-Index
    create_in(directory_containing_the_index, schema)

    # Open the Index
    ix = abc.open_dir(directory_containing_the_index)

    # Fill the Index
    writer = ix.writer()

    data = pd.read_csv(data_path, sep=',', header=0)

    for index, row in data.iterrows():
        id = row['ID']
        content = row['Content']

        writer.add_document(id=str(id), content=content)

    writer.commit()

    ix = abc.open_dir(directory_containing_the_index)

    # Create a MultifieldParser for parsing the input_query
    qp = QueryParser('content', ix.schema)

    query_results = dict()
    for index, query in queries.iterrows():
        query_id = query['Query_ID']
        # print(query_id)
        parsed_query = qp.parse(query['Query'])

        # print('Input Query: ' + query['Query'])
        # print('Parsed Query:' + str(parsed_query))

        # Create a Searcher for the Index with the selected Scoring-Function
        docIDs = []

        with ix.searcher(weighting=scoring_function) as searcher:

            # perform a Search
            results = searcher.search(parsed_query, limit=top_k, terms=True, scored=True)
            # if results.has_matched_terms():
            #     # What terms matched in each hit?
            #     for hit in results:
            #         print('ID:', hit['id'])
            #         print(hit.score)
            #         print('Terms Matched:', hit.matched_terms())
            #         print('================')
            # print the ID of the best document
            for relev in results:
                docIDs.append(relev['id'])
        query_results[str(query_id)] = list(map(int, docIDs))

    # write query results
    utils.write_json('../../../data/query_results_time.json', query_results)

    return query_results


def main():
    # CRANFIELD
    data_path = '../../../data/DOCUMENTS_CRAN/html_content_cran.tsv'
    query_path = '../../../data/cran_Queries.tsv'
    configuration_path = '../../../data/SearchEnginesCran.csv'
    top_k = 30

    queries = pd.read_csv(query_path, sep='\t')

    configurations = pd.read_csv(configuration_path)
    print(configurations)

    total_query_results = defaultdict(dict)

    for index, SE in configurations.iterrows():
        SE_ID = SE['SE_ID']
        text_analyzer = eval(SE['Text_Analyzer'])
        scoring_function = eval(SE['Scoring_Functions'])
        directory_containing_the_index = '../../../index/' + str(SE_ID)

        query_results = SearchEngineTime(queries, text_analyzer, scoring_function, data_path,
                                         directory_containing_the_index, top_k)
        print(SE_ID, query_results)
        total_query_results[SE_ID] = query_results

    utils.write_json('../../../data/total_query_results_cran.json', total_query_results)

    # TIME
    data_path = '../../../data/DOCUMENTS_TIME/html_content_time.tsv'
    query_path = '../../../data/time_Queries.tsv'
    configuration_path = '../../../data/SearchEnginesTime.csv'
    top_k = 30

    queries = pd.read_csv(query_path, sep='\t')

    configurations = pd.read_csv(configuration_path)
    print(configurations)

    total_query_results = defaultdict(dict)

    for index, SE in configurations.iterrows():
        SE_ID = SE['SE_ID']
        text_analyzer = eval(SE['Text_Analyzer'])
        scoring_function = eval(SE['Scoring_Functions'])
        directory_containing_the_index = '../../../index/' + str(SE_ID)

        query_results = SearchEngineCran(queries, text_analyzer, scoring_function, data_path,
                                         directory_containing_the_index, top_k)
        print(SE_ID, query_results)
        total_query_results[SE_ID] = query_results

    utils.write_json('../../../data/total_query_results_time.json', total_query_results)


if __name__ == "__main__":
    main()
