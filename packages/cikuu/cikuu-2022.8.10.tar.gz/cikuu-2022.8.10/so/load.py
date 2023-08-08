# 2022.8.30 , pure load _source | {"_index": "gzjc", "_type": "_doc", "_id": "2897-stype", "_source": {"src": 2897, "tag": "simple_snt", "type": "stype"}}
import json,fire,sys, os, time ,  fileinput #, so
from elasticsearch import Elasticsearch,helpers
from cikuu.pypi import so

def run(infile, index:str=None, batch=200000, refresh:bool=True, eshost='es.jukuu.com:9200', overwrite_index:bool=False):  # in local, set it to 127.0.0.1:9200
	''' python3 -m cikuu.pypi.so.load gzjc.esdump.gz '''
	start = time.time()
	es	  = Elasticsearch([ f"http://{eshost}" ])  
	if index is None : index = infile.split('.')[0]
	print(">>load started: " , infile, index, ',refresh=', refresh, ' ,eshost=', eshost, ' ,batch=', batch, flush=True )
	if refresh or not es.indices.exists(index=index): 
		if es.indices.exists(index=index):es.indices.delete(index=index)
		es.indices.create(index=index, body=so.config) #, body=snt_mapping

	actions=[]
	for line in fileinput.input(infile,openhook=fileinput.hook_compressed): 
		try:
			arr = json.loads(line.strip())
			arr.update({'_op_type':'index', '_index':index}) #overwrite_index
			actions.append( arr )

			if len(actions) >= batch: 
				helpers.bulk(client=es,actions=actions, raise_on_error=False)
				print ( actions[-1], flush=True)
				actions = []
		except Exception as e:
			print("ex:", e)	
	if actions : helpers.bulk(client=es,actions=actions, raise_on_error=False)
	print(">>python -m cikuu.pypi.so.load finished:" , infile, index , ' using:', round(time.time() - start,2))

if __name__ == '__main__':
	fire.Fire(run)

'''
GET /index_*/_search
GET /index_01,index_02/_search
python -m cikuu.pypi.so.load gzjc.esdump --eshost es.jukuu.com

'''