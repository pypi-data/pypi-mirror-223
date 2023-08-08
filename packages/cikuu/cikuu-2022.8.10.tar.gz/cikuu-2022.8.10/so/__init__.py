# 2022.5.11 updated , add sqlrow for EachRowJson
# 2022.2.13 created 
import requests,json, os, math,re,traceback,fire,time,sys,hashlib
from elasticsearch import Elasticsearch,helpers
from collections import	defaultdict, Counter
import warnings #import pandas as pd # remove dependency 2023.4.7
warnings.filterwarnings("ignore")

if not hasattr(requests, 'eshost'): # or use: so.eshost ?
	requests.eshost	= os.getenv("eshost", "172.17.0.1:9200" if 'linux' in sys.platform else 'es.jukuu.com:9200') 
	requests.es		= Elasticsearch([ f"http://{requests.eshost}" ])  

config = {  
		"settings" : {
			"refresh_interval": "1s",
			"number_of_shards": "3",
			"max_result_window":"2147483647",
			"index.mapping.ignore_malformed": "true",
			#"xpack.security.enabled": "false", # added 2023.5.22 
			#"index.codec" : "best_compression", # added 2022.8.21
			"analysis": {
			  "filter": {
				"postag_filter": {
				  "type": "pattern_capture",   # add _contact_VERB as a term , => _contact_VERB with  ( _([a-z]+)_(VERB|NOUN|ADJ|ADV)
				  "preserve_original": "false",
				  "patterns": [
					#"(^([^_]+)_[a-z]+[,\\.$]?)",  
					"(^[^_]+)",   # first lex
					"(_[a-z]+_[VERB|NOUN|ADJ|ADV]+)", # lex_tag_lem_pos , _contact_VERB (VERB|NOUN|ADJ|ADV)
					"(_[a-z]+_VERB_[VBD|VBP|VBG|VBZ|VB]+_)",  # except VBN, 2023.3.20
					"(_[a-z]+_VERB_VBN_)", 
					#"(_[a-zA-Z\\-\\.\\'\\$0-9]+)$",  # remove _NP5,  _NP5 => _NP 
					"(_[a-zA-Z,\\-\\.\\'\\$\\*]+)",  # _^ _ADJ _, _NOUN _VERB , _open/VERB 
					#"(_[^\\w]+)_",
					#"([^\\w])_"
				  ]
				},
				"postag_filter1": {
					  "type": "pattern_replace",
					  "pattern": "(^_([a-z]+)_([VERB|NOUN|ADJ|ADV]))",
					  "replacement": "$2/$3",  # _open_VERB => open/VERB
					  "all": False
					},
				"postag_filterV": {
					  "type": "pattern_replace",
					  "pattern": "(^_([a-z]+)(_VERB_[VBD|VBP|VBG|VBZ|VB]+)_)",
					  "replacement": "$2/V",  # _open_VERB_VBD => open/V
					  "all": False
					},
				"postag_filterVBN": {
					  "type": "pattern_replace",
					  "pattern": "(^_([a-z]+)(_VERB_VBN)_)",
					  "replacement": "$2/VBN",  # _open_VERB_VBN => open/VBN
					  "all": False
					},
				"postag_filter2": {
				  "type": "word_delimiter",
				  "type_table": [
					"^ => ALPHA",
					", => ALPHA",
					"$ => ALPHA",
					"* => ALPHA",
					"/ => ALPHA",
					"_ => ALPHA",
					". => ALPHA",
					"- => ALPHA",
					"! => ALPHA",
					"? => ALPHA",
					"' => ALPHA",
					"0 => ALPHA",
					"1 => ALPHA",
					"2 => ALPHA",
					"3 => ALPHA",
					"4 => ALPHA",
					"5 => ALPHA",
					"6 => ALPHA",
					"7 => ALPHA",
					"8 => ALPHA",
					"9 => ALPHA"
				  ]
				},
				"unique_filter": {
				  "type": "unique",
				  "only_on_same_position": "true"
				}
			  },
			  "analyzer": {
				"postag_ana": {"filter": ["postag_filter", "postag_filterV", "postag_filterVBN", "postag_filter1",  "postag_filter2", "unique_filter"], "type": "custom", "tokenizer": "whitespace" }, #"lowercase",
				"path_ana": {"type": "custom", "tokenizer": "path-tokenizer"},
				"path_ana3": {"type": "custom", "tokenizer": "path-tokenizer3"},
				"feedback_ana": {"type": "custom", "tokenizer": "feedback-tokenizer"},
				"err_ana": {"type": "custom",  "tokenizer": "path-tokenizer1"  },
				"chunk_ana": {"type": "custom", "tokenizer": "path-tokenizer2" },
				"kp_ana": { "filter": ["lowercase"], "type": "custom", "tokenizer": "keyword"}
			  },
			  "tokenizer": {
				"path-tokenizer": { "type": "path_hierarchy",  "delimiter": "/" },
				"path-tokenizer1": {"type": "path_hierarchy",  "delimiter": "|" },
				"path-tokenizer2": {"type": "path_hierarchy",  "delimiter": "/" },
				"path-tokenizer3": {"type": "path_hierarchy",  "delimiter": ":" },
				"feedback-tokenizer": { "type": "path_hierarchy",  "delimiter": "." }
				}
			},
			"number_of_replicas": "0"
		},
		"mappings" : {
			"_source": {"excludes": ["md5"]},
			"properties": {
			 "@timestamp":{"format":"strict_date_optional_time||epoch_millis", "type":"date"},
			 "ddate":{"type": "date", "format": "strict_date_optional_time||yyyy-MM-dd HH:mm:ss||epoch_millis"}, 
			"errs": { "type": "text", "analyzer": "path_ana" ,"fielddata":"true" },
			"feedback": { "type": "text", "analyzer": "feedback_ana" ,"fielddata":"true" },
			"kps": { "type": "text", "analyzer": "path_ana3" ,"fielddata":"true" },
			"pterm": { "type": "text", "analyzer": "path_ana"  }, # path term
			"postag": { "type": "text", "analyzer": "postag_ana"},
			"skenp": { "type": "text", "analyzer": "postag_ana"},
			"skecl": { "type": "text", "analyzer": "postag_ana"}, # added 2023.7.23
			"hyb": { "type": "text", "analyzer": "postag_ana"}, # 2023.3.16
			"sentgram": { "type": "text", "analyzer": "postag_ana","fielddata":"true"}, # simple_complex_headpp compound_question_itis_svo
			"np": { "type": "text", "analyzer": "postag_ana","fielddata":"true"},
			"ske": { "type": "text", "analyzer": "postag_ana","fielddata":"true"},
			"i": { "type": "integer", "index": "false"},
			"start": { "type": "integer", "index": "false"},
			"end": { "type": "integer", "index": "false"},
			"head": { "type": "integer", "index": "false"},
			"score": { "type": "float"},
			"idf": { "type": "float"},
			"ratio": { "type": "float", "index": "false"},
			"memo": { "type": "keyword", "index": "false"}, # to store some memo info, for show only
			"sent": { "type": "keyword", "index": "false"},
			"offset": { "type": "float"},
			"final_score": { "type": "float"},
			"sid": { "type": "keyword"},
			"sntid": { "type": "keyword"},
			"level": { "type": "keyword"},  # awl,gsl1,gsl2
			"pid": { "type": "keyword"}, # parentid 
			"paraid": { "type": "keyword"}, # paragraph
			"id": { "type": "keyword"},
			"adp": { "type": "keyword"},
			"ap": { "type": "keyword"},
			"date": { "type": "keyword"},
			"page": { "type": "keyword"},
			"rid": { "type": "keyword"},
			"did": { "type": "keyword"}, # update keyword -> integer,  in didlist 
			"didver": { "type": "float"},
			"vpat": { "type": "keyword"},
			"ibeg": { "type": "integer"},
			"iend": { "type": "integer"},
			"len": { "type": "integer"}, # [start, start + len) 
			"docid": { "type": "keyword"},
			"uid": { "type": "keyword"},
			"eid": { "type": "keyword"},
			"sntnum": { "type": "integer"},
			"wordnum": { "type": "integer"},
			"awl": { "type": "float"},
			"ttr1": { "type": "float"},
			"word_diff_avg": { "type": "float"},
			"ast": { "type": "float"},
			"cl_ratio": { "type": "float"},
			"doc_tc": { "type": "float"},
			"para_num": { "type": "float"},
			"spell_correct_ratio": { "type": "float"},
			"grammar_correct_ri": { "type": "float"},
			"cnt": { "type": "long"},
			"vers": { "type": "integer"},
			"ver": { "type": "integer"},
			"ct": { "type": "integer"},
			"lem": { "type": "keyword"},
			"frame": { "type": "keyword"}, # flair/frame 
			"lempos": { "type": "keyword"}, # for wordattr , ie: open/VERB 
			"lex": { "type": "keyword"},
			"word": { "type": "keyword"},
			"low": { "type": "keyword"},
			"pos": { "type": "keyword"},
			"tag": { "type": "keyword"},
			"tags": { "type": "keyword"},
			"ctag": { "type": "keyword"}, # chunk tag
			"stag": { "type": "keyword"}, # snt tag
			"term": { "type": "keyword"},
			"gpos": { "type": "keyword"},  "glem": { "type": "keyword"}, "gtag": { "type": "keyword"},
			"lem1": { "type": "keyword"},  "lem2": { "type": "keyword"}, "tag1": { "type": "keyword"}, "tag2": { "type": "keyword"},
			"VERB": { "type": "keyword"},  "NOUN": { "type": "keyword"}, "ADV": { "type": "keyword"},  "ADJ": { "type": "keyword"},
			"advcl": { "type": "keyword"},  "acomp": { "type": "keyword"}, "dobj": { "type": "keyword"},  "nsubj": { "type": "keyword"},"xcomp": { "type": "keyword"},  "amod": { "type": "keyword"},  "advmod": { "type": "keyword"},
			"frame": { "type": "keyword"},
			"stype": { "type": "keyword"},
			"page": { "type": "keyword"},
			"pen": { "type": "keyword"},
			"label": { "type": "keyword"},
			"item": { "type": "keyword"},
			"lang": { "type": "keyword"},
			"key": { "type": "keyword"},
			"s": { "type": "keyword"},
			"item_key": { "type": "keyword"},
			"score": { "type": "float"},
			"tmf": { "type": "float"},
			"url": { "type": "keyword", "index": "false"},
			"tms": { "type": "keyword", "index": "false"},
			"stroke": { "type": "keyword", "index": "false"},
			"strokes": { "type": "keyword", "index": "false"},
			"text": { "type": "keyword", "index": "false"},
			"doc_txt": { "type": "keyword", "index": "false"}, # spider 
			"essay_or_snts": { "type": "keyword", "index": "false"},
			"labels": { "type": "keyword"}, # for annotation 
			"_snt": { "type": "keyword", "index": "false"},
			"_ske": { "type": "keyword", "index": "false"},
			"en": { "type": "text", "analyzer": "standard","fielddata":"true"},
			"content": { "type": "text", "analyzer": "standard","fielddata":"true"},
			"zhseg": { "type": "text", "analyzer": "standard"},
			"zh": { "type": "text", "index": "false"},
			"src": { "type": "keyword"},
			"srcsnt": { "type": "keyword"},
			"segtype": { "type": "keyword"},
			"filename": { "type": "keyword"},
			"fullname": { "type": "keyword"},
			"sect": { "type": "keyword"},
			"index": { "type": "keyword"},
			"corpus": { "type": "keyword"},
			"folder": { "type": "keyword"},
			"head": { "type": "keyword"},
			"attr": { "type": "keyword"},
			"val": { "type": "keyword"}, # head, attr, val 
			"chunk": { "type": "keyword"},
			"name": { "type": "keyword"},
			"attr": { "type": "keyword"},
			"poslist": { "type": "keyword"},
			"type": { "type": "keyword"},
			"fn": { "type": "keyword"},
			"cat": { "type": "keyword"},
			"rel": { "type": "keyword"},
			"gov": { "type": "keyword"},
			"dep": { "type": "keyword"},
			"vp": { "type": "keyword"},
			"ap": { "type": "keyword"},
			"dp": { "type": "keyword"},
			"kp": { "type": "keyword"},
			"trp": { "type": "keyword"}, # open:VERB:dobj:NOUN:door
			"cate": { "type": "keyword"},
			"tail":{ "type": "keyword"},
			"govpos":{ "type": "keyword"}, "govlem":{ "type": "keyword"}, "govtag":{ "type": "keyword"},
			"deppos":{ "type": "keyword"},
			#"fd": { "type": "keyword"},
			"si": {
				   "type": "nested",
				   "properties": {
					  "s": {"type": "keyword"},
					  "i": {"type": "integer"}
				   }
				},
			"fd": {
				   "type": "nested",
				   "properties": {
					  "cate": {"type": "keyword"},
					  "msg": {"type": "keyword"},
					  "ibeg": {"type": "integer"}
				   }
				},
			#{'i':t.i, "head":t.head.i, 'lex':t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, "gpos":t.head.pos_, "glem":t.head.lemma_ }
			"tok": {
				   "type": "nested",
				   "properties": {
					  "i": {"type": "integer"},
					  "head": {"type": "integer"},
					  "lex": {"type": "keyword"},
					  "lem": {"type": "keyword"},
					  "pos": {"type": "keyword"},
					  "tag": {"type": "keyword"},
					  "dep": {"type": "keyword"},
					  "gpos": {"type": "keyword"},
					  "glem": {"type": "keyword"}
				   }
				},
			 "wordvec": {
			   "type": "dense_vector",
			   "dims": 300,  # gpu55:/home/cikuu/gensim-data/glove-wiki-gigaword-300
			   "index": True,
			   "similarity": "l2_norm"
			 },
			 "sntvec": {
			   "type": "dense_vector",
			   "dims": 384,  # sbert, all-MiniLM-L6-v2
			   "index": True,
			   "similarity": "l2_norm"
			 },
			 "skevec": {  # _NP jumped over _NP
			   "type": "dense_vector",
			   "dims": 384,
			   "index": True,
			   "similarity": "l2_norm"
			 },
			"vec": {
				   "type": "dense_vector",
				   "dims": 384, # use sbert 
				   "index": "true",
				   "similarity": "l2_norm"
				 },

			"err": {"type": "text",  "analyzer": "err_ana"},
			#"fd": { "type": "keyword", "index": "false"},
			"short_msg": { "type": "keyword", "index": "false"},
			"arr": { "type": "keyword", "index": "false" }, # dim arr of dsk
			"info": { "type": "keyword", "index": "false" ,"ignore_above": 50},
			"kw": { "type": "keyword", "index": "false" , "ignore_above": 50},
			"meta": { "type": "keyword", "index": "false", "ignore_above": 50},
			"dim": { "type": "keyword", "index": "false" , "ignore_above": 50},
			"dims": { "type": "keyword", "index": "false" , "ignore_above": 50},
			"meta": { "type": "keyword", "index": "false", "ignore_above": 50},
			"mkf": { "type": "keyword", "index": "false", "ignore_above": 50 },
			"tc": {"type": "integer" , "index": "false"},
			"sc": {"type": "integer" , "index": "false"},
			"isum": {"type": "integer" , "index": "false"},
			"md5": { "type": "text", "store": "false", "norms":"false"},
			"md5snt": { "type": "keyword", "index": "false"},
			"sntmd5": { "type": "keyword", "index": "false"}, # added 2023.4.4
			"toks": { "type": "keyword", "index": "false" ,"store": "false"},
			"snts": { "type": "keyword", "index": "false" },
			"blob": { "type": "binary", "store": "false"},
			"zlib": { "type": "binary", "store": "false"},
			"title": { "type": "text", "analyzer": "standard"},
			"essay": { "type": "text", "analyzer": "standard"},
			"body": { "type": "text", "index": "false" },
			"spacy": { "type": "text", "index": "false" }, # spacy json result 
			"doc": { "type": "text", "index": "false" },#"doc": { "type": "keyword", "index": "false" ,"store": "false"}, # dim arr of dsk
			"tm": {"type": "date", "format": "strict_date_optional_time||yyyy-MM-dd HH:mm:ss||epoch_millis"}, #"format": "yyyy-MM-dd HH:mm:ss || yyyy-MM-dd || yyyy/MM/dd HH:mm:ss|| yyyy/MM/dd ||epoch_millis"
			"timestamp": { "type": "date"},
			"pubdate": { "type": "date"},
			"sdate": { "type": "date",  "format": "yyyy-MM-dd"},
			"csv": { "type": "keyword",  "index": "false"},
			"tsv": { "type": "keyword",  "index": "false"},
			"pair": { "type": "keyword",  "index": "false"},
			"json": { "type": "keyword",  "index": "false"},
			"dsk": { "type": "keyword",  "index": "false"},
			"v": { "type": "keyword",  "index": "false"},
			"n": { "type": "keyword",  "index": "false"},
			"adj": { "type": "keyword",  "index": "false"},
			"sent": { "type": "keyword",  "index": "false"},
			"snt": { "type": "text", "analyzer": "standard","fielddata":"true"} #,"store":"true"
		  }
		}
	}

