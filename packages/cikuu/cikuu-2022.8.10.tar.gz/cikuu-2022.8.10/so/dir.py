# 2023.8.1
import requests,time, fire,json, traceback,sys

def run(eshost:str='es.jukuu.com:9200', sql:str=None):
	''' python -m cikuu.pypi.so.dir  --sql "select count(*) from ~ where type='snt'"  '''
	rows = requests.post(f"http://{eshost}/_sql",json={"query": "show tables"}).json().get('rows',[]) 
	for row in rows: 
		if not row[1].startswith("."):  #['elasticsearch', 'sino', 'TABLE', 'INDEX'] 	 3062620
			print (row[1], "\t", requests.get(f"http://{eshost}/{row[1]}/_stats").json()['_all']['primaries']['docs']['count'] if sql is None else requests.post(f"http://{eshost}/_sql", json={"query":sql.replace('~',row[1])}).json().get('rows',[]) )

if __name__ == '__main__': 	
	fire.Fire(run)