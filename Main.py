#!/usr/bin/python3
# -*- coding: UTF-8 -*-

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

		row, col=self.read_row_col()
		self.puzzle=Puzzle(row=row, col=col)

		self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
		super().show_message("按光标键可以查看方块。")



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


	def read_row_col(self):
		"读取保存的行列数。"

		self.row_col_path="config/row_col.json"
		if not os.path.exists(self.row_col_path): return 3,3

		with open(self.row_col_path, "r")as f:
			d =json.load(f)
			return d["row"], d["col"]


	def on_char_hook(self, event:wx.KeyEvent):
		self.view_puzzle_block(event)
		self.move_puzzle_block(event)
		self.disorder(event)
		self.order(event)
		self.start_select_row_col(event)
		event.Skip()


	def    start_select_row_col(self, event:wx.KeyEvent):
		if event.ControlDown() and event.GetKeyCode()==ord("R"):
			SelectRowColWindow(self.select_row_col)


	def select_row_col(self, row,col):
		self.puzzle=Puzzle(row=row, col=col)
		super().show_message("拼图现在已经是%s行%s列了。" %(row, col)+self.puzzle.get_focus_block_message())

		# 保存到本地
		d={"row": row, "col": col}
		if not os.path.exists(self.row_col_path): os.makedirs(os.path.dirname(self.row_col_path))
		with open(self.row_col_path,"w", encoding="utf-8") as f:
			json.dump(d, f)


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

		if not moved: Beep(440, 440)
		else: self.show_focus_block_message()

		if self.puzzle.check_successful():
			super().show_message("恭喜你！拼图完成了！按F5可以打乱 顺序重新开始。")
			playsound(os.path.join(self.dir_path, "sounds/congratulation/congratulation.wav"))


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
			Beep(440, 50)
			# block=self.puzzle.get_focus_block()
			return
		self.show_focus_block_message()


	def show_focus_block_message(self):
		"""显示焦点方块信息"""
		message=self.puzzle.get_focus_block_message()
		super().show_message(message)


	def onCloseWindow(self, event):
		self.Destroy()
		# os.startfile(os.path.realpath("../MiniGame.exe"))
		# 返回小游戏界面
		mini_game_path=os.path.join(os.path.dirname(self.dir_path), "MiniGame.exe")
		if os.path.exists:os.startfile(mini_game_path)


try:
	app=wx.App(False)
	PuzzleWindow()
	app.MainLoop()
except BaseException as e:
		print(e)