newindex= lambda idxname : (requests.es.indices.delete(idxname) if requests.es.indices.exists(idxname) else None, requests.es.indices.create(idxname, config))[1] # body=
rows	= lambda query: requests.post(f"http://{requests.eshost}/_sql",json={"query": query}).json().get('rows',[]) 
sql		= lambda query: requests.post(f"http://{requests.eshost}/_sql",json={"query": query}).json().get('rows',[]) 
sntnum	= lambda cp: sql(f"select count(*) cnt from {cp} where type = 'snt'" )[0][0] #75222
sntsum	= lambda cp: sql(f"select count(*) cnt from {cp} where type = 'snt'" )[0][0] # added 2022.6.29
lexsum	= lambda cp: sql(f"select count(*) cnt from {cp} where type = 'tok'" )[0][0] 
lexnum	= lambda w,cp: sql(f"select count(*) cnt from {cp} where low = '{w}' and type = 'tok'")[0][0] # opened = 70
lemnum	= lambda w,cp: sql(f"select count(*) cnt from {cp} where lem = '{w}' and type = 'tok'")[0][0] 
sqlsi	= lambda query: (si:=Counter(), [si.update({row[0]:1}) for row in sql(query)])[0]
warmup  = lambda : requests.put(f"http://{requests.eshost}/_cluster/settings", json={"persistent": {"search.max_buckets": 1000000}}).text
kwic	= lambda cp, w, topk=3 : [ re.sub(rf"\b({w})\b", f"<b>{w}</b>", row[0]) for row in rows(f"select snt from {cp} where type = 'snt' and match (snt, '{w}') limit {topk}")]
check	= lambda idxname : requests.es.indices.create(index=idxname, body=config) if not requests.es.indices.exists(index=idxname) else None
md5		= lambda text: hashlib.md5(text.encode("utf8")).hexdigest()

