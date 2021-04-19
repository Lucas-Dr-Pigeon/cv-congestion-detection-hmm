# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 14:01:39 2020

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
class HMM_VSW:
    def __scan_vehicles__(self):
        pass
    
    def __sparse__(self):
        sparse_convoy = {}
        whitelist = []
        blacklist = []
        for t in range(list(self.convoy.keys())[0], list(self.convoy.keys())[-1]):
            sparse_convoy[t] = {}
            for v in self.convoy[t]: 
                if v not in whitelist and v not in blacklist:
                    if randint(0,100) > self.mpr:
                        blacklist.append(v)
                    else: 
                        whitelist.append(v)
                if v in blacklist:
                    continue
                if v in whitelist:
                    sparse_convoy[t][v] = self.convoy[t][v]
        self.conovy = sparse_convoy
        
    def __random__(self):
        return randint(0,100)
    
    def __emit__(self, Kj = 150.40, Lambd = -35.30):
        u = self.speed
        self.prev_ems_dens = self.ems_dens
        self.ems_dens = Kj * math.exp(u/Lambd)
        self.ems_denss[str(self.time - self.window)+":"+str(self.time)] = min(130,self.ems_dens)
        
    def __transit__(self):
        self.trans_dens = min(130,self.prev_ems_dens*(self.prev_speed*0.1+self.delta_loc)/(self.speed*0.1+self.delta_loc))
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
                self.converg = 2
            elif self.speed >= 70: 
                self.converg = 0
            else: 
                self.converg = -1
                    
    
    def __init__(self,convoy):
        self.convoy = convoy
        self.mpr = 100
        self.init_time = list(convoy.keys())[0]
        self.time = self.init_time
        self.window = 100
        self.__sparse__()
        self.prev = 0
        self.speed = 0
        self.prev_speed = 0
        self.delta_loc = 0
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
                    self.__transit__()
                    self.__Transition__()
                else:
                    self.hmm[str(self.time - self.window)+":"+str(self.time)] = {0:0,1:0,2:0}
                    if self.converg == -1:
                        emits = [scipy.stats.norm(25,25).pdf(self.ems_dens), scipy.stats.norm(60,30).pdf(self.ems_dens),scipy.stats.norm(90,35).pdf(self.ems_dens)]
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][0] = emits[0]/(emits[0]+emits[1] + emits[2])
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][1] = emits[1]/(emits[0]+emits[1] + emits[2])
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][2] = emits[2]/(emits[0]+emits[1] + emits[2])
                    else:
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][self.converg] = 1
        except KeyError:
            pass
#                    
    def __Transition__(self):
        self.hmm[str(self.time - self.window)+":"+str(self.time)] = {0:0,1:0,2:0}
        if self.converg == -1:
            emits = [scipy.stats.norm(25,25).pdf(self.ems_dens), scipy.stats.norm(60,30).pdf(self.ems_dens),scipy.stats.norm(90,35).pdf(self.ems_dens)]
            transits = [scipy.stats.norm(30,30).pdf(self.trans_dens), scipy.stats.norm(70,30).pdf(self.trans_dens), scipy.stats.norm(110,40).pdf(self.trans_dens)]
            self.hmm[str(self.time - self.window)+":"+str(self.time)][0] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[0]/(emits[0]+emits[1]+emits[2]) *transits[0]/(transits[0]+transits[1]),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[0]/(emits[0]+emits[1]+emits[2]) *transits[0]/(transits[0]+transits[1]) 
                    )
            self.hmm[str(self.time - self.window)+":"+str(self.time)][1] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][0] *emits[1]/(emits[0]+emits[1]+emits[2]) *transits[1]/(transits[0]+transits[1] + transits[2]),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[1]/(emits[0]+emits[1]+emits[2]) *transits[1]/(transits[0]+transits[1] + transits[2]),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[1]/(emits[0]+emits[1]+emits[2]) *transits[1]/(transits[0]+transits[1] + transits[2])
                    )
            self.hmm[str(self.time - self.window)+":"+str(self.time)][2] = max(
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][1] *emits[2]/(emits[0]+emits[1]+emits[2]) *transits[2]/(transits[1]+transits[2]),
                    self.hmm[str(self.prev - self.window)+":"+str(self.prev)][2] *emits[2]/(emits[0]+emits[1]+emits[2]) *transits[2]/(transits[1]+transits[2])
                    )
        else:
            self.hmm[str(self.time - self.window)+":"+str(self.time)][self.converg] = 1
        
        if (self.time - self.init_time)%100 == 0 and (self.time - self.init_time)/100 >= 1:
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][0] *= 10**100
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][1] *= 10**100
                        self.hmm[str(self.time - self.window)+":"+str(self.time)][2] *= 10**100
        
        if self.hmm[str(self.time - self.window)+":"+str(self.time)][0] == max(self.hmm[str(self.time - self.window)+":"+str(self.time)][0],self.hmm[str(self.time - self.window)+":"+str(self.time)][1],self.hmm[str(self.time - self.window)+":"+str(self.time)][2]):
            print ("FLUENT")
            self.predictions[str(self.time - self.window)+":"+str(self.time)] = "FLUENT"
        elif self.hmm[str(self.time - self.window)+":"+str(self.time)][1] == max(self.hmm[str(self.time - self.window)+":"+str(self.time)][0],self.hmm[str(self.time - self.window)+":"+str(self.time)][1],self.hmm[str(self.time - self.window)+":"+str(self.time)][2]):
            print ("MEDIUM")
            self.predictions[str(self.time - self.window)+":"+str(self.time)] = "MEDIUM"
        else:
            print ("HEAVY")
            self.predictions[str(self.time - self.window)+":"+str(self.time)] = "HEAVY"
    
    
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