import numpy as np
import utils
import pandas as pd
import matplotlib.pyplot as plt

# TODO: Make Plots nicer
# TODO: Maybe make code nicer
# TODO: Make variable names clearer
# TODO: improve search engine configurations


def MRR(ground_truth_dict, search_engine_conf):
    """

    :param ground_truth_dict:
    :param search_engine_conf:
    :return:
    """
    MRR_results = []
    for key, value in search_engine_conf.items():
        first_relevant_index_list = []
        for query_id, doc_ids in value.items():
            try:
                first_relevant_index = doc_ids.index(
                    next((i for i in doc_ids if i in ground_truth_dict[str(query_id)]), None)) + 1
                first_relevant_index_list.append(first_relevant_index)
            except:
                continue
        MRR_results.append((1 / len(ground_truth_dict)) * np.sum(1 / np.array(first_relevant_index_list)))

    return MRR_results


def R_Precision(ground_truth_dict, search_engine_conf):

    r_precision_list = []
    for key, value in search_engine_conf.items():
        res_temp = []
        for query_id, doc_ids in ground_truth_dict.items():
            len_ = len(ground_truth_dict[query_id])
            res = len(set(ground_truth_dict[query_id]).intersection(set(value[int(query_id)][:len_]))) / len_
            res_temp.append(res)
        r_precision_list.append(res_temp)

    return r_precision_list


def P_at_k(ground_truth_dict, search_engine_conf, k_vals=[1, 3, 5, 10]):
    """

    :param ground_truth_dict:
    :param search_engine_conf: Should only contain the top 5 already
    :param k_vals:
    :return:
    """
    k_list = dict()
    for k in k_vals:
        p_at_k_list = []
        for key, value in search_engine_conf.items():
            res_temp = []
            for query_id, doc_ids in ground_truth_dict.items():
                res = len(set(ground_truth_dict[query_id]).intersection(
                    set(value[int(query_id)][:k]))) / min(k, len(ground_truth_dict[query_id]))
                res_temp.append(res)
            p_at_k_list.append(res_temp)
        k_list[k] = list(np.mean(p_at_k_list, axis=1))

    return k_list

def R_at_k(ground_truth_dict, search_engine_conf, k_vals=[1, 3, 5, 10]):
    """

    :param ground_truth_dict:
    :param search_engine_conf: Should only contain the top 5 already
    :param k_vals:
    :return:
    """
    k_list = dict()
    for k in k_vals:
        r_at_k_list = []
        for key, value in search_engine_conf.items():
            res_temp = []
            for query_id, doc_ids in ground_truth_dict.items():
                try:
                    res = len(set(ground_truth_dict[query_id]).intersection(
                        set(value[int(query_id)][:k]))) / len(set(ground_truth_dict[query_id]).intersection(set(value[int(query_id)])))
                    res_temp.append(res)
                except:
                    res_temp.append(0)
            r_at_k_list.append(res_temp)
        k_list[k] = list(np.mean(r_at_k_list, axis=1))

    return k_list


def ncdg(ground_truth_dict, search_engine_conf, k_vals=[1, 3, 5, 10]):

    ncdgk = dict()
    for k in k_vals:
        ncdg_at_k_list = []
        for search_engine_id, query_results in search_engine_conf.items():
            ndcg = []
            for query_id, doc_ids in ground_truth_dict.items():
                relevance = np.array([1 if query_results[int(query_id)][i - 1] in doc_ids else 0 for i in range(1, k + 1)])
                log_ = np.array([1 / np.log2(p + 1) for p in range(1, k + 1)])
                dcg = np.sum(relevance * log_)
                idcg = np.sum(log_)
                ndcg.append(dcg/idcg)
            ncdg_at_k_list.append(ndcg)
        ncdgk[k] = list(np.mean(ncdg_at_k_list, axis=1))

    return ncdgk


def main():
    ground_truth_path = './data/cran_Ground_Truth.tsv'
    search_engine_conf_path = './data/total_query_results.json'
    configuration_path = './data/SearchEngines.csv'

    ground_truth_dict = utils.read_ground_truth(ground_truth_path)
    search_engine_conf = utils.read_json(search_engine_conf_path)

    MRR_results = MRR(ground_truth_dict, search_engine_conf)
    R_precision_results = R_Precision(ground_truth_dict, search_engine_conf)

    configurations = pd.read_csv(configuration_path)
    configurations['MRR'] = MRR_results
    configurations['Mean'] = np.mean(R_precision_results, axis=1)
    configurations['Min'] = np.min(R_precision_results, axis=1)
    configurations['Max'] = np.max(R_precision_results, axis=1)
    configurations['Median'] = np.median(R_precision_results, axis=1)
    configurations['1_quartile'] = np.quantile(a=R_precision_results, q=.25, axis=1)
    configurations['3_quartile'] = np.quantile(a=R_precision_results, q=.75, axis=1)

    configurations_top_5 = configurations.sort_values(by=['MRR'], ascending=False).head(5).SE_ID
    print(list(configurations_top_5))
    col_names = ['Conf_'+str(i) for i in list(configurations_top_5)]
    #col_names.reverse()
    search_engine_conf_top_5 = {key: search_engine_conf[key] for key in configurations_top_5}


    print('P@k....')
    P_at_k_res = P_at_k(ground_truth_dict, search_engine_conf_top_5)
    temp_df = pd.DataFrame(P_at_k_res).transpose()
    temp_df.columns = col_names
    ax = temp_df.plot(title='P@k')
    ax.set_xlabel('k values')
    ax.set_ylabel('Mean P@k')
    plt.savefig('./Report/Images/Pk.png')

    print('NCDG@k....')
    ncdg_at_k_res = ncdg(ground_truth_dict, search_engine_conf_top_5)
    temp_df = pd.DataFrame(ncdg_at_k_res).transpose()
    temp_df.columns = col_names
    ax = temp_df.plot(title='NCDG@k')
    ax.set_xlabel('k values')
    ax.set_ylabel('Mean NCDG@k')
    plt.savefig('./Report/Images/NCDGk.png')

    configurations = configurations.sort_values(by=['MRR'], ascending=False)
    configurations.to_csv(r'./data/SearchEnginesResults.csv', index=False)


if __name__ == "__main__":
    main()
