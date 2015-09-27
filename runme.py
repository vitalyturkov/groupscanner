from operator import itemgetter
import json
import sys
import os
# here i will wrap everything together :>
import get_items
import get_prices
import process_status
import get_hours
import get_name_and_state
import get_steamids
# for naming file differently each time
import time


# todo: 
#		add unusual support - implemented w/o correct price
#		add aussie support ( requires binding to tf2schema, not currently possible )
#		add crates support
# 		change interface to accept sys.argv's

print "Welcome! Make sure you're using updated bp schema."

"""
qualities
normal (0 - Normal)
rarity1 (1 - Genuine)
vintage (3 - Vintage)
rarity4 (5 - Unusual)
unique (6 - Unique)
community (7 - Community)
developer (8 - Valve)
self-made (9 - Self-Made)
strange (11 - Strange)
haunted (13 - Haunted)
collectors (14 - Collector's)
15 - decorated ???
"""

quality = {
		'0':'[Normal]',
		'1':'[Genuine]',
		'2':'[idk?]',
		'3':'[Vintage]',
		'4':'[idk?]',
		'5':'[Unusual]',
		'6':'[Unique]',
		'7':'[Community]',
		'8':'[Valve]',
		'9':'[Self-Made]',
		'11':'[Strange]',
		'13':'[Haunted?]',
		'14':'[Collector\'s]',
		'15':'[Decorated?]',
		}

user_input = -1
page_number = -1
hours_max = 400
# if ... then correct amount of params passed, grab them,  
# else: invoke user input instead for group name and page_number
# currently possibly unstable, works only when valid args are passed
# use with caution
if len(sys.argv) % 2 == 1 and len(sys.argv) != 1:
	for i in range(len(sys.argv)-1):
	
	
		'''
		if str(sys.argv[i+1]) != '-g' and str(sys.argv[i+1]) != '-p' and str(sys.argv[i+1]) != '-h':
			print "Wrong argument. Use manual input."
		'''
		
		
		if str(sys.argv[i+1]) == '-g':
			user_input = str(sys.argv[i+2])
		if str(sys.argv[i+1]) == '-p':
			page_number = int(sys.argv[i+2])
		if str(sys.argv[i+1]) == '-h':
			hours_max = int(sys.argv[i+2])
			

if ( user_input == -1 and page_number == -1 ):
	if len(sys.argv) != 1:
		print "Incorrect amount of arguments passed. Use manual input."
	user_input = raw_input("Enter group name: ")

	# page 1 gets first thousand of members, page 2 - second etc
	page_number = raw_input("Pick page (default 1): ")
	if str(page_number).isdigit() == False:
		page_number = 1
	elif page_number == '':
		page_number = 1


apikey = raw_input("Enter steam api key:")
		
players_list = get_steamids.get_steamids( user_input , page_number )

if players_list == []:
	print "No steamids found on page ", page_number,
	exit()

#################################################################################### 
result_string = "<body style='white-space: pre-wrap'> \n"

# this should always work, won't make try-except here
f = open( os.path.dirname(os.path.abspath(__file__)) + '\\schemas\\bp_prices.json','r')
bpdata = f.read()
f.close()
bpdata = json.loads(bpdata)	

print len(players_list), " steamids loaded from page: ", page_number," of <", user_input,"> group."
print "Profiles with hours above ", hours_max," are skippped."

# variable count is used to count amount of
# successfully scanned profiles
count = 0

