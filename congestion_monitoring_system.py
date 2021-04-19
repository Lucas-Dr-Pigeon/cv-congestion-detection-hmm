 # -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import networkx as nx
import math
import sys
import matplotlib.pyplot as plt
from collections import deque
import preprocessing as prep
import time


def virtual_State(convoy):
    VS = {}
    for v in list(convoy.values())[0]:
        vs = list(convoy.values())[0][v]
        vs["State"] = "00"
        VS[v] = vs
    return VS


class Wave:
    def __init__(self,red,index):
        self.propa_v = 120
#        self.last_propa_v = self.propa_v
#       set the initial propagation speed of wave to the free flow speed
        self.stamp = 0
        self.black = []
        self.red = red
        self.blue = []
        self.nextzone = []
        self.index = index
        self.empty = 0
        self.loc = -1
        self.lastLoc = -1
        self.suspend = 1
        self.__Loc__()
        self.__Next_Zone__()
        
    def __Lapse__(self):
        print("====Wave #"+str(self.index)+"====")
#        print("******Reds******")
#        print(self.red)
#        print("******Blacks********")
#        print(self.black)
        print("Est. Propa Speed: "+ str(self.propa_v))
        print("Est. Front Loc: "+ str(self.loc))
        print("Est. Next Zone: "+ str(self.nextzone))
        print("Suspend: "+ str(self.suspend) +"s")
        print(len(self.red)>0)
        self.stamp += 1
#        self.__Transfer__()
        self.__Loc__()
        self.__Propa_Est__()
        self.__Next_Zone__()

    def __Clean__(self):
        self.black = []
        self.red = []
        self.blue = []
#        self.black = [B for B in self.black if B["Speed"]>20]
#        self.red = [R for R in self.red if R["Speed"]>20]
#        self.black = self.black + self.red
#        self.red = []

    def __Empty__(self):
        if len(self.black)+len(self.red) == 0:
            self.empty = 1
    
    def __Loc__(self):
        if self.stamp > 0:
            self.lastLoc = self.loc
        if len(self.red) > 0:
            t_Loc = self.red[0]["Location"]
            for R in self.red:
                t_Loc = min(R["Location"],t_Loc)
            self.loc =t_Loc
            self.suspend = 1
        else:
            self.suspend += 1
        
    def __Propa_Est__(self):
#        print(len(self.red)>0 )
        if len(self.red) > 0 and self.stamp > 0:
                t_propa_v = (self.lastLoc-self.loc)/0.1
                if self.propa_v == 120:
                    self.propa_v = min(t_propa_v,120)
                else:
                    self.propa_v = min((self.propa_v*(self.stamp-1) + t_propa_v)/self.stamp,120)
        if len(self.red) == 0 and self.propa_v == 0:
           self.propa_v = 120
          
    def __Next_Zone__(self):   
        self.nextzone = [self.loc-self.propa_v*0.1*self.suspend-10, self.loc]
         
          
class CM_System:   
    def __Scan__(self):
