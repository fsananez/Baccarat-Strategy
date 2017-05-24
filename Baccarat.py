from __future__ import division
import random
import sys, getopt
from math import *

global game_type
game_type="standard"

no_games = 1000000

global wallet
wallet = 10000000

global earnings
earnings = 0

global betsize
betsize = 1 


def check_winner(player_sum, banker_sum):
    
    if (player_sum > banker_sum):
        return 'PLAYER'
    
    elif (banker_sum > player_sum):
        return 'BANKER'
    
    else:
        return 'TIE'

def shoe_shuffle():

    suit = [(1,1), (2,1), (3,2), (4,2), (5,-1), (6,-2), (7,-2), (8,-1), (9,0), (10,0), (10,0), (10,0), (10,0)]
    deck = suit + suit + suit + suit
    bdeck = deck + deck + deck + deck + deck + deck + deck + deck
    random.shuffle(bdeck)
    random.shuffle(bdeck)

    return bdeck

def play_shoe():

    shoe = shoe_shuffle()
    card_limit = 26
    shoe = shoe[shoe[0][0]+1:]
    
    global wallet
    global earnings
    global betsize


    count = 0
    betting_on = ''
    aux = 0
    
    while len(shoe) > card_limit:
        
        #Placing bet
        if aux > 9:
            
            if count < -5 :
                betting_on = 'PLAYER'
                
                if count < -24:
                    bets = betsize + 2
                    earnings += -betsize - 2
                else:
                    bets = betsize
                    earnings += -betsize

            #elif count > 3:
             #   betting_on = 'BANKER'
              #  
               # if count > 24:
                #    bets = betsize + 2
                 #   earnings += -betsize - 2
                #else:
                 #   bets = betsize
                  #  earnings += -betsize
            else:
                betting_on = ''     
            
        
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
                                        
                elif banker_sum == 4 and not (player_third_card in [1,8,9,10]):
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
                    
        winner = check_winner(player_sum, banker_sum)
            
        if winner == 'TIE':

            if betting_on != '':
                earnings += bets
            
        elif winner == betting_on:
            
            if winner == 'PLAYER':
                earnings += 2*bets
                
            elif winner == 'BANKER':
                earnings += 1.95*bets
            
            if earnings <= 0:

                if earnings + betsize + 1 > 1:
                    betsize = 1 - earnings

                else:
                    betsize += 1   
            
        if earnings > 0:
            wallet += earnings
            betsize = 1
            earnings = 0
        elif earnings < -25:
            wallet += earnings
            betsize = 1
            earnings = 0
            
        shoe = shoe[idx:]
        aux += 1



for i in range(1, no_games):

    play_shoe()

    sys.stdout.write("\033[F") #cursor up one line
    sys.stdout.write("\033[K") #clear current line
    print 'Progress %.2f --- Wallet: %.2f ---' % ((i / no_games)*100, wallet)