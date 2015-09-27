# ID 64 = 76561197960265728 + (B*2)+ A
# only steam id 3 values are acceptable here

def process_status( status_output ):
	result_list = []
	return_list = []
	
	list_to_process = status_output.split(' ')
	for item in list_to_process:
		if "[U:1:" in item:
			result_list.append(item[5:(len(item)-1)])
	# here we got clean list of steam id3 values, let's make them steam64
	
	for item in result_list:
		item = int(item) + 76561197960265728
		return_list.append(item)
	
	#print result_list
	
	return return_list