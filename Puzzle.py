#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Block import Block

class Puzzle:
    DISORDERED=0
    ORDER=1

    def __init__(self, row=3, col=3, block_titles=[], flag=DISORDERED):
        self.blocks=[[]]
        if flag ==Puzzle.ORDER:self.init_ordered(row, col, block_titles)

    def init_ordered(self,row, col, block_titles):
        if len(block_titles)==0:block_titles=[str(i) for i in range(1, row*col+1)]
        for i in range(col):block_titles.insert(0,"空")
        self.blocks =[[Block(block_titles[r*col +c], r, c+1) for c in range(col)] for r in range(row+1)]