def sqlrow(query="select lem, count(*) cnt  from gzjc where type = 'tok' and pos != 'PUNCT' group by lem order by cnt desc limit 10"):
	''' {'columns': [{'name': 'lem', 'type': 'keyword'}, {'name': 'cnt', 'type': 'long'}], 'rows': [['the', 7552], ['be', 5640], ['and', 3604], ['to', 3561], ['of', 3127], ['a', 2902], ['in', 2687], ['I', 2063], ['have', 1562], ['it', 1311]]} '''
	res = requests.post(f"http://{requests.eshost}/_sql",json={"query": query}).json() 
	columns = [ ar['name'] for ar in res['columns'] ]
	return  [  dict(zip(columns, ar)) for ar in res['rows'] ] #[{'lem': 'the', 'cnt': 7552}, {'lem': 'be', 'cnt': 5640}, {'lem': 'and', 'cnt': 3604}, {'lem': 'to', 'cnt': 3561}, {'lem': 'of', 'cnt': 3127}, {'lem': 'a', 'cnt': 2902}, {'lem': 'in', 'cnt': 2687}, {'lem': 'I', 'cnt': 2063}, {'lem': 'have', 'cnt': 1562}, {'lem': 'it', 'cnt': 1311}]

## added 2022.7.3
cursor_sql = lambda query, cursor: requests.post(f"http://{requests.eshost}/_sql", json={"query":query, "cursor":cursor}).json() 
def cursor_rows(query="select did, doc from testdoc where type ='doc' and did is not null"): #select dep, gov, lem, pos, count(*) cnt from gzjc where type='tok' group by dep, gov, lem, pos
	rows = []				
	cursor=''
	while True : 
		res = cursor_sql(query, cursor)  
		rows.extend(res['rows'])
		cursor = res.get('cursor','') 
		if not cursor: break
	return rows 

