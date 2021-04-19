# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 01:52:58 2020

@author: Lucas
"""
import numpy as np
import pandas as pd
import networkx as nx
import math
import sys
import matplotlib.pyplot as plt
from collections import deque
import preprocessing as prep
import time
import scipy.stats
class HMM2:
    def __mean_speed__(self):
        if self.time > self.init_time:
            self.prev_speed = self.speed
            agg_v = 0
            count_v = 0
            for v in self.convoy[self.time]:
                if v in self.convoy[self.prev]:
                    agg_v += 0.1/(self.convoy[self.time][v]["Location"]-self.convoy[self.prev][v]["Location"]+0.0000000000000000000001)
                    count_v += 1
            self.speed = count_v/agg_v*3.6
            self.speeds[self.time] = self.speed
        
    def __loc__(self):
        if self.time > self.init_time:
            self.prev_loc = self.loc
        agg_loc = 0
        count_loc = 0
        for v in self.convoy[self.time]:
            agg_loc += self.convoy[self.time][v]["Location"]
            count_loc += 1
        self.loc = agg_loc/count_loc
        
    def __Emission_Dens__(self,uf = 93.51, kj = 197.58):
        u= self.speed
        self.prev_ems_dens = self.ems_dens
#        self.ems_dens = min(kj*math.exp(u/lambd),120)
        self.ems_dens = min(kj*(1-(u/uf)**(1/3)),130)
        self.ems_denss[self.time] = self.ems_dens
    
    def __Transition_Dens__(self):
        self.trans_dens = min(130,self.prev_ems_dens*(self.prev_speed*self.step+self.loc-self.prev_loc)/(self.speed*self.step+self.loc-self.prev_loc))
        self.trans_denss[self.time] = self.trans_dens
              
    def __init__(self, convoy):
        self.step = 1
        self.convoy = convoy
        self.init_time = list(convoy.keys())[0]
        self.time = self.init_time
        self.speed = 0
        self.prev_speed = 0
        self.loc = 0
        self.prev = 0
        self.prev_loc = 0
        self.func = "norm"
        self.speeds = {}
        self.ems_denss = {}
        self.trans_denss = {self.init_time:"N/A"}
        self.__loc__()
        self.ifconverg = 0
        self.__ifconverg__()
        self.hmm = {}
        self.prediction = {}
        self.curr_state = -1
        self.prev_state = -1
        self.prev_ems_dens = -1
        self.ems_dens = -1
        self.trans_dens = -1
#        self.__emission__()
        
        self.predictions = {}
        self.true_density = {}
        
       
    def __ifconverg__(self):
        if self.time > self.init_time+1:
            if self.speed <= 5:
                self.ifconverg = 1
                self.curr_state = 2
            elif self.speed >= 70: 
                self.ifconverg = 0
                self.curr_state = 0
    
    def __lapse__(self):
        self.prev = self.time
        self.time += self.step 
        self.__ifconverg__()
        self.__mean_speed__()
        if self.time == self.init_time + 1:
            self.__Emission_Dens__()
            self.hmm[self.init_time+1] = {}
            emits = [scipy.stats.norm(25,25).pdf(self.ems_dens), scipy.stats.norm(60,30).pdf(self.ems_dens),scipy.stats.norm(90,35).pdf(self.ems_dens)]
            self.hmm[self.init_time+1][0] = emits[0]/(emits[0]+emits[1] + emits[2])
            self.hmm[self.init_time+1][1] = emits[1]/(emits[0]+emits[1] + emits[2])
            self.hmm[self.init_time+1][2] = emits[2]/(emits[0]+emits[1] + emits[2])
#           self.__true_density__()
        self.__loc__()
        self.__Emission_Dens__()
        self.__Transition_Dens__()
        self.__transition__()
        
#        try:
#            self.prev = self.time
#            self.time += self.step 
#            self.__ifconverg__()
#            self.__mean_speed__()
#            if self.time == self.init_time + 1:
#                self.__Emission_Dens__()
#                self.hmm[self.init_time+1] = {}
#                emits = [scipy.stats.norm(25,25).pdf(self.ems_dens), scipy.stats.norm(60,30).pdf(self.ems_dens),scipy.stats.norm(90,35).pdf(self.ems_dens)]
#                self.hmm[self.init_time+1][0] = emits[0]/(emits[0]+emits[1] + emits[2])
#                self.hmm[self.init_time+1][1] = emits[1]/(emits[0]+emits[1] + emits[2])
#                self.hmm[self.init_time+1][2] = emits[2]/(emits[0]+emits[1] + emits[2])
##            self.__true_density__()
#            self.__loc__()
#            self.__Emission_Dens__()
#            self.__Transition_Dens__()
#            self.__transition__()
#        except KeyError:
#            pass
#        
#    def __emission__(self):
#        if self.func == "norm":
#            if self.time > self.init_time:
#                self.hmm[self.time] = {}
#                self.hmm[self.time][0] *= scipy.stats.norm(25,25).pdf(self.Greenburgs(self.speed))
#                self.hmm[self.time][1] *= scipy.stats.norm(60,30).pdf(self.Greenburgs(self.speed))
#                self.hmm[self.time][2] *= scipy.stats.norm(90,35).pdf(self.Greenburgs(self.speed))
#                if self.hmm[self.time][0] == max(self.hmm[self.time][0],self.hmm[self.time][1],self.hmm[self.time][2]):
#                    print ("FLUENT")
#                elif self.hmm[self.time][1] == max(self.hmm[self.time][0],self.hmm[self.time][1],self.hmm[self.time][2]):
#                    print ("MEDIUM")
#                else:
#                    print ("HEAVY")
                
    def __transition__(self):
        if self.func == "norm":
            if self.time > self.init_time+1:
                self.hmm[self.time] = {}
                if self.curr_state == 0:
                    try:
                        self.hmm[self.time][0] = 1
                        self.hmm[self.time][1] = 0
                        self.hmm[self.time][2] = 0
                    except KeyError:
                        self.hmm[self.time][0] = 1
                        self.hmm[self.time][1] = 0
                        self.hmm[self.time][2] = 0
                else:
                    emits = [scipy.stats.norm(30,30).pdf(self.ems_dens),scipy.stats.norm(70,30).pdf(self.ems_dens),scipy.stats.norm(110,40).pdf(self.ems_dens)]
                    transits = [scipy.stats.norm(30,30).pdf(self.trans_dens), scipy.stats.norm(70,30).pdf(self.trans_dens), scipy.stats.norm(110,40).pdf(self.trans_dens)]
                    self.hmm[self.time][0] = max(self.hmm[self.prev][0] *emits[0]/(emits[0]+emits[1]+emits[2]) *transits[0]/(transits[0]+transits[1]) ,
                            self.hmm[self.prev][1] *emits[0]/(emits[0]+emits[1]+emits[2]) *transits[0]/(transits[0]+transits[1]))
                self.hmm[self.time][1] = max(self.hmm[self.prev][0] *emits[1]/(emits[0]+emits[1]+emits[2]) *transits[1]/(transits[0]+transits[1]+transits[2]) ,
                        self.hmm[self.prev][1] *emits[1]/(emits[0]+emits[1]+emits[2]) *transits[1]/(transits[0]+transits[1]+transits[2]), 
                        self.hmm[self.prev][2] *emits[1]/(emits[0]+emits[1]+emits[2]) *transits[1]/(transits[0]+transits[1]+transits[2]))
                if self.curr_state == 2:
                    try:
                        self.hmm[self.time][2] = 1
                        self.hmm[self.time][0] = 0
                        self.hmm[self.time][1] = 0
                    except KeyError:
                        self.hmm[self.time][2] = 1
                        self.hmm[self.time][0] = 0
                        self.hmm[self.time][1] = 0
                else:
                    self.hmm[self.time][2] = max(self.hmm[self.prev][1] *emits[2]/(emits[0]+emits[1]+emits[2]) *transits[2]/(transits[1]+transits[2]),
                            self.hmm[self.prev][2] *emits[2]/(emits[0]+emits[1]+emits[2]) *transits[2]/(transits[1]+transits[2]))
        
                if (self.time - self.init_time+1)%100 == 0 and (self.time - self.init_time+1)/100 >= 1:
                        self.hmm[self.time][2] *= 10**100
                        self.hmm[self.time][0] *= 10**100
                        self.hmm[self.time][1] *= 10**100
        
        
        
                if self.hmm[self.time][0] == max(self.hmm[self.time][0],self.hmm[self.time][1],self.hmm[self.time][2]):
                    print ("FLUENT")
                    self.predictions[self.time] = "FLUENT"
                elif self.hmm[self.time][1] == max(self.hmm[self.time][0],self.hmm[self.time][1],self.hmm[self.time][2]):
                    print ("MEDIUM")
                    self.predictions[self.time] = "MEDIUM"
                else:
                    print ("HEAVY")
                    self.predictions[self.time] = "HEAVY"
#                est = self.__Transition_Prob__(self.__Emission_Prob__(self.prev_speed),self.prev_speed,self.speed,self.loc-self.prev_loc,self.step*0.1)
#                self.hmm[self.time][0] = max(self.hmm[self.time-self.step][0] * scipy.stats.norm(25,25).pdf(est),self.hmm[self.time-self.step][1] * scipy.stats.norm(25,25).pdf(est))
#                self.hmm[self.time][1] = max(self.hmm[self.time-self.step][0] * scipy.stats.norm(60,30).pdf(est),self.hmm[self.time-self.step][1] * scipy.stats.norm(60,30).pdf(est),self.hmm[self.time-self.step][2] * scipy.stats.norm(60,30).pdf(est))
#                self.hmm[self.time][2] = max(self.hmm[self.time-self.step][0] * scipy.stats.norm(90,50).pdf(est)
#                
    
            
    def __proceed__(self,frame):
        for t in range(self.init_time+1, frame + 1):
            self.__lapse__()
    
    def __true_density__(self,frame):
        for t in range(self.init_time+1, frame + 1):
            if t < self.init_time+1 + 10:
                continue
            else:
#                in_out_time = {}
                total_time = 0
                area_dist = [999999,-1]
                area_time = 1
                for tt in range(t - 10, t + 1):
                    for v in self.convoy[tt]:
                            area_dist[0] = min(area_dist[0], self.convoy[tt][v]["Location"])
                            area_dist[1] = max(area_dist[1], self.convoy[tt][v]["Location"])
                            total_time += len(self.convoy[tt])
                self.true_density[t - 5] = total_time/((area_dist[1] - area_dist[0])*area_time)
#                        if v not in in_out_time:
#                            in_out_time[v] = [9999999,-1]
#                            in_out_time[v][0] = min(in_out_time[v][0], tt)
#                            in_out_time[v][1] = max(in_out_time[v][1], tt)
                            
#                        else:
#                            in_out_time[v][0] = min(in_out_time[v][0], tt)
#                            in_out_time[v][1] = max(in_out_time[v][1], tt)
#                            total_time += 0.1
                            
                            
                
                            
                    
                    
        
        
                         
