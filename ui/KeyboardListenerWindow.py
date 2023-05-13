#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import wx

wkd_path=os.path.dirname(os.path.realpath("."))

sys.path.append(wkd_path)
import Translater

if not Translater.init(locale_path=os.path.join(wkd_path, "locale")): lambda x:x


class KeyboardListenerWindow(wx.Frame):
    """键盘监听窗口。
    按下键盘按键时 会显示对应键码。
    """

    def __init__(self,parent=None, id=-1, title="键盘监听器", *args, message="按下键盘按键会在这里显示对应键码。", **kw):
        super().__init__(parent, id, title,*args, **kw)

        panel=wx.Panel(self,-1)
        l=[message]
        self.lb=wx.ListBox(panel,-1,choices=l, style=wx.LB_SINGLE)
        self.lb.SetSize((300, 200))
        self.lb.SetSelection(0)
        self.lb.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)
        self.Show(True)
        return None

    def on_char_hook(self, event:wx.KeyEvent):
        self.show_message(str(event.GetKeyCode()))
        event.Skip()

    def show_message(self, message):
        # 让屏幕阅读器可以朗读。
        self.lb.SetString(0, message)
        return None
