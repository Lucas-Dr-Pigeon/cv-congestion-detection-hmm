# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
#import networkx as nx
#import math
#import sys
import matplotlib.pyplot as plt
#import collections
import preprocessing as prep
import congestion_monitoring_system as cms
import time
import HMM
import HMM2
import HMM_VSW 
from hmm7 import hmm7
from copy import deepcopy
import pandas as pd

if __name__ == "__main__":
    path = r"vehicle-trajectory-data\0805am-0820am\trajectories-0805am-0820am.csv"
    us101_data = pd.read_csv(path)
    us101_data_vehicles = list(set(list(us101_data["Vehicle_ID"])))
    us101 = prep.dataset(data = us101_data, vehicles = [])
    us101_vehicles = us101.data_by_vehicle()
    #us101_lanes = us101.data_by_lane()
    us101.read_vehicle(5)
    
    Convoy464 = us101.get_preceding_convoy(464,200,[2150,2200],by_lane=True)
    
    System464 = cms.CM_System(convoy=Convoy464,thres_v = 10)
    System464.__Proceed__(2200)
    
    for W in System464.waves:
        print(System464.waves[W].loc)
    
    Convoy484 = us101.get_preceding_convoy(484,300,[2150,3000],by_lane=True)
    HMM484 = HMM_VSW(convoy = Convoy484)
    HMM484.__proceed__(3000)
    HMM484_dict = HMM484.hmm
    HMM484_ems_denss = HMM484.ems_denss
    HMM484_trans_denss = HMM484.trans_denss
    HMM484_predictions = HMM484.predictions
    HMM484_speeds = HMM484.speeds
    HMM484.__true_density__(3000)
    HMM484_trueK = HMM484.true_densitys
    plt.plot(list(HMM484.speeds.values()),list(HMM484.true_densitys.values()),'.')
    plt.plot(list(HMM484.speeds.keys()),list(HMM484.speeds.values()))
    plt.show()
    
    us101_vehicles[1][270]
    
    
    Convoy484f = us101.get_preceding_convoy(484,300,[2150,3000],by_lane=False)
    
    
    hmm7_484 = hmm7(convoy = Convoy484, mpr = 100)
    hmm7_484.__proceed__(3000)
    hmm7_484_hmm = hmm7_484.hmm
    hmm7_484_predictions = hmm7_484.predictions
    
    hmm7_30_484 = hmm7(convoy = Convoy484, mpr = 30)
    hmm7_30_484.convoy == hmm7_484.convoy
    hmm7_30_484.__proceed__(3000)
    hmm7_30_484_predictions = hmm7_30_484.predictions
    
    hmm7_50_484 = hmm7(convoy = Convoy484, mpr = 50)
    hmm7_50_484.convoy == hmm7_484.convoy
    hmm7_50_484.__proceed__(3000)
    hmm7_50_484_predictions = hmm7_50_484.predictions
    
    hmm7_70_484 = hmm7(convoy = Convoy484, mpr = 70)
    hmm7_70_484.convoy == hmm7_484.convoy
    hmm7_70_484.__proceed__(3000)
    hmm7_70_484_predictions = hmm7_70_484.predictions
    
    System_30_484 = cms.CM_System(convoy = hmm7_30_484.convoy, thres_v = 5/3.6)
    System_30_484.__Time_Spac__()
    
    #Plot the results:
    System484 = cms.CM_System(convoy = Convoy484, thres_v = 5/3.6, lead= 484)
    System484.__Time_Spac__()
    trj484 = System484.trajectory
    #num = len(System484.trajectory)
    dataT = np.arange(2176,2925)
    #dataX = []
    dataC = np.zeros(2925-2176)
    dataS = np.zeros(2925-2176)
    #dataC_30 = np.zeros(2925-2176)
    #dataC_50 = np.zeros(2925-2176)
    #dataC_70 = np.zeros(2925-2176)
    for T in dataT:
    #    dataX[T-2251] = hmm7_484.speeds[list(hmm7_484.speeds.keys())[T-2251]]
        dataC[T-2176] = hmm7_484.predictions[list(hmm7_484.predictions.keys())[T-2176]]
    #    dataS[T-2176] = hmm7_484.speeds[list(hmm7_484.predictions.keys())[T-2176]]
    #    dataC_30[T-2176] = hmm7_30_484.predictions[list(hmm7_30_484.predictions.keys())[T-2176]]
    #    dataC_50[T-2176] = hmm7_50_484.predictions[list(hmm7_50_484.predictions.keys())[T-2176]]
    #    dataC_70[T-2176] = hmm7_70_484.predictions[list(hmm7_70_484.predictions.keys())[T-2176]]
    fig,ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel("time(0.1s)")
    ax1.set_ylabel("distance(m)")
    
    #ax1.plot(dataT, dataS, color = "blue", label = "Speed")
    for V in trj484:
        ax1.plot(trj484[V]["times"],trj484[V]["locations"])
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    
    color = 'tab:blue'
    ax2.set_ylabel('congestion level', color= color)
    #line30 = ax2.plot(dataT, dataC_30, color = "black", label="30% MPR")
    #line50 = ax2.plot(dataT, dataC_50, color = "green", label="50% MPR")
    #line70 = ax2.plot(dataT, dataC_70, color = "blue", label="70% MPR")
    line100 = ax2.plot(dataT, dataC, color = "red", label="Congestion Level 100%MPR")
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc="lower right")
    ax2.set_ylim([0,7])
    fig.tight_layout()
    #plt.savefig('images/100-70-50-30_2.png',dpi = 1200)
    plt.show()
    
    
    
    Convoy369= us101.get_preceding_convoy(369,300,[1800,2550],by_lane=True)
    hmm7_369 = hmm7(convoy = Convoy369, mpr = 100)
    hmm7_369.__proceed__(2550)
    hmm7_369_hmm = hmm7_369.hmm
    hmm7_369_predictions = hmm7_369.predictions
    
    hmm7_30_369 = hmm7(convoy = Convoy369, mpr = 30)
    hmm7_30_369.convoy == hmm7_369.convoy
    hmm7_30_369.__proceed__(2550)
    hmm7_30_369_predictions = hmm7_30_369.predictions
    
    hmm7_50_369 = hmm7(convoy = Convoy369, mpr = 50)
    hmm7_50_369.convoy == hmm7_369.convoy
    hmm7_50_369.__proceed__(2550)
    hmm7_50_369_predictions = hmm7_50_369.predictions
    
    hmm7_70_369 = hmm7(convoy = Convoy369, mpr = 70)
    hmm7_70_369.convoy == hmm7_369.convoy
    hmm7_70_369.__proceed__(2550)
    hmm7_70_369_predictions = hmm7_70_369.predictions
    
    
    #Plot the results:
    System369= cms.CM_System(convoy = Convoy369, thres_v = 5/3.6)
    System369.__Time_Spac__()
    trj369 = System369.trajectory
    dataT = np.arange(1825,2474)
    dataC = np.zeros(2474-1825)
    dataC_30 = np.zeros(2474-1825)
    dataC_50 = np.zeros(2474-1825)
    dataC_70 = np.zeros(2474-1825)
    for T in dataT:
        dataC[T-1825] = hmm7_369.predictions[list(hmm7_369.predictions.keys())[T-1825]]
        dataC_30[T-1825]  = hmm7_30_369.predictions[list(hmm7_30_369.predictions.keys())[T-1825]]
        dataC_50[T-1825]  = hmm7_50_369.predictions[list(hmm7_50_369.predictions.keys())[T-1825]]
        dataC_70[T-1825]  = hmm7_70_369.predictions[list(hmm7_70_369.predictions.keys())[T-1825]]
    fig,ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel("time(0.1s)")
    ax1.set_ylabel("distance(m)")
    for V in trj369:
        ax1.plot(trj369[V]["times"],trj369[V]["locations"])
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    
    color = 'tab:blue'
    ax2.set_ylabel('congestion level', color= color)
    line30 = ax2.plot(dataT, dataC_30, color = "black", label="30% MPR")
    line50 = ax2.plot(dataT, dataC_50, color = "green", label="50% MPR")
    line70 = ax2.plot(dataT, dataC_70, color = "blue", label="70% MPR")
    line100 = ax2.plot(dataT, dataC, color = "red", label="100% MPR")
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc="lower right")
    ax2.set_ylim([0,7])
    fig.tight_layout()
    #plt.savefig('images/100-70-50-30_2.png',dpi = 1200)
    plt.show()
    
    
    
    
    
    
    
    
    #hmm7_484.speeds[list(hmm7_484.speeds.keys())[2799-2250]]
    #hmm7_484.predictions[list(hmm7_484.predictions.keys())[2749-2201]]
    #hmm7_484.speeds.keys() == hmm7_484.predictions.keys()
    
    Convoy484_1 = us101.get_preceding_convoy(484,300,[2800,3000],by_lane=True)
    System484_1 = cms.CM_System(convoy = Convoy484_1, thres_v = 5/3.6)
    System484_1.__Proceed__(3000)
    System484_1.__Time_Spac__()
    hmm7_484_1 = hmm7(convoy = Convoy484_1)
    hmm7_484_1.__proceed__(3000)
    hmm7_484_1_hmm = hmm7_484_1.hmm
    hmm7_484_1_predictions = hmm7_484_1.predictions
    
    Convoy67 = us101.get_preceding_convoy(67,300,[600,1090],by_lane=False,convoy_size=30)
    #Convoy67 = us101.get_preceding_convoy(484,300,[2800,3000],by_lane=True)
    hmm7_67 = hmm7(convoy = Convoy67,mpr=100)
    hmm7_67.__proceed__(1090)
    hmm7_67_hmm = hmm7_67.hmm
    hmm7_67_predictions = hmm7_67.predictions
    show_predictions(Convoy67,300,[600,1090],15,67,hmm7_67,hmm7_67,hmm7_67,hmm7_67)
    
    
    
    
    
    
    HMM67 = HMM_VSW(convoy = Convoy67)
    HMM67.__proceed__(1090)
    HMM67_dict = HMM67.hmm
    HMM67_ems_denss = HMM67.ems_denss
    HMM67_trans_denss = HMM67.trans_denss
    HMM67_predictions = HMM67.predictions
    HMM67_speeds = HMM67.speeds
    HMM67.__true_density__(1090)
    HMM67_trueK = HMM67.true_densitys
    Convoy67L = us101.get_preceding_convoy(67,300,[600,1090],by_lane=True,convoy_size=30)
    HMM67L = HMM_VSW(convoy = Convoy67L)
    HMM67L.__proceed__(1090)
    HMM67L.__true_density__(1090)
    HMM67_trueK = HMM67L.true_densitys
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    System484 = cms.CM_System(convoy = Convoy484, thres_v = 10/3.6)
    System484.__Proceed__(2800)
    System484.ffs
    System484.__Time_Spac__()
    System484. __Plot_Speeds__()
    System484.__Stat_Wavelet__()
    System484.state
    System484.trajectory
    Record484 = System484.waves_record
    State484 = System484.state_record
    System484.__Plot_Speed_Acc__(veh=531)
    System484.__Plot_Speed_Acc__(veh=539)
    
    System484.waves[2].black
    
    System484.waves[4].black
    
    
    
    #Convoy 1761 Length 750
    iConvoy1761 = Convoy484F = us101.get_preceding_convoy(1761,300,[6700,7450],by_lane=True,convoy_size=15)
    hmm7_1761 = hmm7(convoy = iConvoy1761, mpr = 100)
    hmm7_1761.__proceed__(7450)
    hmm7_1761_hmm = hmm7_1761 .hmm
    hmm7_1761_predictions = hmm7_1761 .predictions
    
    hmm7_30_1761 = hmm7(convoy = iConvoy1761, mpr = 30)
    hmm7_30_1761.__proceed__(7450)
    hmm7_30_1761_hmm = hmm7_30_1761.hmm
    hmm7_30_1761_predictions = hmm7_30_1761.predictions
    
    hmm7_50_1761 = hmm7(convoy = iConvoy1761, mpr = 50)
    hmm7_50_1761.__proceed__(7450)
    hmm7_50_1761_hmm = hmm7_50_1761.hmm
    hmm7_50_1761_predictions = hmm7_50_1761.predictions
    
    hmm7_70_1761 = hmm7(convoy = iConvoy1761, mpr = 70)
    hmm7_70_1761.__proceed__(7450)
    hmm7_70_1761_hmm = hmm7_70_1761.hmm
    hmm7_70_1761_predictions = hmm7_70_1761.predictions
    
    
    #Plot the results:
    System1761= cms.CM_System(convoy = iConvoy1761, thres_v = 5/3.6)
    System1761.__Time_Spac__()
    trj1761 = System1761.trajectory
    dataT = np.arange(6725,7374)
    dataC = np.zeros(7374-6725)
    dataC_30 = np.zeros(7374-6725)
    dataC_50 = np.zeros(7374-6725)
    dataC_70 = np.zeros(7374-6725)
    for T in dataT:
        dataC[T-6725] = hmm7_1761.predictions[list(hmm7_1761.predictions.keys())[T-6725]]
        dataC_30[T-6725]  = hmm7_30_1761.predictions[list(hmm7_30_1761.predictions.keys())[T-6725]]
        dataC_50[T-6725]  = hmm7_50_1761.predictions[list(hmm7_50_1761.predictions.keys())[T-6725]]
        dataC_70[T-6725]  = hmm7_70_1761.predictions[list(hmm7_70_1761.predictions.keys())[T-6725]]
    fig,ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel("time(0.1s)")
    ax1.set_ylabel("distance(m)")
    for V in trj1761:
        ax1.plot(trj1761[V]["times"],trj1761[V]["locations"])
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    
    color = 'tab:blue'
    ax2.set_ylabel('congestion level', color= color)
    line30 = ax2.plot(dataT, dataC_30, color = "black", label="30% MPR")
    line50 = ax2.plot(dataT, dataC_50, color = "green", label="50% MPR")
    line70 = ax2.plot(dataT, dataC_70, color = "blue", label="70% MPR")
    line100 = ax2.plot(dataT, dataC, color = "red", label="100% MPR")
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc="lower right")
    ax2.set_ylim([0,7])
    fig.tight_layout()
    plt.savefig('images/100-70-50-30_1761.png',dpi = 1200)
    plt.show()
    
    
    
    Convoy1554 = us101.get_preceding_convoy(1554,300,[6000,6750],by_lane=True,convoy_size=15)
    hmm7_1554 = hmm7(convoy = Convoy1554, mpr = 100)
    hmm7_1554.__proceed__(6750)
    hmm7_1554_hmm = hmm7_1554.hmm
    hmm7_1554_predictions = hmm7_1554.predictions
    
    
    
    #Plot the results:
    System1554= cms.CM_System(convoy = Convoy1554, thres_v = 5/3.6)
    System1554.__Time_Spac__()
    trj1554 = System1554.trajectory
    dataT = np.arange(6025,6674)
    dataC = np.zeros(6674-6025)
    dataC_30 = np.zeros(6674-6025)
    dataC_50 = np.zeros(6674-6025)
    dataC_70 = np.zeros(6674-6025)
    for T in dataT:
        dataC[T-6025] = hmm7_1554.predictions[list(hmm7_1554.predictions.keys())[T-6025]]
    #    dataC_30[T-6025]  = hmm7_30_1554.predictions[list(hmm7_30_1554.predictions.keys())[T-6025]]
    #    dataC_50[T-6025]  = hmm7_50_1554.predictions[list(hmm7_50_1554.predictions.keys())[T-6025]]
    #    dataC_70[T-6025]  = hmm7_70_1554.predictions[list(hmm7_70_15541.predictions.keys())[T-6025]]
    fig,ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel("time(0.1s)")
    ax1.set_ylabel("distance(m)")
    for V in trj1554:
        ax1.plot(trj1554[V]["times"],trj1554[V]["locations"])
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()
    
    color = 'tab:blue'
    ax2.set_ylabel('congestion level', color= color)
    #line30 = ax2.plot(dataT, dataC_30, color = "black", label="30% MPR")
    #line50 = ax2.plot(dataT, dataC_50, color = "green", label="50% MPR")
    #line70 = ax2.plot(dataT, dataC_70, color = "blue", label="70% MPR")
    line100 = ax2.plot(dataT, dataC, color = "red", label="100% MPR")
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc="lower right")
    ax2.set_ylim([0,7])
    fig.tight_layout()
    plt.savefig('images/100-70-50-30_1761.png',dpi = 1200)
    plt.show()
    
    
    
    Convoy899 = us101.get_preceding_convoy(899,300,[3850,4542],by_lane=True,convoy_size=15)
    
    hmm7_899 = hmm7(convoy = Convoy899, mpr = 100)
    hmm7_899.__proceed__(4542)
    hmm7_899_hmm = hmm7_899.hmm
    hmm7_899_predictions = hmm7_899.predictions
    
    show_predictions(Convoy899,300,[3850,4542],15,899,hmm7_899,hmm7_899,hmm7_899,hmm7_899)
    
    
    
    Convoy490 = us101.get_preceding_convoy(490,300,[2150,3000],by_lane=True,convoy_size = 15)
    
    hmm7_490 = hmm7(convoy = Convoy490, mpr = 100)
    hmm7_490.__proceed__(3000)
    hmm7_490_hmm = hmm7_490.hmm
    hmm7_490_predictions = hmm7_490.predictions
    
    
    hmm7_30_490 = hmm7(convoy = Convoy490, mpr = 30)
    hmm7_30_490 .__proceed__(3000)
    hmm7_30_490_hmm = hmm7_30_490.hmm
    hmm7_30_490_predictions = hmm7_30_490.predictions
    
    i350 = us101.read_vehicle(350)
    Convoy350 = us101.get_preceding_convoy(350,300,[1780,2500],by_lane=True,convoy_size=15)
    
    i650 = us101.read_vehicle(650)
    Convoy650 = us101.get_preceding_convoy(650,300,[2713,3772],by_lane=True,convoy_size = 15)
    #Convoy650 = us101.get_preceding_convoy(650,300,[2713,3772],by_lane=True,convoy_size = 15)
    hmm7_650 = hmm7(convoy = Convoy650, mpr = 100)
    hmm7_650.__proceed__(3772)
    hmm7_650_hmm = hmm7_650.hmm
    hmm7_650_predictions = hmm7_650.predictions
    
    show_predictions(Convoy650,300,[2713,3772],15,650,hmm7_650,hmm7_650,hmm7_650,hmm7_650)
    
    i620 = us101.read_vehicle(620)
    Convoy620 = us101.get_preceding_convoy(620,300,[2600,3600],by_lane=True,convoy_size = 15)
    hmm7_620 = hmm7(convoy = Convoy620, mpr = 100)
    hmm7_620.__proceed__(3600)
    hmm7_620_hmm = hmm7_620.hmm
    hmm7_620_predictions = hmm7_620.predictions
    show_predictions(Convoy620,300,[2600,3600],15,620,hmm7_620,hmm7_620,hmm7_620,hmm7_620)
    
    
    i670 = us101.read_vehicle(670)
    Convoy670 = us101.get_preceding_convoy(670,300,[2785,3855],by_lane=True,convoy_size = 15)
    hmm7_670 = hmm7(convoy = Convoy670, mpr = 100)
    hmm7_670.__proceed__(3855)
    hmm7_670_hmm = hmm7_670.hmm
    hmm7_670_predictions = hmm7_670.predictions
    show_predictions(Convoy670,300,[2785,3855],15,670,hmm7_670,hmm7_670,hmm7_670,hmm7_670)
    
    i700 = us101.read_vehicle(700)
    Convoy700 = us101.get_preceding_convoy(700,300,[3000,3900],by_lane=True,convoy_size = 15)
    hmm7_700 = hmm7(convoy = Convoy700, mpr = 100)
    hmm7_700.__proceed__(3900)
    hmm7_700_hmm = hmm7_700.hmm
    hmm7_700_predictions = hmm7_700.predictions
    
    hmm7_30_700 = hmm7(convoy = Convoy700, mpr = 30)
    hmm7_30_700.__proceed__(3900)
    hmm7_30_700_hmm = hmm7_30_700.hmm
    hmm7_30_700_predictions = hmm7_30_700.predictions
    
    hmm7_50_700 = hmm7(convoy = Convoy700, mpr = 50)
    hmm7_50_700.__proceed__(3900)
    hmm7_50_700_hmm = hmm7_50_700.hmm
    hmm7_50_700_predictions = hmm7_50_700.predictions
    
    hmm7_70_700 = hmm7(convoy = Convoy700, mpr = 70)
    hmm7_70_700.__proceed__(3900)
    hmm7_70_700_hmm = hmm7_70_700.hmm
    hmm7_70_700_predictions = hmm7_70_700.predictions
    
    show_predictions(Convoy700,300,[3000,3900],15,700,hmm7_700,hmm7_30_700,hmm7_50_700,hmm7_70_700)
    
    hmm7_350 = hmm7(convoy = Convoy350, mpr = 100)
    hmm7_350.__proceed__(2500)
    hmm7_350_hmm = hmm7_350.hmm
    hmm7_350_predictions = hmm7_350.predictions
    
    hmm7_30_350 = hmm7(convoy = Convoy350, mpr = 30)
    hmm7_30_350.__proceed__(2500)
    hmm7_30_350_hmm = hmm7_30_350.hmm
    hmm7_30_350_predictions = hmm7_30_350.predictions
    
    hmm7_50_350 = hmm7(convoy = Convoy350, mpr = 50)
    hmm7_50_350.__proceed__(2500)
    hmm7_50_350_hmm = hmm7_50_350.hmm
    hmm7_50_350_predictions = hmm7_50_350.predictions
    
    hmm7_70_350 = hmm7(convoy = Convoy350, mpr = 70)
    hmm7_70_350.__proceed__(2500)
    hmm7_70_350_hmm = hmm7_70_350.hmm
    hmm7_70_350_predictions = hmm7_70_350.predictions
    
    show_predictions(Convoy350,300,[1780,2500],15,350,hmm7_350,hmm7_30_350,hmm7_50_350,hmm7_70_350)
    #show_predictions(Convoy350,300,[1780,2500],15,350,hmm7_350,hmm7_350,hmm7_350,hmm7_350)
    
    Convoy346 = us101.get_preceding_convoy(346,300,[1750,2490],by_lane=True,convoy_size = 15)
    
    hmm7_346 = hmm7(convoy = Convoy346, mpr = 100)
    hmm7_346.__proceed__(2490)
    hmm7_346_hmm = hmm7_346.hmm
    hmm7_346_predictions = hmm7_346.predictions
    show_predictions(Convoy346,300,[1750,2490],15,346,hmm7_346,hmm7_346,hmm7_346,hmm7_346)
    
    def show_predictions(convoy,dist,zone,convoy_size,lead,hmm7C,hmm7C30,hmm7C50,hmm7C70):
    #    hmm7C = hmm7(convoy, mpr = 100)
    #    hmm7C.__proceed__(6750)
    #    hmm7C_hmm = hmmC.hmm
    #    hmm7C_predictions = hmm7C.predictions
    #    
    #    hmm7C30 = hmm7(convoy, mpr = 30)
    #    
    #    hmm7C.__proceed__(6750)
    #    hmm7C_hmm = hmmC.hmm
    #    hmm7C_predictions = hmm7C.predictions
    
        iSystem = cms.CM_System(convoy,5/3.6,lead)
        iSystem.__Time_Spac__()
        trj = iSystem.trajectory
        dataT = np.arange(zone[0]+25,zone[1]-76)
        dataC = np.zeros(zone[1]-76-zone[0]-25)
        dataC30 = np.zeros(zone[1]-76-zone[0]-25)
        dataC50 = np.zeros(zone[1]-76-zone[0]-25)
        dataC70 = np.zeros(zone[1]-76-zone[0]-25)
        for T in dataT:
            dataC[T-zone[0]-25] = hmm7C.predictions[list(hmm7C.predictions.keys())[T-zone[0]-25]]
            dataC30[T-zone[0]-25]  = hmm7C30.predictions[list(hmm7C30.predictions.keys())[T-zone[0]-25]]
            dataC50[T-zone[0]-25]  = hmm7C50.predictions[list(hmm7C50.predictions.keys())[T-zone[0]-25]]
            dataC70[T-zone[0]-25]  = hmm7C70.predictions[list(hmm7C70.predictions.keys())[T-zone[0]-25]]
        fig,ax1 = plt.subplots()
        plt.style.use('default')
        color = 'tab:red'
        ax1.set_xlabel("time(0.1s)")
        ax1.set_ylabel("distance(m)")
        for V in trj:
            ax1.plot(trj[V]["times"],trj[V]["locations"])
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()
        
        color = 'tab:blue'
        ax2.set_ylabel('congestion level', color= color)
        line30 = ax2.plot(dataT, dataC30, color = "black", label="30% MPR")
        line50 = ax2.plot(dataT, dataC50, color = "green", label="50% MPR")
        line70 = ax2.plot(dataT, dataC70, color = "blue", label="70% MPR")
        line100 = ax2.plot(dataT, dataC, color = "red", label="100% MPR")
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.legend(loc="lower right")
        ax2.set_ylim([0,7])
        fig.tight_layout()
        plt.savefig('images/100-70-50-30_'+str()+'.png',dpi = 1200)
        plt.show()
        
    
        







