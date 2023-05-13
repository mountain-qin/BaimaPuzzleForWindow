#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""翻译模块
调用的模块要在模块开始写上：
import Translater
if not Translater.init(): _=lambda x:x
"""


import gettext
import locale
import os
import sys


def init(
	# mo文件名
	# 和主py文件名一致
	# domain=os.path.splitext(os.path.split(sys.argv[0])[1])[0],
	domain="Puzzle",
	locale_path=os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"locale"),
	languages=[locale.getdefaultlocale()[0]]
	):
	try:
		translater=gettext.translation(domain,locale_path,languages=languages)
		translater.install()
	except BaseException as e:
		print(e)
		return False
	return True

