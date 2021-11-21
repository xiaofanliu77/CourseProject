import math
import sys
import time
import metapy
import pytoml


if __name__ == '__main__':

    cfg = "config.toml"
    # print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = metapy.index.OkapiBM25(k1=1.5, b=0.75, k3=500)
    # ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    # start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'CampusWireHeading_Queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    # ndcg = 0.0
    num_queries = 0

    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            print(results)
            # ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1
    # ndcg= ndcg / num_queries


    # print("NDCG@{}: {}".format(top_k, ndcg))
    # print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