Convoy484F = us101.get_preceding_convoy(484,300,[2150,2800],by_lane=False,convoy_size=30)
System484F = cms.CM_System(convoy = Convoy484F, thres_v = 10/3.6)
HMM484F = HMM(convoy = Convoy484F)
HMM484F.__proceed__(2800)
HMM484F_dict = HMM484F.hmm

HMM484F_ems_denss = HMM484F.ems_denss
HMM484F_trans_denss = HMM484F.trans_denss
HMM484F_predictions = HMM484F.predictions
HMM484F.__true_density__(2800)
HMM484F_trueK = HMM484F.true_density

HMM484 = HMM(convoy = Convoy484)
HMM484.__proceed__(2800)


HMM484F2 = HMM2(convoy = Convoy484F)
HMM484F2.__proceed__(2800)
HMM484F2_dict = HMM484F2.hmm
HMM484F2_ems_denss = HMM484F2.ems_denss
HMM484F2_trans_denss = HMM484F2.trans_denss
HMM4842F_predictions = HMM484F2.predictions


HMM484V2 = HMM_VSW(convoy = Convoy484F)
HMM484V2.__proceed__(2800)
HMM484V2_dict = HMM484V2.hmm
HMM484V2_ems_denss = HMM484V2.ems_denss
HMM484V2_trans_denss = HMM484V2.trans_denss
HMM484V2_predictions = HMM484V2.predictions
HMM484V2_speeds = HMM484V2.speeds
HMM484V2.__true_density__(2800)
HMM484V2_trueK = HMM484V2.true_densitys
plt.plot(list(HMM484V2.speeds.values()),list(HMM484V2.true_densitys.values()),'.', color='blue')
plt.show()


