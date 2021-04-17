# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 15:33:07 2020

@author: Scott
this is a dumb program to play Egyptian ratscrew

TODO

deal cards
    allow for custom starting hands

play war
simulate slap
    improve statistics of slap algorithm
plot game

"""

import random
from collections import deque


#global objects
n_players = 4
#players = list(range(n_players))
player_hands = {}
pile = []
deck_def = {}
cur_player = 0
cardnames = {1  :   "ace",
            11 :   "jack",
            12 :   "queen",
            13 :   "king"}

#==============================================================================
def gen_deck():
    #geneates 52 cards plus a zero card representing the start of play
    
    n = 0
    deck ={n : [0,0]}
    
    for suit in range(1,5):
        
        for card in range(1,14):
            
            n +=1
            
            deck[n] = [card, suit]
            
    return deck

#==============================================================================
#checks if someone has won the game

def winstate_check(hands):
    
    global pile
    
    zeros = 0
    winner = ""
    tot = 0
    
    for player in hands:
        
        cards = len(hands[player])
        tot += cards
        if cards == 0:
            zeros += 1
        else:
            winner = player
            
        #print(str(tot + len(pile)) + " cards in play")
            
    if zeros == (len(hands)-1):
        with open("game log.txt","a") as f:
            update_log("Victory")
            temp = "Victory for player " + str(winner)
            f.write(temp)
            
        return winner
    else:
        return False
    
#==============================================================================
#slap!
#purely random slap
#should be updated to give each player a "personality"
#returns player who won the slap
    
def slap():
    
    global player_hands, pile, n_players, cur_player
    
    if len(pile) < 2:
        return False
    
    if deck_def[pile[-1]][0] == deck_def[pile[-2]][0]:
    
        #print("slap! \n")
              
        a = list(range(n_players))
        random.shuffle(a)
        
        #print("Player " + str(a[0]) + " wins the slap!")
        player_hands[a[0]] = player_hands[a[0]] + deque(pile)
        pile = []
        cur_player = a[0]
        
        with open("game log.txt","a") as f:
            f.write(str(a[0]))
            f.write(" slaps!\n")
        
        return
    
    else:
        return False

#==============================================================================
#facecard check
#returns an int of the number of cards the next player has to place
    
def face_check():
    
    global deck_def, pile
    
    if len(pile) == 0:
        return False
    
    facecards = {1  :   4,
                 11 :   1,
                 12 :   2,
                 13 :   3}
    
    if deck_def[pile[-1]][0] in list(facecards.keys()):
        return facecards[deck_def[pile[-1]][0]]
    else:
        return False
    
#==============================================================================
#facecard play
#removes number of cards from players hand depending on facecard drawn
#if the player's deck is exhausted, check win condition and move to the next player
        
def facecard_play(pull,player):
    
    global player_hands, pile, cardnames, deck_def
    
    victim = (player + 1) % n_players
    
    while pull > 0:
        
        #pull card
        if len(player_hands[victim]) > 0:
            pile.append(player_hands[victim].popleft())
        else:
            if winstate_check(player_hands):
                return
            victim = (victim + 1) % n_players
            continue
        
        if winstate_check(player_hands):
            return
            
        if slap():
            return
        
        fc = face_check()
        
        if fc:
            #print(str(victim) + " played a " + cardnames[deck_def[pile[-1]][0]])
            facecard_play(fc,victim)
            return
        
        pull -= 1
        
    #if play goes uninterrupted
    with open("game log.txt","a") as f:
        f.write(str(player))
        f.write(" wins!\n")
    player_hands[player] = player_hands[player] + deque(pile)
    pile = []
    return

#==============================================================================
#log file formatter

# def log_formatter(deck):

#     for 
    
  
#==============================================================================
#update log file
        
def update_log(play_type):
    
    global player_hands, pile, cur_player
    
    with open("game log.txt","a") as f:
        
        temp = str(cur_player) + " " + play_type + "\n"
        f.write(temp)
        f.write("Pile: ")
        f.write(str(pile)) 
        f.write("\nHands: ")
        for hand in player_hands:
            f.write(str(hand))
            f.write(" ")
            f.write(str(player_hands[hand]))
            f.write("\n")
        f.write("\n")
    
        
#==============================================================================
#main function
    
def main():
    
    global deck_def, n_players
    deck_def = gen_deck()
    
    #==============================================================================
    #deal cards
    
    deal = list(range(1,53))
    #deal cards
    random.shuffle(deal)
    
    cur_player = 0
    
    for playN in range(n_players):
        
        player_hands[playN] = deque([])
    
    for card in deal:
        
        player_hands[cur_player].append(card) 
        
        cur_player = (1 + cur_player) % (n_players)
        
    #==============================================================================
    #intiate log file
    with open("game log.txt","w+") as f:
        
        temp = "Players: " + str(n_players)
        f.write(temp)
        f.write("\n")
        f.write("Hands: ") 
        for hand in player_hands:
            f.write(str(hand))
            f.write(" ")
            f.write(str(player_hands[hand]))
            f.write("\n")
        f.write("\n")
    
    #==============================================================================
    #play game
    
    while winstate_check(player_hands) == False:
        
        if len(player_hands[cur_player]) > 0:
            pile.append(player_hands[cur_player].popleft())
            #print(str(cur_player) + " played " + str(deck_def[pile[-1]][0]))
        else:
            cur_player = (cur_player + 1) % n_players
            continue
        
        #slap check
        if slap():
            update_log("Slap!")
            if winstate_check(player_hands):
                break
            continue
        
        #check face cards
        facecard = face_check()
        if facecard:
            update_log("Facecard!")
            #print(str(cur_player) + " played a " + cardnames[deck_def[pile[-1]][0]])
            facecard_play(facecard,cur_player)
            if winstate_check(player_hands):
                break
            continue
            
        if winstate_check(player_hands):
            break
        
        cur_player = (cur_player + 1) % n_players
        
    print("Player " + str(winstate_check(player_hands)) + " wins the game!")
  
#send it
if __name__ == "__main__":
    main()
    