#       what if some vehicles exiting or joining in the convoy
        self.prev_state = self.state
        self.state = self.convoy[self.time]
        for s in self.state:
            self.state[s]["Vehicle"] = s
            if s in self.prev_state:
                try:
                    if self.prev_state[s]["Speed"] <= self.thres_v and self.state[s]["Speed"] <= self.thres_v:
                        self.state[s]["State"] = "11"
                        self.state[s]["Wave"] = self.prev_state[s]["Wave"]
                        self.waves[self.state[s]["Wave"]].black.append(self.state[s])
                    elif self.prev_state[s]["Speed"] > self.thres_v and self.state[s]["Speed"] <= self.thres_v:
                        self.state[s]["State"] = "01"
                        sort = 0
                        for W in self.waves:
                            if self.waves[W].nextzone[0] <= self.state[s]["Location"] <= self.waves[W].nextzone[1]:
                                self.state[s]["Wave"] = W
                                self.waves[W].red.append(self.state[s])
                                sort = 1
                                break
                        if sort == 0:
                            self.unsorted_congest.append(self.state[s])
                    elif self.prev_state[s]["Speed"] <= self.thres_v and self.state[s]["Speed"] > self.thres_v:
                        self.state[s]["State"] = "10"
                        self.state[s]["Wave"] = self.prev_state[s]["Wave"]
                        self.waves[self.state[s]["Wave"]].blue.append(self.state[s])
                        self.state[s]["Wave"] = 0
                    elif self.prev_state[s]["Speed"] > self.thres_v and self.state[s]["Speed"] > self.thres_v:  
                        self.state[s]["State"] = "00"
                        self.state[s]["Wave"] = 0
                except KeyError:
                    continue
            else:
                if self.state[s]["Speed"] > self.thres_v:
                    self.state[s]["State"] = "00"
                else:
                    self.state[s]["State"] = "01"
                    for W in self.waves:
                        if self.waves[W].nextzone[0] <= self.state[s]["Location"] <= self.waves[W].nextzone[1]:
                            self.state[s]["Wave"] = W
                            self.waves[W].red.append(self.state[s])
                            sort = 1
                            break
        self.__Create_Waves__()
        
#                    self.unsorted_congest.append(self.state[s])
#                    Well, how to deal with the new joining vehicles?  
    def __init__(self,convoy,thres_v,lead):
        self.convoy = convoy
        self.time = list(convoy.keys())[0]
        self.init_time = self.time
        self.convoy_size = len(list(self.convoy.values())[0])
        self.thres_v = thres_v
        self.state = virtual_State(self.convoy)
        self.prev_state = self.state
        self.unsorted_congest = []
        self.updated_congest = [] 
        self.waves={}
        self.__Scan__()
        self.wave_count = 1
        self.trajectory = {}
        self.speedsplot = {}
        self.waves_record = {}
        self.state_record = {}
        self.ffs = 120
        self.lead = lead 
            
    def __Lapse__(self):
        self.__Record__()
        self.time += 1
        print("================="+str(self.time)+"====================")
        self.convoy_size = len(list(self.convoy[self.time]))
        self.__Waves_Clean__()
        self.__Scan__()
        self.__Waves_Transfer__() 
        self.__Dissip__()

             
                    
    def __Create_Waves__(self): 
#        sort_class = {self.unsorted_congest[0]:1}
        s_congest = self.unsorted_congest
        sort_class = {}
        while (len(s_congest)>0):
            sort_class[self.wave_count] = [s_congest[0]]
            self.state[s_congest[0]["Vehicle"]]["Wave"] = self.wave_count
            for cong0 in s_congest :
                ss_congest = []
                for cong1 in s_congest:
                    if (cong1 == cong0):
                        continue
                    if abs(cong0["Location"]-cong1["Location"]) <= 10:
                        cong1["Wave"] = self.wave_count
                        self.state[cong1["Vehicle"]]["Wave"] = self.wave_count
                        sort_class[self.wave_count].append([cong1])   
                    else:
                        ss_congest.append(cong1)
            s_congest = ss_congest
            newWave = Wave(index = self.wave_count,red=sort_class[self.wave_count]) 
            self.waves[self.wave_count] = newWave
            self.wave_count += 1
        self.unsorted_congest = []
            
#        while(len(self.unsorted_congest)>0):
#            unsort = []
#            new_wave = Wave(red = [self.unsorted_congest[0]],index = self.wave_count)
#            cong0 = self.unsorted_congest[0]
#            for cong1 in self.unsorted_congest:
#                if (cong1 == cong0): 
#                    continue
#                if abs(cong0["Location"]-cong1["Location"]) <= 10:
#                    new_wave.red.append(cong1)
#                    sort_class[cong1] = sort_count
#                else:
#                    unsort.append(cong1)
#                
#        while(len(self.unsorted_congest)>0):
#            new_wave = Wave(red = [self.unsorted_congest[0]],index=self.wave_count)
#            cong0 = self.unsorted_congest[0]
#            self.unsorted_congest.remove(cong0)
#            for cong1 in self.unsorted_congest:
#                if abs(cong0["Location"]-cong1["Location"]) <= 10:
#                    new_wave.red.append(cong1)
#                    self.unsorted_congest.remove(cong1)
#            self.waves[self.wave_count]=new_wave
#            self.wave_count+=1
    def __Waves_Clean__(self):
        for W in self.waves:
            self.waves[W].__Clean__()
        
    def __Waves_Transfer__(self):
