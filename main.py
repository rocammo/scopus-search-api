import requests
import json

from progress.bar import IncrementalBar
from scopus import SCOPUS_API_KEY


def filter_by_quality_indicator(document_results=None):
    results = document_results if document_results != None else json.load(
        open("document_results.json"))
    qi = json.load(open("quality-indicator.json"))

    print("\n\033[4mStep 2\033[0m")
    bar = IncrementalBar("Filtering", max=len(results))

    document_results_filtered = {}
    for key, result in results.items():
        bar.next()
        for _, source in qi.items():
            if source in result["source"]:
                document_results_filtered[key] = result
                continue

    bar.finish()

    with open("results/document-results-filtered_%d.json" % len(results), 'w', encoding="utf-8") as output_stream:
        json.dump(document_results_filtered, output_stream,
                  ensure_ascii=False, indent=4)


def scopus_query(query, document_results_limit=None):
    print("\n\033[4mQuery\033[0m\n%s" % query)

    items_per_page = 25
    start_index = items_per_page

    scopus_author_search_url = "https://api.elsevier.com/content/search/scopus?"
    headers = {"Accept": "application/json", "X-ELS-APIKey": SCOPUS_API_KEY}
    search_query = 'query=%s' % (query)

    total_results = None
    if document_results_limit != None:
        remainder = document_results_limit % items_per_page
        total_results = document_results_limit + (items_per_page - remainder)
    else:
        request = requests.get(scopus_author_search_url +
                               search_query, headers=headers)
        response = json.loads(request.content.decode("utf-8"))
        total_results = int(
            response["search-results"]["opensearch:totalResults"])

    document_results = {}
    print("\n\033[4mStep 1\033[0m")
    bar = IncrementalBar("Indexing", max=total_results)

    for i in range((total_results + (items_per_page - 1)) // items_per_page):
        request = requests.get(
            scopus_author_search_url + search_query + '&start=' + str(start_index * i), headers=headers)
        response = json.loads(request.content.decode("utf-8"))
        for j in range(len(response["search-results"]["entry"])):
            title = response["search-results"]["entry"][j]["dc:title"]
            source = response["search-results"]["entry"][j]["prism:publicationName"]
            # year = int(''.join(filter(
            #     str.isdigit, response["search-results"]["entry"][j]["prism:coverDisplayDate"]))[-4:])

            document_results[start_index * i + j +
                             1] = dict(title=title, source=source)
            bar.next()

    bar.finish()

    with open("results/document-results_%d.json" % total_results, 'w', encoding="utf-8") as output_stream:
        json.dump(document_results, output_stream,
                  ensure_ascii=False, indent=4)

    filter_by_quality_indicator(document_results)


if __name__ == "__main__":
    queries = {4: 'TITLE-ABS-KEY("Program Synthesis") AND TITLE-ABS-KEY("Model Driven Development" OR "MDD") AND SUBJAREA(COMP)',
               9: 'TITLE-ABS-KEY("Program Synthesis") AND TITLE-ABS-KEY("Model Driven Engineering" OR "MDE" OR "Model Driven Development" OR "MDD") AND SUBJAREA(COMP)',
               95: 'TITLE-ABS-KEY("Program Synthesis" OR "Synthesis") AND TITLE-ABS-KEY("Model Driven Development" OR "MDD") AND SUBJAREA(COMP)',
               197: 'TITLE-ABS-KEY("Synthesis") AND TITLE-ABS-KEY("Model Driven Engineering" OR "MDE" OR "Model Driven Development" OR "MDD") AND SUBJAREA(COMP)',
               340: 'TITLE-ABS-KEY("Program Synthesis") AND TITLE-ABS-KEY("Model Driven Engineering" OR "MDE" OR "Model Driven Development" OR "MDD" OR "Model") AND SUBJAREA(COMP)'}

    for _, query in queries.items():
        scopus_query(query=query)

    # scopus_query(
    #     query='TITLE-ABS-KEY("Program Synthesis" OR "Synthesis") AND TITLE-ABS-KEY("Model Driven Development" OR "MDD") AND SUBJAREA(COMP)',
    #     document_results_limit=23
    # )
