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

stopwords = []

'''
Prints a truncated version of doc containing the first k occurences
of the words in query, where the k words in query are highlighted
'''
def print_with_highlight(doc, query, k, doc_id=None):
    highlight_list = []
    for w in query.split(" "):
        if w not in stopwords:
            highlight_list.append(w.capitalize())
            highlight_list.append(w.lower())
            highlight_list.append(w.upper())


    words = doc.split(" ")
    count = 0
    start, end = -1, -1
    seen = False
    for i, word in enumerate(words):
        if word in highlight_list and len(word) >= 1:
            if not seen:
                start = i
                seen = True
                print("seen: ", word, i)
            count += 1
            if count == k:
                end = i
                break

    if start == -1 or end == -1:
        cutoff = 150
        content = ' '.join(words[:cutoff]) + "......"
    else:
        print("start, end", start, end)
        i = max(start - 4, 0)
        j = min(end + 4, len(words))
        content_words = ' '.join(words[i:j])
        content = "......" + content_words + "......"


    highlight_str = r"\b(?:" + '|'.join(highlight_list) + r")\b"
    text_highlight = re.sub(highlight_str, '\033[36;40m\g<0>\033[m', content)
    if doc_id:
        print("{}. {}...\n".format(d_id, text_highlight))
    else:
        print(text_highlight)

if __name__ == '__main__':

    with open('stopwords.txt') as f:
        stopwords = f.read().splitlines()

    cfg = "config.toml"
    idx = metapy.index.make_inverted_index(cfg)
    ranker = metapy.index.OkapiBM25()


    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)



    top_k = 10
    query_path = query_cfg.get('query-path', 'CampusWireHeading_Queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    query_text = input("please enter a search query: ")
    ranking_function = input("""Please select a ranking function. Enter
        1 for Okapi BM25
        2 for Jelinek-Mercer
        3 for DirichletPrior
""")

    query.content(query_text.lower())

    top_docs = ranker.score(idx, query, num_results=10)

    print("top docs: ")
    print(top_docs)
    print(idx.num_docs())

    for num, (d_id, _) in enumerate(top_docs):
        content = idx.metadata(d_id).get('content')
        if content is not None:
            print_with_highlight(content, query_text, 5, d_id)

















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
