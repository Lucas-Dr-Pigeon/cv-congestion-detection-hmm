# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import math
import string
import random
from matplotlib import figure
class HMM_Partial:
    
    def __get_actual_levels__(self):
        self.actual_levels = np.full((len(self.windows), len(self.zones)), -1)
        for z in range(len(self.zones)):
            for w in range(len(self.windows)):
                actual_density = self.data[self.zones[z]][self.windows[w]][2] 
                offsets = np.asarray([abs( actual_density - level ) for level in self.density_levels]) 
                # print ( np.argmin(offsets) )
                self.actual_levels[w][z] = np.arange(self.levels)[np.argmin(offsets)]
                
    def __sparse__(self):
        num_vehs = len(self.vehicles)

        self.vehicles = self.vehicles[ random.sample( range(0, num_vehs), int ( num_vehs * self.mpr/100 )) ]
        
    def __get_speeds__(self):
        
        dx = 0
        dt = 0
        speeds = np.zeros(len(self.zones))
        for z in range(len(self.zones)):
            try: 
                zone = self.zones[z]
                trajectory = self.trj[zone][self.t]
                for veh in list(trajectory.keys()):
                    
                    if veh in self.vehicles:
                        dx += ( trajectory[veh]["x"][-1] - trajectory[veh]["x"][0] ) /3.28084 /1000
                        dt += ( trajectory[veh]["t"][-1] - trajectory[veh]["t"][0] ) *0.1/3600 
                speeds[z] = dx / dt
            except:
                speeds[z] = self.speed_profile[z][self.frame - 1]
            if speeds[z] * 0 != 0:
                speeds[z] = self.speed_profile[z][self.frame - 1]
            
        return speeds
                     
        
                    
    
    def __init__(self, data, trj, vehs, mpr, levels = 3): 
        self.levels = levels
        self.data = data
        self.density_levels = [40, 70, 100] 
        self.sigma = 7.5
        self.trj = trj
        self.mpr = mpr
        self.vehicles = vehs
        self.__sparse__()
        def __find_union_windows__(data_dict):
            Zones = list(data_dict.keys())
            union = set(data_dict[Zones[0]].keys())
            for zone in Zones:
                union = set.intersection(union, set(data_dict[zone].keys()) ) 
            return list(sorted(union))
        
        
        self.zones = list(data.keys())
        self.windows = __find_union_windows__(self.data)
        self.dx = 60.96 
        self.dt = 1 
        self.frame = 0
        self.t = self.windows[self.frame]
        self.__get_actual_levels__()
        self.speed_profile = np.zeros(shape = (len(self.zones), len(self.windows)))
        all_states = np.zeros(shape = (self.levels ** len(self.zones), len(self.zones)))
        
        def convertToBase7(num: int) -> str:
            base7 = []
            if num < 0:
                flag = 1
                num = -num
            else:
                flag = 0
            while num >= self.levels:
                fig = str(num % self.levels)
                base7.append(fig)
                num = num // self.levels
            base7.append(str(num))
            if flag:
                base7.append('-')
            base7.reverse()
            return ''.join(base7)
        
        
        for s in range(1, all_states.shape[0]):
            hexa = convertToBase7(s)
            for c in range(len(hexa)):
                all_states[s][-1 - c] = hexa[-1 - c]
                
        self.all_states = all_states
        # self.speeds = [ self.data[zone][self.t][1] for zone in self.zones  ]
        self.speeds = self.__get_speeds__()
        self.speed_profile[:,self.frame] = self.speeds
        self.prev_speeds = None
        self.prev_t = None
        
        self.hmm = {}
        for window in self.windows:
            self.hmm[window] = { }
            for state in self.all_states:
                self.hmm[window][tuple(state)] = {"prev_state": None, "Cumulative_prob": -1, "if_Trans": False }
        self.__cal_emit__()
        self.__emit__()
            
        
        
        
    
    def __emit__(self):
        
        print ("calculating emission probability: window" + str(self.t))
        levels = np.arange(self.levels).astype(int)
        emit_probs = np.full(self.all_states.shape[0], 1)
        
        for sid in range(len(self.all_states)):
            state = self.all_states[sid]
            for zone in range(len(self.zones)):
                level = int(state[zone])
                emit_probs[sid] *= self.indv_emit_probs[zone][level] * 10
                
        self.emit_probs = emit_probs
        # sum_emit_probs = np.sum(emit_probs)  
         
        max100sid = emit_probs.argsort()[-10:]
        for sid in max100sid:
            state = self.all_states[sid]
            if self.hmm[self.t][tuple(state)]["Cumulative_prob"] == -1:
                state = self.all_states[sid]
                self.hmm[self.t][tuple(state)]["Cumulative_prob"] = emit_probs[sid] 
        
        # for sid in range(len(self.all_states)):
        #     state = self.all_states[sid]
        #     if self.hmm[self.t][tuple(state)]["Cumulative_prob"] == -1:
        #         state = self.all_states[sid]
        #         self.hmm[self.t][tuple(state)]["Cumulative_prob"] = emit_probs[sid] 
                
        
        
           
        
        
    def __cal_emit__(self, Kj = 130.4, Lambda = -35.30):
        si = self.sigma
        indv_emit_probs = np.zeros(shape=(len(self.zones), self.levels))
        for z in range(indv_emit_probs.shape[0]):
            Ke = min(Kj * math.exp(self.speeds[z]/Lambda), 130.4) 
            # print ("Ke: " + str(est_dens))  
            gauss = np.zeros(self.levels)  
            for d in range(self.levels):
                Ks = self.density_levels[d]
                gauss[d] = scipy.stats.norm(Ke,5).cdf(Ks + 2*si) - scipy.stats.norm(Ke,5).cdf(Ks - 2*si) if Ks - 2*si > 0 \
                    else scipy.stats.norm(Ke,5).cdf(Ks + 2*si)

            indv_emit_probs[z] = gauss/np.sum(gauss)
        self.indv_emit_probs = indv_emit_probs
            
    # def __cal_emit__(self, Kj = 150.4, Uf = 96.04):
        
    #     indv_emit_probs = np.zeros(shape=(len(self.zones), self.levels))
    #     for z in range(indv_emit_probs.shape[0]):
    #         est_dens = min(Kj * (1 - self.speeds[z] / Uf), 130) if self.speeds[z] < 96.04 else 0
    #         # print ("Ke: " + str(est_dens))
    #         gauss = np.array([ scipy.stats.norm(d,15).pdf(est_dens) for d in self.density_levels ])
    #         indv_emit_probs[z] = gauss/np.sum(gauss)
    #     self.indv_emit_probs = indv_emit_probs
 
        
    def __transit__(self):
        
        print ("calculating transition probability: window" + str(self.t))
        for psid in range(len(self.all_states)):      
            prev_state = self.all_states[psid]
            
            if self.hmm[self.prev_t][tuple(prev_state)]["Cumulative_prob"] <= 0:
                continue
            
            for sid in range(len(self.all_states)):
                
                state = self.all_states[sid] 
                
                if self.hmm[self.t][tuple(state)]["Cumulative_prob"] <= 0:
                    continue
                
                trans_prob =  self.__cal_transit__(prev_state, state) 
                if trans_prob == 0:
                    continue
                print ("progress: " + str(self.t) + " : " + str(prev_state) + " --> " + str(state))
                
                cumulative_prob = self.hmm[self.t][tuple(state)]["Cumulative_prob"] * trans_prob * 10
                if self.hmm[self.t][tuple(state)]["if_Trans"] == False:
                    self.hmm[self.t][tuple(state)]["Cumulative_prob"] = cumulative_prob
                    self.hmm[self.t][tuple(state)]["if_Trans"] = True
                    self.hmm[self.t][tuple(state)]["prev_state"] = prev_state
                if cumulative_prob > self.hmm[self.t][tuple(state)]["Cumulative_prob"]:
                    self.hmm[self.t][tuple(state)]["Cumulative_prob"] = cumulative_prob
                    self.hmm[self.t][tuple(state)]["prev_state"] = prev_state
                    self.hmm[self.t][tuple(state)]["if_Trans"] = True
                    
                    0
    def __cal_transit__(self, prev_state, state):
        si = self.sigma
        trans_prob = 1
        # state = [1,2,3,4,5]
        # prev_state = [0,3,4,5,6]
        for zone in range(1, len(state)):
             # indv_trans_probs = np.zeros(self.levels) 
            k_i_t = self.density_levels[int(prev_state[zone])]
            k_i_1_t = self.density_levels[int(prev_state[zone - 1])]
            u_i_t = self.prev_speeds[int(zone)]
            u_i_1_t = self.prev_speeds[int(zone - 1)]
            Ke = k_i_t + self.dt/self.dx * (u_i_1_t * k_i_1_t - u_i_t * k_i_t) / 3.6
            # print ("Transition density: " + str(Ke))
            G_si = si + self.dt/self.dx * (u_i_1_t * si) / 3.6 + self.dt/self.dx * (u_i_t * si) / 3.6
            Ks = self.density_levels[int(state[zone])]
            gauss_cdf = np.zeros(self.levels)
            for d in range(self.levels):
                apx_density = self.density_levels[d]
                gauss_cdf[d] = scipy.stats.norm(Ke,G_si).cdf(apx_density + 2*si) - scipy.stats.norm(Ke,G_si).cdf(apx_density - 2*si) if apx_density - 2*si > 0 \
                          else scipy.stats.norm(Ke,G_si).cdf(apx_density + 2*si)
                
            # gauss_cdf = np.array( [ scipy.stats.norm(Ke,45).cdf(d + 15) - scipy.stats.norm(Ke,45).cdf(d - 15) for d in self.density_levels ] )
            trans_prob *=  gauss_cdf[int(state[zone])] / np.sum(gauss_cdf) 
        return trans_prob
        
    def __time_lapse__(self):
        self.prev_speeds = self.speeds
        self.prev_t = self.windows[self.frame]
        
        self.frame += 1
        self.t = self.windows[self.frame]
        
        # self.speeds = [ self.data[zone][self.t][1] for zone in self.zones  ]
        self.speeds = self.__get_speeds__()
        self.speed_profile[:,self.frame] = self.speeds
        self.__cal_emit__()
        self.__emit__()
        self.__transit__()
        
        
    def __go_through__(self):
        # T = 4
        T = len(self.windows) - 1
        
        for t in range(T):
            self.__time_lapse__()
        self.__get_results__()
        self.__get_analysis__()
        self.__visualize__() 
        # self.__visualize_speeds__()
        
    def __get_results__(self):
            
        last_probs = np.zeros(len(self.all_states))
        last_window = self.t
        for sid in range(len(self.all_states)):
            state = self.all_states[sid]
            last_probs[sid] = self.hmm[last_window][tuple(state)]["Cumulative_prob"]
        
        max_sid = np.argmax(last_probs) 
        max_last_state = self.all_states[max_sid]
        
        res = [max_last_state]
        for f in range(self.frame, 1, -1):
            max_prev_state = self.hmm[self.windows[f]][tuple(res[0])]["prev_state"]
            res.insert(0, max_prev_state)
        self.res = np.asarray(res)
        return res
    
    def __get_analysis__(self):
        confusion_matrix = np.zeros(shape = (self.levels, self.levels))
        _correct = 0
        _total = self.res.shape[0] * self.res.shape[1]
        
        for w in range(self.res.shape[0]):
            for z in range(self.res.shape[1]):
                _predict = int(self.res[w][z])
                _actual = int(self.actual_levels[w][z])
                confusion_matrix[_predict][_actual] += 1
                if _predict == _actual:
                    _correct += 1
                    
        self.accuracy = _correct / _total
        self.confusion_matrix = confusion_matrix
                    
        
        
        
          
    def __visualize__(self):
        
        image = np.asarray(self.res).T
        
        y_labels = self.zones
        x_labels = self.windows
        plt.matshow(image)
        plt.xticks(range(0, len(x_labels), 20), np.arange(x_labels[0][0], x_labels[-1][-1] + 1, 20 * 10))
        plt.yticks(range(len(y_labels)), y_labels)
        plt.savefig('congestion_heatmap.png', dpi = 1200)
        plt.show()
        
            
    def __visualize_speeds__(self):
        
        image = np.asarray(self.speed_profile)
        y_labels = self.zones
        x_labels = self.windows
        plt.matshow(image)
        plt.xticks(range(0, len(x_labels), 20), x_labels)
        plt.yticks(range(len(y_labels)), y_labels)
        plt.savefig('speed_heatmap.png', dpi=1200)
        plt.show() 

        
        
