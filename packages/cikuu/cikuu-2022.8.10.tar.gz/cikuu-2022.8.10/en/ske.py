# 2023.7.20  REGEX   *self, *ing   _fate _be _ADJ/_VBN/_NP/_VBG/that   move to wrapper/spacyskemather.py,  this copy to be deleted later 
import json,os,time

# considering the possibilty that |  justice denied is justice delayed  |  There is no compression algorithm on user experience. 
rules ={ # ske-rules
"mtlp:1": [ {"LEMMA": "be", "TAG": {"NOT_IN": ["VBN","VBG"]}}, {"POS": "VERB", "TAG": {"IN": ["VBN"]}}, {"LEMMA": "to"},{"TAG": "VB"},],  # _be _VBN* to _VERB
"pelt:0": [ {"POS": "VERB", "TAG": {"NOT_IN": ["VBN"]}}, {"ENT_TYPE": "NP"},{"POS": "ADP"},{"TAG": "VBG"},], # _VERB* _NP from _VBG
"plele": [ {"POS": "VERB", "TAG": {"NOT_IN": ["VBN"]}}, {"POS": "ADP"}, {"ENT_TYPE": "NP"},{"POS": "ADP"},{"ENT_TYPE": "NP"},],  # _VERB* from _NP to _NP
"tmt": [ {"TAG": "VBG"}, {"LEMMA": "be", "TAG": {"NOT_IN": ["VBN","VBG"]}}, {"TAG": "VBN"}], # smoking is banned 
}

def vpat(snt:str="I varied from the box to the table, and I stop the box from leaving, and I am forced to go there."):
	''' [{'q': '_VERB* from _NP to _NP', '*': 'vary', 'pos': 'VERB', 'tag': 'VBD'}, {'q': '_VERB* _NP from _VBG', '*': 'stop', 'pos': 'VERB', 'tag': 'VBP'}, {'q': '_be _VBN* to _VERB', '*': 'force', 'pos': 'VERB', 'tag': 'VBN'}] '''
	import spacy,requests
	from spacy.matcher import Matcher
	if not hasattr(spacy,'nlp'): 
		spacy.nlp	= spacy.load("en_core_web_sm")
		spacy.matcher = Matcher(spacy.nlp.vocab)
		for n, p in requests.get("http://api.jukuu.com/kvr-hgetall",params={"key":"config:ske-rules"}).json().items():
			try:
				rule = eval(p)
				spacy.matcher.add(n.split('#')[0].strip(), [rule]) 
			except Exception as ex:
				print ( ">>ske-rules ex:", ex, "\t", n, p, flush=True) 

	def merge_np(doc):
		with doc.retokenize() as retokenizer:
			for np in doc.noun_chunks:
				attrs = {"tag": np.root.tag, "dep": np.root.dep, "ent_type": "NP", "lemma":doc[np.end-1].lemma} # , "lemma":doc[np.end-1].lemma | added 2022.7.26
				retokenizer.merge(np, attrs=attrs) 
		return doc

	def hyb(doc, start, pat): #m:lemma l:kex  p:pos t:tag , e:ent_type 
		arr = []
		for i,c in enumerate(pat): 
			if c == 'm':	arr.append('_' + doc[start +i].lemma_)
			elif c == 'p':	arr.append('_' + doc[start +i].pos_)
			elif c == 't':	arr.append('_' + doc[start +i].tag_)
			elif c == 'e':	arr.append('_' + doc[start +i].ent_type_)
			elif c == 'l':	arr.append(doc[start +i].text.lower())
			else :			arr.append(doc[start +i].text.lower())
		return arr #' '.join(arr) 

	doc = spacy.nlp(snt)
	doc = merge_np(doc)
	
	rows = []
	for name, ibeg,iend in spacy.matcher(doc):
		tag			= spacy.nlp.vocab[name].text
		offset		= int(tag.split(':')[-1]) if ':' in tag else 0 
		arr			= hyb(doc, ibeg, tag.split(':')[0] )
		arr[offset] = arr[offset] + '*'
		rows.append({"chunk": doc[ibeg:iend].text, 'q': ' '.join(arr), '*': doc[ibeg+offset].lemma_ , 'pos':doc[ibeg+offset].pos_, 'tag':doc[ibeg+offset].tag_}) 
	return rows 

if __name__	== '__main__': 
	print ( vpat()) 


