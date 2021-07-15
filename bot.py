import socket

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect(('irc.libera.chat',6665))
server.send('NICK WolfGame\r\n'.encode())
server.send('USER WolfGame WolfGame WolfGame :WolfGame\r\n'.encode())
server.send('PRIVMSG NickServ :IDENTIFY WolfGame xiaodong2009\r\n'.encode())
server.send('JOIN #wolf-game\r\n'.encode())
server.send('NOTICE #wolf-game :[WolfGame] bot已启动\r\n'.encode())
server.send('PRIVMSG ChanServ :OP #wolf-game WolfGame\r\n'.encode())
server.send('PRIVMSG ChanServ :SET MLOCK #wolf-game +\r\n'.encode())
server.send('CMODE #wolf-game -m\r\n'.encode())
server.send('CMODE #wolf-game -n\r\n'.encode())
server.send('CMODE #wolf-game +t\r\n'.encode())

state = 0
users = []
votes = []
voted = []

while True:
	data = server.recv(2147483647)
	if data.decode().find('PING') != -1:
		buf = 'PONG %s\r\n' % data.decode().split(' ')[1]
		buf = buf.encode()
		server.send(buf)
	if data.decode().split()[1] == 'PRIVMSG':
		nick = data.decode().split()[0]
		nick = ''.join(list(nick.split('!')[0])[1:len(nick.split('!')[0])])
		command = ''.join(data.decode().split()[3:len(data.decode().split())])
		if command == ':@HELP':
			server.send('NOTICE #wolf-game :----------[WolfGame] 帮助----------\r\n'.encode())
			server.send('NOTICE #wolf-game :@REGISTER 加入游戏\r\n'.encode())
			server.send('NOTICE #wolf-game :@EXIT 退出游戏\r\n'.encode())
			server.send('NOTICE #wolf-game :@LIST 玩家列表\r\n'.encode())
			server.send('NOTICE #wolf-game :@VOTE [id] 投票\r\n'.encode())
			server.send('NOTICE #wolf-game :----------[WolfGame] 帮助----------\r\n'.encode())
		elif command == ':@REGISTER':
			if len(users) >= 12:
				server.send('NOTICE #wolf-game :[WolfGame] 人数已满\r\n'.encode())
			elif state != 0:
				server.send('NOTICE #wolf-game :[WolfGame] 游戏已开始\r\n'.encode())
			elif {'nick':nick} in users:
				server.send('NOTICE #wolf-game :[WolfGame] 您已加入\r\n'.encode())
			else:
				users.append({'nick':nick})
				server.send('NOTICE #wolf-game :[WolfGame] 加入成功\r\n'.encode())
		elif command == ':@EXIT':
			if state != 0:
				server.send('NOTICE #wolf-game :[WolfGame] 游戏已开始\r\n'.encode())
			elif {'nick':nick} not in users:
				server.send('NOTICE #wolf-game :[WolfGame] 您未加入\r\n'.encode())
			else:
				server.send('NOTICE #wolf-game :[WolfGame] 退出成功\r\n'.encode())
				users.remove({'nick':nick})
		elif command == ':@LIST':
			server.send('NOTICE #wolf-game :----------[WolfGame] 玩家列表----------\r\n'.encode())
			server.send('NOTICE #wolf-game :序号\t昵称\r\n'.encode())
			for i in range(len(users)):
				server.send(('NOTICE #wolf-game :%d\t%s\r\n'%(i,users[i]['nick'])).encode())
			server.send('NOTICE #wolf-game :----------[WolfGame] 玩家列表----------\r\n'.encode())
		elif ''.join(command[0:6]) == ':@VOTE':
			if state == 0:
				server.send('NOTICE #wolf-game :[WolfGame] 游戏未开始\r\n'.encode())
			elif state == 1:
				if nick in voted:
					server.send(('NOTICE %s :[WolfGame] 已投票\r\n'%nick).encode())
				else:
					server.send(('NOTICE %s :[WolfGame] 投票成功\r\n'%nick).encode())
			elif state == 2:
				pass

	print(data.decode())
