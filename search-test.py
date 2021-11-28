import math
import sys
import time
import metapy
import pytoml
import io
# import docx
# from docx.enum.text import WD_COLOR_INDEX
import re

# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


if __name__ == '__main__':

    cfg = "config.toml"
    # print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = metapy.index.OkapiBM25()
    # ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=0)
    # ranker = metapy.index.JelinekMercer()


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
    query_text = "Question on Probabilistic retrieval model"

    query.content(query_text.lower())

    top_docs = ranker.score(idx, query, num_results=10)
    print(top_docs)

    print(idx.num_docs())

    for num, (d_id, _) in enumerate(top_docs):
        content = idx.metadata(d_id).get('content')
        if content is not None:
            # print("{}. {}...\n".format(d_id+1, content))
            highlight_list = query_text.split(" ")
            highlight_str = r"\b(?:" + '|'.join(highlight_list) + r")\b"
            text_highlight = re.sub(highlight_str, '\033[36;40m\g<0>\033[m', content)
            print("{}. {}...\n".format(d_id, text_highlight))


    # # ndcg = 0.0
    # num_queries = 0
    #
    #
    #
    #
    #
    #
    # print('Running queries')
    # with open(query_path) as query_file:
    #     for query_num, line in enumerate(query_file):
    #         query.content(line.strip())
    #         results = ranker.score(idx, query, top_k)
    #         print(results)
    #         # ndcg += ev.ndcg(results, query_start + query_num, top_k)
    #         num_queries+=1
    # # ndcg= ndcg / num_queries


    # print("NDCG@{}: {}".format(top_k, ndcg))
    # print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
