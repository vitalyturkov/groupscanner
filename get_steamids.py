import requests
import untangle
# this function recieves group name as it appears
# in steamcommunity link and returns a list  of
# it's user's steamids in proper format for scanner 
# to process
#
#  TO DO:
#  for additional steamids visit same url with params: ?xml=1&p=2

def get_steamids( group_name , page_number = 1):
	obj = 0

	while True:
		try:
			url = 'http://steamcommunity.com/groups/' + str(group_name) + '/memberslistxml/?xml=1&p=' + str(page_number)
			obj = untangle.parse(url)
		except:
			pass
		if str(obj) != '0':
			break

	try:
		string_obj = str(obj.memberList.members.steamID64)
	except:
		return []
		
	string_obj = string_obj.split(' ')
	

	
	steamids = []
	for item in string_obj:
		if '7656' in item:
			steamids.append(item[0:17])
	
	return steamids