#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Block:
    def __init__(self, title, row, col):
        self.title=title
        self.row=row
        self.col=col

        self.can_left=False
        self.can_up=False
        self.can_right=False
        self.can_down=False