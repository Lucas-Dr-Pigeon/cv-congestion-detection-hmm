# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 23:41:50 2020

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
from random import randint
from copy import deepcopy
class hmm7:
    def __scan_vehicles__(self):
        pass
    
    def __sparse__(self):
        sparse_convoy = {}
        whitelist = []
        blacklist = []
        for t in range(list(self.convoy.keys())[0], list(self.convoy.keys())[-1]):
            sparse_convoy[t] = {}
            self.sparse_convoy[t] = {}
            for v in self.convoy[t]: 
                if v not in whitelist and v not in blacklist:
                    if randint(0,100) > self.mpr:
                        blacklist.append(v)
                        print("blacklist: "+str(v))
                    else: 
                        whitelist.append(v)
                        print("whitelist: "+str(v))
                if v in blacklist:
                    continue
                elif v in whitelist:
                    sparse_convoy[t][v] = self.convoy[t][v]
                    self.sparse_convoy[t][v] = self.convoy[t][v]
        self.conovy = sparse_convoy
        
    def __random__(self):
        return randint(0,100)
    
    def __emit__(self, Kj = 150.40, Lambd = -35.30):
        u = self.speed
        self.prev_ems_dens = self.ems_dens
        self.ems_dens = Kj * math.exp(u/Lambd)
        self.ems_denss[str(self.time - self.window)+":"+str(self.time)] = min(130,self.ems_dens)
        
    def trans_prob(self,prev_s,s):
#        Ki = [25,40,55,70,85,100,115]
        Ki = [15,30,45,60,75,90,105]
        trans_index = Ki[prev_s]* ((self.prev_speed*10.1*self.window +self.delta_loc)/(self.speed*10.1*self.window +self.delta_loc) - 1)
        trans_p = scipy.stats.norm(Ki[s] - Ki[prev_s],30).pdf(trans_index)
        return trans_p
           
#    def __transit__(self):
#        self.trans_dens = min(130,self.prev_ems_dens*(self.prev_speed*0.1*self.window+self.delta_loc)/(self.speed*0.1*self.window+self.delta_loc))
        self.trans_denss[str(self.time - self.window)+":"+str(self.time)] = min(130,self.trans_dens)
    
    def __mean_speed__(self):
        if self.time >= self.init_time + self.window:
            if self.time >= self.init_time + self.window + 1:
                self.prev_speed = self.speed
            travel_dist = {}
            travel_time = {}
#            vehicle_list = []
#            for tt in range(self.time-self.window, self.time + 1):
#                for vv in list(self.convoy[tt].keys()):
#                    if vv not in vehicle_list:
#                        vehicle_list.append(vv)
            for t in range(self.time-self.window, self.time + 1):
                for v in self.convoy[t]:
                    if  v not in travel_dist:
                        travel_dist[v] = [99999,-1]
                        travel_time[v] = 0
                    travel_dist[v][0] = min(travel_dist[v][0], self.convoy[t][v]["Location"])
                    travel_dist[v][1] = max(travel_dist[v][1], self.convoy[t][v]["Location"])
                    travel_time[v] += 0.1
            harmo_speed = 0
            for v in travel_dist:
                if travel_time[v] != 0.1:
                    harmo_speed += travel_time[v] / (travel_dist[v][1] - travel_dist[v][0] + 0.1)
            self.speed = len(travel_dist)/harmo_speed *3.6
            self.speeds[str(self.time - self.window)+":"+str(self.time)] = self.speed
        self.__ifconverg__()
        
    def __loc__(self):
        sum_delta_loc = 0
        loc_count = 0
        if self.time >= self.init_time + self.window:
            for v in self.convoy[self.time]:
                if v in self.convoy[self.time - self.window]:
                    sum_delta_loc += (self.convoy[self.time][v]["Location"] - self.convoy[self.time - self.window][v]["Location"])
                    loc_count += 1
        self.delta_loc = sum_delta_loc / loc_count / 1000
                    
