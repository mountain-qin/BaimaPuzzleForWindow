#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from winsound import Beep
import wx
import sys

from Puzzle import Puzzle

sys.path.append("ui")
from KeyboardListenerWindow import KeyboardListenerWindow

class PuzzleWindow(KeyboardListenerWindow):

    def __init__(self,title="拜玛拼图",message="按光标键可以查看方块。") -> None:
        super().__init__(title=title, message=message)

        self.puzzle=Puzzle()


    def on_char_hook(self, event:wx.KeyEvent):
        self.view_puzzle_block(event)
        self.move_puzzle_block(event)

        event.Skip()


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

        if not moved: Beep(220, 400)
        else: self.show_focus_block_message()

        if self.puzzle.check_successful():
            super().show_message("恭喜你！拼图完成了！")
            Beep(1600, 1000)


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


app=wx.App(False)
PuzzleWindow()
app.MainLoop()