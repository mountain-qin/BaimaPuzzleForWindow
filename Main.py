#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
from pygame import mixer
import threading
from urllib import request
import json
import os
from winsound import Beep
import zipfile
from playsound import playsound
import wx
import sys

from Puzzle import Puzzle
import AppInfo

sys.path.append("ui")
from KeyboardListenerWindow import KeyboardListenerWindow
from SelectRowColWindow import SelectRowColWindow


class PuzzleWindow(KeyboardListenerWindow):

	def __init__(self,title="拜玛拼图",*args, **kw) -> None:
		super().__init__(title=title, *args, **kw)

		# self.check_update()

		self.dir_path=os.path.dirname(os.path.realpath(sys.argv[0]))

# 读取用户配置
		self.user_settin_pathg=os.path.join(self.dir_path,"config\\user_setting.json")
		self.user_setting={}
		if os.path.exists(self.user_settin_pathg):
			with open(self.user_settin_pathg,"r", encoding="utf-8") as f:
				self.user_setting=json.load(f)

		self.row =self.user_setting["row"] if self.user_setting.__contains__("row")  else 3
		self.col=self.user_setting["col"] if self.user_setting.__contains__("col")  else 3
		self.puzzle=Puzzle(row=self.row, col=self.col)

		self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
		super().show_message("按光标键可以查看方块。")
		self.show_help()
		self.init_mixer()



	def show_update_dialog(self, message, caption, url_download):
		md=wx.MessageDialog(self, message, caption, style=wx.OK|wx.CANCEL)
		while(True):
			id=md.ShowModal()
			# 只能点确定按钮
			if id==wx.ID_OK:
				break

		super().show_message("正在下载请稍候...这需要一定的时间，你可以继续玩游戏。")
		t=threading.Thread(target=self.down_update, args=(url_download,))
		t.start()
		# t.join()


	def down_update(self, url_down):
		# github下载太慢了
		try:
			temp_path=os.path.realpath("temp")
			if not os.path.exists(temp_path):os.mkdir(temp_path)
			file_path=os.path.join(temp_path, os.path.split(url_down)[1])

			req=request.Request(url_down)
			req.add_header("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36")
			with request.urlopen(req) as f:
				with open(file_path, "wb") as ff:
						ff.write(f.read())

			zip_file=zipfile.ZipFile(file_path)
			zip_file.extract(temp_path)
			zip_file	.close()

		except BaseException as e:
			print(e)


	def check_update(self):
		try:
			self.latest=None
			t=threading.Thread(target=self.check_new_version)
			t.start()
			t.join()

			if not self.latest:return

			# "tag_name": "v1.0",
			tag_name=str(self.latest["tag_name"]).lower().strip()
				# version_name="1.0"
			version_name=("v%s" %AppInfo.version_name).lower().strip()
			if tag_name==version_name:return

			assets=self.latest["assets"]
			for asset in assets:
				if asset["name"]==AppInfo.app_name+".zip":
					url_download=asset["browser_download_url"]

			body=self.latest["body"]
			if body: message=tag_name +"。\n"+ body
			self.show_update_dialog(message, "发现新版本", url_download)
		except:
			pass


	def check_new_version(self):
		urlreleases_latest="https://api.github.com/repos/mountainqin/PuzzleForWindow/releases/latest"
		req=request.Request(url=urlreleases_latest)
		req.add_header("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36")
		with request.urlopen(req) as f:
			self.latest=json.load(fp=f)


	def on_char_hook(self, event:wx.KeyEvent):
		# 查看帮助
		if event.GetKeyCode()==wx.WXK_F1:os.startfile(os.path.join(self.dir_path, "readme.html"))
		self.control_sound(event)
		self.control_bgm(event)
		self.view_puzzle_block(event)
		self.move_puzzle_block(event)
		self.disorder(event)
		self.order(event)
		self.start_select_row_col(event)
		event.Skip()


	def control_sound(self,event:wx.KeyEvent):
		if event.AltDown() and event.ShiftDown():
			key_code=event.GetKeyCode()
			if key_code==wx.WXK_PAGEUP:
				if self.volume_sound<100:self.volume_sound+=1
				self.set_sound_volume(self.volume_sound)
				super().show_message("音效音量：%s"%self.volume_sound)
			elif key_code==wx.WXK_PAGEDOWN:
				if self.volume_sound>0:self.volume_sound-=1
				self.set_sound_volume(self.volume_sound)
				super().show_message("音效音量：%s"%self.volume_sound)
			elif key_code==wx.WXK_HOME:
				self.is_play_sound=not self.is_play_sound
				super().show_message("音效开" if self.is_play_sound else "音效关")


	def init_mixer(self):
		volume=self.user_setting["bgm"]["volume"] if self.user_setting.__contains__("bgm") else 0.5
		play=self.user_setting["bgm"]["play"] if self.user_setting.__contains__("bgm") else True

		mixer.init()
		mixer.music.load(os.path.join(self.dir_path,"sounds\\bgm\\bgm.mp3"))

		threading.Thread(target=self.evenly_add_volume, args=(volume,)).start()
		if play:mixer.music.play(-1)

		# 音效
		# 自己用的音量0到100
		self.volume_sound = self.user_setting["sound"]["volume"] if self.user_setting.__contains__("sound") else 30
		self.is_play_sound=self.user_setting["sound"]["play"] if self.user_setting.__contains__("sound") else True
		