#        wave_dissip = []
        for W in self.waves:
#            if self.waves[W].empty == 1:
#                wave_dissip.append(W)
#                continue
#            else:
                self.waves[W].__Lapse__()
#        for W in wave_dissip:
#            del self.waves[W]
    def __Dissip__(self):
        wave_dissip = []
        for W in self.waves:
            self.waves[W].__Empty__()
            if (self.waves[W].empty == 1):
                wave_dissip.append(W)
        for W in wave_dissip:
            del self.waves[W]
                
    def __Proceed__(self,frame): 
        for t in range(self.init_time, frame):
            self.__Lapse__()
            
    def __Time_Spac__(self):
        for t in self.convoy:
            for v in self.convoy[t]:
                if v not in self.trajectory:
                    self.trajectory[v] = {"times":[], "locations":[]}
                    self.trajectory[v]["times"].append(t)
                    self.trajectory[v]["locations"].append(self.convoy[t][v]["Location"])
                else:
                    self.trajectory[v]["times"].append(t)
                    self.trajectory[v]["locations"].append(self.convoy[t][v]["Location"])
        for vv in self.trajectory:
            plt.plot(self.trajectory[vv]["times"],self.trajectory[vv]["locations"])
        plt.show()    
        
    def __Plot_Speed_Acc__(self,veh):
        times = []
        speeds = []
        acc = []
        for t in self.convoy:
            for v in self.convoy[t]:
                if v == veh:
                    times.append(t)
                    speeds.append(self.convoy[t][v]["Speed"])
                    acc.append(self.convoy[t][v]["Acc"])
        plt.plot(times,speeds)
        plt.plot(times,acc)
        plt.show()
        
    def __Stat_Wavelet_(self):
        for t in self.convoy:
            axes = plt.gca()
            axes.set_ylim(-15,15)
            xscale = []
            vscale = []
            for v in self.convoy[t]:
                xscale.append(self.convoy[t][v]["Location"])
                vscale.append(self.convoy[t][v]["Speed"])
            line, = axes.plot(xscale,vscale)
            line.set_xdata(xscale)
            line.set_ydata(vscale)
            plt.draw()
            plt.pause(1e-17)
            time.sleep(0.1)
            plt.show()
            
    def __Plot_Speeds__(self):
        for t in self.convoy:
            for v in self.convoy[t]:
                if v not in self.speedsplot:
                    self.speedsplot[v] = {"times":[], "speeds":[]}
                    self.speedsplot[v]["times"].append(t)
                    self.speedsplot[v]["speeds"].append(self.convoy[t][v]["Speed"])
                else:
                    self.speedsplot[v]["times"].append(t)
                    self.speedsplot[v]["speeds"].append(self.convoy[t][v]["Speed"])
        for vv in self.speedsplot:
            plt.plot(self.speedsplot[vv]["times"],self.speedsplot[vv]["speeds"])
        plt.show()     
        
    def __Record__(self):
        self.waves_record[self.time] = {}
        self.state_record[self.time] = {}
        for W in self.waves:
            self.waves_record[self.time][self.waves[W].index] = {"P_Speed":round(self.waves[W].propa_v,3),"Front_Loc":round(self.waves[W].loc,3),"P_Zone":[round(self.waves[W].nextzone[0],3),round(self.waves[W].nextzone[1],3)],"Black":self.waves[W].black,"Red":self.waves[W].red}
        for v in self.state:
            try:
                self.state_record[self.time][v] = self.state[v]["Wave"]
            except:
                self.state_record[self.time][v] = 0
                


            
        
        
            
            
        