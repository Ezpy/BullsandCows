# -*- coding: utf-8 -*-
# Filename: BaseballBot.py

import random

def Load():
    # Make all number posibilties to an array
    _list = []
    for i in range(10):
        for j in range(10):
            for m in range(10):
                for n in range(10):
                    if len(set([i,j,m,n])) == 4:
                        # If all four numbers are different
                        _list.append('%d%d%d%d' % (i,j,m,n))
    return _list
    
def Filter(_list, num, guess):
    new = []
    for i in _list:
        if Compare(i, num) == guess:
            new.append(i)
    return new
    
def Compare(m, n):
    strike = 0
    ball = 0
    for i in range(len(m)):
        if m[i] == n[i]:
            strike += 1
        elif m[i] in n:
            ball += 1
        else:
            pass
    return strike*10 + ball*1
    
def CompareStr(m, n):
    strike = 0
    ball = 0
    for i in range(len(m)):
        if m[i] == n[i]:
            strike += 1
        elif m[i] in n:
            ball += 1
        else:
            pass
    return 's: %d b: %d' % (strike, ball)
    
def BestPick(_list):
    pick = random.choice(_list)
    return pick
    
def Play(_list):
    print '* start *'
    
    # Set user and computer number
    user_number = raw_input('Your Number: ').strip()
    computer_number = random.choice(_list)
    
    # nth turn
    _index = 1
    
    
    # to guess second time better
    # in most cases, computer cannot get 4 numbers correct at first.
    # It those cases force the computer to guess number
    # comprised of the numbers which wasn't memtioned at first turn.
    initial_guess = range(10)
    first_got_number = 0
    
    while True:
        print '====================================='
        print ' %d turn' % _index        
        print '====================================='
        
        # User guess
        user_guess = raw_input('Your guess :').strip()
        print CompareStr(user_guess, computer_number)
        if Compare(user_guess, computer_number) == 40:
            # all strike
            print 'You win :)'
            global user_win
            user_win += 1
            break
        print '====================================='
        # Compuer Guess
        if _index == 1:
            temp_pick = random.choice(_list)
            for i in temp_pick:
                initial_guess.remove(int(i))
            if Compare(temp_pick, user_number) in [40,31,22,13]:
                first_got_number = 4
        elif _index == 2 and first_got_number is not 4:
            temp_pick = ''
            for i in range(4):
                c = random.choice(initial_guess)
                temp_pick += str(c)
                initial_guess.remove(c)
        else:
            temp_pick = BestPick(_list)

        print 'Computer guess %s ..' % temp_pick
        print CompareStr(temp_pick, user_number)
        n = Filter(_list, temp_pick, Compare(temp_pick, user_number))
            
        # Check if computer won
        if Compare(temp_pick, user_number) == 40:
            print ' Computer win :('
            global computer_win
            computer_win += 1
            print 'Computer Number: ', computer_number
            break

        print 'Computer possibilities left: %d' % len(n)
        _list = n
        _index += 1
        
if __name__ == '__main__':
    _list = Load()
    user_win = 0
    computer_win = 0
    print '====================================='
    print ' ** Loading Completed'
    print '====================================='
    while True:
        Play(_list)
        print ''
        print 'win: %d lose: %d' % (user_win, computer_win)
        if raw_input('Play again(y/n)? > ') == 'n':
            break
        else:
            print ''
            print '====================================='
