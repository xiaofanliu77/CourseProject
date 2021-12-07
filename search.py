import sys
import metapy
import pytoml
import re


stopwords = []

'''
Prints a truncated version of doc containing the first k occurences
of the words in query, where the k words in query are highlighted
'''
def print_with_highlight(doc, query, k, idx=None):
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
            count += 1
            if count == k:
                end = i
                break

    if start == -1 or end == -1:
        cutoff = 150
        content = ' '.join(words[:cutoff]) + "......"
    else:
        i = max(start - 4, 0)
        j = min(end + 4, len(words))
        content_words = ' '.join(words[i:j])
        content = "......" + content_words + "......"


    highlight_str = r"\b(?:" + '|'.join(highlight_list) + r")\b"
    text_highlight = re.sub(highlight_str, '\033[36;40m\g<0>\033[m', content)
    if idx:
        print("{}. {}...\n".format(idx, text_highlight))
    else:
        print(text_highlight)

if __name__ == '__main__':

    with open('stopwords.txt') as f:
        stopwords = f.read().splitlines()

    cfg = "config.toml"
    idx = metapy.index.make_inverted_index(cfg)

    # testing code - not used in final program
    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    top_k = 10
    query_path = query_cfg.get('query-path', 'CampusWireHeading_Queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    # get the query from user input
    query_text = input("please enter a search query: ")
    query = metapy.index.Document()
    query.content(query_text.lower())


    # get ranking function from user input
    ranking_function = input("""Please select a ranking function. Enter
        1 for Okapi BM25
        2 for Pivoted Length Normalization
        3 for Jelinek-Mercer Smoothing
        4 for Dirichlet Prior Smoothing.
        (Note: If none of these is entered, Okapi BM25 will be used by default.)
""")


    if ranking_function == "2":
        print("Selected Pivoted Length Normalization as ranking function.")
        ranker = metapy.index.PivotedLength(s=0.2)
    elif ranking_function == "3":
        print("Selected Jelinek-Mercer Smoothing as ranking function.")
        ranker = metapy.index.JelinekMercer(.85)
    elif ranking_function == "4":
        print("Selected Dirichlet Prior Smoothing as ranking function.")
        ranker = metapy.index.DirichletPrior(2000)
    else:
        print("Selected Okapi BM25 as ranking function.")
        ranker = metapy.index.OkapiBM25(k1=1.2, b=.75, k3=500)

    top_docs = ranker.score(idx, query, num_results=10)

    print("Returning top search results: ")

    for num, (d_id, _) in enumerate(top_docs):
        content = idx.metadata(d_id).get('content')
        if content is not None:
            print_with_highlight(content, query_text, 5, num+1)



