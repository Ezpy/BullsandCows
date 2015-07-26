# -*- coding: utf-8 -*-
# Filename: Baseball.py

from BaseballBot import Load, CompareStr, Compare, BestPick, Filter
import random
import wx
import sys
from wx.lib.mixins.listctrl import ColumnSorterMixin
import os

FRAME_SIZE = (500, 300)
FRAME_TITLE = 'Bulls and Cows'

class SortedListCtrl(wx.ListCtrl, ColumnSorterMixin):
    def __init__(self, parent, _list):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_HRULES,size=(300,350))
        ColumnSorterMixin.__init__(self, len(_list))
        self.itemDataMap = _list
    def GetListCtrl(self):
        return self
        
class MyGame(wx.Frame):
    def __init__(self, parent, _id, title):
        wx.Frame.__init__(self, parent,_id,title,(500,500),FRAME_SIZE,wx.DEFAULT_FRAME_STYLE)
        
        # score
        self.user_win = 0
        self.computer_win = 0
        
        # check if game is on or off
        self.playing = False
        
        user = wx.Panel(self, -1)
        com = wx.Panel(self, -1)
        
        # TextCtrl
        left_statictext = wx.StaticText(self, -1, label='User',size=(140,25),style=wx.BORDER_SUNKEN|wx.ALIGN_CENTER)
        right_statictext = wx.StaticText(self, -1, label='Computer',size=(140,25),style=wx.BORDER_SUNKEN|wx.ALIGN_CENTER)
        guess_static = wx.StaticText(self, -1, label='Guess',size=(50,25),style=wx.BORDER_SUNKEN|wx.ALIGN_CENTER)
        guess_static.SetBackgroundColour((255,230,230))
        self.guess_ctrl = wx.TextCtrl(self, -1,size=(50,25))
        
        self.winlose_static = wx.StaticText(self,-1,label='', size=(280,25),style=wx.BORDER_SUNKEN|wx.ALIGN_CENTER)
        self.winlose_static.SetBackgroundColour((230,255,230))
        self.play_button = wx.Button(self, -1, 'Play', size=(50,25))
        self.left_possible = wx.TextCtrl(self, -1, size=(130,25))
        self.left_possible.SetValue('')
        
        # ListCtrl
        self.data_dict = {0:'',1:'',2:''}
        self.list = SortedListCtrl(user, self.data_dict)
        self.list.InsertColumn(0,'#',wx.LIST_FORMAT_CENTER,width=20)
        self.list.InsertColumn(1,'Num',wx.LIST_FORMAT_CENTER,width=50)
        self.list.InsertColumn(2,'Result',wx.LIST_FORMAT_CENTER,width=70)
        self.list.SetSize((140,200))
        
        self.data_dict1 = {0:'',1:'',2:''}
        self.list1 = SortedListCtrl(com, self.data_dict1)
        self.list1.InsertColumn(0,'#',wx.LIST_FORMAT_CENTER,width=20)
        self.list1.InsertColumn(1,'Num',wx.LIST_FORMAT_CENTER,width=50)
        self.list1.InsertColumn(2,'Result',wx.LIST_FORMAT_CENTER,width=70)
        self.list1.SetSize((140,200))
        
        # BoxSizer
        v = wx.BoxSizer(wx.VERTICAL)
        header = wx.BoxSizer(wx.HORIZONTAL)
        foot1 = wx.BoxSizer(wx.HORIZONTAL)
        
        header.Add(left_statictext,0,wx.EXPAND|wx.ALL)
        header.Add(right_statictext,0,wx.EXPAND|wx.ALL)
        
        h = wx.BoxSizer(wx.HORIZONTAL)
        h.Add(user,0,wx.EXPAND|wx.ALL|wx.GROW)
        h.Add(com,0,wx.EXPAND|wx.ALL|wx.GROW)
        
        foot1.Add(guess_static)
        foot1.Add(self.guess_ctrl)
        foot1.Add(self.left_possible)
        foot1.Add(self.play_button)
        
        v.Add(header)
        v.Add(h)
        v.Add(foot1)
        v.Add(self.winlose_static,0,wx.EXPAND|wx.ALL|wx.GROW)
        
        self.SetSizerAndFit(v)
        self.RefreshScore()
        
        # EVENT BIND
        self.guess_ctrl.Bind(wx.EVT_TEXT_ENTER, self.UserGuess)
        self.play_button.Bind(wx.EVT_BUTTON, self.OnPlay)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def OnClose(self, e):
        os.system('taskkill /f /pid %s' % os.getpid())

    def OnPlay(self, e):
        if self.playing == True:
            msg = wx.MessageBox('Do you really want to give up?', 'Give up ?', wx.ICON_INFORMATION|wx.YES_NO|wx.NO_DEFAULT)
            if msg == wx.YES:
                self.playing = False
                self.play_button.SetLabel('Play')
                self.list.DeleteAllItems()
                self.list1.DeleteAllItems()
                self.computer_win += 1
                self.RefreshScore()
        else:
            self._list = Load()
            self.index = 1
            self.first_got_number = 0
            self.computer_number = random.choice(self._list)
            self.initial_guess = range(10)
            
            while True:
                self.user_number = wx.GetTextFromUser('Your number ?', 'Your number Input','')
                if len(self.user_number) == 4:
                    test = True
                    for i in range(4):
                        if self.user_number.count(self.user_number[i]) > 1:
                            test = False
                else:
                    test = False
                if test or self.user_number.strip() == '':
                    break
            if self.user_number.strip() != '':
                self.playing = True
                self.play_button.SetLabel('Stop')
                self.list.DeleteAllItems()
                self.list1.DeleteAllItems()
                
    def RefreshScore(self):
        try:
            percent = int(100*self.user_win/(self.user_win+self.computer_win))
        except:
            percent = 0
        self.winlose_static.SetLabel('win: %d lose: %d (%d%%)' % (self.user_win, self.computer_win, percent))
        self.winlose_static.SetSize((280,25))
        
    def UserGuess(self, e):
        user_guess = str(self.guess_ctrl.GetValue())
        if len(user_guess) == 4:
            test = True
            for i in range(4):
                if user_guess.count(user_guess[i]) > 1:
                    test = False
            if test:
                userwin = False
                comwin = False
                index = self.list.InsertStringItem(sys.maxint, unicode(self.index)) # item
                self.list.SetStringItem(index, 1, unicode(user_guess))
                self.list.SetStringItem(index, 2, unicode(CompareStr(user_guess,self.computer_number)))
                self.list.SetItemData(index, self.index)
                self.data_dict[self.index] = (unicode(self.index), unicode(user_guess),unicode(CompareStr(user_guess, self.computer_number)))
                
                if Compare(user_guess, self.computer_number) == 40:
                    self.user_win += 1
                    userwin = True
                
                # Computer guess
                if self.index == 1:
                    temp_pick = random.choice(self._list)
                    for i in temp_pick:
                        self.initial_guess.remove(int(i))
                    if Compare(temp_pick, self.user_number) in [40,31,22,13]:
                        self.first_got_number = 4
                elif self.index == 2 and self.first_got_number is not 4:
                    temp_pick = ''
                    for i in range(4):
                        c = random.choice(self.initial_guess)
                        temp_pick += str(c)
                        self.initial_guess.remove(c)
                else:
                    temp_pick = BestPick(self._list)
                    
                # Insert into ListCtrl
                index = self.list1.InsertStringItem(sys.maxint, unicode(self.index)) # item
                self.list1.SetStringItem(index, 1, unicode(temp_pick))
                self.list1.SetStringItem(index, 2, unicode(CompareStr(temp_pick,self.user_number)))
                self.list1.SetItemData(index, self.index)
                self.data_dict1[self.index] = (unicode(self.index), unicode(temp_pick),unicode(CompareStr(temp_pick, self.user_number)))
                    
                # Filter
                n = Filter(self._list, temp_pick, Compare(temp_pick, self.user_number))
                
                # Check if computer won
                if Compare(temp_pick, self.user_number) == 40:
                    self.computer_win += 1
                    comwin = True
                # Define who won
                if userwin == True and comwin != True:
                    # user won
                    wx.MessageBox('You win:)', 'Game Result', wx.OK|wx.ICON_INFORMATION)
                    self.playing = False
                    self.play_button.SetLabel('Play')
                    self.RefreshScore()
                elif userwin == True and comwin == True:
                    wx.MessageBox('Draw !', 'Game Result', wx.OK|wx.ICON_INFORMATION)
                    self.playing = False
                    self.play_button.SetLabel('Play')
                    self.computer_win -= 1
                    self.user_win -= 1
                elif comwin == True:
                    wx.MessageBox('Computer win :(\n\nComputer number was %s' % self.computer_number, 'Game Result', wx.OK|wx.ICON_INFORMATION)
                    self.playing = False
                    self.play_button.SetLabel('Play')
                    self.RefreshScore()
                
                self.left_possible.SetValue('Left possibilities: '+str(len(n)))
                self._list = n
                self.index += 1
            else:
                wx.MessageBox('Your number input format is not correct', 'ERROR', wx.ICON_ERROR|wx.OK)

class Baseball(wx.App):
    def OnInit(self):
        frame = MyGame(None, -1, FRAME_TITLE)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
        
if __name__ == '__main__':
    app = Baseball(0)
    app.MainLoop()