def esindex(idxname, id , source): 
	''' source = {"did": sid,'pid': did, 'type':'snt', 'snt': sp.text.strip(), 'tc': len(sp)} '''
	try:
		requests.es.index(index=idxname, body=source, id = id)
	except Exception as e:
		print ("esindex ex:",e, idxname, source, id)
		exc_type, exc_value, exc_traceback_obj = sys.exc_info()
		traceback.print_tb(exc_traceback_obj)

def walk(query): 
	cursor=''
	while True : 
		res = cursor_sql(query, cursor)  
		yield res['rows']
		cursor = res.get('cursor','') 
		if not cursor: break

def sqlsi(query): #select lex, count(*)
	si = Counter()
	cursor=''
	while True : 
		res = cursor_sql(query, cursor)  
		si.update( dict(res['rows']) )
		cursor = res.get('cursor','') 
		if not cursor: break
	return si #dict(si.most_common())

def sqlssi(query="select lem, lex, count(*) cnt from gzjc where type = 'tok' and lem rlike '[a-z]+' group by lem, lex"
		, iftrue = lambda s1, s2: s1 and s2
		, s1_func = lambda s: s
		, s2_func = lambda s: s  # lower()
		): 
	ssi = defaultdict(Counter)
	cursor=''
	while True : 
		res = cursor_sql(query, cursor) 
		[ ssi[ s1_func(s1) ].update({ s2_func(s2) :cnt}) for s1, s2, cnt in res['rows'] if iftrue(s1, s2) ] 
		cursor = res.get('cursor','') 
		if not cursor: break
	return ssi 

