# in order to get item list 
# use http://api.steampowered.com/IEconItems_440/GetPlayerItems/v0001/?steamid=76561198066920828&key=xxx
# function will accept steamid64 and return list of items
# if something goes wrong - returns 0

import requests
import json

def get_items( steamid , key ):
	apikey = key
	
	params = { 'key':apikey, 'steamid':steamid }
	# params = { 'key':apikey, 'steamid':76561198066920828 }
	try:
		r = requests.get("http://api.steampowered.com/IEconItems_440/GetPlayerItems/v0001/", params, timeout = 15)
	except:
		print "Error while retrieving someone's inventory. Aborting."
		return 0
		
	data = json.loads(r.text)
	
	#check of profile is private or steamid is invalid
	if data['result']['status'] == 8 or data['result']['status'] == 18:
		print "Error: steamid invalid or missing"
		return 0
	
	if data['result']['status'] == 15:
		#print "Backpack is private\n"
		return 0
	
	# i came up with an idea of storing 3 values for each item:
	# it's defindex (used to identify items), quality and price
	# in this function i generate a list of lists of items
	# where each internal list has 3 items in it:
	# [ 'defindex' , 'quality', 'price'], price being empty
	# for the next function to fill it
	# p.s. i also skip all decorated weapons for now :\
	
	list_of_items = []
	
	for item in data['result']['items']:
		if item['quality'] == 15:
			#print "Decorated weapon spotted? Scan for those isn't yet implemented, skipping."
			continue
			
		# skip all non-tradable items:
		try:
			if item['flag_cannot_trade'] ==  True:
				continue
		except:
			pass
			
		try:
			if item['flag_cannot_craft'] ==  True:
				craftability = "Non-Craftable"
			if item['flag_cannot_craft'] ==  False:
				craftability = "Craftable"
		except:
			craftability = "Craftable"
		
		
		list_of_items.append([ item['defindex'] , item['quality'] ,'' , craftability, ''])
		# so in the end we a have a list of all tradable items user has (except decorated)
		
	return list_of_items