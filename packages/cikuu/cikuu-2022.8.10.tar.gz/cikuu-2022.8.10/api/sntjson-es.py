# 2023.1.7, cp from esjson.py 
import json, traceback,sys, time,  fileinput, os, en, so, fire
from collections import Counter
from elasticsearch import Elasticsearch,helpers

def run(infile, index:str=None, batch=200000, refresh:bool=True, host='172.17.0.1',port=9200): 
	''' python3 -m api.sntjson-es gzjc.jsonlg.3.4.1.gz'''
	es	  = Elasticsearch([ f"http://{host}:{port}" ])  
	if index is None : index = infile.split('.')[0]
	print(f">>load started: host={host}, index={index} " , infile, index, flush=True )
	if refresh or not es.indices.exists(index=index): 
		if es.indices.exists(index=index):es.indices.delete(index=index)
		es.indices.create(index=index, body=so.config) 

	actions=[]
	for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): 
		try:
			doc = Doc(spacy.nlp.vocab).from_json(json.loads(line.strip())) # add skenp 
			for t in doc: #"src": doc.text, 
				source = {"type":"tok", "id": f"{sid}-tok-{t.i}", "sid":sid, 'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_ , "gtag":t.head.tag_ }
				actions.append( {'_op_type':'index', '_index':index, '_id': source['id'], '_source': source } )
			for sp in doc.noun_chunks:
				source = {"type":"NP", "id": f"{sid}-NP-{sp.start}", "sid":sid, 'chunk':sp.text, 'lem':doc[sp.end-1].lemma_ }
				actions.append( {'_op_type':'index', '_index':index, '_id': source['id'], '_source': source } )
			for lem, pos, type, chunk in en.kp_matcher(doc): #brink:NOUN:pp:on the brink # [('pp', 'on the brink', 2, 5), ('ap', 'very happy', 9, 11)]
				source = {"type":type, "id": f"{sid}-{type}-{chunk}", "sid":sid,  'chunk':chunk, 'lem':lem , "pos":pos} #"src": doc.text,
				actions.append( {'_op_type':'index', '_index':index, '_id': source['id'], '_source': source } )

			for name, ar in en.depmatch()(doc) : 
				type = spacy.nlp.vocab[name].text # worry be thrilled
				lem = doc[ar[0]].lemma_
				source = {"type":type, "id": f"{sid}-{type}-{lem}", "sid":sid,  'lem':lem,  'tag':doc[ar[0]].tag_, 'lem1':doc[ar[1]].lemma_, 'lem2':doc[ar[2]].lemma_ , 'tag1':doc[ar[1]].tag_ , 'tag2':doc[ar[2]].tag_ } 
				actions.append( {'_op_type':'index', '_index':index, '_id': source['id'], '_source': source } )

			# merged NP must be finally called 
			actions.append( {'_op_type':'index', '_index':index, '_id': sid, '_source': {'type':'snt',  "sid":sid,  'snt':doc.text, 'postag': en.es_postag(doc), 'tc': len(doc), 'skenp': en.es_skenp(doc) } } ) #, 'kps': en.kps(doc)
			if len(actions) >= batch: 
				helpers.bulk(client=es,actions=actions, raise_on_error=False)
				print ( actions[-1], flush=True)
				actions = []
		except Exception as e:
			print("ex:", e, sid, line)	
			exc_type, exc_value, exc_obj = sys.exc_info() 	
			traceback.print_tb(exc_obj)

	if actions : helpers.bulk(client=es,actions=actions, raise_on_error=False)
	print(">>load finished:" , infile, index )

if __name__	== '__main__':
	fire.Fire(run)