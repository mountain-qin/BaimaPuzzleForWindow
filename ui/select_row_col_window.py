#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import wx
from keyboard_listener_window import KeyboardListenerWindow

main_dir_path=os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(main_dir_path)
import translater
if not translater.init(locale_path=os.path.join(main_dir_path,"locale")): _=lambda x:x


class  SelectRowColWindow(KeyboardListenerWindow):
	def __init__(self,select_row_col, title=_("Baima Puzzle - Select count of Rows and columns"), *args,  **kw) -> None:
		super().__init__(title=title, *args,  **kw)
		self.select_row_col=select_row_col
		self.row,self.col=0,0

		super().show_message(_("Please press the up or down arrow to select the count of rows, press the left or right arrow to select the count of columns, and press Enter to confirm"))
		self.Show    (True)


	def on_char_hook(self, event:wx.KeyEvent):
		key_code =event.GetKeyCode()
# 上光标
		if key_code==wx.WXK_UP:
			if self.row>1:self.row-=1
			super().show_message("%s%s"%(self.row,_("rows")))

		# 下光标
		if key_code==wx.WXK_DOWN:
			self.row+=1
			super().show_message("%s%s"%(self.row,_("rows")))

# 左光标
		elif key_code==wx.WXK_LEFT:
			if self.col>1: self.col-=1
			super().show_message("%s%s"%(self.col,_("columns")))

		# 右光标
		elif key_code==wx.WXK_RIGHT:
			self.col+=1
			super().show_message("%s%s"%(self.col,_("columns")))

# 回车
		elif key_code==wx.WXK_RETURN:
			if  self.row==0:super().show_message(_("Please press the up or down arrow to select the count of rows"))
			elif self.col==0: super().show_message(_("Please press the left or right arrow to select the count of columns."))
			elif self.row>0 and self.col>0:
				self.select_row_col(self.row,self.col)
				self.Close()

		elif key_code==wx.WXK_ESCAPE:self.Close()

		event.Skip()
