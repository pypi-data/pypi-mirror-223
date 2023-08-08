# 2022.6.30 | pip install transformers torch  | 
from uvirun import *
import re, os, json, math #torch
model	= os.getenv('gec_model', "/grammar_error_correcter_v1")
device	= int ( os.getenv('gec_cuda', -1) )

token_split	= lambda sent: re.findall(r"[\w']+|[.,!?;]", sent) # return list
def common_perc(snt="She has ready.", trans="She is ready."): 
	toks = set(token_split(snt))
	return len([t for t in token_split(trans) if t in toks]) / (len(toks)+0.01)

@app.post('/gec', tags=["gec"])
def gecsnts(snts:list=["She has ready.","It are ok."],  max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5):
	''' LOCAL version 
	batch_size needs to be used on the pipe call, not on the pipeline call. |https://github.com/huggingface/transformers/issues/14613
	return {'She has ready.': 'She is ready.'}, 'It are ok.': 'It is ok.'}	'''
	from transformers import pipeline #None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.

	if not hasattr(gecsnts, 'pipe'): gecsnts.pipe = pipeline("text2text-generation", model=model, device=device)
	snts = [snt for snt in snts if snt.count(' ') + 10 < max_length ] # skip extra long sents 	# check the extreme long sent ?  truncate it ? 2022.4.3 
	dic = {} #{'hello world': 'Hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello', 'I am ok.': 'I am ok.'}
	sntslen = len(snts) 
	offset = 0 
	while offset < sntslen: # added 2022.4.5
		for snt, tgt in zip(snts, gecsnts.pipe(snts[offset:offset + batch_size],  max_length=max_length, do_sample=do_sample, batch_size=batch_size)):
			trans = tgt['generated_text']  # todo : if token change > 50% , skip the trans
			if not ' ' in trans or not ' ' in snt.strip(): # ' ' => "generated_text": "Then, a few years later, the saga began."
				dic[snt] = snt # keep unchanged
			elif common_perc(snt, trans) < unchanged_ratio or abs(math.log( len(snt)/len(trans))) > len_ratio:
				dic[snt] = snt # changed too much, -> discard 
			else:
				dic[snt] = trans
		offset = offset + batch_size
	return dic

@app.get('/gec', tags=["gec"])
def gecsnts_get(snt:str="She has ready.", max_length:int=128,  do_sample:bool=False, batch_size:int=64, unchanged_ratio:float=0.45, len_ratio:float=0.5):
	''' # [{'snt': 'She has ready.', 'trans': 'She is ready.', 'changed': True}], based on local model, no REDIS '''
	dic = gecsnts( [snt], max_length,  do_sample, batch_size, unchanged_ratio, len_ratio)
	return [ { 'snt': snt, 'trans': dic.get(snt,snt), 'changed':  dic.get(snt,snt) != snt }]

@app.post('/xgec',tags=["gec"])
def xgec(snts:list=["She has ready.","It are ok."], host:str="192.168.201.120", port:int=6379, db:int=0, timeout:int=5): # put into the ufw white ip list 
	''' get {snt:tgt} from redis xadd/blpop, 2022.9.7 '''
	import redis
	if not hasattr(xgec, 'r'): xgec.r = redis.Redis(host=host,port=port, db=db, decode_responses=True)
	if not snts : return {}
	id  = xgec.r.xadd("xsnts", {"snts":json.dumps(snts)})
	res	= xgec.r.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
	return {} if res is None else json.loads(res[1])

if __name__ == "__main__":   #{'She has ready.': 'She is ready.', 'It are ok.': 'It is ok.'}
	print ( "local gecsnts",  gecsnts_get() )