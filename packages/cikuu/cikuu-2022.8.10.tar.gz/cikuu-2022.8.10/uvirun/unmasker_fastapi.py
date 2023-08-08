# 2022.6.30  #uvicorn trf_unmasker_fastapi:app --reload --port 80 --host 0.0.0.0
from uvirun import *

@app.get('/unmasker', tags=["unmasker"])
def unmasker(q:str="The goal of life is *.", model:str='native', topk:int=10, verbose:bool=False): 
	''' model: native/nju/fengtai/sino/sci/gblog/twit	'''
	from transformers import pipeline
	if not hasattr(unmasker, model): 
		setattr(unmasker, model, pipeline('fill-mask', model=f'/data/model/unmasker/distilbert-base-uncased-{model}') )
	arr = getattr(unmasker, model)(q.replace('*','[MASK]'), top_k = topk) #result: [{'score': 0.03619174659252167, 'token': 8404, 'token_str': 'happiness', 'sequence': 'the goal of life is happiness.'}, {'score': 0.030553610995411873, 'token': 7691, 'token_str': 'survival', 'sequence': 'the goal of life is survival.'}, {'score': 0.016977205872535706, 'token': 12611, 'token_str': 'salvation', 'sequence': 'the goal of life is salvation.'}, {'score': 0.016698481515049934, 'token': 4071, 'token_str': 'freedom', 'sequence': 'the goal of life is freedom.'}, {'score': 0.015267301350831985, 'token': 8499, 'token_str': 'unity', 'sequence': 'the goal of life is unity.'}]
	return [ dict( row, **{"name": model}) for row in arr ] if verbose else [ {"name": model, "word": row["token_str"], "score": round(row["score"], 4)} for row in arr ]

@app.get('/cloze', tags=["unmasker"])
def cloze(q:str="The goal of life is *.", model:str='native', topk:int=10): 
	''' model: native/nju/fengtai/sino/sci/gblog/twit, 2023.1.13	'''
	rows = unmasker(q, model, topk, True)
	return {"body": q, "model":model, "topk":topk, "data": [ {"name": row["token_str"], "value": round(row["score"], 4)} for row in rows ] }

@app.get('/unmasker/single', tags=["unmasker"])
def unmasker_single(body:str="Parents * much importance to education.", options:str="attach,pay,link,apply", sepa:str=",", model:str='native', topk:int=1000): 
	'''  2022.8.6 '''
	rows = unmasker(body,  model=model, topk=topk)
	arr  = options.strip().split(sepa) 
	#return {"rank": [ (row['word'], row['score'], i+1) for i, row in enumerate(rows) if row['word'] in arr ], "cands": rows}
	return {"rank": [ {"word":row['word'], "prob": 100 * row['score'], "rank":i+1} for i, row in enumerate(rows) if row['word'] in arr ], "cands": rows}

@app.get('/unmaskers', tags=["unmasker"])
def unmaskers(q:str="The goal of life is *.", models:str='native,nju', topk:int=10): 
	''' model: native/nju/fengtai/sino/sci/gblog/twit  2022.7.1 '''
	arr = []
	[ arr.extend(unmasker(q, model, topk)) for model in models.strip().split(',') ]
	return arr

@app.get('/unmasker/html', response_class=HTMLResponse)
def unmasker_html(q:str="The goal of life is *.", model:str='native', topk:int=10): 
	''' return HTML <ol><li> , 2022.7.23 '''
	rows = unmasker(q, model, topk) 
	maxscore = rows[0]['score'] + 0.01 # font-weight: 100, 200, ..., 900
	snts = "\n".join([f"<li><span style='font-weight:{int(10*row['score']/maxscore)}00'>{row.get('word','')}<span></li>" for row in rows])
	return HTMLResponse(content=f"<ol>{snts}</ol>")

from functools import lru_cache
@lru_cache(maxsize=128)
def pos_dic(pos:str='VBD'):
	return requests.get(f"http://files.jukuu.com:8001/static/yulk/lemset-{pos}.json").json()

@app.get('/snt/cloze', tags=["unmasker"])
def snt_cloze(snt:str="Parents * much importance to education.", word:str='attached', pos:str='VBD', model:str='native', topk:int=1000): 
	''' model: native/nju/fengtai/sino/sci/gblog/twit, 2023.2.27	'''
	rows	= unmasker(snt, model, topk, True)
	words	=  { row["token_str"] : round(row["score"], 4) for row in rows }
	posdic	= pos_dic(pos) 
	posw	= {s:i for s,i in words.items() if s in posdic}

	cands = requests.post(f"http://cpu76.wrask.com:8002/gensim/distance/words?src={word}",json=[s for s,i in posw.items()]).json() #[{'word': 'have', 'distance': 0.8523787260055542},
	cands.sort(key=lambda a:a['distance'])
	return [ dict(row, **{"score": posw.get(row['word'],0) })  for row in cands]

if __name__ == '__main__': #print (models['native']("The goal of life is [MASK]."))
	print(unmasker_single())