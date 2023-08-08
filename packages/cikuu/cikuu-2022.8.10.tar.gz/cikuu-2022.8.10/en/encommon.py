# 2023.7.26, cp from skecl.py  
import os,json,fire,requests,spacy,sys,traceback
if not hasattr(spacy, 'nlp'):
	spacy.nlp		= spacy.load(os.getenv('spacy_model', 'en_core_web_sm')) # 3.4.1
	spacy.from_json = lambda arr: spacy.tokens.Doc(spacy.nlp.vocab).from_json(arr) # added 2022.8.19
	spacy.merge_nps	= spacy.nlp.create_pipe("merge_noun_chunks")

rules = {
"advp" : {'adv_adv': [[{"POS":"ADV", "TAG":"RB", "DEP":"advmod"}, {"POS":"ADV", "TAG":"RB"}]]}, 
}

def match(name, doc, ent_type:str='NP', offset:int=-1): 

	def new_matcher(rules_dic): 
		from spacy.matcher import Matcher
		matcher = Matcher(spacy.nlp.vocab)
		for n, p in rules_dic.items(): #requests.get("http://api.jukuu.com/kvr-hgetall",params={"key":'config:ske-rules'}).json().items():
			try:
				matcher.add(n.strip(), p) 
			except Exception as ex:
				print ( ">>rules ex:", ex, "\t", n, p, flush=True) 
		return matcher

	if not hasattr(match, name): 
		setattr(match, name, new_matcher(rules.get(name,{})) )
	
	def merge_by_matcher(doc, matcher, ent_type:str='NP', offset:int=-1): 
		with doc.retokenize() as retokenizer:
			for name, start, end in matcher(doc):
				try:
					idx = start + offset  if offset >= 0 else end + offset # when offset = -1
					attrs = {"tag": doc[idx].tag, "dep": doc[idx].dep, "ent_type": ent_type, "lemma":doc[idx].lemma} #"pos": doc[i].pos,
					retokenizer.merge(doc[start : end], attrs=attrs)
				except Exception as e:
					print ( "merge_by_matcher ex:", e , start, end)
					exc_type, exc_value, exc_obj = sys.exc_info() 	
					traceback.print_tb(exc_obj)
		return doc

	return merge_by_matcher(doc, getattr(match, name), ent_type, offset) 

def merge_np(doc):
	with doc.retokenize() as retokenizer:
		for np in doc.noun_chunks:
			attrs = {"tag": np.root.tag, "dep": np.root.dep, "ent_type": "NP", "lemma":doc[np.end-1].lemma} # , "lemma":doc[np.end-1].lemma | added 2022.7.26
			retokenizer.merge(np, attrs=attrs) 
	return doc

def merge_np_and_np(doc,nlp=spacy.nlp): #the fate of the passengers and crew was sealed.
	from spacy.matcher import Matcher
	if not hasattr(merge_np_and_np, 'matcher'):
		merge_np_and_np.matcher = Matcher(nlp.vocab)
		merge_np_and_np.matcher.add('np_and_np', [[{"ENT_TYPE":"NP"}, {"POS":"CCONJ", "TAG":"CC"}, {"ENT_TYPE":"NP","DEP":"conj"}], [{"ENT_TYPE":"NP"}, {"POS":"CCONJ", "TAG":"CC"}, {"ENT_TYPE":"NP","DEP":"conj"}, {"POS":"CCONJ", "TAG":"CC"}, {"ENT_TYPE":"NP","DEP":"conj"}] , [{"ENT_TYPE":"NP"}, {"POS":"CCONJ", "TAG":"CC"}, {"ENT_TYPE":"NP","DEP":"conj"}, {"POS":"CCONJ", "TAG":"CC"}, {"ENT_TYPE":"NP","DEP":"conj"}, {"POS":"CCONJ", "TAG":"CC"}, {"ENT_TYPE":"NP","DEP":"conj"}] ],  greedy ='LONGEST') 
	with doc.retokenize() as retokenizer:
		for name, start, end in merge_np_and_np.matcher(doc):
			try:
				attrs = {"tag": doc[start].tag, "dep": doc[start].dep, "ent_type": "NP", "lemma":doc[start].lemma} #"pos": doc[i].pos,
				retokenizer.merge(doc[start : end], attrs=attrs)
			except Exception as e:
				print ( "merge_np_and_np ex:", e , start, end, doc.text)
				exc_type, exc_value, exc_obj = sys.exc_info() 	
				traceback.print_tb(exc_obj)
	return doc


