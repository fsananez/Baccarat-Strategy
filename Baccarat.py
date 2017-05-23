from __future__ import division
import random
import sys, getopt
from math import *

global game_type
game_type="standard"

no_games = 1000000

global no_decks
no_decks = 8

global wallet
wallet = 10000000

def usage():
    print "Usage: python baccarat_test.py [-t|--type EZ|standard (default)] [-g|--games <# games> (1M default)]. "


#opts = getopt.getopt(sys.argv[1:], "t:", ["type="])
try:
    opts, args = getopt.getopt(sys.argv[1:], "g:t:", ["type=", "games="])
except getopt.GetoptError as err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ("-t", "--type"):
        if (a.lower() == "ez" or a.lower() == "standard"):
            game_type = a.lower()
            print "Playing " + a + " style baccarat"
        else:
            print "Unrecognized game type. Only 'EZ' and 'standard' are supported"
    elif o in ("-g", "--games"):
        no_games = int(a)
    else:
        assert False, "unhandled option"

def check_winner(player_sum, banker_sum, player_cards, banker_cards):
    if (player_sum > banker_sum):
        
        ##if (game_type == "ez" and player_cards == 3 and player_sum == 8):
        ##    return 'PANDA'
        
        return 'PLAYER'
    
    elif (banker_sum > player_sum):
        
        ##if (game_type == "ez" and banker_cards == 3 and banker_sum == 7):
        ##    return 'DRAGON'
        
        return 'BANKER'
    
    else:
        return 'TIE'

def shoe_shuffle():
    suit = [(1,1), (2,1), (3,1), (4,2), (5,-1), (6,-2), (7,-1), (8,-1), (9,0), (10,0), (10,0), (10,0), (10,0)]
    deck = suit + suit + suit + suit
    if no_decks != 8:
        bdeck = deck + deck + deck + deck + deck + deck
    else:
        bdeck = deck + deck + deck + deck + deck + deck + deck + deck
    random.shuffle(bdeck)
    random.shuffle(bdeck)
    return bdeck

def play_shoe():
    shoe = shoe_shuffle()
    card_limit = 6
    ##shoe = shoe[shoe[0][0]+1:]
    betting_on = ''
    bets = 0 
    aux = 0 
    
    global wallet
    
    count = 0
    
    while len(shoe) > card_limit:
        
        #Placing bet
        if aux > 9:
            
            if count >= 128:
                betting_on = 'PLAYER'

                bets += 1
                wallet += -1
            #else:
                #betting_on = 'BANKER'
                #bets += 1
                #wallet += -1
            
                      
            
        
        #Dealing cards
        player = [shoe[0][0],shoe[2][0]]
        banker = [shoe[1][0],shoe[3][0]]
        player_cards = 2
        banker_cards = 2
        idx = 4
        
        #Counting Cards
        drawn = [shoe[0][1],shoe[1][1],shoe[2][1],shoe[3][1]]
        count += sum(drawn)
        
        #Calculating Sums
        player_sum = sum(player) % 10
        banker_sum = sum(banker) % 10
        
        #3rd card step
        if (player_sum < 8 and banker_sum < 8):
            
            if player_sum <= 5:
                
                #player draws a third card
                player_cards += 1
                player_third_card = shoe[idx][0]
                count += shoe[idx][1]
                idx += 1
                                
                player_sum = (player_sum + player_third_card) % 10
                
                #If the player does take a third card then the Bank's third-card-rule below will determine if the bank takes 
                #    a third card.
                #If the bank's total is 2 or less then bank draws a card, regardless of what the players third card is.
                #If the banks total is 3 then the bank draws a third card unless the players third card was an 8.
                #If the banks total is 4 then the bank draws a third card unless the players third card was a 0, 1, 8, or 9.
                #If the banks total is 5 then the bank draws a third card if the players third card was 4, 5, 6, or 7.
                #If the banks total is 6 then the bank draws a third card if the players third card was a 6 or 7.
                #If the banks total is 7 then the bank stands.
                if banker_sum <= 2:
                    banker_cards += 1
                    banker_sum = (banker_sum + shoe[idx][0]) % 10
                    count += shoe[idx][1]
                    idx += 1
                                        
                elif banker_sum == 3 and not player_third_card == 8:
                    banker_cards += 1
                    banker_sum = (banker_sum + shoe[idx][0]) % 10
                    count += shoe[idx][1]
                    idx += 1
                                        
                elif banker_sum == 4 and not (player_third_card in [0,1,8,9]):
                    banker_cards += 1
                    banker_sum = (banker_sum + shoe[idx][0]) % 10
                    count += shoe[idx][1]
                    idx += 1
                                        
                elif banker_sum == 5 and (player_third_card in [4,5,6,7]):
                    banker_cards += 1
                    banker_sum = (banker_sum + shoe[idx][0]) % 10
                    count += shoe[idx][1]
                    idx += 1
                                        
                elif banker_sum == 6 and (player_third_card in [6,7]):
                    banker_cards += 1
                    banker_sum = (banker_sum + shoe[idx][0]) % 10
                    count += shoe[idx][1]
                    idx += 1
                    
                #else:
                    #bank does not take a third card, done
                    
            else:
    
                #player does not draw a third card
                if banker_sum < 6:
                    banker_cards += 1
                    banker_sum = (banker_sum + shoe[idx][0]) % 10
                    count += shoe[idx][1]
                    idx += 1  
                    
                #else:
                    #bank does not take a third card, done 
                    
        winner = check_winner(player_sum, banker_sum, player_cards, banker_cards)
            
        if winner == 'TIE':
            wallet += bets
            bets = 0 
            
        elif winner == betting_on:
            
            if winner == 'PLAYER':
                wallet += 2*bets
                bets = 0
                
            elif winner == 'BANKER':
                wallet += 1.95*bets
                bets = 0 
        else:
            bets = 0
            
             
        
        shoe = shoe[idx:]
        aux += 1
        
        
    #return [count,shoe]

for i in range(1, no_games):

    play_shoe()

    sys.stdout.write("\033[F") #cursor up one line
    sys.stdout.write("\033[K") #clear current line
    print 'Progress %.2f --- Wallet: %.2f ---' % ((i / no_games)*100, wallet)