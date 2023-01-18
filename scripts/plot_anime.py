#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

## first, execute measure_current.py
# cut -d ","  hang_opt_2023-01-17-21-33-17-001_motor_states.csv -f 1-3,5-49,278-280,289,305,321,337,353,369,385,401,417,433,449,465,481,497,513,529,545,561,577,593,609,625,641,657,673,689,705,721,737,753,769,785,801,817,833,849,865,881,897,913,929,945,961,977,993 > hang_opt_2023-01-17-21-33-17-001_motor_states_cut1-3_5-49_278-280_289_305_321_337_353_369_385_401_417_433_449_465_481_497_513_529_545_561_577_593_609_625_641_657_673_689_705_721_737_753_769_785_801_817_833_849_865_881_897_913_929_945_961_977_993.csv

# opt = True
# python ~/catkin_ws/remote_control_ws/src/plotter/scripts/plot_anime.py hang_opt_2023-01-17-21-33-17-001_motor_states_cut1-3_5-49_278-280_289_305_321_337_353_369_385_401_417_433_449_465_481_497_513_529_545_561_577_593_609_625_641_657_673_689_705_721_737_753_769_785_801_817_833_849_865_881_897_913_929_945_961_977_993 opt_pose "plot" 17
opt = False
# python ~/catkin_ws/remote_control_ws/src/plotter/scripts/plot_anime.py hang_no_2023-01-17-20-05-56-002_motor_states_cut1-3_5-49_278-280_289_305_321_337_353_369_385_401_417_433_449_465_481_497_513_529_545_561_577_593_609_625_641_657_673_689_705_721_737_753_769_785_801_817_833_849_865_881_897_913_929_945_961_977_993 no_opt_pose "plot" 17

class Plotter():
    def __init__(self,target_file, output_file,offset):
        self.fig = plt.figure(figsize=[16,9])
        data_csv = pd.read_csv(target_file + ".csv")
        self.jname_data = data_csv[data_csv.keys()[3:48]].values[1]
        print("self.jname_data = {}".format(self.jname_data))
        self.time_data = data_csv[data_csv.keys()[0]].values# [0:100]# .tolist()
        self.step_data = data_csv[data_csv.keys()[1]].values# .tolist()
        self.data = (data_csv[data_csv.keys()[51:]]).values# [0:100]# .tolist()
        self.time = (self.time_data - self.time_data[0]) *10**(-9)
        self.offset = offset

    def do_plot(self):
        plt.cla()
        plt.rcParams["font.size"] = 12
        plt.tick_params(labelsize=14)

        plt.xlabel("Time Stamp[s]", fontsize=16)
        plt.xlim(0,1450)
        plt.ylabel("Temperature[C]", fontsize=16)
        plt.ylim(20,79)
        for i in range (len(self.data[0])-self.offset-12):
            plt.plot(self.time[::100], self.data[::100,self.offset+i], label=self.jname_data[self.offset+i].replace("_JOINT",""))

        if opt:
            plt.title("Temperature [Optimized Pose]", fontsize=18)
            plt.legend(bbox_to_anchor=(1.12, 1.0))
        else:
            plt.title("Temperature [Non Optimized Pose]", fontsize=18)
            plt.legend(bbox_to_anchor=(1.01, 1.0))
        # plt.show()
        plt.savefig(output_file+ ".png", format="png")

    def do_plot_for_anime(self,data):
        plt.cla()
        plt.rcParams["font.size"] = 12
        plt.tick_params(labelsize=14)

        plt.xlabel("Time Stamp[s]", fontsize=16)
        plt.xlim(0,1450)
        plt.ylabel("Temperature[C]", fontsize=16)
        plt.ylim(20,79)
        for i in range (len(self.data[0])-self.offset-12):
            plt.plot(self.time[::100], self.data[::100,self.offset+i], label=self.jname_data[self.offset+i].replace("_JOINT",""))

        if opt:
            plt.title("Temperature [Optimized Pose]", fontsize=18)
            plt.legend(bbox_to_anchor=(1.12, 1.0))
        else:
            plt.title("Temperature [Non Optimized Pose]", fontsize=18)
            plt.legend(bbox_to_anchor=(1.01, 1.0))
        # plt.show()
        plt.savefig(output_file+ ".png", format="png")

    def make_anime(self):
        ani = animation.FuncAnimation(self.fig, self.do_plot_for_anime, interval=200, blit=True)
        plt.show()
        #ani.save('test.gif', writer='imagemagick')

if __name__ == '__main__':
    args = sys.argv
    if len(args)<4:
        print("please input 4 args")
        exit
        # target_dir = os.path.expanduser('~/dynamixel_data/')
    target_file = args[1]
    output_file = args[2]
    offset = int(args[4])
    s=Plotter(target_file, output_file, offset)
    if args[3] == "plot":
        s.do_plot()
    else:
        s.make_anime()