def merge_advp(doc,nlp=spacy.nlp): #After all, forced waiting requires patience.
	from spacy.matcher import Matcher
	if not hasattr(merge_advp, 'matcher'):
		merge_advp.matcher = Matcher(nlp.vocab)
		merge_advp.matcher.add('advp', [[{"POS":"ADV", "TAG":"RB", "DEP":"advmod"}, {"POS":"ADV", "TAG":"RB"}]],  greedy ='LONGEST') 
	with doc.retokenize() as retokenizer:
		for name, start, end in merge_advp.matcher(doc):
			try:
				attrs = {"tag": doc[end-1].tag, "dep": doc[end-1].dep, "ent_type": "ADVP", "lemma":doc[end-1].lemma} #"pos": doc[i].pos,
				retokenizer.merge(doc[start : end], attrs=attrs)
			except Exception as e:
				print ( "merge_advp ex:", e , start, end)
				exc_type, exc_value, exc_obj = sys.exc_info() 	
				traceback.print_tb(exc_obj)
	return doc

def merge_np_of_np(doc,nlp=spacy.nlp):
	from spacy.matcher import Matcher
	if not hasattr(merge_np_of_np, 'matcher'):
		merge_np_of_np.matcher = Matcher(nlp.vocab)
		merge_np_of_np.matcher.add("np-of-np", [[{"ENT_TYPE": "NP"}, {"LEMMA":"of"},{"ENT_TYPE": "NP"}], [{"ENT_TYPE": "NP"}, {"LEMMA":"of"},{"POS": "NOUN"}]], greedy ='LONGEST')
	with doc.retokenize() as retokenizer:
		for name, start, end in merge_np_of_np.matcher(doc):
			try:
				attrs = { "tag": doc[start].tag, "dep": doc[start].dep, "lemma":doc[start].lemma, "ent_type": "NP"} #"pos": doc[start].pos,
				retokenizer.merge(doc[start : end], attrs=attrs)
			except Exception as e:
				print ( "merge_np_of_np ex:", e , start, end)
	return doc

# last update: 2023.7.24 , add auxpass
def merge_cl(doc): # subtree of a verb is the clause , https://subscription.packtpub.com/book/data/9781838987312/2/ch02lvl1sec13/splitting-sentences-into-clauses
	with doc.retokenize() as retokenizer:
		for v in [t for t in doc if ( t.pos_ == 'VERB' or ( t.lemma_ == 'be' and t.tag_ not in ('VBN','VBG') )) and t.dep_ != 'ROOT'  and t.dep_ not in ('xcomp','auxpass') ] : # non-root /and t.tag_ != 'VBN' and len(t.subtree) > 1
			try:
				children = list(v.subtree)
				start = children[0].i  	
				end = children[-1].i 
				attrs = {"tag": v.tag, "dep": v.dep, "ent_type": "CL" + v.dep_ ,"lemma":v.lemma} # S.advcl ,  S.conj 
				retokenizer.merge(doc[start : end+1], attrs=attrs)
			except Exception as e:
				pass # print ( "merge_cl ex:", e, v, doc.text )
	return doc

def skecl_tok(t): 
	from dic.oneself import oneself 
	pair = f"_{t.ent_type_}" if t.ent_type_ else f"_{t.lemma_}_{t.pos_}_NP_{t.dep_}{t.head.i}" if (t.ent_type_ == 'NP' and t.lemma_ not in ('that','which')) else f"_{t.pos_}_{t.tag_}_{t.dep_}{t.head.i}" if t.pos_ in ('PROPN','NUM','X','SPACE','PUNCT') else f"{t.text if t.text in ('I') else t.text.lower()}_{t.lemma_}_{t.pos_}_{t.tag_}{oneself.get(t.text.lower(), '')}_{t.dep_}{t.head.i}"
	return pair 

def skecl(doc, mergenp:bool=True): 
	''' cp from cikuu/pypi/en/skecl.py ''' 
	try: 
		if mergenp: doc = merge_np(doc)
		doc = merge_np_and_np(doc)
		doc = merge_np_of_np(doc)
		doc = merge_cl(doc)
		return "_^ " + ' '.join([ skecl_tok(t) for t in doc])
	except Exception as e:
		print ( "skecl ex:", e, doc.text )
	return '' 

if __name__ == "__main__": #[{'q': '_be _ADJ* with', '*': 'angry', 'pos': 'ADJ', 'tag': 'JJ', 'chunk': 'am angry with'}]
	doc = spacy.nlp("Lucy discovers the winter land of Narnia where she and her two brothers and sister meet the White Witch .") #Would you like a cup of coffee?
	print ( skecl( doc)) 
