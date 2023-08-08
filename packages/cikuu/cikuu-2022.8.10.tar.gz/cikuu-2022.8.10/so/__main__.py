# 2023.5.1  .# 2022-2-13  cp from cikuu/bin/es.py 
import so, requests,time,os, fire

def add(infile, idxname="testdoc", taglist:str=None):
	''' add doc only , 2023.5.1 '''
	so.check(idxname)
	start = time.time()
	text = open(infile, 'r').read().strip() 
	did	 = so.md5(text)
	requests.es.index(index=idxname, body={"did": f"doc-{did}", "doc":text,  "filename": infile, 'type':'doc', 'tags':[] if taglist is None else taglist.strip().split(',') if isinstance(taglist, str) else taglist }, id = f"doc-{did}")
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

def addfolder(folder:str, idxname:str=None, pattern:str=".txt"): 
	''' folder -> esindex '''
	if idxname is None : idxname=  folder
	print("addfolder started:", folder, idxname, requests.es, flush=True)
	for root, dirs, files in os.walk(folder):
		for file in files: 
			if file.endswith(pattern):
				add(f"{folder}/{file}", idxname = idxname, taglist=folder) 
				print (f"{folder}/{file}", flush=True)
	print("addfolder finished:", folder, idxname, requests.es, flush=True)

def init(idxname):
	''' init a new index '''
	if requests.es.indices.exists(index=idxname):requests.es.indices.delete(index=idxname)
	requests.es.indices.create(index=idxname, body=so.config) #, body=snt_mapping
	print(">>finished " + idxname )

def drop(idxname): 
	''' drop a index ''' 
	print ( requests.es.indices.delete(index=idxname) )

def dump(index, host:str='172.17.0.1', port:int=9200, batch:int=10000):  #sudo npm install elasticdump -g | https://github.com/elasticsearch-dump/elasticsearch-dump
	''' elasticdump --input=http://172.17.0.1:9200/clec --output=clec.esdump --type=data --limit 10000  '''
	os.system(f"elasticdump --input=http://{host}:{port}/{index} --output={index}.esdump --type=data --limit {batch} ")

def restore(infile, index:str=None, host:str='172.17.0.1', port:int=9200, batch:int=10000):  #{"_index":"clec","_type":"_doc","_id":"snt-146:tok-8","_score":1,"_source":{"gtag":"VB","lem":"!","pos":"PUNCT","i":8,"tag":".","type":"tok","glem":"imagine","gpos":"VERB","did":"snt-146","lex":"!","dep":"punct"}}
	''' elasticdump --input=clec.esdump --output=http://172.17.0.1:9200 --type=data --limit 10000  '''
	if index is None : index = infile.split('/')[1].split('.')[0] 
	init(index) 
	os.system(f"elasticdump --input={infile} --output=http://{host}:{port} --type=data --limit {batch} ")

if __name__ == '__main__':
	fire.Fire()

'''
1. ubuntu@dicvec-scivec-jukuu-com-flair-64-245:~/cikuu/pypi/so$ python __main__.py addfolder inaugural
2. ubuntu@dicvec-scivec-jukuu-com-flair-64-245:~/cikuu/pypi/so$ python sntbr.py inaugural
58
sntbr indexing finished: inaugural, 	| using:  54.86855387687683

python sntbr.py inaugural --debug true --postag true

POST /policy_document/policy_document/222/_update
{
  "doc": {
    "tags":["VIP"]
  }
}

  es.update( # excpetion here 
            index=log['_index'],
            doc_type='_doc',
            id=log['_id'],
            body={'doc':log['_source']} # 
        )

ubuntu@dicvec-scivec-jukuu-com-flair-64-245:~/cikuu/pypi/so/inaugural$ find . -name "*.txt" -exec python ../__main__.py add {} --taglist inau \;
'''