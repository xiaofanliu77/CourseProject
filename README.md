# CS410 Project Documentation
Xiaofan Liu / Boyu Pang / Brittany West

## Introduction 

Our project is called “Campuswire and Coursera Query Link”, which falls under the “Intelligent Browsing” theme. We developed a program that gives users relevant information from Coursera related to questions that are posted on Campuswire. This program facilitates the learning process by providing relevant ranked documents from Coursera to the user, which reduces the quantity of repeated questions on Campuswire that could quickly crowd out other questions/answers. 

## Using the software

To use the software, the user can simply run the main function in search.py. The user will be prompted to provide a query of their choice, as well as a ranking function from a defined set of choices. When both of these are provided, the program will output the top 10 documents that best matched the user query, with the relevant terms highlighted.

Note that by default, Okapi BM25 is used as the ranking function. Furthermore, to reduce complexity for the user, all ranking functions by default are initialized with the best set of parameters as decided in ModelEvaluation.py.

You can also run the code in evaluation.py to see how various scoring functions perform on a predetermined query set, defined in CampusWireHeading_Queries.txt. This is a set of 15 queries that we scraped from the Fall 2021 CS410 Campuswire page, for which we manually determined query relevance judgments (which can be found in qrels.txt). The output is a table that shows the parameters, the Mean Average Precision (MAP), and NDCG for four different types of ranking functions evaluated on CampusWireHeading_Queries.txt.

## Files

Here we will give a brief description of the main files in the repo:

DataCleaning.py
- The python file used to parse the raw data and create documents.txt

config.toml
- The config file specifying how the index should be built

documents.txt
- The text file used to create the reverse index, generated from DataCleaning.py

CampusWireHeading_Queries.txt
- A text file of queries selected from this semester’s (Fall 2021) Campuswire posts

qrels.txt
- Manually curated relevance judgments for each of the queries in CampusWireHeading_Queries.txt

ModelEvaluation.py
- The python file used to evaluate different ranking algorithms and parameters. It reads in CampusWireHeading_Queries.txt and scores the results from running the queries using MAP (Mean Average Precision) and NDCG for the following ranking functions: Okapi BM25, Pivoted Length Normalization, Jelinek-Mercer, and Dirichlet Prior.

search.py
- The main python file that the user interacts with. The user provides a query and ranking function, and the top results are printed to the screen with relevant terms highlighted.

## Code Implementation 

First we used Coursera Downloader, an open-source tool for downloading data from Coursera courses one subscribes to, to collect data from the CS410 Fall 2021 course. The dataset mainly consists of lecture transcripts (txt files) and course-related instructional materials (html files).

The downloaded data was first examined and filtered manually to leave only the most relevant data for the purpose of this query link project. For example, transcripts in languages other than English or html files that do not contain useful course-related information were removed. Next, we converted all documents into a single .txt file (Documents.txt), within which each line represents one document. This was accomplished by the code in DataCleaning.py. Transcript documents were further cleaned with code written to remove irrelevant words such as [NOISE] or [SOUND]. The html2text library was helpful in translating html files into text documents. 

In the meantime, we each collected 5 real queries from Campuswire posted by students in the course, a total of 15 queries as the training set. This information was documented in the CampusWireHeading_Queries.txt file. With the queries and dataset, we then generated the qrels.txt file by manually going through each query and giving values of relevance (from 1 to 4, 1 being somewhat relevant to 4, very relevant) for top 5 - 10 relevant documents. 

Next, we explored how various ranking functions perform on the collected 15 queries. This was done in the ModelEvaluation.py file. 3 ranking functions were tested: Okapi BM25, JelinekMercer and Dirichlet Prior, each with various parameter settings. We found out that Okapi BM25 almost consistently yielded the best results among all three ranking functions. So that is the default ranking function we are utilizing in the next step.

Finally, the search and ranking program was implemented in the search.py file. The first block of code in this file, the “print_with_highlight” function is a helper function for presenting data to the user in a more succinct and meaningful way. This is further explained in the “Function Reference” section of this document. 

In the main section of the search.py file, we first set up the configuration for metapy processing by importing “config.toml” (code below) which contains instructions for index building, such as the query files, type of analyzers and so forth.
```
cfg = "config.toml"
with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)
```
Next, we created a metapy index which is going to be the foundation for further analysis.
```
idx = metapy.index.make_inverted_index(cfg)
```
The next block of code is to achieve interaction with users. This is further explained in the “Using the Software” section of this document. The following code generates the top results based on the query and ranking functions the user has specified.
```
#Assume OkapiBM25 is used as the ranking function
ranker = metapy.index.OkapiBM25(k1=1.2, b=.75, k3=500)
top_docs = ranker.score(idx, query, num_results=10)
```
However, top_docs is merely a series of document ids and their scores that are not exactly what a user is looking for. So the last block of code loops through the top 10 results and outputs the document content in a truncated form with keywords highlighted.
```
for num, (d_id, _) in enumerate(top_docs):
        content = idx.metadata(d_id).get('content')
        if content is not None:
            print_with_highlight(content, query_text, 5, num+1)
```
## Packages Needed
Coursera downloader was used to scrape CS410 course data from Coursera website. Html2text was used to convert html webpage files to plain text documents. Numpy and pytoml were used in the search.py file to accomplish document searching and ranking functions. Below is a list of them and their official page links.

- Coursera-dl https://github.com/coursera-dl/coursera-dl 
- Html2text https://pypi.org/project/html2text/ 
- Numpy https://numpy.org/ 
- Pytoml https://pypi.org/project/pytoml/0.1.14/ 

## Function Reference
```
print_with_highlight(doc, query, k, doc_id = None)
```
Prints out a truncated version of doc containing the first k occurrences of the non-stopword terms in query. If doc_id is provided, the printed content is prefixed with the doc_id. The highlighting was implemented as in this stackoverflow post: https://stackoverflow.com/questions/68200973/highlight-multiple-substrings-in-a-string-in-python

### Parameters:
doc: the content of the document to be printed (string)
query: the query for the document (string)
k: the number of highlights occurrences of query terms to include in the output (int)
doc_id: the document id (int, optional_

### Returns:
None


## Team Contributions:

As a team of three we equally contributed to the list of tasks below:
Brainstorming and team meetings (5 hours)
Scraping and Data cleaning, including structuring and cleaning the coursera documents, gathering queries to test our ranking function (10 hours)
Researching, implementing, fine tuning ranking functions (20 hours)
Testing ranking functions and improving them (10 hours)
Documenting code and writing project updates (5 hours)
Preparing and creating presentation (10 hours)

Total hours : 60


