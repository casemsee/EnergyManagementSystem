"""
Information receive and send functions for the energy management system
"""
def information_send(*args):  # Send information via socket
	socket = args[0]  # The socket information
	info = args[1]  # The information model
	info_type = args[2]  # The information type, 1= message, 2  = Google protocal
	if info_type == 0:  # The informaiton model is a binary string.
		socket.send(info)
	else:  # The informaiton model follows Google protocol.
		message = info.SerializeToString()
		socket.send(message)

	return 0

def information_receive(*args):  # Obtain information via socket
	socket = args[0]  # The socket information
	info = args[1]  # The information model
	info_type = args[2]  # The information type, 0= message, 1= Google protocal
	if info_type == 0:  # The informaiton model is a binary string.
		info = socket.recv()  # Receive information from given socket
	else:  # The informaiton model follows Google protocol.
		message = socket.recv()
		info.ParseFromString(message)
	# Return the information model
	return info