Convoy116 = us101.get_preceding_convoy(116,300,[1000,1200],by_lane=True)  
HMM116 = HMM_VSW(convoy = Convoy116)
HMM116.__proceed__(1200)
HMM116_dict = HMM116.hmm
HMM116_ems_denss = HMM116.ems_denss
HMM116_trans_denss = HMM116.trans_denss
HMM116_predictions = HMM116.predictions
HMM116_speeds = HMM116.speeds
HMM116.__true_density__(1200)
HMM116_trueK = HMM116.true_densitys
HMM116_congestions = HMM116.true_congestions
plt.plot(list(HMM116.speeds.keys()),list(HMM116.speeds.values()))
plt.plot(list(HMM116.speeds.values()),list(HMM116.true_densitys.values()))
plt.show()




Convoy019 = us101.get_preceding_convoy(19,300,[316,700],by_lane=True)  
HMM019V2 = HMM_VSW(convoy = Convoy019)
HMM019V2.__proceed__(700)
HMM019V2_ems_denss = HMM019V2.ems_denss
HMM019V2_trans_denss = HMM019V2.trans_denss
HMM019V2_predictions = HMM019V2.predictions
HMM019V2_speeds = HMM019V2.speeds
HMM019V2.__true_density__(700)
HMM019V2_trueK = HMM019V2.true_densitys

