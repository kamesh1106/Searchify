

import elasticsearch
import sys
import os


def usage1():
    sys.exit('Usage : python ' + sys.argv[0] + ' filename author title ')
'''
if(len(sys.argv) != 4):
    print('hi')
    print(str(len(sys.argv)) + ' args provided')
    usage1()
'''
fileName = sys.argv[1]
author = sys.argv[2]
title = sys.argv[3]
query = sys.argv[4]

if os.path.isfile(fileName) is False:
    print('File not found: ' + fileName)
    usage1()

es = elasticsearch.Elasticsearch()

book = open(fileName)
lineNum = 0
txtNum = 0

try:
    for lineText in book:
        lineNum += 1
        if len(lineText) > 0:
            txtNum += 1
            es.index(index=author, doc_type=title, id=txtNum, body = {'lineNum': lineNum,'text': lineText})
except UnicodeDecodeError as e:
    print("Decode error at: " + str(lineNum) + ':' + str(txtNum))
    print(e)

book.close()
print(es.get(index=author, doc_type=title, id=txtNum))



def usage2():
    sys.exit('Usage: ' + sys.argv[0] + '   [num results]')


numArgs = len(sys.argv)
if numArgs < 3:
    print(str(len(sys.argv)) + ' args provided')
    usage2()
'''
author = sys.argv[1]
query = sys.argv[2]

print(author,query)
if numArgs == 4:
    numResults = sys.argv[3]
else:
    numResults = 10
'''
#es = elasticsearch.Elasticsearch()
numResults = 10
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