#!/usr/bin/python3
#coding: utf8

import re
import os
import sys
import pymp
import getopt
import pickle
import requests
import multiprocessing
import vk_api
from vk_api import audio
from time import time

class vkMusicDownloader():

	CONFIG_DIR = 'config'
	USERDATA_FILE = '{}/UserData.datab'.format(CONFIG_DIR) # файл хранит логин, пароль и id
	REQUEST_STATUS_CODE = 200

	login = ''
	password = ''
	user_id = ''
	out_dir = ''
	new_auth = False

	def parse_cl(self, argv):
		help_str = sys.argv[0] + ' -a -u <login> -p <password> -i <user_id> -d <output_directory>'
		try:
			opts, args = getopt.getopt(argv, 'hau:p:i:d:', ['cl_user=', 'cl_pass=', 'cl_uid=', 'cl_dir='])
		except getopt.GetOptError:
			print(help_str)
			sys.exit(2)
		for opt, arg in opts:
			if opt == '-h':
				print(help_str)
				sys.exit()
			elif opt == '-a':
				self.new_auth = True
			elif opt in ('-u', '--cl_user'):
				self.login = arg
			elif opt in ('-p', '--cl_pass'):
				self.password = arg
			elif opt in ('-i', '--cl_uid'):
				self.user_id = arg
			elif opt in ('-d', '--cl_dir'):
				self.out_dir = arg
			else:
				sys.exit(2)

	def auth_handler(self, remember_device=None):
		code = input('Enter confirmation code\n> ')
		if (remember_device == None):
			remember_device = True
		return code, remember_device

	def saveUserData(self):
		SaveData = [self.login, self.password, self.user_id]

		with open(self.USERDATA_FILE, 'wb') as dataFile:
			pickle.dump(SaveData, dataFile)

	def auth(self, new):
		try:
			if (os.path.exists(self.USERDATA_FILE) and new == False):
				with open(self.USERDATA_FILE, 'rb') as DataFile:
					LoadedData = pickle.load(DataFile)
				if (self.login == ''):
					self.login = LoadedData[0]
				if (self.password == ''):
					self.password = LoadedData[1]
				if (self.user_id == ''):
					self.user_id = LoadedData[2]
			else:
				if (os.path.exists(self.USERDATA_FILE) and new == True):
					os.remove(self.USERDATA_FILE)

				self.login = str(input('Enter login\n> '))
				self.password = str(input('Enter password\n> '))
				self.user_id = str(input('Enter profile ID\n> '))
				self.saveUserData()

			SaveData = [self.login, self.password, self.user_id]
			with open(self.USERDATA_FILE, 'wb') as dataFile:
				pickle.dump(SaveData, dataFile)

			try:
				vk_session = vk_api.VkApi(login=self.login, password=self.password, app_id=2685278)
				vk_session.auth()
			except Exception as e:
		                print('[error]:', e)
		                return

			print('Authorization successfull')

			self.vk = vk_session.get_api()
			self.vk_audio = audio.VkAudio(vk_session)

		except KeyboardInterrupt:
			sys.exit(2)

	def getaudio(self, audio):
		index = 1

		for i in audio:
			fileMP3 = '{} - {}.mp3'.format(i['artist'], i['title'])
			fileMP3 = re.sub('/', '_', fileMP3)
			fileURL = audio[index-1]['url']
			try:
				print('{:05} {}'.format(index, fileMP3), end = '', flush=True)
				if os.path.isfile(fileMP3):
					print(' - already exists')
				else:
# старая реализация
#					r = requests.get(fileURL)
#					if r.status_code == self.REQUEST_STATUS_CODE:
#						with open(fileMP3, 'wb') as output_file:
#							output_file.write(r.content)
#							print(' - download complette')

# новая реализация
					cmd = 'ffmpeg -http_persistent false -v 16 -i {} -c copy -map a "{}"'.format(fileURL, fileMP3)
					os.system(cmd)
					if os.path.getsize(fileMP3) > 0:
						print(' - download complette')
                    
			except OSError:
				print(' - download failed')

			index += 1

	def main(self, auth_dialog = 'yes'):

		self.parse_cl(sys.argv[1:])

		try:
			if (not os.path.exists(self.CONFIG_DIR)):
				os.mkdir(self.CONFIG_DIR)

			if ((not os.path.exists(self.USERDATA_FILE)) or self.new_auth):
				self.auth(new=True)
			else:
				self.auth(new=False)

			print('user    ' + self.login)
			print('pass    ' + self.password)
			print('user_id ' + self.user_id)
			print('out_dir ' + self.out_dir)

			# В папке загрузки создаем папку с именем пользователя, музыку которого скачиваем.
			info = self.vk.users.get(user_id=self.user_id)

			if (self.out_dir == ''):
				self.out_dir = 'music'

			music_path = '{}/{} {}'.format(self.out_dir, info[0]['first_name'], info[0]['last_name'])

			if not os.path.exists(music_path):
				os.makedirs(music_path)

			time_start = time() # сохраняем время начала скачивания
			print('Getting file list, please wait...')

			os.chdir(music_path) # меняем текущую директорию

			audio = self.vk_audio.get(owner_id=self.user_id)
			print('{} audio will be downloaded'.format(len(audio)))
			files = len(audio)
			self.getaudio(audio) # загружаем музыку

			# загружаем музыку из альбомов
			os.chdir('../..')
			albums = self.vk_audio.get_albums(owner_id=self.user_id)
			print('{} albums will be downloaded'.format(len(albums)))
			for i in albums:
				audio = self.vk_audio.get(owner_id=self.user_id, album_id=i['id'])
				files = files + len(audio)
				print('{} audio will be downloaded from album {}.'.format(len(audio), i['title']))

				album_path = '{}/{}'.format(music_path, i['title'])
				print(album_path)
				if not os.path.exists(album_path):
					os.makedirs(album_path)

				os.chdir(album_path) # меняем текущую директорию

				self.getaudio(audio) # загружаем музыку

				os.chdir('../../..')

			time_finish = time()
			print(str(files) + ' audio downloaded in ' + str(round(time_finish - time_start)) + ' seconds')

		except KeyboardInterrupt:
			sys.exit(2)

if __name__ == '__main__':
	vkMD = vkMusicDownloader()
	vkMD.main()
