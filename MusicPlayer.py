import os,threading,thread,random,Queue
# -*- coding: utf-8 -*-
#
# threading lock 
#
play_lock = threading.Lock()
#
# play music server 
#
def play():
	# init id
	music_id = None
	# init list
	music_file = open('playlist','r')
	# play list
	music_list = music_file.readlines()
	# ID list
	music_listd = music_list
	music_file.close()
	# is list null
	if len(music_list) > 1:
		# list > 1
		music_id = random.randint(0,len(music_list) - 1)
	else:
		# only one body 
		music_id = 0
	# init play server play
	inenv = 'play'
	while 1 :
		# get play thread lock
		play_lock.acquire()
		# check con queue
		if music_que.empty() == False :
			# 
			inenv = music_que.get()
		#	print 'inenv get ok'
		#	print inenv
		play_lock.release()
		if int(inenv.find('stop')) > -1 :
			play_lock.acquire()
		#	if music_que.empty() == False :
		#		music_que.get()
			while music_isplay.empty() == False:
				music_isplay.get()
				if music_que.empty() == False:
					music_que.get()
				print 'Stop Play',
			else :
				pass
			music_isplay.put(music_id)
			play_lock.release()
			return 0
		elif int(inenv.find('quite')) > -1 :
		#	if playing > 0:
		#		os.system('killall play-audio')
		#	print ' play exit'
			return 0	
		elif int(inenv.find('play')) > -1 :
			#
			if music_isplay.empty() == False:
				#music_list[music_id] = music_list[-1]
				#music_list.pop()
				if len(music_list) > 1:
					music_id = random.randint(0,len(music_list) - 1)
					pass
				else:
					music_id = 0
			if len(music_list) > 0:
				#music_id = random.randint(0,len(music_list) - 1)
				play_lock.acquire()
				if music_que.empty() == False :
					music_que.put('wait')
					id_tmp = music_que.get()
					if id_tmp.find('next') > -1:
						music_name = str(music_list[music_id])
						print '\rPlaying\t\t\nID:\t',music_id,'\nname:\t',music_name.split('/')[-1],'Path:\t',music_name
					elif id_tmp.find('wait') > -1:
						music_name = str(music_list[music_id])
						for get_id in range(len(music_listd) - 1):
							if music_listd[get_id].find(music_name) > -1 :
								music_id = get_id
						print '\rPlaying\t\t\nID:\t',music_id,'\nname:\t',music_name.split('/')[-1],'Path:\t',music_name
					else :
						if int(id_tmp) > len(music_listd) - 1:
							id_tmp = len(music_listd) - 1
						music_name = str(music_listd[int(id_tmp)])
						print '\rPlaying\t\t\nID:\t',id_tmp,'\nname:\t',music_name.split('/')[-1],'Path:\t',music_name
				else:
					music_name = str(music_list[music_id])
					print '\rPlaying        \nID:\t',music_id,'\nname:\t',music_name.split('/')[-1],'Path:\t',music_name

				os.environ['music_id'] = music_name
				
				if music_isplay.empty() == True:
					music_isplay.put('playing')
			#	try:
			#		play_lock.release()
				
			#		print 'play unlock'
			#	finally:
				if music_que.empty() == False:
					music_que.get()
				play_lock.release()
				os.system('play-audio $music_id 2>/dev/null')
			else :
				if music_que.empty() == False:
					music_que.get()
				music_file = open('playlist','r')
				music_list = music_file.readlines()
				music_file.close()


		else :
			play_lock.acquire()
			if music_que.empty() == False:
				music_que.get()
			play_lock.release()
			inenv = 'play'
			pass
		#	print 'play unlock'
