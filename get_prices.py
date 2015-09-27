# get_prices(...) accepts list of items (result of get_items() ) and bp_schema data
# then processes list adding prices to empty ('') spots in it.
# for crates I set price to -1 because fuck you

def get_prices( list_of_items, bpdata ):
	
	if type(list_of_items) != type([1,2]):
		print "List of items wrong type!"
	if type(bpdata) != type({'lol':'pidr'}):
		print "Bpdata wrong type!"

		
	for item in list_of_items:
		for bp_item in bpdata['response']['items']:
			# most players don't have aussie items, those who have won't trade it away for sure
			# so here i hide them from search because my matching algorithm has troubles with them
			#
			# TO DO: first match by quality, then by defindex
			
			if "Australium" in bp_item:
				
				continue
				
			if item[0] in bpdata['response']['items'][bp_item]['defindex']:
				#set name here lol:
				item[4] = bp_item.encode('utf-8')
				try:
					if item[1] == 5:
						item[2] = 999
					else:
						if bpdata['response']['items'][bp_item]['prices'][str(item[1])]['Tradable'][item[3]]["0"]['currency'] == 'keys':
							item[2] = bpdata['response']['items'][bp_item]['prices'][str(item[1])]['Tradable'][item[3]]["0"]['value'] * 16
						else:
							item[2] = bpdata['response']['items'][bp_item]['prices'][str(item[1])]['Tradable'][item[3]]["0"]['value']
				except:
					item[2] = 0
			else:
				continue
				
	return list_of_items