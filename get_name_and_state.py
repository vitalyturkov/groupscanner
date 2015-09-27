import requests
import json

# returns list of [ name , state ] (if 0 - haven't set up steam profile yet)
def get_name_and_state( steamid , key):
	apikey = key
	params = {'key':apikey, 'steamids':steamid, 'format':'json'}
	
	json_object = 0
	while True:
		try:
			r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/', params, timeout = 10)
			json_object = json.loads(r.text)
		except:
			pass
		if str(json_object) != '0':
			break
	
	name = json_object['response']['players'][0]['personaname']
	profilestate = 0
	try:
		profilestate = json_object['response']['players'][0]['profilestate']
	except:
		pass
	
	# kinda check if account is private, but not really
	communityvisibilitystate = 1
	try:
		communityvisibilitystate = json_object['response']['players'][0]['communityvisibilitystate']
	except:
		pass
	
	return [name.encode("utf-8") , profilestate, communityvisibilitystate]