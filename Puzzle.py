#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from Block import Block

class Puzzle:
    DISORDERED=0
    ORDER=1
    SPACE="空"

    def __init__(self, row=3, col=3, block_titles=[], flag=DISORDERED):
        """
        block_titles的长度要等于row *col,或者是0。
        """

        self.row, self.col=row,col
        self.row_space_block, self.col_space_block=0,0
        self.row_focus_block, self.col_focus_block=1,0

        if flag ==Puzzle.ORDER:self.init_ordered(row, col, block_titles)
        elif flag==Puzzle.DISORDERED: self.init_disordered(row,col,block_titles)
        else: self.blocks=None

    def init_disordered(self,row, col, block_titles):
        self.init_ordered(row,col,block_titles)


    def init_ordered(self,row, col, block_titles):
        if len(block_titles)==0:self.block_titles=[str(i) for i in range(1, row*col+1)]
        for i in range(col):self.block_titles.insert(0,Puzzle.SPACE)
        self.blocks =[[Block(self.block_titles[r*col +c]) for c in range(col)] for r in range(row+1)]


    def move_to_left(self,):
        if self.row_focus_block!=self.row_space_block or self.col_focus_block<=self.col_space_block: return False
        l =self.blocks[self.row_space_block][self.col_space_block+1: self.col_focus_block+1]
        block_space =self.blocks[self.row_space_block][self.col_space_block]
        for b in l:
            self.blocks[self.row_space_block][self.col_space_block]=b
            self.col_space_block+=1

        # self.col_focus_block-=1
        self.blocks[self.row_space_block][self.col_space_block]=block_space
        return True


    def move_to_up(self):
        if self.row_focus_block<=self.row_space_block or self.col_focus_block!=self.col_space_block :return False
        l =[self.blocks[r][self.col_focus_block] for r in range(self.row_space_block+1, self.row_focus_block+1)]
        block_space =self.blocks[self.row_space_block][self.col_space_block]
        for b in l:
            self.blocks[self.row_space_block][self.col_space_block]=b
            self.row_space_block+=1

        # self.row_focus_block-=1
        self.blocks[self.row_space_block][self.col_space_block]=block_space
        return True


    def move_to_right(self):
        if self.row_focus_block!=self.row_space_block or self.col_focus_block>=self.col_space_block: return False
        l =self.blocks[self.row_space_block][self.col_focus_block: self.col_space_block]
        l.reverse()
        block_space =self.blocks[self.row_space_block][self.col_space_block]
        for b in l:
            self.blocks[self.row_space_block][self.col_space_block]=b
            self.col_space_block-=1

        # self.col_focus_block+=1
        self.blocks[self.row_space_block][self.col_space_block]=block_space
        return True


    def move_to_down(self):
        if self.row_focus_block>=self.row_space_block or self.col_focus_block!=self.col_space_block :return False
        l =[self.blocks[r][self.col_focus_block] for r in range(self.row_focus_block, self.row_space_block)]
        l.reverse()
        block_space =self.blocks[self.row_space_block][self.col_space_block]
        for b in l:
            self.blocks[self.row_space_block][self.col_space_block]=b
            self.row_space_block-=1

        # self.row_focus_block+=1
        self.blocks[self.row_space_block][self.col_space_block]=block_space
        return True


    def view_left(self):
        if self.col_focus_block>0:
            self.col_focus_block-=1
            return self.blocks[self.row_focus_block][self.col_focus_block]
        return None


    def view_up(self)    :
        # 如果是第0列可以上到第0行.如果不是第0列只能到第1行
        if self.col_focus_block==0 and self.row_focus_block>0 or self.col_focus_block>0 and self.row_focus_block>1:
            self.row_focus_block-=1
            return self.blocks[self.row_focus_block][self.col_focus_block]
        return None

    def view_right(self):
        # 如果是0,0索引 ，不能往右
        if self.row_focus_block==0 and self.col_focus_block==0: return
        if self.col_focus_block<self.col-1:
            self.col_focus_block+=1
            return self.blocks[self.row_focus_block][self.col_focus_block]
        return None

    def view_down(self):
        # 在开头加了1列，不用减1
        if self.row_focus_block <self.row:
            self.row_focus_block+=1
            return self.blocks[self.row_focus_block][self.col_focus_block]
        return None


    def check_successful    (self):
        # 所有方块标标题的顺序对了就可以
        # python ok
        return self.block_titles ==[b.get_title() for blocks in self.blocks for b in blocks]


    def get_focus_block_message(self):
        title =self.blocks[self.row_focus_block][self.col_focus_block].get_title()
        return "%s。%s行 %s列" %(title, self.row_focus_block, self.col_focus_block+1)