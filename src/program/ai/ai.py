#AI class
import copy
import sys
from ..puzzles import game_model
class AI:
    def __init__(self,style):
        self.style = style
    
    def find_solution(self,numbergame):
        self.temp_options = copy.deepcopy(numbergame.options)
        
        if self.style == "bottom":
            return self.goal_oriented_search(numbergame,)
        else:
            return self.start_oriented_search(numbergame,self.temp_options)
        
        
    def start_oriented_search(self,numbergame,temp_options):
        path = []
        closest_path = []
        closest_answer = numbergame.answer 
        tracker = 0            
        for n in range(0,len(temp_options)):
            path = []
            new_options =  copy.deepcopy(temp_options)
            tracker = new_options.pop(n) 
            path.append(tracker)
            pot_answer,ans_path = self.rec_dfs_start(new_options,tracker,numbergame.answer,path,closest_answer,closest_path)
            if pot_answer == numbergame.answer:
                ans_path.append(4)
                ans_path.append(pot_answer)
                break
        
        return AI.rephrase_answer(ans_path)
    
    
    def rec_dfs_start(self,options,tracker,answer,path,closest_answer,closest_path):
        
        for i in range(0,4):
            path.append(i)
            for n in range(0,len(options)):              
                current_num = options[n]
                check = game_model.game_model.make_operation(tracker,current_num,i)
                path.append(current_num)                  
                if check > 0:
                    tracker = game_model.game_model.make_operation(tracker,current_num,i)
                                        
                    if len(options) == 1:
                        if tracker == answer:
                            return tracker,path
                        else:
                            if abs(tracker - answer) < closest_answer:
                                closest_answer = abs(tracker-answer)
                                closest_path = path
                        
                    else:
                        new_options = copy.deepcopy(options)
                        new_options.pop(n)
                        pot_answer,ans_path = self.rec_dfs_start(new_options, tracker, answer, path, 
                                           closest_answer, 
                                           closest_path)
                        if pot_answer == answer:
                            return pot_answer,ans_path
                        else:
                            closest_answer, closest_path = pot_answer, ans_path
                    
                    tracker = game_model.game_model.undo_operation(tracker,current_num,i)
                path.pop()
            path.pop()    
        return closest_answer,closest_path 
    def goal_oriented_search(self,numbergame):
        path = []
        closest_path = []
        closest_answer = numbergame.answer 
        tracker = numbergame.answer
        new_options =  copy.deepcopy(self.temp_options)

        pot_answer,ans_path = self.rec_dfs_goal(new_options, tracker, numbergame.options, path, 
                                                                     closest_answer, closest_path)
        ans_path = AI.rephrase_org_path(ans_path,numbergame.answer)
        return AI.rephrase_answer(ans_path)
        
   
    def rec_dfs_goal(self,options,tracker,answers,path,closest_answer,closest_path):
        if len(options) == 2:
            temp_o = copy.deepcopy(options)
            for m in range(0,2):
                current_num = temp_o.pop(m)
                path.append(current_num)
                for j in range(0,4):
                    path.append(j)
                    temp_t = game_model.game_model.make_operation(current_num,temp_o[0],j)
                    if temp_t == tracker:
                        path.append(temp_o[0])
                        return temp_o[0],path
                    path.pop()
                path.pop()
                temp_o = copy.deepcopy(options)
        else:
            for i in range(0,4):
                path.append(i)
                for n in range(0,len(options)):              
                    current_num = options[n]
                    check = game_model.game_model.undo_operation(tracker,current_num,i)
                    path.append(current_num)                  
                    if check > 0:
                        tracker = game_model.game_model.undo_operation(tracker,current_num,i)
                                            
                        if len(options) == 1:
                            if tracker == options[0]:
                                return tracker,path
                            else:
                                if abs(tracker - options[0]) < closest_answer:
                                    closest_answer = abs(tracker-options[0])
                                    closest_path = path
                            
                        else:
                            new_options = copy.deepcopy(options)
                            new_options.pop(n)
                            pot_answer,ans_path = self.rec_dfs_goal(new_options, tracker, answers, path, 
                                               closest_answer, 
                                               closest_path)
                            if pot_answer in options:
                                return pot_answer,ans_path
                            else:
                                closest_answer, closest_path = pot_answer, ans_path                
                        tracker = game_model.game_model.make_operation(tracker,current_num,i)
                    path.pop()
                path.pop()    
        return closest_answer,closest_path
    
    def rephrase_answer(ans_path):
        ans_str = ""
        stage = 0
        for val in ans_path:
            if stage%2 == 0:
                if stage+1 != len(ans_path) and stage != 0:
                    ans_str = "(" + ans_str + str(val) + ")"
                else:
                    ans_str = ans_str + str(val) 
            else:
                opp_str = ""
                if val == 0:
                    opp_str = " + "
                elif val == 1:
                    opp_str = " - "
                elif val == 2:
                    opp_str = " / "
                elif val == 3:
                    opp_str = " * "
                else:
                    opp_str = " = "
                ans_str = ans_str + opp_str
            stage = stage + 1
        if stage == 1:
            ans_str = "N/A"
        return ans_str
    def rephrase_org_path(ans_path,answer):
        new_path = []
        if len(ans_path) > 1:
            new_path.append(ans_path.pop(8))
            new_path.append(ans_path.pop(8))
            new_path.append(ans_path.pop(8))
            for i in range(0,4):
                new_path.insert(3,ans_path.pop(0))
                new_path.insert(4,ans_path.pop(0))
            new_path.append(4)
            new_path.append(answer)
            
        else:
            new_path = [0]
        return new_path
