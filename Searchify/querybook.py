import elasticsearch
import sys
import json
from loadbook import es

def usage2():
    sys.exit('Usage: ' + sys.argv[0] + '   [num results]')


numArgs = len(sys.argv)
if numArgs < 3:
    print(str(len(sys.argv)) + ' args provided')
    usage2()
author = sys.argv[1]
query = sys.argv[2]
print(author,query)
if numArgs == 4:
    numResults = sys.argv[3]
else:
    numResults = 10
    
#es = elasticsearch.Elasticsearch()
print(es)
results = es.search(
    index=author,
    body={
        "size": numResults,
        "query": {"match": {"text": {"query": query}}}})

print(results)

hitCount = results['hits']['total']['value']
print(hitCount)
if hitCount > 0:
    if hitCount is 1:
        print(str(hitCount) + ' result')
    else:
        print(str(hitCount) + ' results')
    
    for hit in results['hits']['hits']:
        text = hit['_source']['text']
        lineNum = hit['_source']['lineNum']
        score = hit['_score']
        title = hit['_type']
        if lineNum > 1:
            previousLine = es.get(index=author, doc_type=title, id=lineNum-1)
        nextLine = es.get(index=author, doc_type=title, id=lineNum+1)
        print(title + ': ' + str(lineNum) + ' (' + str(score) + '): ')
        print(previousLine['_source']['text'] + text + nextLine['_source']['text'])
else:
    print('No results')