trpssi	= lambda idxname, dep='dobj', gpos='VERB', dpos='NOUN': sqlssi(f"select gov, lem, count(*) cnt from {idxname} where type = 'tok' and pos = '{dpos}' and dep ='{dep}' and lem rlike '[a-z]+' and gov like '%_{gpos}' group by gov, lem", s1_func =lambda s: s.split('_')[0])
_trpssi = lambda idxname, dep='dobj', gpos='VERB', dpos='NOUN': sqlssi(f"select lem, gov, count(*) cnt from {idxname} where type = 'tok' and pos = '{dpos}' and dep ='{dep}' and lem rlike '[a-z]+' and gov like '%_{gpos}' group by lem, gov", s2_func =lambda s: s.split('_')[0])

def readline(infile, sepa=None):
	with open(infile, 'r') as fp:
		while True:
			line = fp.readline()
			if not line: break
			yield line.strip().split(sepa) if sepa else line.strip()

def likelihood(a,b,c,d, minus=None):  #from: http://ucrel.lancs.ac.uk/llwizard.html
	try:
		if a is None or a <= 0 : a = 0.000001
		if b is None or b <= 0 : b = 0.000001
		E1 = c * (a + b) / (c + d)
		E2 = d * (a + b) / (c + d)
		G2 = round(2 * ((a * math.log(a / E1)) + (b * math.log(b / E2))), 2)
		if minus or  (minus is None and a/c < b/d): G2 = 0 - G2
		return G2
	except Exception as e:
		print ("likelihood ex:",e, a,b,c,d)
		return 0

#PUT twitter/_mapping {  "properties": {  "email": { "type": "keyword"  }  }}#"stroke": { "type": "keyword", "index": "false"},
def delete_index(cp:str='testidx'): 	return requests.delete(f"http://{requests.eshost}:{requests.esport}/{cp}").text #DELETE /twitter
def new_empty_index(cp:str='testidx', delete:bool=True): 
	if delete: requests.delete(f"http://{requests.eshost}:{requests.esport}/{cp}").text
	return requests.put(f"http://{requests.eshost}:{requests.esport}/{cp}", data={}).text #PUT twitter  {}
def add_mapping_keyword(kws:list, cp:str='testidx'): 		return [requests.put(f"http://{requests.eshost}:{requests.esport}/{cp}/_mapping/", data={"properties": {  f"{kw}": { "type": "keyword"  }  }}).text for kw in kws]
def add_mapping_keyword_noindex(kws:list, cp:str='test'):	return [requests.put(f"http://{requests.eshost}:{requests.esport}/{cp}/_mapping/", data={"properties": {  f"{kw}": { "type": "keyword", "index": "false"} }}).text for kw in kws]
def add_mapping_float(kws:list, cp:str='testidx'): 			return [requests.put(f"http://{requests.eshost}:{requests.esport}/{cp}/_mapping/", data={"properties": {  f"{kw}": { "type": "float"  }  }}).text for kw in kws]
def add_mapping_integer(kws:list, cp:str='testidx'): 		return [requests.put(f"http://{requests.eshost}:{requests.esport}/{cp}/_mapping/", data={"properties": {  f"{kw}": { "type": "integer"  }  }}).text for kw in kws]
def add_mapping(dic:dict, cp:str='testidx'):				return [requests.put(f"http://{requests.eshost}:{requests.esport}/{cp}/_mapping/", data={"properties": {  f"{k}": { "type": "{v}"  }  }}).text for k,v in dic.items()] #''' {"num":"integer", "awl":"float", "tag":"keyword"} '''

