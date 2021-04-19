# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import math
class HMM_time_space:
    
    def __emit__(self):
        
        for zone in self.Zones:
            mean_speed = self.data[zone][self.t][1]
            self.HMM[zone][self.t][:, 2] = self.__cal_emit__(mean_speed)
            self.HMM[zone][self.t][:, 1] = np.arange(7)
        self.__time_lapse__()
        self.__prev_max_prob__()     
    
    def __time_lapse__(self):
        self.prev_t = self.t
        self.frame += 1
        self.t = self.Windows[self.frame]
        
    def __prev_max_prob__(self): 
        for zone in self.Zones:
            if self.HMM[zone][self.t][:, 0] == 0:
                self.HMM[zone][self.t][:, 0] = np.argmax(self.HMM[zone][self.prev_t][:,2]) 
            else:
                self.HMM[zone][self.t][:, 0] *= np.argmax(self.HMM[zone][self.prev_t][:,2]) 
            
    def __init__(self, data, num_of_class = 7):
        self.data = data
        self.class_num = num_of_class
        # There's room to improve
        self.Char_Dens_list = [15,30,45,60,75,90,105]
        
        def __find_union_windows__(data_dict):
            Zones = list(data_dict.keys())
            union = set(data_dict[Zones[0]].keys())

            for zone in Zones:
                union = set.intersection(union, set(data_dict[zone].keys()) )

            return list(sorted(union))
        self.Zones = list(data.keys())
        self.Windows = __find_union_windows__(self.data)
        self.dx = 60.96
        self.dt = 1
        
        
        def __init_HMM__(data_dict):
            Zones = list(data_dict.keys())
            Windows = self.Windows
            hmm = { }
            for zone in Zones:
                hmm[zone] = {}
                for window in Windows:
                    # prev_state, state, cumulative_prob
                    hmm[zone][window] = np.zeros(shape = (self.class_num, 3))
            return hmm
            
        
        
        # self.HMM = np.zeros(shape = (len(self.Zones), len(self.Windows)))
        self.HMM = __init_HMM__(data)
        
        self.frame = 0
        self.t = self.Windows[self.frame]
        self.__emit__()
        
        
    
            
        
    def __cal_emit__(self, mean_speed, sigma = 15, Kj = 150.4, Lambda = -35.30):
        
        est_dens = min(Kj * math.exp(mean_speed/Lambda), 130)
        gauss = np.array([ scipy.stats.norm(d,15).pdf(est_dens) for d in self.Char_Dens_list ])
        emit_probs = gauss/np.sum(gauss)
    
        return emit_probs
        
    def __work_flow__(self):
        
        self.__transit__()
        self.__emit__()

        
         
    def __cal_trans__(self, v_x_t, s_x_t, v_x_1_t, s_x_1_t):
        
        k_x_t = self.Char_Dens_list[s_x_t]
        k_x_1_t = self.Char_Dens_list[s_x_1_t]
        q_x_t = k_x_t * v_x_t
        q_x_1_t = k_x_1_t * v_x_1_t
        
        return  k_x_t +  1/60.96 * (q_x_1_t - q_x_t)
    
    def __transit__(self):
        
        zones = self.Zones
        for zid in range(1, len(self.Zones)):
            
            v_curr = self.data[zones[zid]][self.t][1]
            v_last_t = self.data[zones[zid]][self.prev_t][1]
            v_last_x = self.data[zones[zid - 1]][self.t][1]
            
            s_last_t = self.HMM[zones[zid]][self.prev_t]
            
            
            
            
            
            
    
    
    
    
if __name__ == "__main__":
    hmm = HMM_time_space(new_ress)
    
    # hmm.__work_flow__()
    
    hmm_dict = hmm.HMM
    print (hmm.t)
    
    

