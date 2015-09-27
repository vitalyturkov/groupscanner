import requests
import os
# manual check: http://backpack.tf/api/IGetPrices/v4/?key=yyy

def reload( key ):
	bp_key = key
	for i in range(3):
		try:
			r = requests.get('http://backpack.tf/api/IGetPrices/v4/', {'key':bp_key}, timeout = 15 )
		except:
			if i < 2:	
				print "Error occured while reloading bp schema. Retrying ..."
			else:
				print "Error occured after 3 retries. Try again later."
				return 0
	
	f = open( os.path.dirname(os.path.abspath(__file__)) + '\\schemas\\bp_prices.json','w')
	f.write(r.text)
	f.close()
	return 1