from __future__ import division
import random
import sys, getopt
from math import *
import pandas as pd

global game_type
game_type="standard"

no_games = 10000

def check_winner(player_sum, banker_sum):
    
    if (player_sum > banker_sum):
        return 'PLAYER'
    
    elif (banker_sum > player_sum):
        return 'BANKER'
    
    else:
        return 'TIE'

def shoe_shuffle():

    suit = [(1,440), (2,522), (3,649), (4,1157), (5,-827), (6,-1132), (7,-827), (8,-502), (9,-231), (10,188), (10,188), (10,188), (10,188)]
    deck = suit + suit + suit + suit
    bdeck = deck + deck + deck + deck + deck + deck + deck + deck
    random.shuffle(bdeck)
    random.shuffle(bdeck)

    return bdeck

def play_shoe():

    shoe = shoe_shuffle()
    card_limit = 26
    shoe = shoe[shoe[0][0]+1:]
    out = []
    count = 0

    while len(shoe) > card_limit:
        
        #Dealing cards
        player = [shoe[0][0],shoe[2][0]]
        banker = [shoe[1][0],shoe[3][0]]
        player_cards = 2
        banker_cards = 2
        idx = 4
        count_beg = count

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
              
        shoe = shoe[idx:]
        
        result = [(winner,count_beg)]
        out += result

    return out

data = []

for i in range(1, no_games):

    data = data + play_shoe()

    sys.stdout.write("\033[F") #cursor up one line
    sys.stdout.write("\033[K") #clear current line
    print 'Progress %.2f' % ((i / no_games)*100)

final = pd.DataFrame(data,columns = ['WINNER','COUNT'])

csv_out = final[(final['COUNT'] > -5000) & (final['COUNT'] < 5000)].pivot_table(index = 'COUNT', columns= 'WINNER', aggfunc= len, fill_value=0)

csv_out.to_csv('C:/Users/fs1556/Documents/GitHub/Baccarat-Strategy/count.csv')