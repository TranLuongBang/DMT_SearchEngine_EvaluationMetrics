import utils
import numpy as np
import EvaluationMetrics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():

    ground_truth_path = './data/part_1_2__Ground_Truth.tsv'
    result_se1_path = './data/part_1_2__Results_SE_1.tsv'
    result_se2_path = './data/part_1_2__Results_SE_2.tsv'
    result_se3_path = './data/part_1_2__Results_SE_3.tsv'

    ground_truth = utils.read_ground_truth(ground_truth_path)

    se1 = utils.read_result_se(result_se1_path)
    se2 = utils.read_result_se(result_se2_path)
    se3 = utils.read_result_se(result_se3_path)

    search_engine_conf = {1: se1, 2: se2, 3: se3}

    print('P@k....')
    P_at_k_res = EvaluationMetrics.P_at_k(ground_truth, search_engine_conf, k_vals=[4])
    PK = []
    for k, P_k_list in P_at_k_res.items():
        count = 1
        for pk in P_k_list:
            SE = 'SE' + str(count)
            PK.append([SE, pk])
            count += 1

    df = pd.DataFrame(PK, columns=['SE', 'PK'])
    print(P_at_k_res)
    plt.figure(figsize=(15, 7))
    plot = sns.barplot(x='SE', y='PK', data=df)
    for p in plot.patches:
        plot.annotate(format(p.get_height(), ',.2f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center',
                      va='center',
                      xytext=(0, 10),
                      textcoords='offset points')

    plt.title('P@k Evaluation Metrics of Search Engines with k =4')
    plt.xlabel('Search Engines')
    plt.ylabel('The average P@k over all provided queries')
    plt.ylim(0, df['PK'].max() * 1.2)
    plt.savefig('./Report/Images/Pk_part1_2.png')

    print('R@k....')
    R_at_k_res = EvaluationMetrics.R_at_k(ground_truth, search_engine_conf, k_vals=[4])
    RK = []
    for k, R_k_list in R_at_k_res.items():
        count = 1
        for rk in R_k_list:
            SE = 'SE' + str(count)
            RK.append([SE, rk])
            count += 1
    print(R_at_k_res)
    df = pd.DataFrame(RK, columns=['SE', 'RK'])
    print(df)
    plt.figure(figsize=(15, 7))
    plot = sns.barplot(x='SE', y='RK', data=df)
    for p in plot.patches:
        plot.annotate(format(p.get_height(), ',.2f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center',
                      va='center',
                      xytext=(0, 10),
                      textcoords='offset points')

    plt.title('R@k Evaluation Metrics of Search Engines with k =4')
    plt.xlabel('Search Engines')
    plt.ylabel('The average R@k over all provided queries')
    plt.ylim(0, df['RK'].max() * 1.2)
    plt.savefig('./Report/Images/Rk_part1_2.png')


    print('NCDG@k....')
    ncdg_at_k_res = EvaluationMetrics.ncdg(ground_truth, search_engine_conf, k_vals=[4])

    nDCG_results = []
    for k, nDCG_list in ncdg_at_k_res.items():
        count = 1
        for nDCG in nDCG_list:
            SE = 'SE' + str(count)
            nDCG_results.append([SE, nDCG])
            count += 1

    df = pd.DataFrame(nDCG_results, columns=['SE', 'nDCG'])
    print(df)
    plt.figure(figsize=(15, 7))
    plot = sns.barplot(x='SE', y='nDCG', data=df)
    for p in plot.patches:
        plot.annotate(format(p.get_height(), ',.2f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center',
                      va='center',
                      xytext=(0, 10),
                      textcoords='offset points')

    plt.title('nDCG Evaluation Metrics of Search Engines with k =4')
    plt.xlabel('Search Engines')
    plt.ylabel('The average nDCG over all provided queries')
    plt.ylim(0, df['nDCG'].max() * 1.2)
    plt.savefig('./Report/Images/nDCG_part1_2.png')

if __name__ == "__main__":
    main()