kp_rules = {
"Vend":[[{"POS": {"IN": ["AUX","VERB"]}},{"POS": {"IN": ["ADV"]}, "OP": "*"}, {"POS": {"IN": ["ADJ","VERB"]}, "OP": "*"},{"POS": {"IN": ["PART","ADP","TO"]}, "OP": "*"},{"POS": 'VERB'}]], # could hardly wait to meet
"vp":  [[{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ"]}, "OP": "*"},{"POS": 'NOUN'}, {"POS": {"IN": ["ADP","TO"]}, "OP": "*"}], [{'POS': 'VERB'},{"POS": {"IN": ["DET","ADP","ADJ","TO","PART"]}, "OP": "*"},{"POS": 'VERB'}]], # wait to meet
"pp":  [[{'POS': 'ADP'},{"POS": {"IN": ["DET","NUM","ADJ",'PUNCT','CONJ']}, "OP": "*"},{"POS": {"IN": ["NOUN","PART"]}, "OP": "+"}]],    
"ap":  [[{"POS": {"IN": ["ADV"]}, "OP": "+"}, {"POS": 'ADJ'}]],  
"vprt":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'TO']}, "OP": "+"}]],   # look up /look up from,  computed twice
"vtov":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'TO'},{"TAG": 'VB'}]],   # plan to go
"vvbg":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"TAG": 'VBG'}]],   # consider going
"vpg":	[[{"POS": 'VERB', "TAG": {"NOT_IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}, "OP": "+"},{"TAG": 'VBG'}]],   # insisted on going
"be_vbn_p": [[{'LEMMA': 'be'},{"TAG": {"IN": ["VBN"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]],   # base:VERB:be_vbn_p:be based on   
"be_adj_p": [[{'LEMMA': 'be'},{"POS": {"IN": ["ADJ"]}}, {"POS": {"IN": ["PREP", "ADP",'PART']}}]],   # be angry with
} #for name, ibeg,iend in matcher(doc) : print(spacy.nlp.vocab[name].text, doc[ibeg:iend].text)


'''
def kp_matcher(doc): #[('vend', 'consider going', 1, 3), ('vp', 'consider going', 1, 3), ('vvbg', 'consider going', 1, 3), ('vprt', 'going to', 2, 4)]
	if not hasattr(kp_matcher, 'matcher'): 
		kp_matcher.matcher = Matcher(spacy.nlp.vocab)
		[kp_matcher.matcher.add(name, patterns,  greedy ='LONGEST') for name, patterns in kp_rules.items() ]
	tups = set()  # remove the duplicated entries 
	[tups.add( kp_span(doc,ibeg,iend, spacy.nlp.vocab[name].text) ) for name, ibeg,iend in kp_matcher.matcher(doc)] 
	return tups

_verbnet_rules = {  # :1 , verb's offset 
	"NP V:1": [[NP_start,VERB, PUNCT]], 
	"NP of NP V:3": [[ NP_start,{"LEMMA": "of"}, {"ENT_TYPE": "NP"}, VERB,PUNCT]], 
	"NP V NP:1": [[NOUN,VERB, NOUN,{"POS": {"IN": ["PUNCT"]}}]], 
	"NP V NP ADJ:1": [[NOUN,VERB, NOUN,{"POS": {"IN": ["ADJ"]}}]], 
	"NP V NP NP:1": [[NOUN,VERB, NOUN,NOUN]], 
	"NP V NP-Dative NP:1": [[NOUN,VERB, {"DEP": {"IN": ["dative"]}},NOUN]], 
	"NP V NP PP:1": [[NOUN,VERB, NOUN,{"DEP": {"IN": ["prep"]}}]], 
	"NP V NP PP PP:1": [[NOUN,VERB, NOUN,{"DEP": {"IN": ["prep"]}}, NOUN,{"DEP": {"IN": ["prep"]}}, NOUN]], 
	"NP V S_ING:1": [[NOUN,VERB, {"TAG": {"IN": ["VBG"]}}]], 
	"NP V whether/how S_INF:1": [[NOUN,VERB, {"LEMMA": {"IN": ["whether","how"]}}, {"LEMMA": {"IN": ["to"]}}, VERB]], 
	"NP V NP to be NP:1": [[NOUN,VERB, {"LEMMA": {"IN": ["to"]}}, {"LEMMA": {"IN": ["be"]}}, NOUN]], 
	"NP V that/how S:1": [[NOUN,VERB, {"LEMMA": {"IN": ["that","how"]}, "OP":"*"}, NOUN, {"POS": {"IN": ["AUX","PART"]}, "OP":"*"},{"DEP": {"IN": ["ccomp"]}}]],  #They considered that he was the professor.
	"NP V whether/if S:1": [[NOUN,VERB, {"LEMMA": {"IN": ["whether","if"]}}, NOUN,{"POS": {"IN": ["AUX","PART"]}, "OP":"*"}, {"DEP": {"IN": ["ccomp"]}}]],  #He considered whether he should come.
	"NP V what S:1": [[NOUN,VERB, {"LEMMA": {"IN": ["what"]}}, NOUN,{"POS": {"IN": ["AUX","PART"]}, "OP":"*"}, {"DEP": {"IN": ["ccomp"]}}]],  
	"NP V what S_INF:1": [[NOUN,VERB, {"LEMMA": {"IN": ["what"]}}, {"LEMMA": {"IN": ["to"]}},VERB]],
}
def verbnet_matcher(doc): 
	if not hasattr(verbnet_matcher, 'matcher'): 
		verbnet_matcher.matcher = Matcher(spacy.nlp.vocab)
		[ verbnet_matcher.matcher.add(name, patterns, greedy ='LONGEST')  for name, patterns in _verbnet_rules.items() ]
	merge_np(doc)
	merge_vp(doc)
	res = []
	for name, ibeg, iend in verbnet_matcher.matcher(doc):
		try:
			arr = spacy.nlp.vocab[name].text.split(':') 
			verb_i = ibeg + int(arr[-1]) 
			res.append( (verb_i, ibeg, iend, arr[0].strip()) ) 
		except Exception as e:
			print ('verbnet ex:', e, name, ibeg, iend)
	return res 

ske_rules = requests.get("http://api.jukuu.com/kvr-hgetall",params={"key":"config:ske-rules"}).json() 
print(ske_rules)

'''