#list(Convoy484F[2150].keys())  
    def __ifconverg__(self):
        if self.time >= self.init_time + self.window:
            if self.speed <= 5:
                self.converg = 6
            elif self.speed >= 70: 
                self.converg = 0
            else: 
                self.converg = -1
                    
    
    def __init__(self,convoy,mpr):
        self.convoy = convoy
        self.mpr = mpr
        self.init_time = list(convoy.keys())[0]
        self.time = self.init_time
        self.window = 100
        self.sparse_convoy = {}
        self.__sparse__()
        self.convoy = self.sparse_convoy
        self.prev = 0
        self.speed = 0
        self.prev_speed = 0
        self.delta_loc = 0
        self.flow_alert = 0
#        self.loc = 0
#        self.prev_loc = 0
        
#        self.trajectories = {}
        self.converg = -1
        self.hmm = {}
        self.prev_ems_dens = 0
        self.ems_dens = 0
        self.trans_dens = 0
        self.true_densitys = {}
        self.predictions = {}
        self.ems_denss = {}
        self.trans_denss = {}
        self.speeds = {}
        self.true_congestions = {}
        
    def __lapse__(self):
#        self.prev = self.time
#        self.time += 1 
#        if self.time >= self.init_time + self.window:
#            self.__mean_speed__()
#            self.__loc__()
#            self.__emit__()
#            if self.time >= self.init_time + self.window + 1:
#                self.__transit__()
#                self.__Transition__()
#            else:
#                self.hmm[str(self.time - self.window)+":"+str(self.time)] = {0:0,1:0,2:0}
#                if self.converg == -1:
#                    emits = [scipy.stats.norm(25,25).pdf(self.ems_dens), scipy.stats.norm(60,30).pdf(self.ems_dens),scipy.stats.norm(90,35).pdf(self.ems_dens)]
#                    self.hmm[str(self.time - self.window)+":"+str(self.time)][0] = emits[0]/(emits[0]+emits[1] + emits[2])
#                    self.hmm[str(self.time - self.window)+":"+str(self.time)][1] = emits[1]/(emits[0]+emits[1] + emits[2])
#                    self.hmm[str(self.time - self.window)+":"+str(self.time)][2] = emits[2]/(emits[0]+emits[1] + emits[2])
#                else:
#                    self.hmm[str(self.time - self.window)+":"+str(self.time)][self.converg] = 1
        try:
            self.prev = self.time
            self.time += 1 
            if self.time >= self.init_time + self.window:
                self.__mean_speed__()
                self.__loc__()
                self.__emit__()
                if self.time >= self.init_time + self.window + 1:
                    self.__Transition__()
                else:
                    self.hmm[str(self.time - self.window)+":"+str(self.time)] = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0}
                    if self.converg == -1:
#                        emits = [scipy.stats.norm(25,15).pdf(self.ems_dens), 
#                                 scipy.stats.norm(40,15).pdf(self.ems_dens),
#                                 scipy.stats.norm(55,15).pdf(self.ems_dens),
#                                 scipy.stats.norm(70,15).pdf(self.ems_dens),
#                                 scipy.stats.norm(85,15).pdf(self.ems_dens),
#                                 scipy.stats.norm(100,15).pdf(self.ems_dens),
#                                 scipy.stats.norm(115,15).pdf(self.ems_dens),]
                        emits = [scipy.stats.norm(15,15).pdf(self.ems_dens), 
                                 scipy.stats.norm(30,15).pdf(self.ems_dens),
                                 scipy.stats.norm(45,15).pdf(self.ems_dens),
                                 scipy.stats.norm(60,15).pdf(self.ems_dens),
                                 scipy.stats.norm(75,15).pdf(self.ems_dens),
                                 scipy.stats.norm(90,15).pdf(self.ems_dens),
                                 scipy.stats.norm(105,15).pdf(self.ems_dens),]
                        sum_emits = emits[0]+emits[1]+emits[2]+emits[3]+emits[4]+emits[5]+emits[6]
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][0] = emits[0]/sum_emits 
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][1] = emits[1]/sum_emits 
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][2] = emits[2]/sum_emits
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][3] = emits[3]/sum_emits 
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][4] = emits[4]/sum_emits 
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][5] = emits[5]/sum_emits 
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][6] = emits[6]/sum_emits 
                    else:
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][self.converg] = 1
        except KeyError:
            pass
