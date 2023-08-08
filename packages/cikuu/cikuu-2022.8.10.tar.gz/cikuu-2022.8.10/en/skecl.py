# 2023.7.26
from cikuu.pypi.en.encommon import *  

def run(name, model:str=spacy_model, overwrite:bool=False, batch:int=10000): 
	''' name: gzjc/clec, 2023.7.23 ''' 
	r = rcon(kvryulk) 
	parser	= nlp(model)
	start = time.time()
	print ( 'skecl started:', name, flush=True ) 
	for i in range(int(r.get(f"hsnt:{name}:#"))): 
		try: 
			if i % batch == 0: print ( f"[{name}] i=", i, " |tim=", round(time.time() - start, 2) , flush=True)
			if overwrite or not r.hexists(f"hsnt:{name}:{i}", "skecl"): # resumable 
				spa = r.hget(f"hsnt:{name}:{i}", 'spacy')
				doc = parse(spa)
				doc = merge_np(doc)
				doc = merge_np_and_np(doc,parser)
				doc = merge_np_of_np(doc, parser)
				doc = merge_cl(doc)
				skecl = "_^ " + ' '.join([ skecl_tok(t) for t in doc])
				r.hset(f"hsnt:{name}:{i}", "skecl", skecl )
		except Exception as ex:
			print ( ">>walk ex:", ex, "\t", i, flush=True)
			exc_type, exc_value, exc_obj = sys.exc_info() 	
			traceback.print_tb(exc_obj)
	print ( 'skecl finished:', name, flush=True ) 

def test():
	parser	= nlp()
	doc = parser('Benjamin was forced to admit what he had been doing.')
	doc = merge_np(doc)
	doc = merge_np_and_np(doc,parser)
	doc = merge_np_of_np(doc, parser)
	doc = merge_cl(doc)
	skecl = "_^ " + ' '.join([ skecl_tok(t) for t in doc])
	print (skecl)

if __name__ == "__main__": #[{'q': '_be _ADJ* with', '*': 'angry', 'pos': 'ADJ', 'tag': 'JJ', 'chunk': 'am angry with'}]
	fire.Fire(run) # run('gzjc') 