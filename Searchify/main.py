from flask import Flask, render_template, request, redirect, url_for, flash, session
from forms import EntryForm, SearchForm
from werkzeug import secure_filename
from myclass import es
import elasticsearch

app = Flask(__name__)
res = []

app.config['SECRET_KEY'] = 'f5a117a3ab54a2f5476857b652a0c8a6'

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
	form = EntryForm()
	if(form.validate_on_submit()):
		#filename = secure_filename(form.filepath.data.filename)
		print(form.filename.data, form.index.data)
		session['filename'] = form.filename.data
		session['index'] = form.index.data
		#session['title'] = form.title.data
		#form.filename.data.save('uploads/'+form.filename.data)
		return redirect(url_for('output'))
	return render_template('index.html', form=form)


@app.route('/output', methods = ['GET', 'POST'])
def output():
	if(('filename' in session) and ('index' in session)):
		filename = session['filename']
		author = session['index']
		#title = session['title']

		print(filename)
		#es = elasticsearch.Elasticsearch()
		book = open(filename)
		lineNum = 0
		txtNum = 0

		try:
		    for lineText in book:
		        lineNum += 1
		        if len(lineText) > 0:
		            txtNum += 1
		            es.index(index=author, id=txtNum, body = {'lineNum': lineNum,'text': lineText})
		except UnicodeDecodeError as e:
		    print("Decode error at: " + str(lineNum) + ':' + str(txtNum))
		    print(e)
		    book.close()
		print(es.get(index=author, id=txtNum))

	return redirect(url_for('index'))


@app.route('/search', methods = ['GET', 'POST'])
def search():
	form = SearchForm()
	res = []
	if(form.validate_on_submit()):
		author = request.form['index']
		query = request.form['query']
		numResults = 10
		es = elasticsearch.Elasticsearch()


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
		            previousLine = es.get(index=author,id=lineNum-1)
		        nextLine = es.get(index=author, id=lineNum+1)
		        res.append(title + ': ' + str(lineNum) + ' (' + str(score) + '): ')
		        res.append(previousLine['_source']['text'] + text + nextLine['_source']['text'])
		else:
		    print('No results')
	print(form)
	return render_template('search.html', form=form, res=res)

if(__name__ == '__main__'):
	app.run(debug=True)