#                    
    def __Transition__(self):
        self.hmm[str(self.time - self.window)+":"+str(self.time)] = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0}
        if self.converg == -1:
#            emits = [scipy.stats.norm(25,15).pdf(self.ems_dens), 
#                     scipy.stats.norm(40,15).pdf(self.ems_dens),
#                     scipy.stats.norm(55,15).pdf(self.ems_dens),
#                     scipy.stats.norm(70,15).pdf(self.ems_dens),
#                     scipy.stats.norm(85,15).pdf(self.ems_dens),
#                     scipy.stats.norm(100,15).pdf(self.ems_dens),
#                     scipy.stats.norm(115,15).pdf(self.ems_dens),]
            emits = [scipy.stats.norm(15,15).pdf(self.ems_dens), 
                     scipy.stats.norm(30,15).pdf(self.ems_dens),
                     scipy.stats.norm(45,15).pdf(self.ems_dens),
                     scipy.stats.norm(60,15).pdf(self.ems_dens),
                     scipy.stats.norm(75,15).pdf(self.ems_dens),
                     scipy.stats.norm(90,15).pdf(self.ems_dens),
                     scipy.stats.norm(105,15).pdf(self.ems_dens),]
            sum_emits = emits[0]+emits[1]+emits[2]+emits[3]+emits[4]+emits[5]+emits[6]
