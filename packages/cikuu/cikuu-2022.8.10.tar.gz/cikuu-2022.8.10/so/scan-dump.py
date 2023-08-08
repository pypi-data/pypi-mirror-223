# 2023.8.1  python -m cikuu.pypi.so.dump gzjc 
import traceback,sys , fire,os,json,time
from elasticsearch import Elasticsearch,helpers

def run(index,  type:str=None, suffix:str='es-jsonl', eshost:str='es.jukuu.com:9200'):
	'''  '''
	outfile = f"{index}.{suffix}" if type is None else f"{index}.type-{type}.{suffix}"
	print ('[dump] start to walk:', index, outfile, eshost, flush=True)
	start = time.time()
	es	= Elasticsearch([ f"http://{eshost}" ])   # {'_index': 'nju2020', '_type': '_doc', '_id': 'doc-8697:snt-0:tok-15', '_score': None, '_source': {'level': 'gsl1', 'i': 15, 'idf': 2.6, 'type': 'tok', 'rid': 10, 'dep': 'conj', 'govlem': 'be', 'govpos': 'VERB', 'uid': 3544545, 'lem': 'have', 'pos': 'VERB', 'tag': 'VBZ', 'sntid': 'doc-8697:snt-0', 'did': 8697, 'lex': 'has'}, 'sort': [32]}
	with open( outfile, 'w') as fw:
		q = {"match_all" : {}} if type is None else {"match" : {"type":type}}
		for doc in helpers.scan(client=es, query={"query" : q }, index=index): 
			try:
				doc.pop('_score', None)
				doc.pop('sort', None) 
				fw.write( json.dumps(doc) + "\n" )
			except Exception as ex:
				print(">>eswalk ex:", ex)
	print ('finished dump:', index, outfile, " |tim=", round(time.time() - start, 2),  flush=True)

if __name__ == '__main__':
	fire.Fire(run)