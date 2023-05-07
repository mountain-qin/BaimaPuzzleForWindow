#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wx
from KeyboardListenerWindow import KeyboardListenerWindow

class  SelectRowColWindow(KeyboardListenerWindow):
	def __init__(self,select_row_col, title="拜玛拼图-选择行列数", *args,  **kw) -> None:
		super().__init__(title=title, *args,  **kw)
		self.select_row_col=select_row_col
		self.row,self.col=0,0

		super().show_message("请按上下光标选择行数，按左右光标选择列数，按回车确定。")
		self.Show    (True)


	def on_char_hook(self, event:wx.KeyEvent):
		key_code =event.GetKeyCode()
# 上光标
		if key_code==wx.WXK_UP:
			if self.row>1:self.row-=1
			super().show_message("%s行"%self.row)

		# 下光标
		if key_code==wx.WXK_DOWN:
			self.row+=1
			super().show_message("%s行"%self.row)

# 左光标
		elif key_code==wx.WXK_LEFT:
			if self.col>1: self.col-=1
			super().show_message("%s列"%self.col)

		# 右光标
		elif key_code==wx.WXK_RIGHT:
			self.col+=1
			super().show_message("%s列"%self.col)

# 回车
		elif key_code==wx.WXK_RETURN:
			if  self.row==0:super().show_message("请上下光标选择行数。")
			elif self.col==0: super().show_message("请左右光标选择列数。")
			elif self.row>0 and self.col>0:
				self.select_row_col(self.row,self.col)
				self.Close()

		elif key_code==wx.WXK_ESCAPE:self.Close()

		event.Skip()
