stoplist={',', '.', ';','"', "'",'!', '?', 'very','ourselves','am','doesn','through','me','against','up','just','her','ours','couldn','because','is','isn','it','only','in',
'such','too','mustn','under','their','if','to','my','himself','after','why','while','can','each','itself','his','all','once','herself','more',
'our','they','hasn','on','ma','them','its','where','did','ll','you','didn','nor','as','now','before','those','yours','from','who','was','m',
'been','will','into','same','how','some','of','out','with','s','being','t','mightn','she','again','be','by','shan','have','yourselves','needn',
'and','are','o','these','further','most','yourself','having','aren','here','he','were','but','this','myself','own','we','so','i','does','both',
'when','between','d','had','the','y','has','down','off','than','haven','whom','wouldn','should','ve','over','themselves','few','then','hadn',
'what','until','won','no','about','any','that','for','shouldn','don','do','there','doing','an','or','ain','hers','wasn','weren','above','a',
'at','your','theirs','below','other','not','re','him','during','which',
"\n", "\r", "\n\n"}

def feed_pika():
	import redis
	r = redis.Redis(host='dev.werror.com', db=0, port=8008,  decode_responses=True)
	for w in stoplist : r.sadd('stoplist', w )
	print("done")

if __name__ == '__main__': 
	import redis
	r = redis.Redis('files.jukuu.com', port=6666, decode_responses=True)
	[r.sadd('dict:stoplist', s) for s in stoplist] 