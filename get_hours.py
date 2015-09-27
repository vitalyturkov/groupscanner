import requests
import json


def get_hours( steamid , key):
	apikey = key
	params = {'key':apikey, 'steamid':steamid, 'format':'json', 'include_played_free_games':1}
	
	json_object = 0
	while True:
		try:
			r = requests.get('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/', params, timeout = 10)
			json_object = json.loads(r.text)
		except:
			pass
		if str(json_object) != '0':
			break
		
	
	for game in json_object['response']['games']:
		if game['appid'] == 440:
			return game['playtime_forever']/60