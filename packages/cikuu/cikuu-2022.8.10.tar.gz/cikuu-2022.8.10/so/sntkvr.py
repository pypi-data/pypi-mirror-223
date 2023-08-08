# cp from flair-snt.py , 2023.7.9 
# 2023.7.2  docker run -it --rm --name tt -v /data/cikuu/bin:/app wrask/benepar python /app/sntkvr.py beneparsnt gzjc 
import sys,redis,json,os, fire,platform, time,fileinput, traceback, requests
import spacy 
if not hasattr(spacy, 'nlp'):
	spacy.nlp		= spacy.load(os.getenv('spacy_model','en_core_web_sm')) # 3.5.0
	spacy.from_json = lambda arr: spacy.tokens.Doc(spacy.nlp.vocab).from_json(arr) # added 2022.8.19

zscore = lambda  s= 'gzjc:LEM|book': ( arr := s.split('|'),  redis.r.zscore(arr[0], arr[-1]) )[-1]
from math import log as ln
def likelihood(a,b,c,d, minus=None):  #from: http://ucrel.lancs.ac.uk/llwizard.html
	try:
		if a is None or a <= 0 : a = 0.000001
		if b is None or b <= 0 : b = 0.000001
		if c is None or c <= 0 : c = 0.000001
		if d is None or d <= 0 : d = 0.000001
		E1 = c * (a + b) / (c + d)
		E2 = d * (a + b) / (c + d)
		G2 = round(2 * ((a * ln(a / E1)) + (b * ln(b / E2))), 2)
		if minus or  (minus is None and a * d < b * c): G2 = 0 - G2 #if minus or  (minus is None and a/c < b/d): G2 = 0 - G2
		return round(G2,1)
	except Exception as e:
		print ("likelihood ex:",e, a,b,c,d)
		return 0

def snts(name:str='gzjc'):
	for i in range(int(redis.r.get(f"hsnt:{name}:#"))): 
		snt = redis.r.hget(f"hsnt:{name}:{i}", 'snt')
		if snt: yield i, snt

def snts_batch(name:str='gzjc', batch:int=100): # add 2023.7.12, upon gecedit
	for i in range(0, int(redis.r.get(f"hsnt:{name}:#")), batch): 
		snts = [ (redis.r.hget(f"hsnt:{name}:{i+j}", 'snt'), i+j) for j in range(batch)]
		yield i, snts

def docs(name:str='gzjc'):
	for i in range(int(redis.r.get(f"hsnt:{name}:#"))): 
		spa = redis.r.hget(f"hsnt:{name}:{i}", 'spacy')
		if spa: yield i, spacy.from_json(json.loads(spa) )

def benep(): 
	import benepar
	if not hasattr(benep,'parser'): benep.parser = benepar.Parser("benepar_en3")
	return benep.parser

def frame_snt(snt:str="He had a look at different hats."):    
	''' He had <have.LV> a look <look.01> at different hats .   https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_2_TAGGING.md '''
	from flair.models import SequenceTagger
	from flair.tokenization import SegtokSentenceSplitter
	from flair.data import Sentence
	if not hasattr(frame_snt, 'tagger'):  frame_snt.tagger = SequenceTagger.load('frame-fast')  # 115M 
	sentence_1 = Sentence(snt)
	frame_snt.tagger.predict(sentence_1)
	return sentence_1.to_dict() #{'text': 'George returned to Berlin to return his hat.', 'all labels': [{'value': 'return.01', 'confidence': 0.986716628074646}, {'value': 'return.02', 'confidence': 0.47414299845695496}]}