if __name__ == "__main__":
    0
    
    this_hmm = HMM_Partial(data = new_ress, trj = dict_win_vtx_dictt, vehs = vehs, mpr = 100 )
    this_hmm.__go_through__()
    hmm_res = this_hmm.res
    hmm_accuracy= this_hmm.accuracy
    hmm_confusion_matrix = this_hmm.confusion_matrix
    
    hmm_indv_emit = this_hmm.indv_emit_probs
    hmm_speed_profile =this_hmm.speed_profile
    hmm_actual = this_hmm.actual_levels
    
    
    # this_hmm.__visualize__()
    
    # def __visualize__(hmm):
        
        
    #     image = np.asarray(hmm.res)
        
    #     y_labels = hmm.zones 
    #     x_labels = hmm.windows
        
    #     # plt.figure(figsize=(50,10))
    #     plt.matshow(image, fignum=1)
    #     plt.xticks(range(0, len(x_labels), 20), np.arange(x_labels[0][0], x_labels[-1][-1], 20 * 10))
    #     plt.yticks(range(len(y_labels)), y_labels)
    #     plt.xlabel('Frame (0.1s)')
    #     plt.ylabel('Segment (feet)')
        
    #     plt.savefig('congestion_heatmap.png')
        
    #     plt.show()
        
    def __visualize__(hmm):
        
        y_labels = hmm.zones
        x_labels = hmm.windows
        res = hmm.res
        
        Y = np.arange(len(hmm.zones))
        segments = np.arange(len(hmm.windows))
        colors = ["green","yellow","red"]
        plt.style.use('dark_background')
        plt.figure(figsize=(10,5))
        plt.grid(False)
        for z in Y:
            for w in range(len(hmm.windows) - 1):
                plt.plot([w, w+1], [z, z], color = colors[int(res[w][z])], linewidth = 3) 
                
        plt.xticks(range(0, len(x_labels), 50), np.arange(x_labels[0][0], x_labels[-1][-1], 50 * 10))
        plt.yticks(range(len(y_labels)), y_labels)  
        plt.xlabel('Frame (0.1s)')
        plt.ylabel('Segment (feet)')
        plt.savefig('congestion_barchart.png')
        plt.show()
        
        
    
    
    __visualize__(this_hmm)
    
    
    # def __visualize_speeds__(hmm):
        
    #     image = np.asarray(hmm.speed_profile)
    #     y_labels = hmm.zones
    #     x_labels = hmm.windows
    #     plt.matshow(image,origin='lower')
    #     plt.xticks(range(len(x_labels)), x_labels)
    #     plt.yticks(range(len(y_labels)), y_labels)
    #     plt.show()
    #     plt.savefig('speed_profile.png')
        
    # __visualize_speeds__(this_hmm)
    
    # arr = np.array([5,2,3,4,5,6,1,2,3,4,2])
    # print (arr.argsort()[-5:][::-1])
    
    # all_States = this_hmm.all_states
    # speeds = this_hmm.speeds
    
    # this_hmm.__cal_emit__()
    # indv_emit_probs = this_hmm.indv_emit_probs
    # this_hmm.__emit__()
    
    # hmm_dict = this_hmm.hmm
    # hmm_3200_3210 = hmm_dict[tuple([3200,3210])]
    
    
    def convertToBase7(num: int) -> str:
        base7 = []
        if num < 0:
            flag = 1
            num = -num
        else:
            flag = 0
        while num >= 7:
            fig = str(num % 7)
            base7.append(fig)
            num = num // 7
        base7.append(str(num))
        if flag:
            base7.append('-')
        base7.reverse()
        return ''.join(base7)

    # print (convertToBase7(34241)[5])

        
        