def bulk(arr, batch=100000, debug=False):
	''' bulk submit , added 2022.3.27, not tested yet '''
	if not hasattr(bulk, 'actions'):	bulk.actions=[]
	bulk.actions.append(arr)  #{'_op_type':'index', '_index':idxname, '_id': did, '_source': arr}
	if len(bulk.actions) > batch : 
		try:
			helpers.bulk(client=es,actions=actions, raise_on_error=False)
			if debug: print (bulk.actions[-1], flush=True) 
			bulk.actions = []
		except Exception as ex:
			print(">>bulk ex:", ex)

	def submit(): 
		print ("bulk submit is called, un-submiited actions len: ", len(bulk.actions)) 
		if len(bulk.actions) >0 : 
			helpers.bulk(client=es,actions=bulk.actions, raise_on_error=False)
			bulk.actions = []	

def ids(_ids:list, cp:str='inau'): 
	''' ["one","two"] '''
	sql	= { "query": {  "ids" : {    "type" : "_doc",   "values" : _ids }		}	}
	return requests.post(f"http://{requests.eshost}/{cp}/_search/", json=sql).json()

def term_to_snts(sql): 
	rows = requests.es.sql(sql) #f"select src from {cp} where type = 'trp' and gov='{gov}' and rel='{rel}' and dep='{dep}' limit {topk}"
	sql	= { "query": {   "ids" : {   "type" : "_doc",
            "values" : [row[0] for row in rows] #clec:snt-34993,  clec:snt-32678
			}}	}
	return requests.post(f"http://{requests.eshost}/{cp}/_search/", json=sql).json()

def match_phrase(phrase:str='opened the box', cp:str='clec', topk:int=10): 
	''' '''
	sql	= {  "query": { "match_phrase": { "snt": phrase    } }  , "size": topk}
	return requests.post(f"http://{requests.eshost}/{cp}/_search/", json=sql).json()

def alltrue(must_match:dict={"rid" : 230537,"type" : "sntfd","cate" : "e_snt.nv_agree" }, index:str='essay', topk:int=10): 
	''' 2023.5.2 '''
	sql	= { "query": {
        "bool": {"must": [ {"match": {k:v}} for k,v in must_match.items() ]  }
    }, "size": topk }
	return requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()

def lemlist(index:str='essay', pos:str='VERB', topk:int=1000): 
	''' "aggregations" : { "buckets" : [  {   "key" : "have",   "doc_count" : 70 '''
	sql = {  "query": {    "match": {"pos":pos}  },  "size" : 0,
    "aggs" : { "termrank" : { "terms" : { "field" : "lem", "size":1000  }  }    }  }
	return requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()

phrase_num = lambda phrase, cp='clec', topk=10: match_phrase(phrase, cp, topk)["hits"]["total"]["value"]