def play_con():
	while 1:
	#	while int(str(os.environ.get('print_ok')).find('ok')) < 0:
			#print_ok = os.environ.get('print_ok')
		while music_que.empty() == False :
			pass
	#	play_lock.acquire()
		music_con = raw_input('\nInput Command: ')
		play_lock.acquire()
	#	print 'play_con lock'
		if int(music_con.find('p')) == 0:
			#os.system('killall play-audio')
			play_con_tmp = music_con.split()
			if len(play_con_tmp) == 1:
				if music_isplay.empty() == False:
					mu_id_tp = str(music_isplay.get())
				if mu_id_tp.find('playing') < 0:
					music_que.put('play')

					music_que.put(mu_id_tp)
					play_music = threading.Thread(target=play)
					play_music.start()


				else :
					print 'Playing now!'
			else :
				music_que.put('play')
				music_que.put(play_con_tmp[1])
				if str(music_isplay.get()).find('play') < 0:
					play_music = threading.Thread(target=play)
					play_music.start()
				os.system('killall play-audio')	
			#os.environ['music_con']='play'
			#os.environ['print_ok'] = 'wait'
			music_con = 'none'
		elif int(music_con.find('s')) == 0:
			#os.environ['print_ok'] = 'wait'
			#os.environ['music_con']='stop'
			if music_isplay.empty() == False:
				while music_que.empty() == False :
					music_que.get()
				music_que.put('stop')
				music_que.put('wait')
				os.system('killall play-audio 1>/dev/null')
			else:
				print 'Playing Not!'
			music_con = 'none'
		elif int(music_con.find('q')) == 0:
			while music_que.empty() == False :
				music_que.get()
			music_que.put('quite')
			#os.environ['music_con']='quite'
			os.system('killall play-audio')
			play_lock.release()
			return 0
		elif int(music_con.find('n')) == 0:
			while music_que.empty() == False :
				music_que.get()
			if music_isplay.empty() == False :
				play_id_tmp = music_isplay.get()
				if str(play_id_tmp).find('playing') > -1:
					music_que.put('play')
					music_que.put('next')
					music_isplay.put('playing')
					os.system('killall play-audio')
				else :
					music_isplay.put(play_id_tmp)
					print 'No playing'
			else:
				print 'No playing'
			music_con = 'none'
		elif int(music_con.find('del')) == 0:
		#	mu_id = os.environ.get('music_id')
		#		if mu_id == None :
		#	print 'No music delete'
		#		else:
		#	os.environ['print_ok'] = 'wait'
		#	os.environ['music_con']='dele'
			music_file = open('playlist','r')
			music_listd = music_file.readlines()
			music_file.close()
			name = os.environ.get('music_id')
			del_con_tmp = music_con.split()
			if len(del_con_tmp) == 1:
				for i in range(len(music_listd) - 1):
						if music_listd[i].find(name) > -1:
							music_listd[i] = music_listd[-1]
							music_listd.pop()
				print 'delete:',name

				os.system('killall play-audio')
			else :
				#music_que.put('delete')
				#music_que.put(del_con_tmp[1])
				music_file = open('playlist','r')
				music_listd = music_file.readlines()
				music_file.close()
				print 'Delete: ',music_listd[int(del_con_tmp[1])],
				if music_listd[int(del_con_tmp[1])].find(name) > -1 :
					os.system('killall play-audio')
				music_listd[int(del_con_tmp[1])] = music_listd[-1]
				music_listd.pop()
			music_file = open('playlist','w')
			music_file.writelines(music_listd)
			music_file.close()
			print 'Ok'
			music_con = 'none'
		elif int(music_con.find('l')) == 0:
			music_file = open('playlist','r')
			music_lists = music_file.readlines()
			music_file.close()
			print 'Play list'
			i = 0
			for name in music_lists:
				print i,name,
				i = i + 1
		elif int(music_con.find('update')) == 0:
			print 'Updating play list'
			os.system('find /mnt/sdcard/ -name *.mp3 > playlist')
			print 'Update play list ok'
		elif int(music_con.find('help')) == 0:
			print 'play [id]:\tStart play the select id of music in playlist\n\nstop:\t\tStop play\n\nquite:\t\tExit player\n\ndelete [id]:\tDelete the select id of music in playlist\n\nnext:\t\tPlay next music\n\nlist:\t\tPrint playlist\n\nupdate list:\tUpdate list with \'find\' command'
			


						
		else:
			pass
		play_lock.release()

play_music = threading.Thread(target=play)
play_con_thread = threading.Thread(target=play_con)
music_que = Queue.Queue(2)
music_isplay = Queue.Queue(1)
music_playid = Queue.Queue(1)
music_que.put('play')
music_que.put('wait')
music_con = 'none'
play_music.start()
play_con_thread.start()
play_con_thread.join()
play_music.join()
print 'Music player exit'