class util(object): 
	def __init__(self, host='172.17.0.1' if not 'Windows' in platform.system() else "files.jukuu.com", port=6666, interval=30) : 
		redis.r = redis.Redis(host=host, port=port, decode_responses=True, health_check_interval=interval )	
		self.start = time.time()
		print (redis.r, flush=True)
	
	def hello(self, name, topn:int=3): 
		''' name: gzjc/loc/dic '''
		for i,snt in docs(name) :
			if i > topn: break
			print (i, snt ) 
	def wget(self, name, hsnt:bool=False): os.system(f"http://files.jukuu.com:8000/sntjsonlg/{name}.jsonlg.3.4.1.gz") if not hsnt else os.system(f"http://files.jukuu.com:8000/sntjsonlg/hsnt-{name}.ktv.gz")

	def beneparsnt(self, name, batch:int=100): 
		''' docker run -it --rm --name benepar -v /data/cikuu/bin:/app wrask/benepar python /app/sntkvr.py beneparsnt sino  '''
		p = benep() 		#redis.r.delete(f"benepar:{name}")
		print ("start to benepar:", name, flush=True)
		for i,snt in snts(name): 
			if i % batch == 0 : print (f"benepar-{name}:", i, snt)  
			if not redis.r.hexists(f"hsnt:{name}:{i}", "benepar"): # resumable ValueError: Sentence of length 531 (in sub-word tokens) exceeds the maximum supported length of 512
				try: 
					t = p.parse(snt.strip())
					line = " ".join([s.strip() for s in str(t).split("\n")])
					redis.r.hset(f"hsnt:{name}:{i}", "benepar" , line )  
				except Exception as e:
					print ("beneparsnt ex:", e, i, snt) 
		print("beneparsnt finished: ", name) 

	def framesnt(self, name , refresh:bool=False, batch:int=100) :
		''' docker run -it --rm --name framesnt -v /data/cikuu/bin:/app wrask/flair python /app/sntkvr.py framesnt gzjc  '''
		print ("framesnt flair started:", name ,  ' -> ',  redis.r, flush=True)
		if refresh: 
			[ redis.r.delete(k) for k in redis.r.keys(f"frame:{name}:*")]
			print ( 'finished deleting:', name, flush=True) 
		for i,snt in snts(name): 
			try:
				if i % batch == 0 : print (f"framesnt-{name}:", i, snt, flush=True) 
				if not redis.r.hexists(f"hsnt:{name}:{i}", "frame"): # resumable 
					res = frame_snt(snt) 
					redis.r.hset( f"hsnt:{name}:{i}", "frame",  json.dumps([ (row['value'], round(row['confidence'],4)) for row in res.get('all labels', []) ]) )  
					for row in res.get('all labels', []): 					#redis.r.hset( f"hsnt:{name}:{i}", "frame:" + row['value'], round(row['confidence'],4))
						redis.r.zincrby( f"frame:{name}:{row['value'].split('.')[0]}", 1, row['value']) #LEM:
			except Exception as e:
				print ("framesnt ex:", e, i, snt) 
		print ('framesnt finished:', name) 

	def framesum(self, name ) :
		''' add _sum to frame:sino:return  | 2023.7.18 '''
		print ("framesum started:", name ,  ' -> ',  redis.r, flush=True)
		for k in redis.r.keys(f"frame:{name}:*"):
			w = k.split(':')[-1]
			_sum = redis.r.zscore(f"{name}:LEM", w)
			if _sum: redis.r.zadd(f"frame:{name}:{w}", {"_sum":_sum})
		print ('framesum finished:', name) 

	def gecedit(self, name, batch:int=100): 
		''' docker run -it --rm --name gecedit -v /data/cikuu/bin:/app wrask/cikuu python /app/sntkvr.py gecedit sino  '''
		print ("start to gecedit:", name, flush=True)
		for i,sntrows in snts_batch(name, batch): 
			print (f"gecedit-{name}:", i, len(sntrows), flush=True)  #if not redis.r.hexists(f"hsnt:{name}:{i}", "gec"): # resumable 
			try:
				sntdic = requests.post(f"http://api.jukuu.com/wrap-xgec", json=[row[0] for row in sntrows]).json() #sntdic = requests.get(f"http://api.jukuu.com/wrap-xgec", params={"snts": snt}).json()  # http://api.jukuu.com/wrap-xgec?snts=hello  => {"hello":"hello"}
				rows = requests.post(f"http://api.jukuu.com/gecv1-bisnts-edits",json=sntdic).json() # http://api.jukuu.com/gecv1-bisnts-edits  { "It are ok.": "It is ok.", "She has ready.": "She is ready."}
				sntid = dict(sntrows) 
				for row in rows: 
					sid = sntid.get(row['snt'],0)
					redis.r.hset(f"hsnt:{name}:{sid}", "gec", row.get('gec',''), mapping={"edits":json.dumps(row.get('edits',[]))} ) 
					#for edit in row.get('edits',[]): redis.r.hset(f"hsnt:{name}:{sid}", f"edit-{edit.get('ibeg',0)}={edit.get('cate','')}", json.dumps(edit)) 
			except Exception as e:
				print ("ex:", e, i, snt) 
		print("gecedit finished: ", name) 

	def skenp(self, name, overwrite:bool=False, batch:int=10000 ): # added 2023.7.23
		import en 
		print("postag/skenp started:", name,flush=True)
		start = time.time()
		for i, doc in  docs(name): 
			try:
				if i % batch == 0: print ( f"[{name}] i=", i, " |tim=", round(time.time() - start, 2) , flush=True)
				if overwrite or not redis.r.hexists(f"hsnt:{name}:{i}", "postag"): # resumable 
					redis.r.hset(f"hsnt:{name}:{i}", "postag", en.es_postag(doc), mapping={'skenp': en.es_skenp(doc)} )
			except Exception as e:
				print ("skenp ex:", e, i, doc) 
		print("postag/skenp finished:", name, " |tim=", round(time.time() - start, 2) )

	def lemkeyness(self, src, tgt, rel:str="LEMPOS", critical:float=3.84 ):
		''' src:sino tgt:dic ''' 
		redis.r.delete(f"keyness:{src}-{tgt}:{rel}")
		for lem in redis.r.hkeys(f"dict:lemlexlist"): # lemlist 
			rows = lem_keyness(rel, lem, src, tgt) 
			if rows: 
				data = { s:i for s,i in rows.items() if s.split(':')[-1] in ('VERB','NOUN','ADV','ADJ')   }
				if data : redis.r.zadd(f"keyness:{src}-{tgt}:{rel}", data) 
				print ( lem, rows, flush=True) 
		print ( 'lemkeyness finished:', src, tgt, rel) 

	def hsnt(self, infile, batch:int=100000):
		''' load from gzjc.jsonlg.3.4.1.gz,  hsnt:gzjc:0,   .. 2023.7.11 ,upgrade version of sntzset (max is 512M) '''
		name = infile.split('/')[-1].split('.')[0] # ./sci.jsonlg.3.4.1.gz
		print ("hsnt started:", name ,  ' -> ',  redis.r, flush=True)
		[ redis.r.delete(k) for k in redis.r.keys(f"hsnt:{name}:*")]
		start = time.time()
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): #356317 docs of each doc file
			if sid % batch == 0: print ( f"[{name}] sid=", sid, " |tim=", round(time.time() - start, 2) , flush=True)
			try:
				doc = spacy.from_json(json.loads(line.strip())) 
				snt = doc.text.strip()
				redis.r.hset(f"hsnt:{name}:{sid}", 'snt', snt, mapping={"spacy":line.strip(), "tc": len(doc)})
			except Exception as e:
				print ("ex:", e, sid, line[0:30]) 
		redis.r.set(f"hsnt:{name}:#", sid + 1) # easy dump: hsnt:gzjc:* 
		redis.r.hset("hsnt", name, sid + 1)  # gzjc=8873, [0 .. 8872]
		print ("hsnt finished:", infile, " using: ", time.time() - start) 

	def parse(self, name): 
		''' name = inau , hashtable = txt:inau, 2023.7.13 '''
		print ("parse started:", name ,  ' -> ',  redis.r, flush=True)
		start = time.time()
		for did, filename in enumerate(redis.r.hkeys(f"txt:{name}")): 
			try:
				txt = redis.r.hget(f"txt:{name}", filename) 
				tdoc = spacy.nlp(txt) 
				print ( filename, len(tdoc), flush=True) 
				redis.r.hset(f"htxt:{name}:{did}", mapping={"filename":filename, "txt":txt, "spacy": json.dumps(tdoc.to_json()), "snts": json.dumps([ sp.text.strip() for sp in tdoc.sents ]), "tc": len(tdoc)} )
				for sid, sp in enumerate(tdoc.sents):
					doc = sp.as_doc() 
					snt = doc.text.strip()
					if not redis.r.exists(f"hsnt:{name}:{snt}"):  # hsnt:inau:11.3
						redis.r.hset(f"hsnt:{name}:{snt}", mapping={"spacy": json.dumps(doc.to_json()), "snt": snt, "tc": len(doc)} )
			except Exception as e:
				print ("ex:", e, did, filename) 
		redis.r.set(f"htxt:{name}:#", did + 1) 
		print ("parse finished:", name, " using: ", time.time() - start) 

	def isalpha(self, zkey): 
		''' zkey: gzjc:LEX , clean with isalpha '''
		print ( "started:", zkey, redis.r.zcard(zkey) ) 
		for s,i in redis.r.zrevrange(zkey, 0, -1,True): 
			if not s.isalpha(): 
				redis.r.zrem(zkey, s)
				print (s, flush=True) 
		print ( "finished:", zkey, redis.r.zcard(zkey)) 

	def htxt(self, infile, refresh:bool=True):
		''' spider.ag.docjsonlg.3.4.1.gz,  info '''
		name = infile.split('/')[-1].split('.')[0] 
		print ("htxt started:", name ,  ' -> ',  redis.r, flush=True)
		if refresh: [ redis.r.delete(k) for k in redis.r.keys(f"htxt:{name}:*")]
		start = time.time()
		redis.r.hset("htxt", name, 0) 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)):
			try:
				arr = json.loads(line.strip())  #	redis.r.hincrby("htxt", name) 
				info = arr.get('info',{}) #		did = info.get('did', 0) 
				redis.r.hset(f'htxt:{name}:{sid}', mapping=info ) 
				arr.pop("info", None)
				redis.r.hset(f'htxt:{name}:{sid}', 'spacy', json.dumps(arr))
			except Exception as e:
				print ("ex:", e, sid, line[0:30]) 
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
		redis.r.hset(f"htxt:{name}:#", name, sid + 1) 
		print(f"{infile} is finished, \t| using: ", time.time() - start) 

	def htxtrid(self, rid, refresh:bool=True):
		''' rid = 230537, added 2023.7.23 '''
		print ("htxtrid started:", rid ,  ' -> ',  redis.r, flush=True)
		for k in redis.r.keys(f"htxt:rid-{rid}:uid-*"):
			try:
				arr = redis.r.hgetall(k) 
				if 'snts' in arr : continue
				essay = arr.get('essay','')
				tdoc = spacy.nlp(essay)
				snts = [sp.text.strip() for sp in tdoc.sents if sp.text.strip()]
				redis.r.hset(k, 'snts', json.dumps(snts))
				for snt in snts: 
					if not redis.r.hexists(f"hsnt:{snt}", 'spacy'):
						doc = spacy.nlp(snt)
						redis.r.hset(f"hsnt:{snt}", "snt", snt, mapping={"tc":len(doc), "spacy": json.dumps(doc.to_json())})
			except Exception as e:
				print ("ex:", e, k) 
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
		print(f"{rid} is finished, \t| using: ", time.time() - self.start)
	
	def hdel(self, name , prefix:str='edit-') :
		''' remove those hashtable whose key startswith prefix   '''
		if prefix == '': return print("prefix cannot be empty") 
		for i,snt in snts(name): 
			[redis.r.hdel(f"hsnt:{name}:{i}", k) for k in redis.r.hkeys(f"hsnt:{name}:{i}") if k.startswith(prefix)]
		print ('hdel finished:', name, prefix) 

	def toes(self, name, index:str=None, debug:bool=False, tok:bool=True, reset:bool=True, batch:int=100000):
		''' name=gzjc/clec, mv from /pypi/so/sntspacy-es.py  2023.7.23 '''
		import dic, so #	from so import * 
		from dic import word_idf
		if index is None : index = name.split('.')[0]
		if reset: so.drop(index)
		so.check(index) 
		word_level = dic.word_level()  
		print ( 'toes started:', index, batch, flush=True)

		start = time.time()
		for did, doc in docs(name) : 
			try:
				sntid = f"snt-{did}"
				arr = redis.r.hgetall(f"hsnt:{name}:{did}")
				source = {"postag": arr.get('postag',''), 'skenp': arr.get('skenp',''), 'skecl': arr.get('skecl','')} #skenp(doc)
				source.update({"did":sntid, "type":"snt", "tc": len(doc),"snt":doc.text.strip()}) 
				so.addaction( {'_op_type':'index', '_index':index, '_id': sntid, '_source': source }, batch)
				
				if tok: 
					for t in doc:
						ar = {"did": sntid, 'i': t.i, 'type':'tok','lex': t.text, 'lem':t.lemma_, 'pos':t.pos_, 'tag':t.tag_, 'dep':t.dep_, 'glem': t.head.lemma_, 'gpos': t.head.pos_, 'gtag': t.head.tag_ }
						idf = word_idf.word_idf.get(t.text.lower(), 0)
						if idf : ar.update({"idf":idf})
						level = word_level.get(t.text.lower(), '') 
						if level: ar.update({"level":level})
						so.addaction( {'_op_type':'index', '_index':index, '_id': f"{sntid}:tok-{t.i}", '_source': ar } )

			except Exception as e:
				print("ex:", e)	

		so.submit_actions()
		print(f"indexing finished: {index}, \t| using: ", time.time() - start) 

	def loadnju(self, infile, refresh:bool=False, dsk:bool=False): 
		''' dis=dsk, info, snts => htxt:rid-2216475:uid-24427507, snts = [spacy] '''
		name = infile.split('.')[0]  # nju 
		if refresh: [redis.r.delete(k) for k in redis.r.keys(f"rids:{name}*")]

		print (name, infile, redis.r, flush=True)
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): #for line in open(infile,'r').readlines():
			#if sid < startid : continue # added 20230724, resumable 
			try:
				arr = json.loads(line) 
				info, dsk, sntspacys = arr.get('info',{}), arr.get('dsk',{}), arr.get('snts',[]) 
				if dsk is None: dsk = {}
				year = info.get('tm','').split('-')[0].strip() #"tm": "2020-11-04 16:31:06"
				rid, uid,score = info.get('rid',0), info.get('uid',0), dsk.get('info',{}).get("final_score",0) # read score from info? 
				if redis.r.exists(f"htxt:rid-{rid}:uid-{uid}"): continue  # added 20230724
				if sid % 100 == 0 : print (sid, uid, rid, score , flush=True)
				docs = [spacy.from_json(spa) for spa in sntspacys if spa]
				if info and docs: 
					redis.r.hset(f"htxt:rid-{rid}:uid-{uid}", mapping=dict(info, **{"snts": json.dumps([d.text.strip() for d in docs])  })) # "dim": json.dumps(dsk.get('doc',{})), 'kw': json.dumps(dsk.get('kw',{})), 'info': json.dumps(dsk.get('info',{}))
				for doc in docs:
					snt = doc.text.strip()
					if not redis.r.hexists(f"hsnt:{snt}", 'spacy'): 
						redis.r.hset(f"hsnt:{snt}", "spacy", json.dumps(doc.to_json()), mapping={"tc":len(doc),"snt":snt})

				if dsk: 
					for arsnt in dsk.get('snt',[]): 
						meta = arsnt.get('meta',{}) 
						snt  = meta.get('snt','').strip() 
						if snt and not redis.r.exists(f"hsnt:{snt}"):
							redis.r.hset(f"hsnt:{snt}", mapping={ k:v if isinstance(v, str) else json.dumps(v) for k,v in meta.items()} )
							[ redis.r.hset(f"hsnt:{snt}",  f"fd:{kp}", json.dumps(cate)) for kp, cate in arsnt.get('feedback',{}).items() ]

				redis.r.zadd(f"riduid:{rid}", {uid: score} ) #redis.r.zadd(f"{name}:rids",{rid: score} ) 
				redis.r.zadd(f"uidrid:{uid}", {rid: score} )
				redis.r.zincrby(f"rids:{name}", 1, rid) 
				redis.r.zincrby(f"rids:{name}-{year}", 1, rid) #redis.r.zadd(f"{name}-{year}:rid:{rid}", {uid: score} ) #verbose, redis.r.sadd(f"{name}-{year}:rids",rid) # corpus name 
			except Exception as e: 
				print ("ex:", e, "\t|",  line[0:50]) 
				exc_type, exc_value, exc_obj = sys.exc_info() 	
				traceback.print_tb(exc_obj)

		print ("finished loading:", infile, redis.r)

	def loaddis(self, infile, refresh:bool=False):
		''' dis=dsk, info, spacy => htxt:rid-2216475:uid-24427507 '''
		name = infile.split('.')[0]  # nju 
		if refresh: [redis.r.delete(k) for k in redis.r.keys(f"rids:{name}*")]

		print (name, infile, redis.r, flush=True)
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): #for line in open(infile,'r').readlines():
			try:
				arr = json.loads(line) 
				info, dsk, spa = arr['info'], arr['dsk'], arr.get('spacy','')
				year = info.get('tm','').split('-')[0].strip() #"tm": "2020-11-04 16:31:06"
				rid, uid,score = info.get('rid',0), info.get('uid',0), dsk.get('info',{}).get("final_score",0)
				tdoc = spacy.from_json(spa) if spa else spacy.nlp(info.get('essay','')) # updated 2023.7.24
				redis.r.hset(f"htxt:rid-{rid}:uid-{uid}", mapping=dict(info, **{"snts": json.dumps([sp.text.strip() for sp in tdoc.sents]) , "dim": json.dumps(dsk.get('doc',{})), 'kw': json.dumps(dsk.get('kw',{})), 'info': json.dumps(dsk.get('info',{})) }))
				for sp in tdoc.sents:
					snt = sp.text.strip()
					if not redis.r.hexists(f"hsnt:{snt}", 'spacy'): 
						redis.r.hset(f"hsnt:{snt}", "spacy", json.dumps(sp.as_doc().to_json()), mapping={"tc":len(sp),"snt":snt})#redis.r.hset(f"htxt:rid-{rid}:uid-{uid}", mapping={ k:v if isinstance(v, str) else json.dumps(v) for k,v in dsk.get('info',{}).items() } ) # flat cate_score_default

				for arsnt in dsk.get('snt',[]): 
					meta = arsnt.get('meta',{}) 
					snt  = meta.get('snt','').strip() 
					if snt and not redis.r.exists(f"hsnt:{snt}"):
						redis.r.hset(f"hsnt:{snt}", mapping={ k:v if isinstance(v, str) else json.dumps(v) for k,v in meta.items()} )
						[ redis.r.hset(f"hsnt:{snt}",  f"fd:{kp}", json.dumps(cate)) for kp, cate in arsnt.get('feedback',{}).items() ]

				redis.r.zadd(f"riduid:{rid}", {uid: score} ) #redis.r.zadd(f"{name}:rids",{rid: score} ) 
				redis.r.zadd(f"uidrid:{uid}", {rid: score} )
				redis.r.zincrby(f"rids:{name}", 1, rid) 
				redis.r.zincrby(f"rids:{name}-{year}", 1, rid) #redis.r.zadd(f"{name}-{year}:rid:{rid}", {uid: score} ) #verbose, redis.r.sadd(f"{name}-{year}:rids",rid) # corpus name 
			except Exception as e: 
				print ("ex:", e, "\t|",  line[0:30]) 
				exc_type, exc_value, exc_obj = sys.exc_info() 	
				traceback.print_tb(exc_obj)

		print ("finished loading:", infile, redis.r)

