import math
import sys
import time
import metapy
import pytoml
import io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

if __name__ == '__main__':

    cfg = "config.toml"
    idx = metapy.index.make_inverted_index(cfg)
    data = []

    #Okapi Ranker with Parameters k1=1.2, b=.75, k3=500
    okapi_rankerp1 = metapy.index.OkapiBM25(k1=1.2, b=.75, k3=500)
    ev = metapy.index.IREval(cfg)

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
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = okapi_rankerp1.score(idx, query, top_k)                            
            avg_p = ev.avg_p(results, query_start + query_num, top_k)
    data.append(['Okapi',1.2, .75, 500,'NA','NA','NA', round(ev.map(),2)])

    #Okapi Ranker with Parameters k1=1.3, b=.8, k3=500
    okapi_rankerp2 = metapy.index.OkapiBM25(k1=1.3, b=.8, k3=500)
    ev2 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = okapi_rankerp2.score(idx, query, top_k)                            
            avg_p = ev2.avg_p(results, query_start + query_num, top_k)
    data.append(['Okapi',1.3, .8, 500,'NA','NA','NA', round(ev2.map(),2)])

    #Okapi Ranker with Parameters k1=1.3, b=.8, k3=500
    okapi_rankerp3 = metapy.index.OkapiBM25(k1=1.1, b=.5, k3=500)
    ev3 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = okapi_rankerp3.score(idx, query, top_k)                            
            avg_p = ev3.avg_p(results, query_start + query_num, top_k)
    data.append(['Okapi',1.1, .5, 500,'NA','NA','NA', round(ev3.map(),2)])

    #Pivoted Length Ranker with Parameters s=.2
    pivoted_length_rankerp1 = metapy.index.PivotedLength(s=.2)
    ev4 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = pivoted_length_rankerp1.score(idx, query, top_k)                            
            avg_p = ev4.avg_p(results, query_start + query_num, top_k)
    data.append(['Pivoted Length','NA','NA','NA',.2, 'NA','NA', round(ev4.map(),2)])

    #Pivoted Length Ranker with Parameters s=.01
    pivoted_length_rankerp2 = metapy.index.PivotedLength(s=.01)
    ev5 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = pivoted_length_rankerp1.score(idx, query, top_k)                            
            avg_p = ev5.avg_p(results, query_start + query_num, top_k)
    data.append(['Pivoted Length','NA','NA','NA',.01, 'NA','NA', round(ev5.map(),2)])

    #Pivoted Length Ranker with Parameters s=.5
    pivoted_length_rankerp3 = metapy.index.PivotedLength(s=.5)
    evhi = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = pivoted_length_rankerp3.score(idx, query, top_k)                            
            avg_p = evhi.avg_p(results, query_start + query_num, top_k)
    data.append(['Pivoted Length','NA','NA','NA',.5, 'NA','NA', round(evhi.map(),2)])

    #JelineK-Mercer Smoothing Ranker with Parameters lambda=.7
    jeline_mercer_p1 = metapy.index.JelinekMercer(.7)
    ev6 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = jeline_mercer_p1.score(idx, query, top_k)                            
            avg_p = ev6.avg_p(results, query_start + query_num, top_k)
    data.append(['JelineK-Mercer','NA','NA','NA','NA', '.7','NA', round(ev6.map(),2)])

    #JelineK-Mercer Smoothing Ranker with Parameters lambda=.5
    jeline_mercer_p2 = metapy.index.JelinekMercer(.5)
    ev7 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = jeline_mercer_p2.score(idx, query, top_k)                            
            avg_p = ev7.avg_p(results, query_start + query_num, top_k)
    data.append(['JelineK-Mercer','NA','NA','NA','NA', '.5','NA', round(ev7.map(),2)])

    #JelineK-Mercer Smoothing Ranker with Parameters lambda=.85
    jeline_mercer_p3 = metapy.index.JelinekMercer(.85)
    ev8 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = jeline_mercer_p2.score(idx, query, top_k)                            
            avg_p = ev8.avg_p(results, query_start + query_num, top_k)
    data.append(['JelineK-Mercer','NA','NA','NA','NA', '.85','NA', round(ev8.map(),2)])

    #Dirichlet Prior Ranker with Parameters lambda=2000
    dirichlet_prior_p1 = metapy.index.DirichletPrior(2000)
    ev9 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = dirichlet_prior_p1.score(idx, query, top_k)                            
            avg_p = ev9.avg_p(results, query_start + query_num, top_k)
    data.append(['Dirichlet Prior','NA','NA','NA','NA', 'NA','2000', round(ev9.map(),2)])

    #Dirichlet Prior Ranker with Parameters lambda=1500
    dirichlet_prior_p2 = metapy.index.DirichletPrior(1500)
    ev10 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = dirichlet_prior_p1.score(idx, query, top_k)                            
            avg_p = ev10.avg_p(results, query_start + query_num, top_k)
    data.append(['Dirichlet Prior','NA','NA','NA','NA', 'NA','1500', round(ev10.map(),2)])

    #Dirichlet Prior Ranker with Parameters lambda=3500
    dirichlet_prior_p3 = metapy.index.DirichletPrior(3500)
    ev11 = metapy.index.IREval(cfg)
    
    with open('CampusWireHeading_Queries.txt') as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = dirichlet_prior_p1.score(idx, query, top_k)                            
            avg_p = ev11.avg_p(results, query_start + query_num, top_k)
    data.append(['Dirichlet Prior','NA','NA','NA','NA', 'NA','3500', round(ev11.map(),2)])

    EvaluationDF = pd.DataFrame(data, columns=['Ranker','k1','b','k3','s','lambda','mu','MAP'])
    print(EvaluationDF)

    