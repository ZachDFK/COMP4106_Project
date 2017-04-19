#Comodity transportation puzzle

from . import puzzle
import random
import copy
from ..ai import ai
import time
 
class game_model:
    
    alphabet_con = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','V','W','X','Y','Z']
    alphabet_vow = ['A','E','I','O','U']
    
    
    
    def __init__(self,game_view,rounds):
        self.flag = True
        self.rounds = rounds
        self.game_view = game_view
        self.players = game_model.generate_players()
    def init_numbers_for_number_round(self):
        self.answer = random.randint(100,999 )
        self.options = []
        
        for i in range(0,6):
            self.options.append(random.randint(1,50))
        #print(self.answer)
        #print(self.options)
        
        
    def is_goal_reached(self,number):
        return self.answer == number
    def is_start_reached(self,number):
        return self.tracker == number
    def undo_operation(number1,number2,type):
        if type == 0:
            return game_model.substraction(number1, number2)
        elif type == 1:
            return game_model.addition(number1, number2)
        elif type == 2:
            return game_model.multiplication(number1, number2)
        else:
            return game_model.division(number1, number2)
        
    def make_operation(number1,number2,type):
        if type == 0:
            return game_model.addition(number1, number2)
        elif type == 1:
            return game_model.substraction(number1, number2)
        elif type == 2:
            return game_model.division(number1,number2)
        else:
            return game_model.multiplication(number1, number2)
    def init_letters_for_letter_round(self):
        self.letters = []
        desired_con = 4
        desired_vow = 3
        for i in range(0,7):
            if random.uniform(0,1) > desired_vow/desired_con:
                self.letters.append(game_model.grab_con())
                desired_con = desired_con - 1
            else:
                self.letters.append(game_model.grab_vow())
                desired_vow = desired_vow - 1
        print(self.letters)
        
    def grab_con():
        return game_model.alphabet_con[random.randint(0,20)]
    def grab_vow():
        return game_model.alphabet_vow[random.randint(0,4)]
    
    def run(self):
        p1_win = 0
        p2_win = 0
        p_match = 0
        p_total = 0
        for i in range(0,self.rounds):
            self.init_round()
            p_stats = []
            for p in range(0,2):
                p_stats.append(self.playing_game(self.players[p]))
            #print(p_stats)
            if p_stats[0][1] != 'N/A' and p_stats[1][1] != 'N/A':
                p_total = p_total + 1
                if p_stats[0][1] == p_stats[1][1]:
                    p_match = p_match + 1
                if p_stats[0][0] > p_stats[1][0]:
                    p1_win = p1_win + 1
                else:
                    p2_win = p2_win + 1
        
        p1_win_rate = p1_win/p_total
        p2_win_rate = p2_win/p_total
        p_match_rate = p_match/p_total
        p_string = "P1 win rate : " + str(p1_win_rate) + "%| " + "P2 win rate : " + str(p2_win_rate) + "%|" + "Matching Soln. : " + str(p_match_rate) + "%|" 
        return  p_string
    def init_round(self):
        self.init_numbers_for_number_round()

    def update_view(self):
        self.game_view.update()
    
    def generate_players():
        player1 = ai.AI('top')
        player2 = ai.AI('bottom')
        players = [player1,player2]
        return players
    
    def multiplication(number1,number2):
        return number1 * number2
    
    def division(number1,number2):
        if number1%number2 == 0:
            return int(number1/number2)
        else:
            return -1
    def addition(number1,number2):
        return number1 + number2
    
    def substraction(number1,number2):
        if number1 - number2 > 0:
            return number1-number2
        else:
            return -1
    
    def playing_game(self,player):
        self.tracker = 0;
        start_time = time.time()
        ans_str = player.find_solution(self)
        end_time = time.time()
        elasped_time = end_time-start_time
        stats = [elasped_time,ans_str]
        return stats
        
    def heuristic(self,type=None):
        return abs(self.tracker-self.answer)