addpat	= lambda s : f"{s}_[^ ]*" if not s.startswith('_') else f"[^ ]*{s}[^ ]*"   # if the last one, add $ 
rehyb   = lambda hyb: ' '.join([ addpat(s) for s in hyb.split()])  #'the_[^ ]* [^ ]*_NNS_[^ ]* of_[^ ]*'
heads   = lambda chunk:  ' '.join([s.split('_')[0].lower() for s in chunk.split()])		#the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
def hybchunk(hyb:str='the _NNS of', index:str='dic', size:int= -1, topk:int=10):
	''' the _NNS of -> {the books of: 13, the doors of: 7} , added 2021.10.13 '''
	sql= { "query": {  "match_phrase": { "postag": hyb  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{requests.eshost}/{index}/_search/", json=sql).json()
	si = Counter()
	repat = rehyb(hyb)
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag']
		m= re.search(repat,postag) #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		if m : si.update({ heads(m.group()):1})
	return si.most_common(topk)

def init(idxname):
	''' init a new index '''
	if requests.es.indices.exists(index=idxname):requests.es.indices.delete(index=idxname)
	requests.es.indices.create(index=idxname, body=config) #, body=snt_mapping
	print(">>finished " + idxname )

def skenp(doc): # added 2023.5.2
	import en 
	#doc = spacy.nlp(snt)
	return {"postag": en.es_postag(doc), 'skenp': en.es_skenp(doc)}

def sntbr(essay): # added 2023.5.2
	import spacy
	from spacy.lang import en
	if not hasattr(sntbr, 'inst'): 
		sntbr.inst = (inst := en.English(), inst.add_pipe("sentencizer"))[0]
	return sntbr.inst(essay) 

def esupdate(idxname, id, arr): # arr = {"tags":"VIP"}
	try:
		return requests.post(f"http://{requests.eshost}/{idxname}/_doc/{id}/_update", json={"doc":arr }).json() 
	except Exception as ex:
		print(">>esupdate ex:", ex)

def drop(idxname): 
	try:
		requests.es.indices.delete(index=idxname)
	except Exception as ex:
		print(">>drop index ex:", ex)

def addfile(infile, idxname="testdoc", taglist:str=None):
	''' add doc only , 2023.5.1 '''
	check(idxname)
	start = time.time()
	text = open(infile, 'r').read().strip() 
	did	 = md5(text)
	esindex(idxname, f"doc-{did}", {"did": f"doc-{did}", "doc":text,  "filename": infile, 'type':'doc', 'tags':[] if taglist is None else taglist.strip().split(',') if isinstance(taglist, str) else taglist })
	print(f"{infile} is finished, \t| using: ", time.time() - start) 

def addfolder(folder:str, idxname:str=None, pattern:str=".txt"): 
	''' folder -> esindex '''
	if idxname is None : idxname=  folder
	print("addfolder started:", folder, idxname, requests.es, flush=True)
	for root, dirs, files in os.walk(folder):
		for file in files: 
			if file.endswith(pattern):
				addfile(f"{folder}/{file}", idxname = idxname, taglist=folder) 
				print (f"{folder}/{file}", flush=True)
	print("addfolder finished:", folder, idxname, requests.es, flush=True)

def walkfolder(folder:str, pattern:str=".txt"): 
	''' 2023.5.5 '''
	for root, dirs, files in os.walk(folder):
		for file in files: 
			if file.endswith(pattern):
				text = open(f"{folder}/{file}", 'r').read().strip() 
				yield (file, text)  #{"folder":folder, "filename":file, "content":text}

fire.actions = []
def addaction(arr, batch:int=200000): #{'_op_type':'index', '_index':index, '_id': sntid, '_source': source }
	fire.actions.append( arr )
	if len(fire.actions) >= batch: 
		helpers.bulk(client=requests.es,actions=fire.actions, raise_on_error=False)
		print (fire.actions[-1], flush=True) 
		fire.actions = []
submit_actions = lambda : helpers.bulk(client=requests.es,actions=fire.actions, raise_on_error=False) if fire.actions else None	

def skenp_source (sntid, doc) : 
	import en 
	return {"postag": en.es_postag(doc), 'skenp': en.es_skenp(doc), "id":sntid,  "type":"snt", "tc": len(doc),"snt":doc.text.strip()} 

# 50631-tok-0,  id=_id, doc-1:snt-2:tok-3, parent_id = id.split(':tok-')[0] 
tok_source = lambda sntid, doc: [{'_id': f"{sntid}:tok-{t.i}",  '_source': {"sntid": sntid, "id": f"{sntid}:tok-{t.i}", 'i': t.i, 'type':'tok','lex': t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, 'glem': t.head.lemma_, 'gpos': t.head.pos_, 'gtag': t.head.tag_ } }  for t in doc]

def testana(index:str='test'):
	requests.eshost	= os.getenv("eshost", "sntvec.wrask.com:9200") 
	requests.es		= Elasticsearch([ f"http://{requests.eshost}" ])  
	init( index ) 
	arr = requests.post(f"http://sntvec.wrask.com:9200/{index}/_analyze", json={
  "analyzer": "postag_ana",
  "text": "booked_book_VERB_VBN_NP5"
}).json()
	for t in arr['tokens']:
		print (t) 

if __name__ == "__main__": 
	import platform
	print( testana()) if platform.system() in ('Windows') else fire.Fire({"init":init,"test":testana}) 
	
'''
{'tokens': [{'token': 'booked', 'start_offset': 0, 'end_offset': 22, 'type': 'word', 'position': 0}, 
{'token': 'd', 'start_offset': 0, 'end_offset': 22, 'type': 'word', 'position': 0}, 
{'token': '_book', 'start_offset': 0, 'end_offset': 22, 'type': 'word', 'position': 0}, 
{'token': '_,', 'start_offset': 0, 'end_offset': 22, 'type': 'word', 'position': 0}]}
the_[^ ]* [^ ]*_NNS_[^ ]* of_[^ ]* 
_^ wxpecially_wxpecially_ADV_RB the_the_DET_DT songs_song_NOUN_NNS of_of_ADP_IN _PROPN_NNP _PUNCT_.
PUT twitter/_mapping 
{
  "properties": {
    "email": {
      "type": "keyword"
    }
  }
}

POST /essay/_doc/doc-1819783:snt-23/_update
{
  "doc": {
    "tags":"VIP"
  }
}


	sql= {
  "query": { 
    "bool": { 
      "must": [
        { "match_phrase": { "postag":  hyb}},
        { "match": { "type":"snt" }}
      ]
    }
  },
  "size":  size
}

PUT my_index
{
  "mappings": {
    "properties": {
      "my_vector": {
        "type": "dense_vector",
        "dims": 4
      },
      "my_text" : {
        "type" : "keyword"
      }
    }
  }
}

GET my_index/_search
{
  "query": {
    "script_score": {
      "query": {
        "match_all": {}
      },
      "script": {
        "source": "cosineSimilarity(params.query_vector, 'my_vector') + 1.0",
        "params": {
          "query_vector": [ 1,2,3]
        }
      }
    }
  }
}

PUT my_index/_doc/1
{
  "my_text" : "text1",
  "my_vector" : [0.5, 10, 6, 3]
}

PUT my_index/_doc/2
{
  "my_text" : "text2",
  "my_vector" : [-0.5, 10, 10, 4]
}

GET /my_index/_search
{
  "query": {
    "match_all": { }
  }
}

essaydm.wrask.com 
ubuntu@VM-171-3-ubuntu:/data$ runlike es
docker run --name=es --hostname=db25101107b8 --user=elasticsearch --mac-address=02:42:ac:12:00:02 --env=discovery.type=single-node --env=PATH=/usr/local/openjdk-11/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin --env=LANG=C.UTF-8 --env=JAVA_HOME=/usr/local/openjdk-11 --env=JAVA_VERSION=11.0.9.1 --env=EK_VERSION=7.15.1 --volume=/ftp/es-9200-eevsnts:/home/elasticsearch/elasticsearch-7.15.1/data --workdir=/home/elasticsearch -p 5601:5601 -p 9200:{requests.esport} --restart=always --label='maintainer=nshou <nshou@coronocoya.net>' --runtime=runc --detach=true nshou/elasticsearch-kibana /bin/sh -c 'elasticsearch-${EK_VERSION}/bin/elasticsearch -E http.host=0.0.0.0 --quiet & kibana-${EK_VERSION}-linux-x86_64/bin/kibana --allow-root --host 0.0.0.0 -Q'

#https://www.elastic.co/cn/blog/introducing-approximate-nearest-neighbor-search-in-elasticsearch-8-0

PUT index
{
 "mappings": {
   "properties": {
     "image-vector": {
       "type": "dense_vector",
       "dims": 128,
       "index": true,
       "similarity": "l2_norm"
     }
   }
 }
}

POST index/_doc
{
 "image-vector": [0.12, 1.34, 3.4]
}

GET index/_knn_search
{
 "knn": {
   "field": "image-vector",
   "query_vector": [-0.5, 9.4, 3],
   "k": 10,
   "num_candidates": 100
 }
}

from dic.word_awl import word_awl 
@app.get("/corpus/word_awl")
def corpus_word_awl(index:str='gzjc', topk:int=10): 
	return (si:= Counter(), [si.update({s:i}) for s,i in rows(f"select lem, count(*) from {index} where type = 'tok' group by lem") if s in word_awl ], si.most_common(topk))[-1]

GET /dic/_search
{
  "query": {
    "match_phrase": {
      "postag": "the _NNS of"
    }
  } ,
  "_source": ["postag"],
  "size":-1
}

POST /clec/_analyze
{
  "analyzer": "postag_ana",
  "text": "booked_book_VBD_VERB_."
}

GET /gzjc/_analyze
{
  "analyzer": "postag_ana", 
  "text": "foxes jumped_jump_VERB_VBD lazy dogs"
}
GET /_analyze
{
  "tokenizer": "whitespace",
  "filter": [
    {
      "type": "pattern_replace",
      "pattern": "((^[^_]+)_([a-z]+)_([VERB|NOUN|ADJ|ADV]+)_.*)",
      "replacement": "$3/$4",
      "all": false
    }
  ],
  "text": "foxes jumped_jump_VERB_VBD lazy dogs"
}

ubuntu@dicvec-scivec-jukuu-com-flair-64-245:~/cikuu/pypi/so$ python __init__.py init test
>>finished test
ubuntu@dicvec-scivec-jukuu-com-flair-64-245:~/cikuu/pypi/so$ python __init__.py test
{'token': 'booked', 'start_offset': 0, 'end_offset': 24, 'type': 'word', 'position': 0}
{'token': 'book/VERB', 'start_offset': 0, 'end_offset': 24, 'type': 'word', 'position': 0}
{'token': '_book', 'start_offset': 0, 'end_offset': 24, 'type': 'word', 'position': 0}
{'token': '_VERB', 'start_offset': 0, 'end_offset': 24, 'type': 'word', 'position': 0}
{'token': '_VBD', 'start_offset': 0, 'end_offset': 24, 'type': 'word', 'position': 0}
{'token': '_NP', 'start_offset': 0, 'end_offset': 24, 'type': 'word', 'position': 0}

GET /self_essay/_search
{
  "query": {
    "bool": {
      "must": [
        {"term": {
          "tag":  "VBD"
        }},
        {"term": {
          "pos":  "VERB"
        }}
      ]
    }
  }
}

GET /essay/_search
{
    "query": {
        "bool": {
            "must": [
                {"match": {"rid" : 230537}},
                {"match": {"type" : "sntfd"}},
                {"match": {"cate" : "e_snt.nv_agree"}}
            ]
        }
    }, "size": topk
}

POST /essay/_search
{
  "query": {
    "match": {"pos":"VERB"}
  },
  "size" : 0,
    "aggs" : {
        "termrank" : {
            "terms" : { "field" : "lem", "size":1000  } 
            
        }
    }
}
'''