#util()
def lem_keyness(rel:str="LEMPOS", lem:str='book', src:str="sino", tgt:str="dic"): 
	dic1    = dict(redis.r.zrevrange(f"{src}:{rel}:{lem}", 0, -1, True))
	dic2    = dict(redis.r.zrevrange(f"{tgt}:{rel}:{lem}", 0, -1, True))
	print ( dic1, dic2) 
	sum1	= zscore(f"{src}:LEM|{lem}")
	sum2	= zscore(f"{tgt}:LEM|{lem}")
	words	= set( list(dic1.keys()) + list(dic2.keys()) )
	rows	= {f"{lem}:{w}" : likelihood(dic1.get(w,0), dic2.get(w,0), sum1, sum2 ) for w in words }
	return rows 	#redis.r.zdd(f"keyness:{src}-{tgt}:{rel}", rows) 
#print( lem_keyness() )

if __name__ == '__main__':
	fire.Fire(util) #if not 'Windows' in platform.system() else util().hello("gzjc") 

'''
htxt:inau:#  = txtnum /snts 
htxt:inau:1
hsnt:inau:1.1   => keys("hsnt:inau:1.*") , all the snts of the given txt 
hsnt:inau:{snt}

htxt:rid-{rid}:uid-{uid}  iterate by txt, dsk/ kw, dim, snts    gzjc: iterate by sentence, hsnt:gzjc:2 
hsnt:{snt}  / nju:hsnt:{snt}
rid:{rid} = {uid:score} zset
uid:{uid}  = {rid:tm}  zset
nju:rids       {rid:tm}   => htxt:rid-{rid}:uid-* 
nju-2020:rids  zset{rid:tm}  -- a corpus name   gzjc:NOUN:force:vpn/nju:NOUN:force:vpn/nju-2020:NOUN:force:vpn/ 230537,230538:NOUN:force:vpn


files:  docker run -it --rm --name tt -v /data/cikuu/bin:/app wrask/benepar python /app/sntkvr.py beneparsnt gzjc 

docker run -it --rm --name tt -v /data/cikuu/bin:/app wrask/flair python /app/sntkvr.py flairsnt gzjc

sntvec: docker run --name=dic --volume=/data/cikuu/entry/flair:/flair --restart=no --runtime=runc -t wrask/flair python /flair/flair-snt.py dic --port 6666

{"k": "hsnt:gzjc:0", "t": "hash", "v": {"snt": "`` Who wants to be a Millionaire ?", "spacy": "{\"text\": \"`` Who wants to be a Millionaire ?\", \"ents\": [], \"sents\": [{\"start\": 0, \"end\": 34}], \"tokens\
": [{\"id\": 0, \"start\": 0, \"end\": 1, \"tag\": \"``\", \"pos\": \"PUNCT\", \"morph\": \"PunctSide=Ini|PunctType=Quot\", \"lemma\": \"`\", \"dep\": \"punct\", \"head\": 3}, {\"id\": 1, \"start\": 1, \"end\": 
2, \"tag\": \"``\", \"pos\": \"PUNCT\", \"morph\": \"PunctSide=Ini|PunctType=Quot\", \"lemma\": \"`\", \"dep\": \"punct\", \"head\": 3}, {\"id\": 2, \"start\": 3, \"end\": 6, \"tag\": \"WP\", \"pos\": \"PRON\", 
\"morph\": \"\", \"lemma\": \"who\", \"dep\": \"nsubj\", \"head\": 3}, {\"id\": 3, \"start\": 7, \"end\": 12, \"tag\": \"VBZ\", \"pos\": \"VERB\", \"morph\": \"Number=Sing|Person=3|Tense=Pres|VerbForm=Fin\", \"l
emma\": \"want\", \"dep\": \"ROOT\", \"head\": 3}, {\"id\": 4, \"start\": 13, \"end\": 15, \"tag\": \"TO\", \"pos\": \"PART\", \"morph\": \"\", \"lemma\": \"to\", \"dep\": \"aux\", \"head\": 5}, {\"id\": 5, \"st
art\": 16, \"end\": 18, \"tag\": \"VB\", \"pos\": \"AUX\", \"morph\": \"VerbForm=Inf\", \"lemma\": \"be\", \"dep\": \"xcomp\", \"head\": 3}, {\"id\": 6, \"start\": 19, \"end\": 20, \"tag\": \"DT\", \"pos\": \"DE
T\", \"morph\": \"Definite=Ind|PronType=Art\", \"lemma\": \"a\", \"dep\": \"det\", \"head\": 7}, {\"id\": 7, \"start\": 21, \"end\": 32, \"tag\": \"NNP\", \"pos\": \"PROPN\", \"morph\": \"Number=Sing\", \"lemma\
": \"Millionaire\", \"dep\": \"attr\", \"head\": 5}, {\"id\": 8, \"start\": 33, \"end\": 34, \"tag\": \".\", \"pos\": \"PUNCT\", \"morph\": \"PunctType=Peri\", \"lemma\": \"?\", \"dep\": \"punct\", \"head\": 3}]
}\n", "tc": "9"}}


127.0.0.1:6666> hkeys "txt-spacy:spider:321023"
 1) "chanel"
 2) "description"
 3) "did"
 4) "doc_txt"
 5) "domain"
 6) "id"
 7) "pub_date"
 8) "spacy"
 9) "tag"
10) "title"
11) "url"

ubuntu@essaydm:/data/tmp$ python sntkvr.py txtspacy spider.ag.docjsonlg.3.4.1.gz 
Redis<ConnectionPool<Connection<host=172.17.0.1,port=6666,db=0>>>
txt-spacy started: spider  ->  Redis<ConnectionPool<Connection<host=172.17.0.1,port=6666,db=0>>>
spider.ag.docjsonlg.3.4.1.gz is finished, 	| using:  987.595950126648

127.0.0.1:6666> hgetall txt-spacy
1) "spider"
2) "169037"

def docs(name:str='gzjc'):
	import spacy 
	if not hasattr(spacy, 'nlp'):
		spacy.nlp		= spacy.load(os.getenv('spacy_model','en_core_web_sm')) # 3.5.0
		spacy.from_json = lambda arr: spacy.tokens.Doc(spacy.nlp.vocab).from_json(arr) # added 2022.8.19
	for k in redis.r.keys(f"snt-spacy:{name}:*"):
		v = redis.r.get(k)  #redis.r.hget(k, 'spacy')
		if not v: continue 
		arr = json.loads(v.strip()) 
		doc = spacy.from_json(arr) 
		yield doc 

def snts(name:str='gzjc'):
	for i in range(redis.r.zcard(f"sntzset:{name}")): 
		snts = redis.r.zrange(f"sntzset:{name}", i, i)
		if snts: yield i, snts[0] 

def snts(name:str='gzjc'):
	num = redis.r.llen(f"sntlist:{name}")
	for i in range(num): 
		snts = redis.r.lrange(f"sntlist:{name}", i, i)
		if snts: yield i, snts[0] 

def sntdoc(snt, name:str='gzjc'):
	v = redis.r.get(f"snt-spacy:{name}:{snt}")  
	return spacy.from_json(json.loads(v) )  if v else None 

	def sntspacy(self, infile):
		name = infile.split('/')[-1].split('.')[0] # ./sci.jsonlg.3.4.1.gz
		print ("snt-spacy started:", name ,  ' -> ',  redis.r, flush=True)
		[ redis.r.delete(k) for k in redis.r.keys(f"snt-spacy:{name}:*")]
		start = time.time()
		redis.r.hset("snt-spacy", name, 0) 
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): #356317 docs of each doc file
			try:
				arr = json.loads(line.strip()) 
				doc = spacy.from_json(arr) 
				snt = doc.text.strip()
				redis.r.hincrby("snt-spacy", name) 
				redis.r.setnx(f"snt-spacy:{name}:{snt}", line) #avoid a super large key 
			except Exception as e:
				print ("ex:", e, sid, line[0:30]) 
				exc_type, exc_value, exc_traceback_obj = sys.exc_info()
				traceback.print_tb(exc_traceback_obj)
		print ("snt-spacy finished:", infile) 

	def sntzset(self, infile):
		#sntzset:gzjc,   sntzset:gzjc:spacy:0,  .. 2023.7.9 ,upgrade version of snt-spacy 
		name = infile.split('/')[-1].split('.')[0] # ./sci.jsonlg.3.4.1.gz
		print ("sntzset started:", name ,  ' -> ',  redis.r, flush=True)
		[ redis.r.delete(k) for k in redis.r.keys(f"sntzset:{name}:*")]
		start = time.time()
		for sid, line in enumerate(fileinput.input(infile,openhook=fileinput.hook_compressed)): #356317 docs of each doc file
			try:
				doc = spacy.from_json(json.loads(line.strip())) 
				snt = doc.text.strip()
				if redis.r.zadd(f"sntzset:{name}", {snt: sid}) > 0 : # sid is INT
					redis.r.setnx(f"sntzset:{name}:spacy:{sid}", line) #avoid a super large key 
			except Exception as e:
				print ("ex:", e, sid, line[0:30]) 
		redis.r.hset("sntzset", name, redis.r.zcard(f"sntzset:{name}")) 
		print ("sntzset finished:", infile, " using: ", time.time() - start) 

	def flairsnt(self, name , refresh:bool=True,batch:int=100) :  # to be deleted later 
		# docker run -it --rm --name tt -v /data/cikuu/bin:/app wrask/flair python /app/sntkvr.py flairsnt gzjc  
		# rediscmd dump flair-gzjc.ktv --pattern flair:gzjc:* 
		print ("flairsnt sntzset started:", name ,  ' -> ',  redis.r, flush=True)
		if refresh: [ redis.r.delete(k) for k in redis.r.keys(f"flair:{name}:*")]
		print ( 'finished deleting:', name, flush=True) 
		for i,snt in snts(name): 
			if i % batch == 0 : print (i, snt, flush=True) 
			res = frame_snt(snt) 
			for row in res.get('all labels', []): 
				redis.r.hset( f"flair:{name}:{i}", row['value'], row['confidence'])
				redis.r.zincrby( f"flair:{name}:LEM:{row['value'].split('.')[0]}", 1, row['value']) 
		print ('flairsnt finished:', name) 

def keyness(src:str="sino:LEMPOS:book", vs:str="endic:LEMPOS:book", srcsum:str=None, vssum:str=None, outer:bool = True, critical:float=3.84): 
	dic1    = dict(redis.r.zrevrange(src, 0, -1, True))
	dic2    = dict(redis.r.zrevrange(vs, 0, -1, True))
	sum1	= dic1.get("_sum", sum( [i for s,i in dic1.items()]) ) + 0.000001
	sum2	= dic2.get("_sum", sum( [i for s,i in dic2.items()]) ) + 0.000001
	words	= set( list(dic1.keys()) + list(dic2.keys()) ) if outer else dic1.keys()
	rows	= [ {"word": w, "src": src.get(w,0), "refer": refer.get(w,0), "src%": round(src.get(w,0)/sum1,4), "refer%": round(refer.get(w,0)/sum2,4), 
				"keyness": likelihood(src.get(w,0), refer.get(w,0), sum1, sum2 )} for w in words if not w.startswith('_sum') ] #_look forward to _VBG
	rows.sort(key=lambda a:a['keyness']) # reverse 
	return {"src": src, "refer": refer, "sum1": sum1, "sum2":sum2, "data": rows }  if verbose else rows
'''