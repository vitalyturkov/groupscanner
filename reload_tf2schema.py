import requests
import os
# manual check: http://api.steampowered.com/IEconItems_440/GetSchema/v0001/?key=xxx

def reload( key ):
	steam_api_key = key
	
	# cycle is a temporary solution here, don't know yet how to make this request work all the time
	# this way it tries 3 times with 15s timeout each time
	
	for i in range(3):
		try:
			r = requests.get('http://api.steampowered.com/IEconItems_440/GetSchema/v0001/', {'key':steam_api_key}, timeout = 15 )
			break
		except:
			if i < 2:	
				print "Error occured while reloading tf2 schema. Retrying ..."
			else:
				print "Error occured after 3 retries. Try again later."
				return 0
		
	f = open( os.path.dirname(os.path.abspath(__file__)) + '\\schemas\\tf2schema.json','w')
	f.write(r.text)
	f.close()