#Puzlle gui

import appJar
from .. import pseudomain
from ..definitions.constants import GuiConstants
from ..puzzles import game_model

class CountDown:

    def __init__(self,type):                        
        self.puzapp = appJar.gui(type,GuiConstants._GuiConstants__puzzle_size)
        self.assign_model()
        self.replicate()
    def assign_model(self):
        rounds = 10      
        self.game_mdoel = game_model.game_model(self,rounds)
    
    def replicate(self):
        reps = 3
        doc_strings = []
        for i in range(0,reps):
            doc_strings.append(self.game_mdoel.run())
            print(doc_strings[i])
        with open("output.txt", "w") as text_file:
                for string in doc_strings:
                    print(string, file=text_file)        
    def update(self):
        if self.game_mdoel.flag:
            pass
        else:
            pass
        
    def press(self,btn):
        self.game_mdoel.init_round()