#            transits = [scipy.stats.norm(30,30).pdf(self.trans_dens), scipy.stats.norm(70,30).pdf(self.trans_dens), scipy.stats.norm(110,40).pdf(self.trans_dens)]
            self.hmm[str(self.time - self.window)+":"+str(self.time)][0] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[0]/sum_emits *self.trans_prob(0,0)/(self.trans_prob(0,0)+self.trans_prob(1,0)+self.trans_prob(2,0)+self.trans_prob(3,0)+self.trans_prob(4,0)+self.trans_prob(5,0)+self.trans_prob(6,0)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[0]/sum_emits *self.trans_prob(1,0)/(self.trans_prob(0,0)+self.trans_prob(1,0)+self.trans_prob(2,0)+self.trans_prob(3,0)+self.trans_prob(4,0)+self.trans_prob(5,0)+self.trans_prob(6,0)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[0]/sum_emits *self.trans_prob(2,0)/(self.trans_prob(0,0)+self.trans_prob(1,0)+self.trans_prob(2,0)+self.trans_prob(3,0)+self.trans_prob(4,0)+self.trans_prob(5,0)+self.trans_prob(6,0)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][3] *emits[0]/sum_emits *self.trans_prob(3,0)/(self.trans_prob(0,0)+self.trans_prob(1,0)+self.trans_prob(2,0)+self.trans_prob(3,0)+self.trans_prob(4,0)+self.trans_prob(5,0)+self.trans_prob(6,0)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][4] *emits[0]/sum_emits *self.trans_prob(4,0)/(self.trans_prob(0,0)+self.trans_prob(1,0)+self.trans_prob(2,0)+self.trans_prob(3,0)+self.trans_prob(4,0)+self.trans_prob(5,0)+self.trans_prob(6,0)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][5] *emits[0]/sum_emits *self.trans_prob(5,0)/(self.trans_prob(0,0)+self.trans_prob(1,0)+self.trans_prob(2,0)+self.trans_prob(3,0)+self.trans_prob(4,0)+self.trans_prob(5,0)+self.trans_prob(6,0)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][6] *emits[0]/sum_emits *self.trans_prob(6,0)/(self.trans_prob(0,0)+self.trans_prob(1,0)+self.trans_prob(2,0)+self.trans_prob(3,0)+self.trans_prob(4,0)+self.trans_prob(5,0)+self.trans_prob(6,0)),
                    )
            self.hmm[str(self.time - self.window)+":"+str(self.time)][1] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[1]/sum_emits *self.trans_prob(0,1)/(self.trans_prob(0,1)+self.trans_prob(1,1)+self.trans_prob(2,1)+self.trans_prob(3,1)+self.trans_prob(4,1)+self.trans_prob(5,1)+self.trans_prob(6,1)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[1]/sum_emits *self.trans_prob(1,1)/(self.trans_prob(0,1)+self.trans_prob(1,1)+self.trans_prob(2,1)+self.trans_prob(3,1)+self.trans_prob(4,1)+self.trans_prob(5,1)+self.trans_prob(6,1)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[1]/sum_emits *self.trans_prob(2,1)/(self.trans_prob(0,1)+self.trans_prob(1,1)+self.trans_prob(2,1)+self.trans_prob(3,1)+self.trans_prob(4,1)+self.trans_prob(5,1)+self.trans_prob(6,1)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][3] *emits[1]/sum_emits *self.trans_prob(3,1)/(self.trans_prob(0,1)+self.trans_prob(1,1)+self.trans_prob(2,1)+self.trans_prob(3,1)+self.trans_prob(4,1)+self.trans_prob(5,1)+self.trans_prob(6,1)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][4] *emits[1]/sum_emits *self.trans_prob(4,1)/(self.trans_prob(0,1)+self.trans_prob(1,1)+self.trans_prob(2,1)+self.trans_prob(3,1)+self.trans_prob(4,1)+self.trans_prob(5,1)+self.trans_prob(6,1)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][5] *emits[1]/sum_emits *self.trans_prob(5,1)/(self.trans_prob(0,1)+self.trans_prob(1,1)+self.trans_prob(2,1)+self.trans_prob(3,1)+self.trans_prob(4,1)+self.trans_prob(5,1)+self.trans_prob(6,1)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][6] *emits[1]/sum_emits *self.trans_prob(6,1)/(self.trans_prob(0,1)+self.trans_prob(1,1)+self.trans_prob(2,1)+self.trans_prob(3,1)+self.trans_prob(4,1)+self.trans_prob(5,1)+self.trans_prob(6,1)),
                    )
            self.hmm[str(self.time - self.window)+":"+str(self.time)][2] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[2]/sum_emits *self.trans_prob(0,2)/(self.trans_prob(0,2)+self.trans_prob(1,2)+self.trans_prob(2,2)+self.trans_prob(3,2)+self.trans_prob(4,2)+self.trans_prob(5,2)+self.trans_prob(6,2)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[2]/sum_emits *self.trans_prob(1,2)/(self.trans_prob(0,2)+self.trans_prob(1,2)+self.trans_prob(2,2)+self.trans_prob(3,2)+self.trans_prob(4,2)+self.trans_prob(5,2)+self.trans_prob(6,2)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[2]/sum_emits *self.trans_prob(2,2)/(self.trans_prob(0,2)+self.trans_prob(1,2)+self.trans_prob(2,2)+self.trans_prob(3,2)+self.trans_prob(4,2)+self.trans_prob(5,2)+self.trans_prob(6,2)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][3] *emits[2]/sum_emits *self.trans_prob(3,2)/(self.trans_prob(0,2)+self.trans_prob(1,2)+self.trans_prob(2,2)+self.trans_prob(3,2)+self.trans_prob(4,2)+self.trans_prob(5,2)+self.trans_prob(6,2)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][4] *emits[2]/sum_emits *self.trans_prob(4,2)/(self.trans_prob(0,2)+self.trans_prob(1,2)+self.trans_prob(2,2)+self.trans_prob(3,2)+self.trans_prob(4,2)+self.trans_prob(5,2)+self.trans_prob(6,2)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][5] *emits[2]/sum_emits *self.trans_prob(5,2)/(self.trans_prob(0,2)+self.trans_prob(1,2)+self.trans_prob(2,2)+self.trans_prob(3,2)+self.trans_prob(4,2)+self.trans_prob(5,2)+self.trans_prob(6,2)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][6] *emits[2]/sum_emits *self.trans_prob(6,2)/(self.trans_prob(0,2)+self.trans_prob(1,2)+self.trans_prob(2,2)+self.trans_prob(3,2)+self.trans_prob(4,2)+self.trans_prob(5,2)+self.trans_prob(6,2)),
                    )
            self.hmm[str(self.time - self.window)+":"+str(self.time)][3] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[3]/sum_emits *self.trans_prob(0,3)/(self.trans_prob(0,3)+self.trans_prob(1,3)+self.trans_prob(2,3)+self.trans_prob(3,3)+self.trans_prob(4,3)+self.trans_prob(5,3)+self.trans_prob(6,3)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[3]/sum_emits *self.trans_prob(1,3)/(self.trans_prob(0,3)+self.trans_prob(1,3)+self.trans_prob(2,3)+self.trans_prob(3,3)+self.trans_prob(4,3)+self.trans_prob(5,3)+self.trans_prob(6,3)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[3]/sum_emits *self.trans_prob(2,3)/(self.trans_prob(0,3)+self.trans_prob(1,3)+self.trans_prob(2,3)+self.trans_prob(3,3)+self.trans_prob(4,3)+self.trans_prob(5,3)+self.trans_prob(6,3)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][3] *emits[3]/sum_emits *self.trans_prob(3,3)/(self.trans_prob(0,3)+self.trans_prob(1,3)+self.trans_prob(2,3)+self.trans_prob(3,3)+self.trans_prob(4,3)+self.trans_prob(5,3)+self.trans_prob(6,3)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][4] *emits[3]/sum_emits *self.trans_prob(4,3)/(self.trans_prob(0,3)+self.trans_prob(1,3)+self.trans_prob(2,3)+self.trans_prob(3,3)+self.trans_prob(4,3)+self.trans_prob(5,3)+self.trans_prob(6,3)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][5] *emits[3]/sum_emits *self.trans_prob(5,3)/(self.trans_prob(0,3)+self.trans_prob(1,3)+self.trans_prob(2,3)+self.trans_prob(3,3)+self.trans_prob(4,3)+self.trans_prob(5,3)+self.trans_prob(6,3)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][6] *emits[3]/sum_emits *self.trans_prob(6,3)/(self.trans_prob(0,3)+self.trans_prob(1,3)+self.trans_prob(2,3)+self.trans_prob(3,3)+self.trans_prob(4,3)+self.trans_prob(5,3)+self.trans_prob(6,3)),
                    )
            self.hmm[str(self.time - self.window)+":"+str(self.time)][4] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[4]/sum_emits *self.trans_prob(0,4)/(self.trans_prob(0,4)+self.trans_prob(1,4)+self.trans_prob(2,4)+self.trans_prob(3,4)+self.trans_prob(4,4)+self.trans_prob(5,4)+self.trans_prob(6,4)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[4]/sum_emits *self.trans_prob(1,4)/(self.trans_prob(0,4)+self.trans_prob(1,4)+self.trans_prob(2,4)+self.trans_prob(3,4)+self.trans_prob(4,4)+self.trans_prob(5,4)+self.trans_prob(6,4)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[4]/sum_emits *self.trans_prob(2,4)/(self.trans_prob(0,4)+self.trans_prob(1,4)+self.trans_prob(2,4)+self.trans_prob(3,4)+self.trans_prob(4,4)+self.trans_prob(5,4)+self.trans_prob(6,4)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][3] *emits[4]/sum_emits *self.trans_prob(3,4)/(self.trans_prob(0,4)+self.trans_prob(1,4)+self.trans_prob(2,4)+self.trans_prob(3,4)+self.trans_prob(4,4)+self.trans_prob(5,4)+self.trans_prob(6,4)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][4] *emits[4]/sum_emits *self.trans_prob(4,4)/(self.trans_prob(0,4)+self.trans_prob(1,4)+self.trans_prob(2,4)+self.trans_prob(3,4)+self.trans_prob(4,4)+self.trans_prob(5,4)+self.trans_prob(6,4)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][5] *emits[4]/sum_emits *self.trans_prob(5,4)/(self.trans_prob(0,4)+self.trans_prob(1,4)+self.trans_prob(2,4)+self.trans_prob(3,4)+self.trans_prob(4,4)+self.trans_prob(5,4)+self.trans_prob(6,4)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][6] *emits[4]/sum_emits *self.trans_prob(6,4)/(self.trans_prob(0,4)+self.trans_prob(1,4)+self.trans_prob(2,4)+self.trans_prob(3,4)+self.trans_prob(4,4)+self.trans_prob(5,4)+self.trans_prob(6,4)),
                    )
            self.hmm[str(self.time - self.window)+":"+str(self.time)][5] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[5]/sum_emits *self.trans_prob(0,5)/(self.trans_prob(0,5)+self.trans_prob(1,5)+self.trans_prob(2,5)+self.trans_prob(3,5)+self.trans_prob(4,5)+self.trans_prob(5,5)+self.trans_prob(6,5)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[5]/sum_emits *self.trans_prob(1,5)/(self.trans_prob(0,5)+self.trans_prob(1,5)+self.trans_prob(2,5)+self.trans_prob(3,5)+self.trans_prob(4,5)+self.trans_prob(5,5)+self.trans_prob(6,5)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[5]/sum_emits *self.trans_prob(2,5)/(self.trans_prob(0,5)+self.trans_prob(1,5)+self.trans_prob(2,5)+self.trans_prob(3,5)+self.trans_prob(4,5)+self.trans_prob(5,5)+self.trans_prob(6,5)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][3] *emits[5]/sum_emits *self.trans_prob(3,5)/(self.trans_prob(0,5)+self.trans_prob(1,5)+self.trans_prob(2,5)+self.trans_prob(3,5)+self.trans_prob(4,5)+self.trans_prob(5,5)+self.trans_prob(6,5)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][4] *emits[5]/sum_emits *self.trans_prob(4,5)/(self.trans_prob(0,5)+self.trans_prob(1,5)+self.trans_prob(2,5)+self.trans_prob(3,5)+self.trans_prob(4,5)+self.trans_prob(5,5)+self.trans_prob(6,5)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][5] *emits[5]/sum_emits *self.trans_prob(5,5)/(self.trans_prob(0,5)+self.trans_prob(1,5)+self.trans_prob(2,5)+self.trans_prob(3,5)+self.trans_prob(4,5)+self.trans_prob(5,5)+self.trans_prob(6,5)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][6] *emits[5]/sum_emits *self.trans_prob(6,5)/(self.trans_prob(0,5)+self.trans_prob(1,5)+self.trans_prob(2,5)+self.trans_prob(3,5)+self.trans_prob(4,5)+self.trans_prob(5,5)+self.trans_prob(6,5)),
                    )
            self.hmm[str(self.time - self.window)+":"+str(self.time)][6] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[6]/sum_emits *self.trans_prob(0,6)/(self.trans_prob(0,6)+self.trans_prob(1,6)+self.trans_prob(2,6)+self.trans_prob(3,6)+self.trans_prob(4,6)+self.trans_prob(5,6)+self.trans_prob(6,6)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[6]/sum_emits *self.trans_prob(1,6)/(self.trans_prob(0,6)+self.trans_prob(1,6)+self.trans_prob(2,6)+self.trans_prob(3,6)+self.trans_prob(4,6)+self.trans_prob(5,6)+self.trans_prob(6,6)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[6]/sum_emits *self.trans_prob(2,6)/(self.trans_prob(0,6)+self.trans_prob(1,6)+self.trans_prob(2,6)+self.trans_prob(3,6)+self.trans_prob(4,6)+self.trans_prob(5,6)+self.trans_prob(6,6)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][3] *emits[6]/sum_emits *self.trans_prob(3,6)/(self.trans_prob(0,6)+self.trans_prob(1,6)+self.trans_prob(2,6)+self.trans_prob(3,6)+self.trans_prob(4,6)+self.trans_prob(5,6)+self.trans_prob(6,6)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][4] *emits[6]/sum_emits *self.trans_prob(4,6)/(self.trans_prob(0,6)+self.trans_prob(1,6)+self.trans_prob(2,6)+self.trans_prob(3,6)+self.trans_prob(4,6)+self.trans_prob(5,6)+self.trans_prob(6,6)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][5] *emits[6]/sum_emits *self.trans_prob(5,6)/(self.trans_prob(0,6)+self.trans_prob(1,6)+self.trans_prob(2,6)+self.trans_prob(3,6)+self.trans_prob(4,6)+self.trans_prob(5,6)+self.trans_prob(6,6)),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][6] *emits[6]/sum_emits *self.trans_prob(6,6)/(self.trans_prob(0,6)+self.trans_prob(1,6)+self.trans_prob(2,6)+self.trans_prob(3,6)+self.trans_prob(4,6)+self.trans_prob(5,6)+self.trans_prob(6,6)),
                    )
        else:
            self.hmm[str(self.time - self.window)+":"+str(self.time)][self.converg] = 1
        

        flow_alertt = 0
        pred = -1
        for st in range(0,7):
            if self.flow_alert == 7:
               self.hmm[str(self.time - self.window)+":"+str(self.time)][st] *= 10**9
            if 0 < self.hmm[str(self.time - self.window)+":"+str(self.time)][st] < 10**-10:
                flow_alertt += 1
            if self.hmm[str(self.time - self.window)+":"+str(self.time)][st] == max(
                            self.hmm[str(self.time - self.window)+":"+str(self.time)][0],
                            self.hmm[str(self.time - self.window)+":"+str(self.time)][1],
                            self.hmm[str(self.time - self.window)+":"+str(self.time)][2],
                            self.hmm[str(self.time - self.window)+":"+str(self.time)][3],
                            self.hmm[str(self.time - self.window)+":"+str(self.time)][4],
                            self.hmm[str(self.time - self.window)+":"+str(self.time)][5],
                            self.hmm[str(self.time - self.window)+":"+str(self.time)][6],
                            ):
                pred = st
        self.predictions[str(self.time - self.window)+":"+str(self.time)] = pred
        print (str(self.time - self.window)+":"+str(self.time)+" Prediciton:" + str(pred))
        self.flow_alert = flow_alertt
        
    
    
    def __proceed__(self,frame):
        for t in range(self.init_time, frame + 1):
            self.__lapse__()
    
    def __true_density__(self,frame):
        for t in range(self.init_time, frame + 1):
            if t < self.init_time + 100:
                continue
            else:
#                in_out_time = {}
                total_time = 0
                area_dist = [999999,-1]
                area_time = 1
                for tt in range(t - 100, t + 1):
                    for v in self.convoy[tt]:
                            area_dist[0] = min(area_dist[0], self.convoy[tt][v]["Location"])
                            area_dist[1] = max(area_dist[1], self.convoy[tt][v]["Location"])
                            total_time += len(self.convoy[tt])
                self.true_densitys[str(t-100)+":"+str(t)] = total_time/((area_dist[1] - area_dist[0])*area_time)
                v_measure = self.speeds[str(t-100)+":"+str(t)]
                k_measure = self.true_densitys[str(t-100)+":"+str(t)]
                if v_measure < 15:
                    true_level = 2
                elif 15 <= v_measure < 40:
                    true_level = 1
                elif 40 <= v_measure:
                    true_level = 0
                if k_measure < 30:
                    true_level += 0
                elif 30 <= k_measure < 90:
                    true_level += 1
                elif 90 <= k_measure:
                    true_level += 2
                if true_level < 2:
                    self.true_congestions[str(t-10)+":"+str(t)] = "FLUENT"
                elif true_level == 2:
                    self.true_congestions[str(t-10)+":"+str(t)] = "MODERATE"
                else:
                    self.true_congestions[str(t-10)+":"+str(t)] = "HEAVY"
#                if v_measure < 40 and k_measure >= 50:
                    
#                if self.speeds[str(t-10)+":"+str(t)] >= 48 and self.true_densitys[str(t-10)+":"+str(t)] <=37:
#                    self.true_congestions[str(t-10)+":"+str(t)] = "FLUENT"
#                elif 24 <= self.speeds[str(t-10)+":"+str(t)] <=64 and self.true_densitys[str(t-10)+":"+str(t)] <=37:       
#        scipy.stats.norm(15,30).pdf(15)