for steamid in players_list:
	# check if user set his profile !OR IF IT IS PRIVATE (KINDA)!
	profiledata = ['','']
	profiledata = get_name_and_state.get_name_and_state( steamid , apikey )
	
	if profiledata[2] == 1:
		print "Profile skipped because of profile privacy", steamid
		print "Completed: ", str( float(players_list.index(steamid)) / float(len(players_list))*100 ),"%."
		continue
	
	if profiledata[1] != 1:
		print "Profile skipped because user hasn't configured profile yet", steamid
		print "Completed: ", str( float(players_list.index(steamid)) / float(len(players_list))*100 ),"%."
		continue
	
	# if he has more than 400 hours (by default, configurable) in game we have >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HOURS HOURS HOURS
	# nothing to do with him :\
	hours_played = 0
	try:
		hours_played = get_hours.get_hours( steamid , apikey )
	except:
		print "Profile skipped because user doesn't play tf2", steamid
		print "Completed: ", str( float(players_list.index(steamid)) / float(len(players_list))*100 ),"%."
		continue
	
	if hours_played > hours_max:
		print "Profile skipped because of excessive amount of playtime", steamid
		print "Completed: ", str( float(players_list.index(steamid)) / float(len(players_list))*100 ),"%."
		continue
		
	# load his items, without prices for now
	# revorked in 2.0
	itemlist = get_items.get_items( steamid , apikey)
	if itemlist == 0:
		print "Profile skipped because of backpack privacy", steamid
		print "Completed: ", str( float(players_list.index(steamid)) / float(len(players_list))*100 ),"%."
		continue
	
	# tag prices and item names
	itemlistpriced = get_prices.get_prices(itemlist, bpdata)
	
	# let's sort it, this way it becomes sorted by price(1) and item name(2)
	pricedlistsorted = sorted(itemlistpriced, key=itemgetter(2,4), reverse=True)
	
	# for some unknown for me yet reason I end up with
	# empty-priced and empty-named objects in here, now i will
	# just delete them, but later I'll have to find what causes them 
	# here I make a little KOCTblJlb, don't judge
	list2 = pricedlistsorted
	pricedlistsorted = []
	for item in list2:
		if item[2] == '':
			continue
		else:
			pricedlistsorted.append(item)
	if len(pricedlistsorted) < 1:
		print "Profile skipped because of 0 tradable items", steamid
		print "Completed: ", str( float(players_list.index(steamid)) / float(len(players_list))*100 ),"%."
		continue
	
	# if he has nothing more valuable than 1 ref, get rid of him :D
	# possible conversion bug ???
	
	# BUG!!! (FIXED?)
	# it occurs when player has 0 tradable items in inventory
	# print pricedlistsorted[0]
	
	if pricedlistsorted[0][2]<1:
		# this guy has nothing to trade :\
		print "Profile skipped because of poorness", steamid
		print "Completed: ", str( float(players_list.index(steamid)) / float(len(players_list))*100 ),"%."
		continue
	
	# at this point we have only users with valuable items left
	# now let's print info we gathered
	
	
	# first print his name and hours played:
	# print profiledata[0],"[", hours_played, "]"
	result_string = (result_string + "\n" + str(profiledata[0]) + " [" +  str(hours_played) + "]\n")
	
	profile_link = "<a href='http://steamcommunity.com/profiles/" + str(steamid) + "/'>Steam profile</a>"
	addfriend_link = "<a href='steam://friends/add/" + str(steamid) +"'>Add via Steam</a>"
	
	result_string = result_string +  profile_link + "  |  " + addfriend_link + "\n"
	
	
	# now print some of his most valuable items:
	# let's say we want 20 of them:
	# print pricedlistsorted
	if len(pricedlistsorted) < 20:
		result_string = result_string + "BP price:   " + str(pricedlistsorted[0][2]) + "     \tItem: " + str(pricedlistsorted[0][4]) + " " + quality[str(pricedlistsorted[0][1])] + "\n"
		result_string = result_string + "This user has less than 10 items, check him manually if you want.\n"
	else:
		for i in range(20):
			result_string = result_string + "BP price:   " + str(pricedlistsorted[i][2]) + "     \tItem: " + str(pricedlistsorted[i][4]) + " " + quality[str(pricedlistsorted[i][1])] + "\n"
		
	result_string = result_string + "\n"
	
	## new line to separate things visually			
	#print "\n"
	print 'Profile scanned successfully', steamid
	count = count + 1
	
	#this string print completion progress
	print "Completed: ", str( float(players_list.index(steamid)) / float(len(players_list))*100 ),"%."


############################################################################################################
result_string = result_string + "</body>"
fr = open( str(user_input) + '_' + time.strftime("%H-%M-%S") + "-page-" + str( page_number ) + '.html','w')
fr.write( result_string )
fr.close()


print "Finished with ", count, " profiles out of", len(players_list), "processed successfully"
exit()