# 增加音效后要在下面的设置音效音量函数增加对应音效
		self.sound_move=mixer.Sound(os.path.join(self.dir_path,"sounds\\move\\move.wav"))
		self.sound_unmove=mixer.Sound(os.path.join(self.dir_path, "sounds\\unmove\\unmove.wav"))
		self.sound_wall=mixer.Sound(os.path.join(self.dir_path, "sounds\\wall\\wall.wav"))
		self.sound_congratulation=mixer.Sound(os.path.join(self.dir_path,"sounds\\congratulation\\congratulation.wav"))

		self.set_sound_volume(self.volume_sound)


	def set_sound_volume(self, volume):
		"""设置音效的音量。
		:: param volume 0到100
		"""
		self.volume_sound=volume
		for sound in [self.sound_move, self.sound_unmove,self.sound_wall,self.sound_congratulation]:
			sound.set_volume(volume/100)


	def evenly_add_volume(self,volume, second=2, n=1000):
		"""在指定时间内均匀增加音量到想要的音量。
		volume 要达到的音量
		::param second 时间
n 调整的次数。
		"""

		if n<=0:mixer.music.set_volume(volume)
		for i in range(1,n+1):
			mixer.music.set_volume(volume/n*i)
			time.sleep(second/n)


	def control_bgm(self, event:wx.KeyEvent):
		if event.ControlDown() and event.ShiftDown():
			key_code=event.GetKeyCode()
			if key_code==wx.WXK_PAGEUP: mixer.music.set_volume(mixer.music.get_volume()+0.02)
			elif key_code==wx.WXK_PAGEDOWN: mixer.music.set_volume(mixer.music.get_volume()-0.02)
			elif key_code==wx.WXK_HOME :
				# if mixer.music.get_busy()==True:mixer.music.stop() else:mixer.music.play(-1)
				if mixer.music.get_busy()==True:mixer.music.stop()
				else:mixer.music.play(-1)


	def    start_select_row_col(self, event:wx.KeyEvent):
		if event.ControlDown() and event.GetKeyCode()==ord("R"):
			SelectRowColWindow(self.select_row_col)


	def select_row_col(self, row,col):
		self.row,self.col=row,col
		self.puzzle=Puzzle(row=row, col=col)
		super().show_message("拼图现在已经是%s行%s列了。" %(row, col)+self.puzzle.get_focus_block_message())


	def order(self, event:wx.KeyEvent):
		if event.GetKeyCode()!=wx.WXK_F6: return
		self.puzzle.order()
		super().show_message("顺序已经调整好。" +self.puzzle.get_focus_block_message())


	def disorder(self,event:wx.KeyEvent):
		if event.GetKeyCode()!=wx.WXK_F5: return
		self.puzzle.disorder()
		super().show_message("顺序已经打乱。" +self.puzzle.get_focus_block_message())

		
	def move_puzzle_block(self, event:wx.KeyEvent):
		"""移动拼图方块"""
		# 需要按下ctrl
		if not event.ControlDown(): return
		moved=False
		key_code=event.GetKeyCode()
		if key_code==wx.WXK_LEFT: moved=self.puzzle.move_to_left()
		elif key_code==wx.WXK_UP: moved =self.puzzle.move_to_up()
		elif key_code==wx.WXK_RIGHT: moved=self.puzzle.move_to_right()
		elif key_code==wx.WXK_DOWN: moved=self.puzzle.move_to_down()
		else: return

		if not moved:self.play_sound(self.sound_unmove)
		else:
			self.show_focus_block_message()
			self.play_sound(self.sound_move)

		if self.puzzle.check_successful():
			super().show_message("恭喜你！拼图完成了！按F5可以打乱 顺序重新开始。")
			self.play_sound(self.sound_congratulation)


	def play_sound(self, sound):
		if self.is_play_sound: mixer.Sound.play(sound)



	def view_puzzle_block(self, event:wx.KeyEvent):
		"""查看拼图方块"""
		# 不按下ctrl
		if event.ControlDown(): return
		key_code=event.GetKeyCode()
		block=None
		if key_code==wx.WXK_LEFT:block=self.puzzle.view_left()
		elif key_code==wx.WXK_UP:block=self.puzzle.view_up()
		elif key_code==wx.WXK_RIGHT: block=self.puzzle.view_right()
		elif key_code==wx.WXK_DOWN:block=self.puzzle.view_down()
		else: return
		
		if not block:
			self.play_sound(self.sound_wall)
			# block=self.puzzle.get_focus_block()
			return
		self.show_focus_block_message()


	def show_focus_block_message(self):
		"""显示焦点方块信息"""
		message=self.puzzle.get_focus_block_message()
		super().show_message(message)


	def onCloseWindow(self, event):
		self.save_user_setting()
		mixer.quit()
		self.Destroy()
		# os.startfile(os.path.realpath("../MiniGame.exe"))
		# 返回小游戏界面
		mini_game_path=os.path.join(os.path.dirname(self.dir_path), "MiniGame.exe")
		if os.path.exists(mini_game_path):os.startfile(mini_game_path)


	def save_user_setting(self):
		# 用户配置
		user_setting={
			"row":self.row,
			"col":self.col,
			"bgm":{
				"volume":mixer.music.get_volume(),
				"play":mixer.music.get_busy()
				},
			"sound":{
				"volume":self.volume_sound,
				"play":self.is_play_sound
				}
			}

		if user_setting==self.user_setting:return

# 用户配置写到本地
		if not os.path.exists(os.path.dirname(self.user_settin_pathg)):os.makedirs(os.path.dirname(self.user_settin_pathg))
		with open(self.user_settin_pathg, "w", encoding="utf-8") as f:
			json.dump(user_setting,f)



	def show_help(self):
		firsted_file=os.path.join(self.dir_path, "config\\firsted")
		if not os.path.exists(firsted_file):
			os.makedirs(os.path.dirname(firsted_file))
			with open(firsted_file,"w") as f:pass
			os.startfile(os.path.join(self.dir_path, "readme.html"))


try:
	app=wx.App(False)
	PuzzleWindow()
	app.MainLoop()
except BaseException as e:
		print(e)