HMM019 = HMM(convoy = Convoy019)
HMM019.__proceed__(700)
HMM019_dict = HMM019.hmm
HMM019_ems_denss = HMM019.ems_denss
HMM019_trans_denss = HMM019.trans_denss
HMM019_predictions = HMM019.predictions

System019 = cms.CM_System(convoy = Convoy019, thres_v = 10/3.6)
System019.__Proceed__(700)
System019.__Time_Spac__()
def acc_speed_plot(Time):
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-15,15)
    xscale = []
    vscale = []
    ascale = []
    Dict = {}
    for v in System484F.convoy[Time]:
        xscale.append(System484F.convoy[Time][v]["Location"])
        Dict[System484F.convoy[Time][v]["Location"]] = {"Speed":System484F.convoy[Time][v]["Speed"],"Acc":System484F.convoy[Time][v]["Acc"]}
    for ss in sorted(xscale):
        vscale.append(Dict[ss]["Speed"])
        ascale.append(Dict[ss]["Acc"])
    ax.plot(sorted(xscale),vscale)
    ax.plot(sorted(xscale),ascale)
    plt.show()
        
    


System484.__Plot_Speed_Acc__(veh=539)



for t in System484F.convoy:
    acc_speed_plot(t)

plt.style.use("ggplot")
#data_plot = pd.DataFrame(HMM484.speeds.values(),HMM484.true_densitys.values())
plt.scatter(HMM484.speeds.values(),HMM484.true_densitys.values(),c="black",s=7)







#for t in System484F.convoy:
#    plt.ion()
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    ax.set_ylim(-0,15)
#    xscale = []
#    vscale = []
#    ascale = []
#    for v in System484F.convoy[t]:
#        xscale.append(System484F.convoy[t][v]["Location"])
#        vscale.append(System484F.convoy[t][v]["Speed"])
#        ascale.append(System484F.convoy[t][v]["Acc"])
#    line1, = ax.plot(xscale,vscale)
#    line1.set_xdata(xscale)
#    line1.set_ydata(vscale)
#    
#    line2, = ax.plot(xscale,ascale)
#    line2.set_xdata(xscale)
#    fig.canvas.draw()
#    line1.set_ydata(ascale)
#    plt.pause(1e-17)
#    time.sleep(0.01)




#for t in System484.convoy:
#    plt.ion()
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    ax.set_ylim(-0,15)
#    xscale = []
#    vscale = []
#    ascale = []
#    for v in System484.convoy[t]:
#        xscale.append(System484.convoy[t][v]["Location"])
#        vscale.append(System484.convoy[t][v]["Speed"])
#        ascale.append(System484.convoy[t][v]["Acc"])
#    line1, = ax.plot(xscale,vscale)
#    line1.set_xdata(xscale)
#    line1.set_ydata(vscale)
#    
#    line2, = ax.plot(xscale,ascale)
#    line2.set_xdata(xscale)
#    fig.canvas.draw()
#    line1.set_ydata(ascale)
#    plt.pause(1e-17)
#    time.sleep(0.01)
#plt.show()


iSystem.state

for i in range(50):
    iSystem.__Lapse__()
    iSystem.waves
    iSystem.unsorted_congest
    

iSystem.state
for W in iSystem.waves:
    print(iSystem.waves[W].black)
iSystem.waves[9].red
#
#for v in us101_vehicles:
#    vv = pd.DataFrame(us101_vehicles[v])
#    vv.to_csv("vehicles\\"+str(v)+".csv")
#    